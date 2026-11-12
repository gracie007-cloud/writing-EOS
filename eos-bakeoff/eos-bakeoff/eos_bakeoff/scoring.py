"""Automatic scoring (SPEC §4.1, §4.2, §4.4).

This module is the ONLY reader of answer keys (CLAUDE.md rule 1). Nothing read here is ever passed to
the prompt builder, and error messages name key fields, never key content.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .config import DATA_DIR, ROOT, Step

ANSWER_KEY_PATH = DATA_DIR / "Run01_ANSWER_KEY.yaml"
TEMPLATE_PATH = ROOT / "docs" / "answer_key_template.yaml"
BLANK = "FILL IN"
OVERLAP_THRESHOLD = 0.6
MISSING_PENALTY = 2
INVENTED_PENALTY = 3
# Titles dropped when deciding whether two invented names are the same person ("Captain Rook" = "Capt. Rook").
TITLES = {"captain", "capt", "doctor", "dr", "detective", "det", "inspector", "insp", "sergeant", "sgt",
          "officer", "professor", "prof", "mr", "mrs", "ms", "miss", "sir", "lady", "lord"}
SHEET_LINE = "False alarm? (yes / no):"
FENCE = re.compile(r"^\s*```[a-zA-Z]*\s*\n(.*?)\n?\s*```\s*$", re.S)


class AnswerKeyProblem(Exception):
    """The answer key is missing, blank or malformed."""


class SheetProblem(Exception):
    """The false-alarm confirmation sheet cannot be imported yet."""


# ---------- the answer key ----------

def load_answer_key(path: Path | str = ANSWER_KEY_PATH) -> dict:
    path = Path(path)
    if "ANSWER_KEY" not in path.name.upper():
        raise AnswerKeyProblem(f"'{path.name}' is not an answer key; the scorer reads only *ANSWER_KEY* files.")
    if not path.is_file():
        raise AnswerKeyProblem(f"No answer key at {path}. Copy {TEMPLATE_PATH.relative_to(ROOT).as_posix()} "
                               f"to data/Run01_ANSWER_KEY.yaml and fill it in from Notion.")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        where = getattr(exc, "problem_mark", None)
        line = f" near line {where.line + 1}" if where else ""
        raise AnswerKeyProblem(f"The answer key is not valid YAML{line}.") from None

    blanks = list(_blank_paths(raw, ""))
    if blanks:
        shown = ", ".join(blanks[:5]) + (f" and {len(blanks) - 5} more" if len(blanks) > 5 else "")
        raise AnswerKeyProblem(f"The answer key still has {len(blanks)} '{BLANK}' value(s): {shown}.")

    key = {"extraction": {}, "verdict": {}}
    for step_name, fields in (raw.get("extraction") or {}).items():
        key["extraction"][step_name] = {
            fname: {kind: [_entry(e, f"extraction.{step_name}.{fname}.{kind}[{i}]")
                           for i, e in enumerate((spec or {}).get(kind) or [])]
                    for kind in ("expected", "forbidden", "allowed")}
            for fname, spec in (fields or {}).items()}
    for step_name, spec in (raw.get("verdict") or {}).items():
        planted = []
        for i, p in enumerate((spec or {}).get("planted") or []):
            where = f"verdict.{step_name}.planted[{i}]"
            if not isinstance(p, dict) or not str(p.get("sentence") or "").strip():
                raise AnswerKeyProblem(f"{where} needs a 'sentence'.")
            keywords = [str(k) for k in p.get("keywords") or [] if str(k).strip()]
            if not keywords:
                raise AnswerKeyProblem(f"{where} needs at least one entry in 'keywords'.")
            planted.append({"id": str(p.get("id") or f"P{i + 1}"), "sentence": str(p["sentence"]),
                            "fact": str(p.get("fact") or ""), "keywords": keywords})
        if not planted:
            raise AnswerKeyProblem(f"verdict.{step_name} lists no planted errors.")
        key["verdict"][step_name] = {"planted": planted}
    return key


def _blank_paths(node, where: str):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from _blank_paths(v, f"{where}.{k}" if where else str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _blank_paths(v, f"{where}[{i}]")
    elif isinstance(node, str) and BLANK in node.upper():
        yield where


def _entry(e, where: str) -> dict:
    if isinstance(e, str) and e.strip():
        return {"name": e, "aliases": []}
    if isinstance(e, dict) and str(e.get("name") or "").strip():
        return {"name": str(e["name"]), "aliases": [str(a) for a in e.get("aliases") or [] if str(a).strip()]}
    raise AnswerKeyProblem(f"{where} needs a 'name'.")


def key_for(key: dict, step: Step) -> dict:
    section = "verdict" if step.scoring == "verdict" else "extraction"
    if step.name not in key[section]:
        raise AnswerKeyProblem(f"The answer key has no '{section}.{step.name}' section.")
    return key[section][step.name]


# ---------- text matching ----------

def normalize(text: str) -> str:
    """Case-, accent- and punctuation-insensitive form."""
    decomposed = unicodedata.normalize("NFKD", str(text))
    bare = "".join(ch for ch in decomposed if not unicodedata.combining(ch)).casefold()
    return " ".join(re.sub(r"[^\w]+", " ", bare).replace("_", " ").split())


def _tokens(text: str) -> list[str]:
    toks = normalize(text).split()
    return toks[1:] if toks[:1] == ["the"] and len(toks) > 1 else toks


def _person(text: str) -> tuple[str, ...]:
    """A name without titles, so one invented person written two ways is penalised once."""
    toks = _tokens(text)
    return tuple(t for t in toks if t not in TITLES) or tuple(toks)


def _span(item: list[str], form: list[str]) -> tuple[int, int] | None:
    n = len(form)
    for i in range(len(item) - n + 1):
        if item[i:i + n] == form:
            return i, i + n
    return None


def _best_span(item: list[str], entry: dict) -> tuple[int, int] | None:
    spans = [s for s in (_span(item, _tokens(f)) for f in [entry["name"], *entry["aliases"]] if _tokens(f)) if s]
    return max(spans, key=lambda s: s[1] - s[0]) if spans else None


def name_matches(item: str, entry: dict) -> bool:
    return _best_span(_tokens(item), entry) is not None


def _matched_entries(item: str, entries: list[tuple[str, dict]]) -> list[tuple[str, dict]]:
    """Entries named in `item`. A match inside a longer match for another entry does not count."""
    toks = _tokens(item)
    hits = [(kind, e, s) for kind, e in entries if (s := _best_span(toks, e))]
    return [(kind, e) for kind, e, s in hits
            if not any(o is not e and o_s[0] <= s[0] and s[1] <= o_s[1] and (o_s[1] - o_s[0]) > (s[1] - s[0])
                       for _, o, o_s in hits)]


def overlap(quote: str, planted: str) -> float:
    """Shared distinct words over the larger word set, so neither a fragment nor a whole paragraph passes."""
    a, b = set(normalize(quote).split()), set(normalize(planted).split())
    return len(a & b) / max(len(a), len(b)) if a and b else 0.0


def _mentions(text: str, keyword: str) -> bool:
    kw = normalize(keyword).split()
    return bool(kw) and _span(normalize(text).split(), kw) is not None


def parse_json_output(text: str | None) -> tuple[object, str]:
    """(data, problem). One surrounding ```json fence is tolerated; any other text is a format failure."""
    body = (text or "").strip()
    fenced = FENCE.match(body)
    if fenced:
        body = fenced.group(1).strip()
    try:
        return json.loads(body), ""
    except (json.JSONDecodeError, ValueError):
        return None, "output is not valid JSON"


# ---------- §4.1 structured extraction ----------

@dataclass
class ExtractionResult:
    score: float
    problem: str = ""
    missing: list[str] = field(default_factory=list)
    forbidden: list[str] = field(default_factory=list)
    invented: list[str] = field(default_factory=list)
    duplicates: list[str] = field(default_factory=list)

    def details(self) -> dict:
        return {"missing": self.missing, "forbidden": self.forbidden, "invented": self.invented,
                "duplicates": self.duplicates}


def score_extraction(text: str | None, step: Step, step_key: dict) -> ExtractionResult:
    data, problem = parse_json_output(text)
    if problem:
        return ExtractionResult(0, problem)
    fields = list((step.schema or {}).keys())
    if not isinstance(data, dict):
        return ExtractionResult(0, "output is not a JSON object")
    for fname in fields:
        value = data.get(fname)
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            return ExtractionResult(0, f"'{fname}' is missing or is not a list of names")
        if fname not in step_key:
            raise AnswerKeyProblem(f"The answer key has no '{step.name}.{fname}' list.")

    result = ExtractionResult(10)
    for fname in fields:
        spec = step_key[fname]
        entries = [(kind, e) for kind in ("expected", "forbidden", "allowed") for e in spec[kind]]
        found, banned, seen_items, invented_people = set(), [], set(), set()
        for item in data[fname]:
            norm = normalize(item)
            if not norm or norm in seen_items:
                continue
            seen_items.add(norm)
            hits = _matched_entries(item, entries)
            if not hits:
                if _person(item) in invented_people:
                    result.duplicates.append(item)
                else:
                    invented_people.add(_person(item))
                    result.invented.append(item)
                continue
            for kind, e in hits:
                if kind == "forbidden":
                    if e["name"] not in banned:
                        banned.append(e["name"])
                elif kind == "expected":
                    if id(e) in found:
                        result.duplicates.append(item)
                    found.add(id(e))
        result.forbidden += banned
        result.missing += [e["name"] for e in spec["expected"] if id(e) not in found]

    penalty = MISSING_PENALTY * len(result.missing) + INVENTED_PENALTY * (len(result.forbidden) + len(result.invented))
    result.score = max(0, 10 - penalty)
    return result


# ---------- §4.2 verdict / check ----------

def verdict_score(caught: int, planted: int, confirmed_false_alarms: int) -> float:
    return max(0, round(caught / planted * 9 + 1 - confirmed_false_alarms, 2))


@dataclass
class Candidate:
    cid: str            # "<blind_id> #<report number>"
    quote: str
    contradicts: str
    hint: str = ""


@dataclass
class VerdictResult:
    planted: int
    problem: str = ""
    caught: list[str] = field(default_factory=list)
    candidates: list[Candidate] = field(default_factory=list)
    duplicates: int = 0

    @property
    def provisional_score(self) -> float:
        return self.score({})

    def score(self, decisions: dict) -> float:
        if self.problem:
            return 0
        confirmed = sum(1 for c in self.candidates if decisions.get(c.cid) is True)
        return verdict_score(len(self.caught), self.planted, confirmed)

    def final(self, decisions: dict) -> bool:
        return bool(self.problem) or all(decisions.get(c.cid) is not None for c in self.candidates)

    def details(self) -> dict:
        return {"caught": self.caught, "reports_to_confirm": [c.cid for c in self.candidates],
                "repeat_reports": self.duplicates}


def score_verdict(text: str | None, step_key: dict, blind_id: str) -> VerdictResult:
    planted = step_key["planted"]
    result = VerdictResult(planted=len(planted))
    data, problem = parse_json_output(text)
    if problem:
        result.problem = problem
        return result
    reports = data.get("contradictions") if isinstance(data, dict) else None
    if not isinstance(reports, list):
        result.problem = "'contradictions' is missing or is not a list"
        return result

    for n, report in enumerate(reports, start=1):
        if not isinstance(report, dict):
            result.candidates.append(Candidate(f"{blind_id} #{n}", str(report), "", "report is not a quote/rule pair"))
            continue
        quote, rule = str(report.get("quote") or ""), str(report.get("contradicts") or "")
        best = max(planted, key=lambda p: overlap(quote, p["sentence"]))
        if overlap(quote, best["sentence"]) >= OVERLAP_THRESHOLD:
            if any(_mentions(rule, k) for k in best["keywords"]):
                if best["id"] in result.caught:
                    result.duplicates += 1
                else:
                    result.caught.append(best["id"])
                continue
            hint = f"quote matches planted error {best['id']}, but the stated rule does not name its fact"
        else:
            hint = ""
        result.candidates.append(Candidate(f"{blind_id} #{n}", quote, rule, hint))
    result.caught.sort(key=[p["id"] for p in planted].index)
    return result


# ---------- the false-alarm confirmation sheet ----------

SHEET_HEADING = re.compile(r"^### (\S+ #\d+)\s*$")


def write_false_alarm_sheet(path: Path, step_name: str, results: dict[str, VerdictResult],
                            previous: dict | None = None) -> int:
    """One entry per candidate false alarm, under blind IDs only. Returns how many are still undecided."""
    previous = previous or {}
    lines = [f"# False-alarm confirmation · {step_name}", "",
             "Each report below did not match a planted error. Decide whether it is a **false alarm** "
             "(the brief does not really contradict the bible). Type `yes` or `no` at the end of each "
             "*False alarm?* line, save, then run:", "",
             f"    python -m eos_bakeoff score --step {step_name} --import", "",
             "Each confirmed false alarm costs that run 1 point. Model names are not shown.", ""]
    undecided = 0
    for blind_id in sorted(results):
        for c in results[blind_id].candidates:
            decision = previous.get(c.cid)
            undecided += decision is None
            answer = "" if decision is None else (" yes" if decision else " no")
            lines += ["---", "", f"### {c.cid}", "", f"**Quoted from the brief:** {c.quote or '(empty)'}", "",
                      f"**Rule it says is broken:** {c.contradicts or '(empty)'}", ""]
            if c.hint:
                lines += [f"*Note: {c.hint}.*", ""]
            lines += [f"{SHEET_LINE}{answer}", ""]
    if not any(r.candidates for r in results.values()):
        lines += ["No reports need confirming.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return undecided


def read_false_alarm_sheet(path: Path) -> dict[str, bool | None]:
    decisions: dict[str, bool | None] = {}
    current = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        heading = SHEET_HEADING.match(line.strip())
        if heading:
            current = heading.group(1)
            decisions[current] = None
        elif current and line.strip().startswith(SHEET_LINE):
            answer = line.strip()[len(SHEET_LINE):].strip().strip("*`").lower()
            if answer in ("yes", "y"):
                decisions[current] = True
            elif answer in ("no", "n"):
                decisions[current] = False
            elif answer:
                raise SheetProblem(f"{current}: answer '{answer}' is not yes or no.")
    return decisions


