"""Agent definitions and the prompt builder (requirements §6.2, §6.7, FR-PP-1 to FR-PP-3, FR-PP-6, FR-CTX-1, FR-CTX-2,
FR-ML-7).

Each agent is one YAML file in `config/agents/`. Its `inputs` list is the only source of what the agent receives
(harness rule 2). An input is one of:

- `author.<name>`: material the Author supplies (braindump, brainstorm, a manuscript type in mind);
- `step.<step>`: the output of a component this one needs (its `needs` in components.yaml);
- `decision.<name>`: what the Author decided at a gate of a component this one needs;
- `library.<pool>`: a slice of a library pool this step may read (`read_by` in library_map.yaml), chosen for the
  book (its genre path, its pen name) and shown through `prompt_view`, never the private fields.

Loading refuses a definition that asks for anything else. The builder labels every part for Show prompt, keeps the
prompt inside the agent's context budget by leaving out the lowest-priority optional blocks first (required blocks
are never cut; if they alone overflow, it stops), records what it left out, and refuses answer-key paths and
anything shaped like a provider key.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .library import (LibraryError, LibraryMap, content_levels_for, describe_levels, pen_names_for, pitches,
                      pools_used_by, prompt_view, themes_for)

APP = Path(__file__).resolve().parent.parent
AGENTS_DIR = APP / "config" / "agents"

# The gate each decision is taken at: the component whose gate it is (components.yaml gate_after).
DECISIONS = {"manuscript_type": "2", "genre_path": "2", "pen_name": "3", "adapted_premise": "3.5"}
KINDS = ("author", "step", "decision", "library")
KEY_SHAPES = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{20,}|Bearer [A-Za-z0-9._-]{20,})")
CHARS_PER_TOKEN = 3.5      # conservative: real tokenizers average about 4 characters a token in English prose


class PromptError(ValueError):
    """A prompt would break a rule; nothing is built or sent."""


class AnswerKeyError(PromptError):
    """An answer key was about to be read into a prompt (FR-ML-7)."""


@dataclass(frozen=True)
class Input:
    source: str               # e.g. "step.2", "library.pen_names"
    label: str
    required: bool = False

    @property
    def kind(self) -> str:
        return self.source.split(".", 1)[0]

    @property
    def name(self) -> str:
        return self.source.split(".", 1)[1]


@dataclass(frozen=True)
class Agent:
    step: str
    id: str
    prompt: str
    inputs: tuple
    output: tuple
    temperature: float
    max_tokens: int
    context_budget_tokens: int
    path: str = ""


@dataclass
class Part:
    label: str                # what Show prompt calls it
    source: str               # template, an input source, or output
    text: str
    tokens: int
    required: bool = True


@dataclass
class Built:
    agent: Agent
    parts: list
    left_out: list = field(default_factory=list)       # (label, tokens, reason)
    template_version: str = ""
    template_sha: str = ""

    @property
    def text(self) -> str:
        return "\n\n".join(p.text for p in self.parts)

    @property
    def tokens(self) -> int:
        return sum(p.tokens for p in self.parts)


def estimate_tokens(text: str) -> int:
    return math.ceil(len(text) / CHARS_PER_TOKEN)


def guard_path(path) -> None:
    if "ANSWER_KEY" in str(path).upper():
        raise AnswerKeyError(f"Refused: {Path(path).name} is an answer key and may only be read by a scorer.")


def load_agent(path) -> Agent:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    inputs = tuple(Input(i["from"], i["label"], bool(i.get("required"))) for i in raw["inputs"])
    return Agent(str(raw["step"]), raw["id"], raw["prompt"], inputs, tuple(raw["output"]), float(raw["temperature"]),
                 int(raw["max_tokens"]), int(raw["context_budget_tokens"]), str(path))


def load_agents(folder=AGENTS_DIR) -> dict:
    """{step: Agent} for every definition in the folder."""
    agents = [load_agent(p) for p in sorted(Path(folder).glob("*.yaml"))]
    by_step = {a.step: a for a in agents}
    if len(by_step) != len(agents):
        raise PromptError("two agent definitions share a step")
    return by_step


def check_agent(agent: Agent, w, lmap: LibraryMap) -> list:
    """Why this definition asks for something its component may not have; empty when every input is allowed."""
    c = w.by_step.get(agent.step)
    if c is None:
        return [f"{agent.id}: step {agent.step} is not in components.yaml"]
    reads = pools_used_by(agent.step, lmap)["reads"]
    problems = []
    for i in agent.inputs:
        if i.kind not in KINDS:
            problems.append(f"{agent.id}: unknown input kind {i.source!r}")
        elif i.kind == "step" and i.name not in c.needs:
            problems.append(f"{agent.id}: reads step {i.name}, which {c.name} does not need (components.yaml)")
        elif i.kind == "decision" and DECISIONS.get(i.name) not in c.needs:
            problems.append(f"{agent.id}: reads the decision {i.name!r}, taken at a gate {c.name} does not follow")
        elif i.kind == "library" and (i.name not in lmap.pools or lmap.pools[i.name]["title"] not in reads):
            problems.append(f"{agent.id}: reads the pool {i.name!r}, which library_map.yaml does not let step "
                            f"{agent.step} read")
    missing = [n for n in c.needs if f"step.{n}" not in {i.source for i in agent.inputs}]
    problems += [f"{agent.id}: needs step {n} (components.yaml) but its definition does not read it" for n in missing]
    return problems


# ---------- library slices, chosen for the book ----------

def _book_path(book: dict) -> dict:
    p = book.get("genre_path") if isinstance(book.get("genre_path"), dict) else {}
    return {k: p.get(k) for k in ("primary_genre", "secondary_genre", "major_subgenre", "minor_subgenre")}


def library_slice(name: str, pools: dict, lmap: LibraryMap, book: dict):
    """What the agent sees of a pool for this book, or None when the book has not decided enough yet to choose."""
    pool = pools.get(name)
    if pool is None:
        return None
    path = _book_path(book)
    minor = path["minor_subgenre"] or path["major_subgenre"]
    if name == "story_pitches":
        return [prompt_view(e, lmap) for e in pitches(pool)]
    if name == "content_levels":
        if not minor:
            return None
        try:
            e = content_levels_for(pool, minor, path["secondary_genre"], path["major_subgenre"])
        except LibraryError as err:
            return {"note": str(err)}
        if e is None:
            return {"note": f"no content levels mapped for {minor}: the Author sets them at Story Setup"}
        return describe_levels(e.fields, lmap)
    if name == "genres":
        if not minor:
            return None
        hits = [prompt_view(e, lmap) for e in pool.entries if not e.missing and e.title.lower() == minor.lower()]
        return hits or {"note": f"{minor} has no entry in the Narrative Genres Pool"}
    if name == "pen_names":
        if book.get("pen_name"):
            hits = [prompt_view(e, lmap) for e in pool.entries if e.title.lower() == book["pen_name"].lower()]
            return hits or {"note": f"{book['pen_name']} is not in the Pen Names Pool"}
        if not minor:
            return None
        return [prompt_view(e, lmap) for e in pen_names_for(pool, minor)]
    if name == "themes":
        if not minor:
            return None
        return [{"theme": f.theme, "fit": f.fit, "type": f.theme_type, "definition": f.definition}
                for f in themes_for(pool, path) if f.fit in ("good", "situational")]
    return [prompt_view(e, lmap) for e in pool.entries if not e.missing]


def _render(value) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, indent=1)


def _block(label: str, source: str, body: str, required: bool) -> Part:
    text = f"## {label}\n\n{body.strip()}"
    return Part(label, source, text, estimate_tokens(text), required)


def _output_part(agent: Agent) -> Part:
    keys = ", ".join(f'"{k}"' for k in agent.output)
    text = ("## Your answer\n\nAnswer with one JSON object and nothing else. Its keys, all of them: " + keys + ". "
            "Use null for anything the inputs do not give; never invent it.")
    return Part("Output schema", "output", text, estimate_tokens(text))


def build_prompt(agent: Agent, *, author: dict, outputs: dict, decisions: dict, pools: dict, lmap: LibraryMap,
                 author_paths=()) -> Built:
    """The prompt for one run, from the definition's inputs only, inside its context budget.

    author: {name: text}; outputs: {step: output}; decisions: {name: value}; pools: {pool: Pool};
    author_paths: the files the Author's material came from, checked against the answer-key rule."""
    for p in author_paths:
        guard_path(p)
    tpath = APP / agent.prompt
    guard_path(tpath)
    raw = tpath.read_text(encoding="utf-8")
    meta, body = {}, raw
    if raw.startswith("---"):
        _, fm, body = raw.split("---", 2)
        meta = yaml.safe_load(fm) or {}
    parts = [Part("Template", "template", body.strip(), estimate_tokens(body.strip()))]
    book = {k: v for k, v in decisions.items() if not (isinstance(v, str) and v.startswith("⟦"))}   # taken ones
    for i in agent.inputs:
        if i.kind == "author":
            value = author.get(i.name)
        elif i.kind == "step":
            value = outputs.get(i.name)
        elif i.kind == "decision":
            value = decisions.get(i.name)
        else:
            value = library_slice(i.name, pools, lmap, book)
        if value in (None, "", [], {}):
            if i.required:
                raise PromptError(f"{agent.id}: its required input {i.label!r} is missing")
            continue
        parts.append(_block(i.label, i.source, _render(value), i.required))
    parts.append(_output_part(agent))
    built = Built(agent, parts, template_version=str(meta.get("version", "")),
                  template_sha=hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12])
    _fit_budget(built)
    if KEY_SHAPES.search(built.text):
        raise PromptError(f"{agent.id}: the prompt holds something shaped like a provider key; nothing is built")
    return built


