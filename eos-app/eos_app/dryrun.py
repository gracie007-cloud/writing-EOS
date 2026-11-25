"""The dry run of the first slice (fixes plan D1; requirements FR-PP-2, FR-GEN-2).

    python -m eos_app.dryrun --project ../projects/dry-run --library ../library \\
        --braindump braindump.md [--brainstorm brainstorm.md] [--manuscript-type Novel] \\
        --genre-path "Primary > Secondary > Major > Minor" --pen-name "<pen name>"

It walks the components Story Pitch depends on, in Flow Order, and for each one builds the prompt from its allowed
inputs, picks its models through the router (the Primary, and for the Full tier a second expert that cross-checks)
and builds the exact request, **without sending anything**. It stops at every Author gate on the way and records the
stop. A dry run cannot take your decisions, so the decisions later prompts read (the genre path, the pen name) are
stand-ins you name on the command line, marked as such everywhere; the outputs of earlier steps are placeholders.

It writes, inside the project folder (outside the app, because it names your library, D10):
- `runs/<date>/runs.jsonl`: one record per planned call (model, route, slot, tokens, cost when a price is known,
  status "not sent");
- `prompts/dry-run/NN-<agent>.md`: Show prompt for each step, every part labelled, with the request;
- `dry-run.html`: one card per step with Proceed and My alternative (disabled: nothing was run), and the gate stops.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .clients import build_request, load_endpoints
from .library import load_map, load_pool
from .prompts import DECISIONS, PromptError, build_prompt, check_agent, guard_path, load_agents, show_prompt
from .registry import load_models
from .router import RoutingError, experts, load_routing, route, unusable, writer_models
from .workflow import load_components, run_plan, waiting_on

PRICES_PATH = Path(__file__).resolve().parent.parent / "config" / "prices.yaml"
POOLS = ("story_pitches", "content_levels", "genres", "pen_names", "themes")
NOT_RUN = "⟦dry run: the output of {name} goes here, as JSON with the keys {keys}⟧"


def slice_for(w, last: str) -> list:
    """The component and everything it needs, directly or not, in Flow Order."""
    want, todo = set(), [last]
    while todo:
        s = todo.pop()
        if s not in want:
            want.add(s)
            todo += w.by_step[s].needs
    return [c for c in w.ordered() if c.step in want]


def parse_path(text: str | None) -> dict | None:
    if not text:
        return None
    parts = [p.strip() or None for p in text.split(">")]
    if len(parts) != 4:
        raise SystemExit('--genre-path takes four levels: "Primary > Secondary > Major > Minor" (leave one empty '
                         'as "Primary > Secondary > Major > " when the path has no minor subgenre)')
    return dict(zip(("primary_genre", "secondary_genre", "major_subgenre", "minor_subgenre"), parts))


def load_prices(path=PRICES_PATH) -> dict:
    """{model name or key: {input, output}} in USD per million tokens; empty when no file exists yet."""
    p = Path(path)
    return (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}


def plan_calls(c, reg, routing) -> tuple:
    """(calls, notes): the models a live run would call, each as (role, model, slot), and what stands in the way."""
    notes = []
    try:
        line = writer_models(c, reg, routing)
    except RoutingError as e:
        return [], [str(e)]
    slots = {m.ident: s for s, m in experts(c, reg)}
    usable = [m for m in line if not unusable(m)]
    if not usable:
        return [], ["blocked: " + "; ".join(unusable(m) for m in line)]
    if unusable(line[0]):
        notes.append(f"degraded: {unusable(line[0])}, so it runs on {usable[0].name}")
    calls = [("writer", usable[0], slots.get(usable[0].ident, "route"))]
    if run_plan(c)["cross_check"]:
        second = next((m for m in usable if m.ident != usable[0].ident), None)
        if second:
            calls.append(("cross-check", second, slots.get(second.ident, "route")))
        else:
            notes.append("degraded: the Full tier cross-checks with a second expert, and it has one")
    return calls, notes


FLAT_RATE = {"Featherless AI"}       # a subscription: a call costs nothing extra


def _cost(model, prices, tokens_in, tokens_out):
    if model.provider in FLAT_RATE:
        return 0.0
    p = prices.get(model.key)
    if not p:
        return None
    return round((tokens_in * p["input"] + tokens_out * p["output"]) / 1_000_000, 4)


def dry_run(project, *, library_root, author: dict, author_paths=(), assumed: dict, last="5",
            prices=None, now=None) -> dict:
    """Walk the slice without sending anything. Returns the summary; writes the project files."""
    now = now or datetime.now(timezone.utc)
    project = Path(project)
    for p in [library_root, *author_paths]:
        guard_path(p)
    w, reg, routing, lmap = load_components(), load_models(), load_routing(), load_map()
    agents, endpoints, prices = load_agents(), load_endpoints(), load_prices() if prices is None else prices
    pools = {p: load_pool(p, library_root, lmap) for p in POOLS}
    order = slice_for(w, last)
    problems = [p for c in order for p in (check_agent(agents[c.step], w, lmap) if c.step in agents
                                            else [f"{c.name} ({c.step}) has no agent definition"])]
    if problems:
        raise PromptError("; ".join(problems))

    decisions = {k: v for k, v in assumed.items() if v}
    for name, gate_step in DECISIONS.items():
        decisions.setdefault(name, f"⟦your decision at the gate after {w.by_step[gate_step].name}⟧")
    events, records, outputs, done, approved, n = [], [], {}, set(), set(), 0
    for c in order:
        for g, _ in waiting_on(w, c, done, approved):
            took = [k for k, s in DECISIONS.items() if s == g.step]
            events.append({"type": "gate", "step": g.step, "component": g.name, "gate": g.gate_after,
                           "decisions": {k: decisions[k] for k in took},
                           "stand_ins": [k for k in took if k in assumed and assumed[k]]})
            approved.add(g.step)
        n += 1
        agent = agents[c.step]
        built = build_prompt(agent, author=author, outputs=outputs, decisions=decisions, pools=pools, lmap=lmap,
                             author_paths=author_paths)
        upstream = sum(agents[s].max_tokens for s in c.needs if s in agents)
        placeholders = sum(p.tokens for p in built.parts if p.source.startswith("step."))
        worst = built.tokens - placeholders + upstream            # with real outputs upstream, at their budgets
        calls, notes = plan_calls(c, reg, routing)
        planned = []
        for role, m, slot in calls:
            r = route(m, routing)
            req = build_request(endpoints.get(r), r, m.model_id, built.text, agent.temperature, agent.max_tokens)
            cost = _cost(m, prices, worst, agent.max_tokens)
            rec = {"time": now.isoformat(), "mode": "dry_run", "status": "not sent", "step": c.step,
                   "component": c.name, "agent": agent.id, "call": role, "model": m.name, "model_key": m.key,
                   "provider": m.provider, "route": r, "slot": slot, "jev": c.jev,
                   "template": agent.prompt, "template_version": built.template_version,
                   "template_sha": built.template_sha, "prompt_tokens": built.tokens,
                   "worst_case_input_tokens": worst, "max_output_tokens": agent.max_tokens,
                   "cost_usd_max": cost, "request_problem": req["problem"],
                   "left_out": [{"label": a, "tokens": t, "why": y} for a, t, y in built.left_out]}
            records.append(rec)
            planned.append((rec, req))
        events.append({"type": "step", "n": n, "step": c.step, "component": c.name, "agent": agent.id,
                       "gate_after": c.gate_after, "notes": notes, "calls": [r for r, _ in planned],
                       "requests": [q for _, q in planned], "show_prompt": show_prompt(built)})
        outputs[c.step] = NOT_RUN.format(name=c.name, keys=", ".join(agent.output))
        done.add(c.step)

    summary = _summary(events, records, assumed)
    _write(project, now, events, records, summary)
    return summary


def _summary(events, records, assumed) -> dict:
    steps = [e for e in events if e["type"] == "step"]
    open_items = sorted({r["request_problem"] for r in records if r["request_problem"]})
    open_items += [f"{e['component']}: {n}" for e in steps for n in e["notes"]]
    unpriced = sorted({r["model"] for r in records if r["cost_usd_max"] is None})
    if unpriced:
        open_items.append("no price for " + ", ".join(unpriced) + " (config/prices.yaml), so the cost cannot be "
                          "estimated yet")
    costs = [r["cost_usd_max"] for r in records]
    return {"prompts": len(steps), "calls": len(records), "gate_stops": sum(e["type"] == "gate" for e in events),
            "steps": [(e["step"], e["component"], [(c["call"], c["model"], c["route"]) for c in e["calls"]])
                      for e in steps],
            "worst_case_tokens": sum(r["worst_case_input_tokens"] + r["max_output_tokens"] for r in records),
            "cost_usd_max": round(sum(costs), 4) if costs and None not in costs else None,
            "stand_ins": {k: v for k, v in assumed.items() if v}, "open_items": open_items}


def _write(project: Path, now, events, records, summary) -> None:
    runs = project / "runs" / now.strftime("%Y-%m-%d")
    shown = project / "prompts" / "dry-run"
    runs.mkdir(parents=True, exist_ok=True)
    shown.mkdir(parents=True, exist_ok=True)
    with open(runs / "runs.jsonl", "a", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    for e in events:
        if e["type"] == "step":
            reqs = "\n".join(f"```json\n{json.dumps({**q, 'body': {**q['body'], 'messages': '(the prompt above)'}}, indent=1)}\n```"
                             for q in e["requests"])
            (shown / f"{e['n']:02d}-{e['agent']}.md").write_text(e["show_prompt"] + "\n\n## Requests (not sent)\n\n"
                                                                 + reqs + "\n", encoding="utf-8")
    (project / "dry-run.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    (project / "dry-run.html").write_text(render_html(events, summary, now), encoding="utf-8")


DECISION_NAMES = {"manuscript_type": "Manuscript type", "genre_path": "Genre path", "pen_name": "Pen name",
                  "adapted_premise": "Adapted premise"}


def plain(value) -> str:
    """A decision as the Author would say it: a genre path as 'A › B › C › D'."""
    if isinstance(value, dict):
        return " › ".join(str(v) for v in value.values() if v)
    return str(value)


def render_html(events, summary, now) -> str:
    """One plain page: a card per step with Proceed and My alternative, and the gate stops between them."""
    e = html.escape
    cards, total = [], sum(ev["type"] == "step" for ev in events)
    for ev in events:
        if ev["type"] == "gate":
            dec = "".join(f"<li><b>{e(DECISION_NAMES.get(k, k))}</b>: {e(plain(v))}"
                          f"{' <i>(stand-in for the dry run)</i>' if k in ev['stand_ins'] else ''}</li>"
                          for k, v in ev["decisions"].items())
            cards.append(f'<section class="gate"><h2>Stop · {e(ev["gate"])}</h2><p>The run waits here for you. '
                         f'After {e(ev["component"])}.</p><ul>{dec}</ul></section>')
            continue
        calls = "".join(f"<li>{e(c['call'].capitalize())}: <b>{e(c['model'])}</b> on {e(c['provider'])} · "
                        f"{e(c['slot'])} · up to {c['worst_case_input_tokens']:,} tokens in, "
                        f"{c['max_output_tokens']:,} out</li>" for c in ev["calls"])
        problems = list(dict.fromkeys(c["request_problem"] for c in ev["calls"] if c["request_problem"]))
        notes = "".join(f"<li>{e(n)}</li>" for n in [*ev["notes"], *problems])
        cards.append(
            f'<section class="card"><p class="eyebrow">{ev["n"]} of {total} · component {e(ev["step"])}</p>'
            f'<h2>{e(ev["component"])}</h2><ul>{calls or "<li>no model may be called</li>"}</ul>'
            + (f'<ul class="notes">{notes}</ul>' if notes else "")
            + f'<details><summary>Show prompt</summary><pre>{e(ev["show_prompt"])}</pre></details>'
            '<p class="actions"><button disabled title="Dry run: nothing was run">Proceed</button> '
            '<button disabled title="Dry run: nothing was run">My alternative</button></p></section>')
    items = "".join(f"<li>{e(i)}</li>" for i in summary["open_items"]) or "<li>none</li>"
    stand = "".join(f"<li>{e(DECISION_NAMES.get(k, k))}: {e(plain(v))}</li>"
                    for k, v in summary["stand_ins"].items()) or "<li>none</li>"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Writing EOS · dry run</title>
<style>body{{font:15px/1.5 system-ui,sans-serif;max-width:880px;margin:2rem auto;padding:0 1rem;color:#1F2937}}
.card,.gate,.top{{border:1px solid #E3E8F0;border-radius:14px;padding:1rem 1.25rem;margin:1rem 0}}
.gate{{background:#FFF8E1;border-color:#F2C94C}}.eyebrow{{margin:0;font-size:12px;font-weight:700;letter-spacing:.12em;
text-transform:uppercase;color:#2E75B6}}h2{{margin:.2rem 0 .6rem;font-size:18px}}.notes{{color:#9A3412}}
pre{{white-space:pre-wrap;background:#F8FAFC;padding:.75rem;border-radius:8px;font-size:12.5px}}
button{{min-height:40px;padding:0 16px;border-radius:9px;border:1px solid #CBD5E1;background:#fff;font-weight:600}}</style>
</head><body><section class="top"><h1>Dry run · nothing was sent</h1>
<p>{now:%Y-%m-%d %H:%M} UTC · {summary["prompts"]} prompts · {summary["calls"]} planned calls ·
{summary["gate_stops"]} gate stops · up to {summary["worst_case_tokens"]:,} tokens ·
cost {"$%.4f at most" % summary["cost_usd_max"] if summary["cost_usd_max"] is not None else "not known yet"}</p>
<p><b>Stand-ins for your gate decisions</b></p><ul>{stand}</ul>
<p><b>Before a live run</b></p><ul>{items}</ul></section>
{"".join(cards)}</body></html>
"""


