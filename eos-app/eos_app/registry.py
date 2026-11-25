"""Model registry (requirements FR-ML-1, D22, D33).

`config/models.yaml` is the app's copy of the Author's model sources, built by one command:

    python -m eos_app.registry "<LLM Identifier export.csv>" \\
        [--mature "<Abliterated & Uncensored Models export.csv>"] [--register ../registry.json]

- The **roster** *LLM Identifier* (Notion, CSV export): every model with a provider, its provider model ID, the
  roster's checkboxes, its Comparable Equivalent Model and Fallback Model (the experts the Author lines up beside it:
  a Mixture of Experts, not model families). Rows with no provider belong to other uses of the roster and are left
  out.
- The **mature catalog** *LLM Identifier for Creative Writing: Abliterated & Uncensored Models* (Notion, CSV export;
  the repository's copy is `llm-identifier-creative-writing-abliterated/abliterated_models.csv`). Every row is an
  uncensored model, so each one is marked uncensored on every route the roster gives it, and a model the roster
  lacks is added on the catalog's provider. Its Genres, Genre Category and Pen Name columns become the model's genre
  tags (its pen names are not copied: they stay outside the app, D10). A row on Hugging Face that is not served through Inference Providers is a GGUF kept as a **fine-tune base**:
  it is recorded and never called (the Author, 2026-11-25).
- The **register** `registry.json` (verified against the provider APIs on 2026-11-14): the context each provider
  actually serves, the register ID (W01 to W77, C01 to C10), the Genre Matrix subgenres each model serves, and the
  same model's OpenRouter route.

Which models write for each pen name in each Genre Matrix path (the register's routing table, `routing.json`) is read
from the repository root when the app loads, like the library pools: it names pen names, so it is never copied into
the app (D10). Model IDs live in config/models.yaml only. The build reports rows that look mistyped.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

CONFIG = Path(__file__).resolve().parent.parent / "config"
MODELS_PATH = CONFIG / "models.yaml"
REPO = CONFIG.parent.parent
REGISTER_PATH = REPO / "registry.json"          # the register and its routing table: outside the app (D10)
ROUTING_PATH = REPO / "routing.json"

# The register's roles, in the order the router may use them for drafting. Short-form and conditional writers, layer
# specialists and component specialists are kept for the prompt builder; they never draft a book.
FIT_ROLES = {"lead_writer": "lead", "adjacent": "adjacent", "short_form_writer": "short_form",
             "conditional": "conditional", "layer_specialist": "layer", "components": "components"}
DRAFTING_ROLES = ("lead", "adjacent")
REGISTER_PROVIDERS = {"Featherless AI": "Featherless AI", "Local (Unsloth Desktop)": "Unsloth Desktop",
                      "Local (GGUF from Hugging Face)": "Hugging Face"}
CATEGORY = re.compile(r"Category ([A-H])\b")


class RegistryError(ValueError):
    """The registry or a lookup in it is not usable."""


@dataclass(frozen=True)
class Model:
    key: str
    name: str
    provider: str
    model_id: str
    frontier: bool
    open_weights: bool
    uncensored: bool
    can_run_locally: bool
    comparable: str = ""
    fallback: str = ""
    modality: str = ""        # Image, Video, Speech, Music, Sound, Speech-to-text; empty for a text model
    genres: tuple = ()        # subgenres it is tuned or fitted for (mature catalog Genres; register paths)
    genre_categories: tuple = ()   # the catalog's Category A to H, as letters
    fine_tune_base: bool = False   # a GGUF kept to fine-tune later: never called
    served_context: int | None = None   # tokens the provider serves (register); size every request to this
    register_id: str = ""     # W01 to W77, C01 to C10
    same_as: str = ""         # the roster name of the model this row is another route to

    @property
    def ident(self) -> str:
        """Which model this is, whatever provider serves it: its roster name, or the name of the model it is another
        route to. P8 compares models by this, never by route."""
        return " ".join((self.same_as or self.name).casefold().split())


@dataclass
class Registry:
    version: str
    models: list
    by_key: dict
    problems: list
    fits: list = field(default_factory=list)      # routing.json: pen name and genre path → models by role

    def resolve(self, text: str | None):
        """The model a cell names, or None when it names none. Accepts the Narrative Components and roster
        spellings: 'GPT-6.1 Sol', 'GLM-5.3-Flash', 'MiMo-2.6-Pro', 'MiMo-V2.6-Pro (least-gap — not parity)' and
        'None genuinely comparable — least-gap: MiMo-V2.6-Pro (not parity)'."""
        name = candidate_name(text)
        if not name:
            return None
        k = _norm(name)
        hits = [m for m in self.models if k in (_norm(m.name), _norm(m.model_id), _norm(m.model_id.replace("-v", "-")))]
        if not hits:
            raise RegistryError(f"{text!r} names no model in the registry")
        if len({m.ident for m in hits}) > 1:       # two different models read alike: take an exact match or refuse
            exact = [m for m in hits if name.casefold() in (m.ident, m.model_id.casefold())]
            if not exact:
                raise RegistryError(f"{text!r} could mean {' or '.join(sorted({m.name for m in hits}))}; "
                                    f"write the roster name exactly")
            hits = exact
        return hits[0]

    def routes(self, model) -> list:
        """Every roster row for this model: the model itself first, then the same model on its other providers
        (D22: when a provider is down, the router tries the model's next route before it changes model)."""
        return [model] + [m for m in self.models if m.ident == model.ident and m.key != model.key]

    def for_genre(self, genre: str) -> list:
        """Models tagged for this subgenre, in roster order."""
        g = _norm(genre)
        return [m for m in self.models if any(_norm(t) == g for t in m.genres)]

    def named(self, ref: str) -> list:
        """The rows for a model named in the routing table (its roster name or provider model ID)."""
        r = ref.casefold()
        return [m for m in self.models if r in (m.name.casefold(), m.model_id.casefold())]

    def fit_writers(self, pen_name: str, genre: str, roles=DRAFTING_ROLES) -> list:
        """The models the register puts on this pen name's rows for this subgenre (minor, or major where the row has
        no minor), lead writers first, each in the register's order. Every row the subgenre sits on counts."""
        p, g = _norm(pen_name), _norm(genre)
        rows = [f for f in self.fits if _norm(f["pen_name"]) == p
                and g == _norm(f["path"][3] or f["path"][2] or "")]
        out, seen = [], set()
        for role in roles:
            for f in rows:
                for ref in f.get(role, []):
                    for m in self.named(ref["model"]):
                        if m.key not in seen:
                            seen.add(m.key)
                            out.append(m)
        return out


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def candidate_name(text: str | None) -> str:
    """The model name inside a model cell, without its notes; '' when the cell names none."""
    t = str(text or "").strip()
    if "least-gap:" in t:
        t = t.split("least-gap:", 1)[1]
    elif t.startswith("None") or t in ("N/A", ""):
        return ""
    return re.sub(r"\(.*?\)", "", t).strip()


def least_gap(text: str | None) -> bool:
    """The database marks an open-weight candidate as the least-gap option, not a true equivalent."""
    return "least-gap" in str(text or "")


def _yes(v) -> bool:
    return str(v).strip().lower() in ("yes", "true", "__yes__", "1")


def _cell(r, column) -> str:
    v = (r.get(column) or "").strip()
    return "" if v in ("None", "N/A") else v


def _split(cell: str) -> list:
    return [x.strip() for x in str(cell or "").split(",") if x.strip()]


def _key(provider: str, ref: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", f"{provider} {ref}".lower()).strip("-")


def _merge(old: list, new) -> list:
    out = list(old)
    for x in new:
        if x and x not in out:
            out.append(x)
    return out


def _read_csv(path) -> list:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _roster(rows: list, problems: list) -> list:
    models, seen = [], {}
    for r in rows:
        provider = (r.get("Provider") or "").strip()
        if not provider:
            continue
        name, mid = r["Model Name"].strip(), (r.get("Provider Model ID") or "").strip()
        if not mid:
            problems.append(f"{provider}: {name!r} has no provider model ID yet; fill it from the provider's model list")
        if "/" in name and name != mid:
            problems.append(f"{provider}: the name {name!r} and the ID {mid!r} disagree (an ID copied from another row?)")
        key = f"{provider}|{mid or name}"
        if key in seen:
            problems.append(f"{provider}: {mid!r} is listed twice (rows {seen[key]!r} and {name!r}); the first is kept")
            continue
        seen[key] = name
        models.append({
            "key": _key(provider, mid or name), "name": name, "provider": provider, "model_id": mid,
            "frontier": _yes(r.get("Frontier Model")), "open_weights": _yes(r.get("Open-Weights Model")),
            "uncensored": _yes(r.get("Uncensored Model")), "can_run_locally": _yes(r.get("Can Run Locally")),
            "comparable": _cell(r, "Comparable Equivalent Model"), "fallback": _cell(r, "Fallback Model"),
            "modality": _cell(r, "Modality"), "genres": [], "genre_categories": [],
            "fine_tune_base": False, "served_context": None, "register_id": "", "same_as": "",
        })
    return models


def _mistyped(m: dict) -> bool:
    """A roster row whose name is a repository other than its ID: the ID was copied from another row."""
    return "/" in m["name"] and m["name"] != m["model_id"]


def _rows_for(models: list, *refs) -> list:
    """The rows for a model, by name, or by ID where the row's name does not contradict its ID."""
    want = {r.casefold() for r in refs if r}
    return [m for m in models if m["name"].casefold() in want
            or (m["model_id"].casefold() in want and not _mistyped(m))]


def _claim(models: list, provider: str, name: str, mid: str, problems: list, source: str):
    """A mistyped roster row that holds this model's ID on this provider: the newer source names it, so the row
    takes that name (and is reported) instead of a second row being added."""
    for m in models:
        if m["provider"] == provider and m["model_id"].casefold() == (mid or name).casefold() and _mistyped(m):
            problems.append(f"{provider}: the row named {m['name']!r} holds the ID {m['model_id']!r}; renamed "
                            f"{name!r} from the {source} (correct the roster)")
            m["name"] = name
            return m
    return None


def _mature(models: list, rows: list, problems: list) -> None:
    """Fold the mature catalog in: every row is uncensored; its genre tags join the model's."""
    for r in rows:
        name, mid, provider = r["Model Name"].strip(), _cell(r, "Provider Model ID"), _cell(r, "Provider")
        if not provider:
            problems.append(f"mature catalog: {name!r} has no provider")
            continue
        base = provider == "Hugging Face" and not _yes(r.get("Via Inference Providers"))
        mine = _rows_for(models, name, mid)
        if not any(m["provider"] == provider for m in mine) and (claimed := _claim(models, provider, name, mid,
                                                                                  problems, "mature catalog")):
            mine.append(claimed)
        if not any(m["provider"] == provider for m in mine):
            new = {"key": _key(provider, mid or name), "name": name, "provider": provider, "model_id": mid,
                   "frontier": False, "open_weights": _yes(r.get("Open-Weights Model")), "uncensored": True,
                   "can_run_locally": _yes(r.get("Can Run Locally")),
                   "comparable": _cell(r, "Comparable Equivalent Model"), "fallback": _cell(r, "Fallback Model"),
                   "modality": "", "genres": [], "genre_categories": [], "fine_tune_base": False,
                   "served_context": None, "register_id": "", "same_as": ""}
            models.append(new)
            mine.append(new)
        for m in mine:
            m["uncensored"] = True
            m["genres"] = _merge(m["genres"], _split(r.get("Genres")))
            m["genre_categories"] = _merge(m["genre_categories"], CATEGORY.findall(r.get("Genre Category") or ""))
            if m["provider"] == provider:
                m["fine_tune_base"] = m["fine_tune_base"] or base


def _register(models: list, register: dict, problems: list) -> None:
    """Fold the register in: served context, register ID, Genre Matrix subgenres, and the same model's OpenRouter
    route."""
    for w in register["models"]:
        inf = w["inference"]
        mine = _rows_for(models, w["hf_repo"], inf["model_id"])
        if not mine and (claimed := _claim(models, REGISTER_PROVIDERS[inf["provider"]], w["hf_repo"],
                                           inf["model_id"], problems, "register")):
            mine = [claimed]
        if not mine:                                 # verified by the register, in neither Notion source: add it
            provider = REGISTER_PROVIDERS[inf["provider"]]
            mine = [{"key": _key(provider, inf["model_id"]), "name": w["hf_repo"], "provider": provider,
                     "model_id": inf["model_id"], "frontier": False, "open_weights": True, "uncensored": False,
                     "can_run_locally": provider != "Featherless AI", "comparable": "", "fallback": "",
                     "modality": "", "genres": [], "genre_categories": [], "fine_tune_base": False,
                     "served_context": None, "register_id": "", "same_as": ""}]
            models.extend(mine)
            problems.append(f"register {w['id']}: {w['hf_repo']!r} is in neither Notion source; added on {provider} "
                            f"from the register (add it to the roster)")
        name = mine[0]["name"]
        subs = [a["minor_subgenre"] or a["major_subgenre"] for a in w["assignments"]]
        for m in mine:
            m["register_id"] = w["id"]
            m["genres"] = _merge(m["genres"], subs)
            if m["provider"] == "Featherless AI" and inf["provider"] == "Featherless AI":
                m["served_context"] = inf["served_context_tokens"]
                if m["model_id"] != inf["model_id"]:
                    problems.append(f"Featherless AI: {m['name']!r} is served as {inf['model_id']!r}, "
                                    f"not {m['model_id']!r} (register {w['id']})")
            if inf["provider"].startswith("Local (GGUF"):
                m["fine_tune_base"] = True
        if inf.get("also_on_openrouter"):
            twin = [m for m in models if m["provider"] == "OpenRouter"
                    and m["model_id"].casefold() == inf["also_on_openrouter"].casefold()]
            for m in twin:                          # one model, two routes: P8 and outages treat it so
                m["same_as"] = name
                m["register_id"] = w["id"]
            uncensored = any(x["uncensored"] for x in mine + twin)      # one model is uncensored on every route
            for m in mine + twin:
                m["uncensored"] = uncensored


def _fits(register: dict, rows: list) -> list:
    """The routing table with register IDs as roster names."""
    names = {w["id"]: w["hf_repo"] for w in register["models"]}
    out = []
    for r in rows:
        f = {"pen_name": r["pen_name"],
             "path": [r["primary_genre"], r["secondary_genre"], r["major_subgenre"], r["minor_subgenre"]]}
        for src, role in FIT_ROLES.items():
            if r.get(src):
                f[role] = [{"model": names[x["model"]], "rank": x["model_fit_rank"], "note": x.get("note") or ""}
                           for x in r[src]]
        out.append(f)
    return out


def build(export_csv, mature_csv=None, register_json=None) -> dict:
    """models.yaml content. Duplicate rows and rows whose name and ID disagree are reported, not guessed at: the
    first row for an ID is kept."""
    problems = []
    models = _roster(_read_csv(export_csv), problems)
    sources = ["Notion LLM Identifier (export)"]
    if mature_csv:
        _mature(models, _read_csv(mature_csv), problems)
        sources.append("Notion LLM Identifier for Creative Writing: Abliterated & Uncensored Models (export)")
    if register_json:
        _register(models, json.loads(Path(register_json).read_text(encoding="utf-8")), problems)
        sources.append("registry.json (verified 2026-11-14)")
    if len({m["key"] for m in models}) != len(models):
        raise RegistryError("two models share a key")
    return {"version": date.today().isoformat(), "source": "; ".join(sources), "problems": problems,
            "models": models}


def load_fits(register_json=REGISTER_PATH, routing_json=ROUTING_PATH) -> list:
    """The register's routing table, read where it lives (outside the app); empty when it is not there."""
    if not (Path(register_json).is_file() and Path(routing_json).is_file()):
        return []
    return _fits(json.loads(Path(register_json).read_text(encoding="utf-8")),
                 json.loads(Path(routing_json).read_text(encoding="utf-8")))


def dump(doc: dict, head: str) -> str:
    return head + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120)


MODELS_HEAD = ("# Writing EOS model registry (FR-ML-1, D33): the app's copy of the Notion roster LLM Identifier, joined\n"
               "# with the mature catalog (Abliterated & Uncensored Models) and the 2026-11-14 register.\n"
               "# Built by `python -m eos_app.registry`; do not edit by hand.\n")


def write(export_csv, mature_csv=None, register_json=None, out=MODELS_PATH) -> dict:
    doc = build(export_csv, mature_csv, register_json)
    Path(out).write_text(dump(doc, MODELS_HEAD), encoding="utf-8")
    return doc


def load_models(path=MODELS_PATH, register_json=REGISTER_PATH, routing_json=ROUTING_PATH) -> Registry:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    models = [Model(**{k: tuple(v) if isinstance(v, list) else v for k, v in m.items()}) for m in raw["models"]]
    by_key = {m.key: m for m in models}
    if len(by_key) != len(models):
        raise RegistryError("two models share a key")
    return Registry(raw["version"], models, by_key, raw.get("problems", []), load_fits(register_json, routing_json))


def main(argv) -> int:
    p = argparse.ArgumentParser(prog="python -m eos_app.registry", description=__doc__.split("\n\n")[0])
    p.add_argument("roster", help="Notion export of the LLM Identifier roster (CSV)")
    p.add_argument("--mature", help="Notion export of the Abliterated & Uncensored Models catalog (CSV)")
    p.add_argument("--register", help="registry.json")
    a = p.parse_args(argv)
    d = write(a.roster, a.mature, a.register)
    print(f"models: {len(d['models'])}")
    for line in d["problems"]:
        print("-", line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
