"""Keep `config/components.yaml` in step with the Notion database *Narrative Components* (D18: the database leads).

The database records each component's order, phase, gate, tier and models. It does not record what a component takes
in, which code parts belong to it, what an evaluation component judges, or what a media component makes; those live
in `config/component_inputs.yaml`, which this app owns. The two are joined here by Step.

    python -m eos_app.sync check  "<Narrative Components export.csv>"    # what the export would change; writes nothing
    python -m eos_app.sync build  "<Narrative Components export.csv>"    # rebuild components.yaml, then check its order
    python -m eos_app.sync export "<out.csv>"                            # the app's copy in the database's columns

The export is Notion's own CSV export of the database (… → Export → Markdown & CSV), like the roster export the
registry is built from. Everything this app depends on is built by a command in this repository.
"""

from __future__ import annotations

import csv
import sys
from datetime import date
from pathlib import Path

import yaml

from .registry import candidate_name
from .workflow import COMPONENTS_PATH, check_order, validate

INPUTS_PATH = COMPONENTS_PATH.with_name("component_inputs.yaml")
COLUMNS = ["Step", "Component", "App Name", "Flow Order", "Phase", "Runs", "Task Type", "Swarm Tier", "Jev Model",
           "Author Gate After", "Category", "Frontier Model", "Comparable Open-Weight", "Fallback Model",
           "Mature Fallback"]
TASK = {"Synthesis": "synthesis", "Extraction": "extraction", "Ideation": "ideation", "Verdict / Check": "verdict",
        "Prose": "prose", "Prose + Verdict": "prose_verdict", "Media generation": "media",
        "No LLM (Code)": "code", "Deterministic tooling": "code"}
RUNS = {"In sequence": "sequence", "Per chapter": "per_chapter", "Per chapter · only on a failed check": "on_failure",
        "On demand": "on_demand", "Cross-cutting": "cross_cutting"}
JEV = {"settles": "jev-1.14.0", "advises": "jev-1.14.0 (decision support only)", "none": ""}
NO_MODEL = "Deterministic tooling — no LLM"
PHASES = {"A": "Intake", "B": "Stage 0", "C": "Naming", "D": "Characters", "E": "Stage 1", "F": "Stage 2",
          "G": "Stage 3", "H": "World", "I": "QA and Bible", "J": "Outline", "K": "Chapters", "L": "Editor tools",
          "M": "Finishing", "N": "Sales", "All": "Throughout"}
HEAD = ("# Writing EOS components: the app's copy of the Notion database Narrative Components (D18).\n"
        "# name = what the writer sees; database_name and step = the Notion row (shown in Engine view).\n"
        "# candidates are the component's line of experts: primary (the database's Frontier Model column),\n"
        "# comparable (Comparable Open-Weight) and fallback (Fallback Model). needs, code, judges, modality and\n"
        "# gate_when_run come from component_inputs.yaml. Built by `python -m eos_app.sync build <export.csv>`;\n"
        "# do not edit by hand.\n")


class SyncError(ValueError):
    """The export or the inputs table cannot be turned into a component list."""


def load_inputs(path=INPUTS_PATH) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["components"]


def read_export(path) -> list:
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    missing = [c for c in COLUMNS if rows and c not in rows[0]]
    if not rows or missing:
        raise SyncError(f"{path}: not a Narrative Components export (missing column: {', '.join(missing) or 'all'})")
    return rows


def _cell(row, column) -> str:
    return (row.get(column) or "").strip()


def component(row: dict, inputs: dict) -> dict:
    """One database row, joined with this app's inputs table, as a components.yaml entry."""
    step = _cell(row, "Step")
    mine = inputs.get(step) or {}
    code = "Deterministic" in _cell(row, "Frontier Model") or _cell(row, "Swarm Tier") in ("", "None")
    try:
        task, runs = ("code" if code else TASK[_cell(row, "Task Type")]), RUNS[_cell(row, "Runs")]
    except KeyError as e:
        raise SyncError(f"{step}: the app has no meaning for the database value {e.args[0]!r}") from None
    jev, flow, phase = _cell(row, "Jev Model"), _cell(row, "Flow Order"), _cell(row, "Phase").split(" · ")[0]
    c = {"step": step, "name": _cell(row, "App Name"), "database_name": _cell(row, "Component"),
         "flow_order": int(float(flow)) if flow else None, "phase": phase, "runs": runs, "task_type": task,
         "swarm": (_cell(row, "Swarm Tier") or "None").lower(),
         "jev": "none" if not jev else ("advises" if "decision support" in jev else "settles"),
         "needs": list(mine.get("needs", [])), "category": _cell(row, "Category")}
    if _cell(row, "Author Gate After"):
        c["gate_after"] = _cell(row, "Author Gate After")
        if mine.get("gate_when_run"):
            c["gate_when_run"] = True
    for key in ("code", "judges", "modality"):
        if mine.get(key):
            c[key] = mine[key]
    if not code:
        primary, comparable = _cell(row, "Frontier Model") or None, _cell(row, "Comparable Open-Weight") or None
        if not candidate_name(primary) and comparable:       # the Author's primary is the open-weight model
            primary, comparable = comparable, None
        c["candidates"] = {"primary": primary, "comparable": comparable}
        if _cell(row, "Fallback Model"):
            c["candidates"]["fallback"] = _cell(row, "Fallback Model")
        if _cell(row, "Mature Fallback"):
            c["mature_fallback"] = _cell(row, "Mature Fallback")
    return c


