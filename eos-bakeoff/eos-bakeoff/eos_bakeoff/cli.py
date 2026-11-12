"""Command line: python -m eos_bakeoff <command> ..."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict

from rich.console import Console
from rich.table import Table

from .clients import OpenRouterClient
from .config import DEFAULT_CONCURRENCY, RUNS_DIR, TEST_PACK, ConfigError, Model, Step, load_all, load_keys
from .prompts import AnswerKeyError, PromptError, build_prompt, check_mature, estimate_tokens, read_test_pack, split_sections
from .runner import RunStore, run_step
from .scoring import AnswerKeyProblem, SheetProblem, load_answer_key, load_records, score_step

console = Console()


def _pick_models(step: Step, models: dict[str, Model], wanted: str | None) -> list[Model]:
    keys = [k.strip() for k in wanted.split(",")] if wanted else list(step.candidates)
    unknown = [k for k in keys if k not in models]
    if unknown:
        raise ConfigError(f"Unknown model key(s): {', '.join(unknown)}. Keys are listed in config/models.yaml.")
    return [models[k] for k in keys]


def _prompt_for(step: Step) -> str:
    return build_prompt(step, split_sections(read_test_pack(TEST_PACK)))


def cmd_estimate(args, models, steps) -> int:
    step = steps[args.step]
    chosen = _pick_models(step, models, args.models)
    prompt = _prompt_for(step)
    in_tokens = estimate_tokens(prompt)
    out_tokens = step.request_max_tokens

    table = Table(title=f"Estimate · {step.name} · {args.runs} run(s) per model")
    for col in ("Model", "ID status", "Input tokens (≈)",
                f"Output max (answer {step.max_tokens:,} + thinking {step.reasoning_max_tokens:,})",
                "Cost per run", "Total"):
        table.add_column(col)
    grand, unknown = 0.0, False
    for model in chosen:
        status = "verified" if model.verified else "NOT VERIFIED"
        if model.provider != "openrouter":
            cost_run, total = "hourly endpoint (Phase 4)", "—"
            unknown = True
        elif model.price_in is None or model.price_out is None:
            cost_run, total = "price unknown", "—"
            unknown = True
        else:
            per = (in_tokens * model.price_in + out_tokens * model.price_out) / 1_000_000
            grand += per * args.runs
            cost_run, total = f"${per:.4f}", f"${per * args.runs:.4f}"
        table.add_row(model.key, status, f"{in_tokens:,}", f"{out_tokens:,}", cost_run, total)
    console.print(table)
    console.print(f"Known total (upper bound): [bold]${grand:.4f}[/bold]"
                  + ("  · some prices unknown: fill price_in / price_out in config/models.yaml" if unknown else ""))
    console.print("Input tokens are approximate (about 4 characters per token); output assumes both budgets are used in full.")
    return 0


def cmd_run(args, models, steps) -> int:
    step = steps[args.step]
    chosen = _pick_models(step, models, args.models)

    runnable, skipped = [], []
    for model in chosen:
        if model.provider != "openrouter":
            skipped.append((model.key, "Hugging Face endpoints arrive in Phase 4"))
        elif not model.verified:
            skipped.append((model.key, "ID still marked VERIFY in config/models.yaml"))
        else:
            check_mature(step, model)
            runnable.append(model)
    for key, why in skipped:
        console.print(f"[yellow]Skipped {key}:[/yellow] {why}")
    if not runnable:
        console.print("[red]Nothing to run.[/red] Verify at least one model ID in config/models.yaml.")
        return 2

    keys = load_keys()
    api_key = keys.get("OPENROUTER_API_KEY")
    if not api_key:
        console.print("[red]OPENROUTER_API_KEY is not set.[/red] Create a file named .env next to README.md containing:\n"
                      "OPENROUTER_API_KEY=your-key-here")
        return 2

    prompt = _prompt_for(step)
    store = RunStore()
    total = len(runnable) * args.runs
    console.print(f"Sending [bold]{total}[/bold] call(s) for step [bold]{step.name}[/bold] "
                  f"({len(runnable)} model(s) × {args.runs} run(s)), at most {args.concurrency} at a time.")
    done = {"n": 0}

    def progress(record):
        done["n"] += 1
        colour = {"ok": "green", "error": "red"}.get(record.status, "yellow")
        console.print(f"  {done['n']}/{total} finished · [{colour}]{record.status}[/{colour}]")

    client = OpenRouterClient(api_key)
    try:
        records = run_step(step, runnable, prompt, args.runs, client, store,
                           concurrency=args.concurrency, on_done=progress)
    finally:
        client.close()

    by_model = defaultdict(list)
    for r in records:
        by_model[r.model_key].append(r)
    table = Table(title=f"{step.name} · results by model (blind IDs are not shown here)")
    for col in ("Model", "Runs", "ok / refused / truncated / error", "Tokens in / out (of which thinking)",
                "Cost", "Avg seconds"):
        table.add_column(col)
    for key, rs in by_model.items():
        counts = {s: sum(r.status == s for r in rs) for s in ("ok", "refused", "truncated", "error")}
        tin = sum(r.input_tokens or 0 for r in rs)
        tout = sum(r.output_tokens or 0 for r in rs)
        think = sum(r.reasoning_tokens or 0 for r in rs)
        costs = [r.cost_usd for r in rs if r.cost_usd is not None]
        cost = f"${sum(costs):.4f}" + ("" if len(costs) == len(rs) else " (partial)") if costs else "unknown"
        avg = sum(r.latency_s for r in rs) / len(rs)
        table.add_row(key, str(len(rs)), " / ".join(str(counts[s]) for s in counts),
                      f"{tin:,} / {tout:,} ({think:,})", cost, f"{avg:.1f}")
    console.print(table)
    for r in records:
        if r.error_message:
            console.print(f"[red]Error on a {r.model_key} run:[/red] {r.error_message}")
    console.print(f"Outputs: {store.dir / step.name}  (named by blind ID)")
    console.print(f"Run records: {store.records_path}")
    console.print(f"Blind map: {store.blind_map_path}  [dim](do not open before scoring)[/dim]")
    return 0 if any(r.status == "ok" for r in records) else 1


def _day_for(step: Step, wanted: str | None):
    if wanted:
        day = RUNS_DIR / wanted
        if not load_records(day, step.name):
            raise AnswerKeyProblem(f"No runs of '{step.name}' in runs/{wanted}.")
        return day
    days = sorted((d for d in RUNS_DIR.iterdir() if d.is_dir() and load_records(d, step.name)),
                  reverse=True) if RUNS_DIR.is_dir() else []
    if not days:
        raise AnswerKeyProblem(f"No runs of '{step.name}' yet. Run it first: python -m eos_bakeoff run --step {step.name}")
    return days[0]


def cmd_score(args, models, steps) -> int:
    step = steps[args.step]
    if step.scoring not in ("extraction", "verdict"):
        console.print(f"'{step.name}' is scored by human review: the review sheet arrives in Phase 3.")
        return 0
    day = _day_for(step, args.date)
    summary = score_step(step, load_answer_key(), day, import_sheet=args.import_)

    table = Table(title=f"Scores · {step.name} · runs/{day.name} (blind IDs; model names are in BLIND_MAP.json)")
    for col in ("Blind ID", "Status", "Score /10", "Notes"):
        table.add_column(col)
    for r in sorted(summary["runs"], key=lambda r: r["blind_id"]):
        d = r["details"]
        if r["problem"]:
            note = r["problem"]
        elif step.scoring == "extraction":
            note = (f"missing {len(d['missing'])} · forbidden {len(d['forbidden'])} · invented {len(d['invented'])}"
                    + (f" · repeats {len(d['duplicates'])}" if d["duplicates"] else ""))
        else:
            note = f"caught {len(d['caught'])} · reports to confirm {len(d['reports_to_confirm'])}"
        score = "not scored" if r["score"] is None else f"{r['score']:g}" + ("" if r["final"] else " (provisional)")
        table.add_row(r["blind_id"], r["status"], score, note)
    console.print(table)

    if summary["sheet"] and not summary["final"]:
        console.print(f"[yellow]{summary['pending']} report(s) need your decision.[/yellow] Open:\n"
                      f"  {summary['sheet']}\n"
                      f"answer each 'False alarm?' line, then run:\n"
                      f"  python -m eos_bakeoff score --step {step.name} --import")
    elif summary["sheet"]:
        console.print(f"False-alarm decisions applied from {summary['sheet']}")
    console.print(f"Scores saved: {day / f'scores_{step.name}.json'}")
    return 0


def cmd_later(args, *_):
    phase = {"sheet": 3, "report": 3}[args.command]
    console.print(f"'{args.command}' arrives in Phase {phase}.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m eos_bakeoff", description="Writing EOS bake-off harness")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="send a step's test material to models and record the results")
    run.add_argument("--step", required=True)
    run.add_argument("--models", help="comma-separated model keys (default: the step's candidates)")
    run.add_argument("--runs", type=int, default=3)
    run.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)

    est = sub.add_parser("estimate", help="projected cost before anything is sent")
    est.add_argument("--step", required=True)
    est.add_argument("--models")
    est.add_argument("--runs", type=int, default=3)

    score = sub.add_parser("score", help="score a step's runs automatically (extraction and verdict steps)")
    score.add_argument("--step", required=True)
    score.add_argument("--date", help="runs/<YYYY-MM-DD> folder to score (default: the latest with this step)")
    score.add_argument("--import", dest="import_", action="store_true",
                       help="apply the completed false-alarm sheet and finalise the scores")

    for name in ("sheet", "report"):
        later = sub.add_parser(name, help=f"(not built yet)")
        later.add_argument("--step")
        later.add_argument("--import", dest="import_", action="store_true")
    return parser


def main(argv=None) -> int:
    # A console that cannot show a character (e.g. "≈" on cp1252) gets "?" instead of a crash.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    args = build_parser().parse_args(argv)
    try:
        models, steps = load_all()
        if getattr(args, "step", None) and args.command in ("run", "estimate", "score") and args.step not in steps:
            console.print(f"[red]Unknown step '{args.step}'.[/red] Steps: {', '.join(steps)}")
            return 2
        handler = {"run": cmd_run, "estimate": cmd_estimate, "score": cmd_score}.get(args.command, cmd_later)
        return handler(args, models, steps)
    except (ConfigError, PromptError, AnswerKeyError, AnswerKeyProblem, SheetProblem) as exc:
        console.print(f"[red]Stopped:[/red] {exc}")
        return 2
