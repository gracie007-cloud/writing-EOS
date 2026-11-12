"""Order of work (requirements v0.10, FR-FLOW-1 to FR-FLOW-6, D17, D18).

The app follows the Notion database *Narrative Components*: `config/components.yaml` is its copy. Each component
has a plain name the writer sees, its database name and Step (shown in Engine view), a place in the Flow Order,
how it runs, the inputs it needs, and how many models work on it (Swarm Tier) and what Jev may do (Jev role).

Code decides what runs next and refuses an order that would run a component before an input it needs. The
Author's final calls stay the Author's: Jev settles only the routing agents may settle (blueprint tables).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .blueprint import who_decides

COMPONENTS_PATH = Path(__file__).resolve().parent.parent / "config" / "components.yaml"
PHASES = "ABCDEFGHIJKLMN"
RUNS = ("sequence", "per_chapter", "on_failure", "on_demand", "cross_cutting")
QUEUED = ("sequence", "per_chapter")          # what the engine queues by itself
SWARM = {"full": 2, "light": 1, "none": 0}    # models working on one run of the component
JEV = ("settles", "advises", "none")


class OrderError(ValueError):
    """The component registry or its order is not usable."""


@dataclass
class Component:
    step: str
    name: str
    database_name: str
    flow_order: int | None
    phase: str
    runs: str
    task_type: str
    swarm: str
    jev: str
    needs: list
    gate_after: str | None = None
    code: list | None = None
    candidates: dict | None = None
    category: str = "Building Blocks"     # the database's Category: Building Blocks, Prose Writing, Sales & Marketing
    judges: list | None = None            # an evaluation component: the components whose output it judges (P8)
    mature_fallback: str | None = None    # an evaluation component: the model for mature text its experts refuse;
                                          # None on an evaluation component means the Author has left it open

    @property
    def is_evaluation(self) -> bool:
        return bool(self.judges)

    @property
    def writes_prose(self) -> bool:
        """A Prose Writing component that writes prose (not a checker or an editing tool): it uses the genre
        fine-tunes."""
        return self.category == "Prose Writing" and not self.judges and self.task_type in ("prose", "prose_verdict")

    @property
    def makes_media(self) -> bool:
        """A component that generates images, video, speech, music or sound."""
        return self.task_type == "media"


@dataclass
class Workflow:
    version: str
    components: list
    by_step: dict
    by_name: dict

    def ordered(self):
        return sorted((c for c in self.components if c.flow_order is not None), key=lambda c: c.flow_order)


def validate(raw: dict) -> Workflow:
    comps, steps, names = [], set(), set()
    for d in raw["components"]:
        c = Component(**d)
        if c.step in steps:
            raise OrderError(f"duplicate step {c.step}")
        if c.name in names:
            raise OrderError(f"duplicate name {c.name!r}: every component needs its own name")
        if c.phase not in PHASES and c.phase != "All":
            raise OrderError(f"{c.name}: unknown phase {c.phase!r}")
        if c.runs not in RUNS:
            raise OrderError(f"{c.name}: unknown runs value {c.runs!r}")
        if c.swarm not in SWARM:
            raise OrderError(f"{c.name}: unknown swarm tier {c.swarm!r}")
        if c.jev not in JEV:
            raise OrderError(f"{c.name}: unknown Jev role {c.jev!r}")
        steps.add(c.step)
        names.add(c.name)
        comps.append(c)
    for c in comps:
        for n in c.needs:
            if n not in steps:
                raise OrderError(f"{c.name} needs step {n}, which is not in the registry")
        if c.mature_fallback and not c.judges:
            raise OrderError(f"{c.name}: only an evaluation component has a Mature Fallback")
        for n in c.judges or []:
            if n not in steps or n == c.step:
                raise OrderError(f"{c.name} judges step {n}, which is not another component in the registry")
    orders = sorted(c.flow_order for c in comps if c.flow_order is not None)
    if orders != list(range(1, len(orders) + 1)):
        raise OrderError("Flow Order must run 1, 2, 3 … with no gaps or repeats")
    return Workflow(raw.get("version", ""), comps, {c.step: c for c in comps}, {c.name: c for c in comps})


def load_components(path=COMPONENTS_PATH) -> Workflow:
    return validate(yaml.safe_load(Path(path).read_text(encoding="utf-8")))


def check_order(w: Workflow) -> list:
    """Every place a component runs before an input it needs, in plain words. Empty means the order works."""
    problems = []
    for c in w.ordered():
        for n in c.needs:
            need = w.by_step[n]
            if need.flow_order is not None and need.flow_order > c.flow_order:
                problems.append(f"{c.name} runs before {need.name}, which it needs.")
    return problems


def display_name(c: Component, view="writer") -> str:
    """Writer view shows the plain name; Engine view shows the database row (NFR-12)."""
    return c.name if view == "writer" else f"{c.step} · {c.database_name}"


def next_to_run(w: Workflow, done: set) -> list:
    """Queued components whose inputs are all done, in Flow Order. Tools and loops are not queued."""
    return [c for c in w.ordered()
            if c.step not in done and c.runs in QUEUED and all(n in done for n in c.needs)]


def chapter_loop(w: Workflow) -> list:
    """The components that run inside every chapter, including the ones that run only on a failed check."""
    return [c for c in w.ordered() if c.phase == "K" and c.runs in ("per_chapter", "on_failure")]


def gates(w: Workflow) -> list:
    """(component, gate) for every Author gate, in Flow Order."""
    return [(c, c.gate_after) for c in w.ordered() if c.gate_after]


def run_plan(c: Component) -> dict:
    """How many models work on one run, whether a second model cross-checks, and Jev's role.

    Swarm full: the Primary plus an independent model from another family; code compares the two.
    Swarm light: one model (the Fallback only on failure). Swarm none: code only."""
    return {"models": SWARM[c.swarm], "cross_check": c.swarm == "full", "jev": c.jev}


def jev_role(c: Component, decision_kind: str, tables) -> str | None:
    """What Jev may do with one decision at this component.

    'settles' only where the component lets Jev settle and the decision is one agents may settle;
    otherwise Jev's pick is a recommendation, preselected in the pitch. Never for the Author's final calls."""
    if c.jev == "none":
        return None
    if c.jev == "settles" and who_decides(decision_kind, tables) == "agent_may_settle":
        return "settles"
    return "recommends"