def build(rows: list, inputs: dict, version: str | None = None) -> dict:
    """components.yaml content from the database's rows. Refuses a step the inputs table does not know, so a new
    database row cannot slip in without its inputs being decided."""
    unknown = [_cell(r, "Step") for r in rows if _cell(r, "Step") not in inputs]
    if unknown:
        raise SyncError("no entry in component_inputs.yaml for: " + ", ".join(unknown)
                        + ". Add each one with the inputs it needs (an empty entry if it needs none).")
    comps = sorted((component(r, inputs) for r in rows),
                   key=lambda c: (c["flow_order"] is not None, c["flow_order"] or 0))
    doc = {"version": version or date.today().isoformat(),
           "source": "Notion database Narrative Components (5c6ac348379e4a3dadf8670b8869e6fa); "
                     "the app follows its order (D18)",
           "phases": dict(PHASES), "jev_model": "typesafe/jev-1.14", "components": comps}
    validate(doc)                    # the same checks the app runs when it loads the file
    return doc


def export_rows(doc: dict) -> list:
    """The app's copy as database rows: what an export would hold if the database matched the app exactly."""
    rows = []
    for c in doc["components"]:
        code, cand = c["task_type"] == "code", c.get("candidates") or {}
        rows.append({
            "Step": c["step"], "Component": c["database_name"], "App Name": c["name"],
            "Flow Order": "" if c["flow_order"] is None else str(c["flow_order"]),
            "Phase": c["phase"] if c["phase"] == "All" else f"{c['phase']} · {doc['phases'][c['phase']]}",
            "Runs": {v: k for k, v in RUNS.items()}[c["runs"]],
            "Task Type": "No LLM (Code)" if code else next(k for k, v in TASK.items() if v == c["task_type"]),
            "Swarm Tier": c["swarm"].capitalize(), "Jev Model": JEV[c["jev"]],
            "Author Gate After": c.get("gate_after") or "", "Category": c["category"],
            "Frontier Model": NO_MODEL if code else (cand.get("primary") or ""),
            "Comparable Open-Weight": cand.get("comparable") or "", "Fallback Model": cand.get("fallback") or "",
            "Mature Fallback": c.get("mature_fallback") or ""})
    return rows


def write_export(doc: dict, path) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(export_rows(doc))


def dump(doc: dict) -> str:
    return HEAD + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120)


def differences(old: dict, new: dict) -> list:
    """What changes between two component lists, in plain words, one line per change."""
    a, b = ({c["step"]: c for c in d["components"]} for d in (old, new))
    out = [f"{b[s]['name']} ({s}) is new" for s in b if s not in a]
    out += [f"{a[s]['name']} ({s}) is gone" for s in a if s not in b]
    for s in a:
        if s in b:
            for key in sorted(set(a[s]) | set(b[s])):
                if a[s].get(key) != b[s].get(key):
                    out.append(f"{a[s]['name']} ({s}): {key} {a[s].get(key)!r} → {b[s].get(key)!r}")
    return out


def main(argv) -> int:
    if len(argv) != 2 or argv[0] not in ("check", "build", "export"):
        print(__doc__)
        return 2
    current = yaml.safe_load(COMPONENTS_PATH.read_text(encoding="utf-8"))
    if argv[0] == "export":
        write_export(current, argv[1])
        print(f"wrote {len(current['components'])} rows to {argv[1]}")
        return 0
    new = build(read_export(argv[1]), load_inputs(), version=current["version"])
    changes = differences(current, new)
    print(f"components: {len(new['components'])} · changes: {len(changes)}")
    for line in changes:
        print("-", line)
    problems = check_order(validate(new))
    for line in problems:
        print("ORDER:", line)
    if argv[0] == "build" and changes and not problems:
        new["version"] = date.today().isoformat()
        COMPONENTS_PATH.write_text(dump(new), encoding="utf-8")
        print(f"wrote {COMPONENTS_PATH}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