def _fit_budget(built: Built) -> None:
    """Leave out optional blocks, lowest priority (latest listed) first, until the prompt fits (FR-CTX-2)."""
    budget = built.agent.context_budget_tokens
    for p in reversed([p for p in built.parts if not p.required]):
        if built.tokens <= budget:
            return
        built.parts.remove(p)
        built.left_out.append((p.label, p.tokens, "over the context budget"))
    if built.tokens > budget:
        raise PromptError(f"{built.agent.id}: its required parts alone take {built.tokens} tokens, over its budget of "
                          f"{budget}; the Author gets a pitch instead of a cut prompt")


def show_prompt(built: Built) -> str:
    """Show prompt (FR-PP-1): every part labelled, with its source and size."""
    lines = [f"# {built.agent.id} · step {built.agent.step}",
             f"template {built.agent.prompt} v{built.template_version} ({built.template_sha}) · "
             f"{built.tokens} of {built.agent.context_budget_tokens} tokens", ""]
    for p in built.parts:
        lines += [f"<!-- part: {p.label} · from {p.source} · {p.tokens} tokens"
                  f"{' · required' if p.required else ''} -->", p.text, ""]
    for label, tokens, why in built.left_out:
        lines.append(f"<!-- left out: {label} · {tokens} tokens · {why} -->")
    return "\n".join(lines)
