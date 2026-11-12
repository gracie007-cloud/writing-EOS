"""Which components could run today, and what stands in the way of the rest.

    python -m eos_app.readiness          # the summary and everything that needs attention
    python -m eos_app.readiness --all    # every component

It asks the router, for each component, which models it could actually call: on the right lane, with a provider
model ID. Nothing is sent to any model. A component is

- ready     its Primary can be called (and, for the Full tier, a second expert for the cross-check);
- degraded  it would run, but not as designed: on a later expert, or with no second expert to cross-check;
- blocked   nothing it could call.

Notes say what does not stop a normal run but should be known: every expert on one provider, no route for mature
material, work that nothing checks.
"""

from __future__ import annotations

import sys
from collections import Counter
from dataclasses import dataclass

from .registry import Registry, RegistryError, load_models
from .router import RoutingError, Routing, checker_models, experts, load_routing, unusable, writer_models
from .workflow import Workflow, chapter_loop, load_components


@dataclass(frozen=True)
class Readiness:
    step: str
    name: str
    state: str            # code, ready, degraded, blocked
    reasons: tuple = ()   # why it is not ready
    notes: tuple = ()     # what does not stop a normal run


def line(c, reg: Registry, routing: Routing) -> list:
    """The models the router would try for this component's normal work, in order."""
    return checker_models(c, reg, routing) if c.is_evaluation else writer_models(c, reg, routing)


def usable(c, reg: Registry, routing: Routing, down_providers=()) -> list:
    try:
        return [m for m in line(c, reg, routing) if not unusable(m, down_providers=down_providers)]
    except RoutingError:
        return []


def has_mature_route(c, reg: Registry, routing: Routing) -> bool:
    if c.is_evaluation:
        return bool(c.mature_fallback)
    try:
        return any(not unusable(m) for m in writer_models(c, reg, routing, mature=True))
    except RoutingError:
        return False


def component_readiness(c, w: Workflow, reg: Registry, routing: Routing) -> Readiness:
    if c.task_type == "code":
        return Readiness(c.step, c.name, "code")
    try:
        tried = line(c, reg, routing)
    except RoutingError as e:
        return Readiness(c.step, c.name, "blocked", (str(e),))
    can = [m for m in tried if not unusable(m)]
    if not can:
        return Readiness(c.step, c.name, "blocked", tuple(unusable(m) for m in tried))
    reasons, notes = [], []
    if unusable(tried[0]):
        reasons.append(f"{unusable(tried[0])}, so it would run on {can[0].name}")
    if c.swarm == "full" and len({m.ident for m in can}) < 2:
        reasons.append("the Full tier cross-checks with a second expert, and it has one")
    missing = [m.name for m in tried[1:] if not m.model_id]
    if missing:
        notes.append("no provider model ID yet for " + ", ".join(missing))
    if len({m.provider for m in can}) == 1:
        notes.append(f"every expert is on {can[0].provider}: an outage there stops it")
    if not has_mature_route(c, reg, routing):
        notes.append("its Mature Fallback is still open" if c.is_evaluation else "no model may handle mature material")
    if (c.writes_prose or c.makes_media) and not any(c.step in (j.judges or []) for j in w.components):
        notes.append("nothing checks its work")
    return Readiness(c.step, c.name, "degraded" if reasons else "ready", tuple(reasons), tuple(notes))


def stopped_by_outage(w: Workflow, reg: Registry, routing: Routing, provider: str) -> list:
    """The components that can run today and could not if this provider went down."""
    return [c for c in w.components if c.task_type != "code" and usable(c, reg, routing)
            and not usable(c, reg, routing, down_providers=(provider,))]


def report(w: Workflow, reg: Registry, routing: Routing) -> dict:
    rows = [component_readiness(c, w, reg, routing) for c in w.components]
    try:
        jev = bool(reg.resolve(w.jev_model))
    except RegistryError:
        jev = False
    return {"components": rows, "counts": Counter(r.state for r in rows), "jev_in_roster": jev,
            "outage": {p: stopped_by_outage(w, reg, routing, p) for p in routing.providers}}


def render(rep: dict, w: Workflow, everything: bool = False) -> str:
    n, rows = rep["counts"], rep["components"]
    per_chapter = {c.step for c in chapter_loop(w)}
    out = [f"Writing EOS readiness · {len(rows)} components",
           f"  ready {n['ready']} · degraded {n['degraded']} · blocked {n['blocked']} · code only {n['code']}", ""]
    for state, title in (("blocked", "Blocked: nothing it could call"), ("degraded", "Degraded: would run, not as designed")):
        hit = [r for r in rows if r.state == state]
        if hit:
            out.append(title)
            out += [f"  {r.name} ({r.step}): " + "; ".join(r.reasons) for r in hit]
            out.append("")
    out.append("If a provider went down, these could no longer run:")
    for p, stopped in rep["outage"].items():
        if stopped:
            inside = sum(1 for c in stopped if c.step in per_chapter)
            out.append(f"  {p}: {len(stopped)} components ({inside} of them run in every chapter)")
    out.append("")
    for needle, title in (("no model may handle mature material", "No route for mature material"),
                          ("its Mature Fallback is still open", "Mature Fallback still open"),
                          ("nothing checks its work", "Writers nothing checks")):
        hit = [r.name for r in rows if needle in r.notes]
        if hit:                                 # a long list is counted here and spelled out by --all
            out.append(f"{title} ({len(hit)})" + (": " + ", ".join(hit) if len(hit) <= 12 or everything else
                                                  " · run with --all to list them"))
    if not rep["jev_in_roster"]:
        out.append(f"Jev ({w.jev_model}) has no row in the roster, so it cannot be routed.")
    if everything:
        out += ["", "Every component"]
        out += [f"  {r.state:9} {r.name} ({r.step})" + ("  · " + "; ".join(r.reasons + r.notes) if r.reasons or r.notes else "")
                for r in rows]
    return "\n".join(out)


if __name__ == "__main__":
    W = load_components()
    print(render(report(W, load_models(), load_routing()), W, everything="--all" in sys.argv[1:]))
