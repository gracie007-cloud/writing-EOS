"""The Story Bible's twelve elements (requirements §4.4, FR-SB-3, D26): what each holds, which components fill it,
which of the Author's pools feed it, and which of the Bible's registers it contains. The Story Bible Builder
assembles the elements; Canon Check and Canon Second Opinion check them; the Author locks the Bible.

This module only describes and checks the structure. Filling an element is its components' job, each routed to
its own model (one job per component, D25)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

BIBLE_PATH = Path(__file__).resolve().parent.parent / "config" / "story_bible.yaml"


class BibleError(ValueError):
    """The Story Bible structure names a component, pool or register that does not exist."""


@dataclass(frozen=True)
class Element:
    id: str
    title: str
    holds: list
    filled_by: list
    sources: list
    registers: list
    approach: dict | None = None


@dataclass(frozen=True)
class StoryBible:
    version: str
    assembled_by: str
    checked_by: list
    kept_by: str
    elements: list

    def element(self, eid: str) -> Element:
        for e in self.elements:
            if e.id == eid:
                return e
        raise BibleError(f"no element {eid!r}")

    def elements_filled_by(self, step: str) -> list:
        """The elements a component contributes to: what its output is assembled into."""
        return [e.title for e in self.elements if step in e.filled_by]


def load_bible(path=BIBLE_PATH) -> StoryBible:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    elements = [Element(e["id"], e["title"], e["holds"], [str(s) for s in e["filled_by"]], e.get("sources", []),
                        e.get("registers", []), e.get("approach")) for e in raw["elements"]]
    return StoryBible(raw["version"], str(raw["assembled_by"]), [str(s) for s in raw["checked_by"]],
                      str(raw["kept_by"]), elements)


def check_bible(bible: StoryBible, components, lmap) -> list:
    """Every step must be a real component, every source a real pool (and field group, where the pool is a sheet),
    and every element must have a component that fills it. Returns the problems (empty when sound)."""
    steps = components.by_step
    problems = []
    if len(bible.elements) != 12:
        problems.append(f"the Story Bible has {len(bible.elements)} elements, not 12")
    for s in [bible.assembled_by, bible.kept_by, *bible.checked_by]:
        if s not in steps:
            problems.append(f"unknown component {s}")
    for e in bible.elements:
        if not e.filled_by:
            problems.append(f"{e.title}: no component fills it")
        for s in e.filled_by:
            if s not in steps:
                problems.append(f"{e.title}: unknown component {s}")
        for src in e.sources:
            pool = src.get("pool")
            if pool not in lmap.pools:
                problems.append(f"{e.title}: unknown pool {pool}")
            elif pool == "themes" and src.get("fields"):
                cfg = lmap.pools["themes"]
                known = {"definition", "complementary_theme", "theme_type", *cfg.get("list_fields", [])}
                for table in cfg["tables"].values():
                    cols = table["columns"]
                    known |= {table["group"]} if table.get("group") else set(cols.values() if isinstance(cols, dict) else cols)
                for f in src["fields"]:
                    if f not in known:
                        problems.append(f"{e.title}: the themes pool has no {f}")
        if e.approach:
            if e.approach.get("decided_by") != "author":
                problems.append(f"{e.title}: the worldbuilding approach must be the Author's decision")
            groups = lmap.pools["themes"].get("world_approaches", {})
            if set(e.approach.get("choices", [])) != set(groups):
                problems.append(f"{e.title}: approach choices differ from the themes pool's approaches")
    return problems
