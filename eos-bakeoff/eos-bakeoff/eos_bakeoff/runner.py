"""Run a step against candidate models, N runs each, and record everything."""

from __future__ import annotations

import json
import secrets
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path

from .clients import CallResult
from .config import RUNS_DIR, Model, Step
from .prompts import check_mature, input_hash

BLIND_PREFIX = {
    "first_draft": "FD",
    "first_draft_mature": "FM",
    "character_selector": "CS",
    "worldbuilding_selector": "WS",
    "scene_brief": "SB",
    "chronology_check": "CC",
}
BLIND_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"  # no 0/O, 1/I/L
REFUSAL_OPENINGS = (
    "i can't", "i cannot", "i can not", "i'm sorry", "i am sorry", "i'm unable", "i am unable",
    "i won't", "i will not", "sorry, but", "as an ai",
)


@dataclass
class RunRecord:
    run_id: str
    timestamp: str
    step: str
    model_key: str
    model_id: str
    run_number: int
    blind_id: str
    input_hash: str
    output_path: str
    input_tokens: int | None
    output_tokens: int | None      # answer + thinking, as billed
    reasoning_tokens: int | None   # thinking only, when the provider reports it
    answer_budget: int
    reasoning_budget: int
    reasoning_path: str
    cost_usd: float | None
    cost_source: str | None
    latency_s: float
    attempts: int
    finish_reason: str | None
    status: str           # ok | refused | truncated | error
    error_message: str


def classify(result: CallResult) -> str:
    """ok / refused / truncated / error. Refusal detection is a first pass; review can overturn it."""
    if result.error:
        return "error"
    if result.finish_reason == "length":
        return "truncated"
    text = (result.text or "").strip()
    if result.finish_reason == "content_filter" or not text:
        return "refused"
    if len(text) < 600 and text.lower().startswith(REFUSAL_OPENINGS):
        return "refused"
    return "ok"


def new_blind_id(step_name: str, taken: set[str]) -> str:
    prefix = BLIND_PREFIX.get(step_name, step_name[:2].upper())
    while True:
        candidate = f"{prefix}-" + "".join(secrets.choice(BLIND_ALPHABET) for _ in range(3))
        if candidate not in taken:
            taken.add(candidate)
            return candidate


class RunStore:
    """runs/<date>/runs.jsonl, runs/<date>/<step>/<blind_id>.md, runs/<date>/BLIND_MAP.json."""

    def __init__(self, day: date | None = None, root: Path = RUNS_DIR):
        self.dir = root / (day or date.today()).isoformat()
        self.dir.mkdir(parents=True, exist_ok=True)
        self.records_path = self.dir / "runs.jsonl"
        self.blind_map_path = self.dir / "BLIND_MAP.json"
        self._lock = threading.Lock()

    def blind_map(self) -> dict:
        if self.blind_map_path.is_file():
            return json.loads(self.blind_map_path.read_text(encoding="utf-8"))
        return {}

    def reserve_blind_id(self, step: Step, model: Model, run_number: int) -> str:
        with self._lock:
            mapping = self.blind_map()
            blind_id = new_blind_id(step.name, set(mapping))
            mapping[blind_id] = {"step": step.name, "model_key": model.key,
                                 "model_id": model.id, "run_number": run_number}
            self.blind_map_path.write_text(json.dumps(mapping, indent=2, sort_keys=True), encoding="utf-8")
            return blind_id

    def save_output(self, step: Step, blind_id: str, text: str, suffix: str = ".md") -> str:
        folder = self.dir / step.name
        folder.mkdir(exist_ok=True)
        path = folder / f"{blind_id}{suffix}"
        with path.open("w", encoding="utf-8", newline="") as fh:
            fh.write(text)  # verbatim: never cleaned or edited
        return path.relative_to(self.dir.parent.parent).as_posix()

    def append(self, record: RunRecord) -> None:
        with self._lock, self.records_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")


def run_step(step: Step, models: list[Model], prompt: str, runs: int, client, store: RunStore,
             concurrency: int = 2, on_done=None) -> list[RunRecord]:
    """Send the same prompt to every model `runs` times. Every call becomes a record, even failures."""
    for model in models:
        check_mature(step, model)
    digest = input_hash(prompt)
    jobs = [(model, n) for model in models for n in range(1, runs + 1)]

    def one(job: tuple[Model, int]) -> RunRecord:
        model, run_number = job
        blind_id = store.reserve_blind_id(step, model, run_number)
        try:
            result = client.chat(model.id, prompt, step.temperature, step.max_tokens, step.reasoning_max_tokens)
        except Exception as exc:  # recorded, never swallowed
            result = CallResult(None, None, None, None, None, None, 0.0, 1, error=f"{type(exc).__name__}: {exc}")
        # Whatever text arrived is kept, including partial text from a truncated run.
        output_path = store.save_output(step, blind_id, result.text) if result.text else ""
        reasoning_path = (store.save_output(step, blind_id, result.reasoning, suffix=".reasoning.md")
                          if result.reasoning else "")
        cost, cost_source = result.cost_usd, result.cost_source
        if cost is None and result.input_tokens is not None and model.price_in is not None and model.price_out is not None:
            cost = (result.input_tokens * model.price_in + (result.output_tokens or 0) * model.price_out) / 1_000_000
            cost_source = "models.yaml prices"
        record = RunRecord(
            run_id=uuid.uuid4().hex[:12],
            timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            step=step.name,
            model_key=model.key,
            model_id=model.id or "",
            run_number=run_number,
            blind_id=blind_id,
            input_hash=digest,
            output_path=output_path,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            reasoning_tokens=result.reasoning_tokens,
            answer_budget=step.max_tokens,
            reasoning_budget=step.reasoning_max_tokens,
            reasoning_path=reasoning_path,
            cost_usd=round(cost, 6) if cost is not None else None,
            cost_source=cost_source,
            latency_s=round(result.latency_s, 2),
            attempts=result.attempts,
            finish_reason=result.finish_reason,
            status=classify(result),
            error_message=result.error or "",
        )
        store.append(record)
        if on_done:
            on_done(record)
        return record

    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
        return list(pool.map(one, jobs))