# ---------- a whole step, from the run records ----------

def load_records(day_dir: Path, step_name: str) -> list[dict]:
    path = day_dir / "runs.jsonl"
    if not path.is_file():
        return []
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [r for r in rows if r.get("step") == step_name]


def sheet_path(day_dir: Path, step_name: str) -> Path:
    return day_dir / f"{step_name}_false_alarms.md"


def score_step(step: Step, key: dict, day_dir: Path, import_sheet: bool = False) -> dict:
    """Score every run of `step` in one day folder; write scores_<step>.json (and the sheet for verdicts)."""
    if step.scoring not in ("extraction", "verdict"):
        raise AnswerKeyProblem(f"'{step.name}' is scored by human review (Phase 3), not automatically.")
    step_key = key_for(key, step)
    records = load_records(day_dir, step.name)
    if not records:
        raise AnswerKeyProblem(f"No runs of '{step.name}' in {day_dir}.")
    base = day_dir.parent.parent

    rows, verdicts = [], {}
    for rec in records:
        row = {"blind_id": rec["blind_id"], "run_id": rec["run_id"], "status": rec["status"],
               "score": None, "final": True, "problem": "", "details": {}}
        text = (base / rec["output_path"]).read_text(encoding="utf-8") if rec.get("output_path") else None
        if rec["status"] == "error":
            row["problem"] = "call failed; not scored (re-run it)"
        elif rec["status"] in ("refused", "truncated"):
            row["score"], row["problem"] = 0, f"{rec['status']} (SPEC §4.4: scores 0)"
        elif step.scoring == "extraction":
            r = score_extraction(text, step, step_key)
            row.update(score=r.score, problem=r.problem, details=r.details())
        else:
            verdicts[rec["blind_id"]] = score_verdict(text, step_key, rec["blind_id"])
        rows.append(row)

    summary = {"step": step.name, "scored_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "final": True, "pending": 0, "sheet": None, "runs": rows}
    if verdicts:
        sheet = sheet_path(day_dir, step.name)
        previous = read_false_alarm_sheet(sheet) if sheet.is_file() else {}
        undecided = write_false_alarm_sheet(sheet, step.name, verdicts, previous)
        decisions = read_false_alarm_sheet(sheet)
        if import_sheet and undecided:
            raise SheetProblem(f"{undecided} still blank on {sheet.name}. Answer every 'False alarm?' line, "
                               f"then import again.")
        for row in rows:
            v = verdicts.get(row["blind_id"])
            if v:
                row.update(score=v.score(decisions), final=v.final(decisions), problem=v.problem,
                           details=v.details())
        summary.update(pending=undecided, sheet=str(sheet))
    summary["final"] = all(r["final"] for r in rows)

    (day_dir / f"scores_{step.name}.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False),
                                                       encoding="utf-8")
    return summary
