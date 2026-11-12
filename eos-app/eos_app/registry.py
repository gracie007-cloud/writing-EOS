"""Model registry (requirements FR-ML-1, D22).

`config/models.yaml` is the app's copy of the Author's Notion roster *LLM Identifier*: every model with a provider,
its provider model ID, the roster's checkboxes, its Comparable Equivalent Model and Fallback Model (the experts the
Author lines up beside it: a Mixture of Experts, not model families), and the genre it is fine-tuned for. It is
built from an export of the roster in Notion's own CSV layout:

    python -m eos_app.registry "<path to the LLM Identifier export.csv>"

Model IDs live in config/models.yaml only (the export sits outside the app). Rows with no provider belong to other
uses of the roster and are left out. The build reports roster rows that look mistyped.
"""

from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

CONFIG = Path(__file__).resolve().parent.parent / "config"
MODELS_PATH = CONFIG / "models.yaml"


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
    genre: str = ""
    modality: str = ""        # Image, Video, Speech, Music, Sound, Speech-to-text; empty for a text model

    @property
    def ident(self) -> str:
        """Which model this is, whatever provider serves it: its roster name. Two roster rows with one name are one
        model reached by two routes; P8 compares models by this, never by route."""
        return " ".join(self.name.casefold().split())


@dataclass
class Registry:
    version: str
    models: list
    by_key: dict
    problems: list

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
        return [m for m in self.models if m.genre and _norm(m.genre) == _norm(genre)]


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


def build(export_csv) -> dict:
    """models.yaml content from a roster export. Duplicate rows and rows whose name and ID disagree are reported,
    not guessed at: the first row for an ID is kept."""
    with open(export_csv, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    models, seen, problems = [], {}, []
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
            "key": re.sub(r"[^a-z0-9]+", "-", f"{provider} {mid or name}".lower()).strip("-"),
            "name": name, "provider": provider, "model_id": mid,
            "frontier": _yes(r.get("Frontier Model")), "open_weights": _yes(r.get("Open-Weights Model")),
            "uncensored": _yes(r.get("Uncensored Model")), "can_run_locally": _yes(r.get("Can Run Locally")),
            "comparable": _cell(r, "Comparable Equivalent Model"), "fallback": _cell(r, "Fallback Model"),
            "genre": _cell(r, "Genre"), "modality": _cell(r, "Modality"),
        })
    return {"version": date.today().isoformat(), "source": "Notion LLM Identifier (export)", "problems": problems,
            "models": models}


def write(export_csv, out=MODELS_PATH) -> dict:
    doc = build(export_csv)
    head = ("# Writing EOS model registry: the app's copy of the Notion roster LLM Identifier (FR-ML-1).\n"
            "# Built by `python -m eos_app.registry <export.csv>`; do not edit by hand.\n")
    Path(out).write_text(head + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    return doc


def load_models(path=MODELS_PATH) -> Registry:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    models = [Model(**m) for m in raw["models"]]
    by_key = {m.key: m for m in models}
    if len(by_key) != len(models):
        raise RegistryError("two models share a key")
    return Registry(raw["version"], models, by_key, raw.get("problems", []))


if __name__ == "__main__":
    d = write(sys.argv[1])
    print(f"models: {len(d['models'])}")
    for p in d["problems"]:
        print("-", p)