def main(argv) -> int:
    a = argparse.ArgumentParser(prog="python -m eos_app.dryrun", description=__doc__.split("\n\n")[0])
    a.add_argument("--project", required=True, help="the project folder to write into (outside the app)")
    a.add_argument("--library", required=True, help="the shared library folder (library/)")
    a.add_argument("--braindump", required=True, help="the story braindump, a text or Markdown file")
    a.add_argument("--brainstorm", help="the Author brainstorm, a text or Markdown file")
    a.add_argument("--manuscript-type", help="the manuscript type you have in mind")
    a.add_argument("--genre-path", help='stand-in for the gate decision: "Primary > Secondary > Major > Minor"')
    a.add_argument("--pen-name", help="stand-in for the gate decision: the pen name")
    x = a.parse_args(argv)
    paths = [p for p in (x.braindump, x.brainstorm) if p]
    for p in paths:
        guard_path(p)
    author = {"braindump": Path(x.braindump).read_text(encoding="utf-8"),
              "brainstorm": Path(x.brainstorm).read_text(encoding="utf-8") if x.brainstorm else None,
              "manuscript_type": x.manuscript_type}
    assumed = {"genre_path": parse_path(x.genre_path), "pen_name": x.pen_name, "manuscript_type": x.manuscript_type}
    try:
        s = dry_run(x.project, library_root=x.library, author=author, author_paths=paths, assumed=assumed)
    except PromptError as err:
        print("stopped:", err)
        return 1
    print(f"dry run · nothing was sent · {s['prompts']} prompts · {s['calls']} planned calls · "
          f"{s['gate_stops']} gate stops · up to {s['worst_case_tokens']:,} tokens · "
          + (f"${s['cost_usd_max']:.2f} at most" if s["cost_usd_max"] is not None else "cost not known yet"))
    for step, name, calls in s["steps"]:
        print(f"  {step:7} {name}: " + "; ".join(f"{r} {m} ({rt})" for r, m, rt in calls))
    print("before a live run:")
    for item in s["open_items"]:
        print("  -", item)
    print(f"see {Path(x.project) / 'dry-run.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
