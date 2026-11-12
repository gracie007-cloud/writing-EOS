"""Phase 2 tests: extraction and verdict scorers, the false-alarm sheet, the answer-key reader.

Every key used here is MADE UP (tests/fixtures/sample_ANSWER_KEY.yaml). No network.
"""

import json
import shutil
from datetime import date
from pathlib import Path

import pytest

from eos_bakeoff.config import ROOT, TEST_PACK, load_all
from eos_bakeoff.prompts import AnswerKeyError, read_test_pack
from eos_bakeoff.runner import RunRecord, RunStore
from eos_bakeoff.scoring import (AnswerKeyProblem, SheetProblem, load_answer_key, name_matches, normalize,
                                 overlap, read_false_alarm_sheet, score_extraction, score_step, score_verdict,
                                 verdict_score, write_false_alarm_sheet)

FIXTURES = Path(__file__).parent / "fixtures"
OUTPUTS = FIXTURES / "outputs"
SAMPLE_KEY = FIXTURES / "sample_ANSWER_KEY.yaml"
TEMPLATE = ROOT / "docs" / "answer_key_template.yaml"


def out(name: str) -> str:
    return (OUTPUTS / name).read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def key():
    return load_answer_key(SAMPLE_KEY)


@pytest.fixture(scope="module")
def steps():
    return load_all()[1]


def chars_key(key):
    return key["extraction"]["character_selector"]


def world_key(key):
    return key["extraction"]["worldbuilding_selector"]


def cc_key(key):
    return key["verdict"]["chronology_check"]


# ---------- the answer key reader ----------

def test_prompt_builder_refuses_the_key_file():
    with pytest.raises(AnswerKeyError):
        read_test_pack(SAMPLE_KEY)


def test_key_reader_only_reads_answer_keys():
    with pytest.raises(AnswerKeyProblem):
        load_answer_key(TEST_PACK)


def test_missing_key_explains_what_to_do(tmp_path):
    with pytest.raises(AnswerKeyProblem, match="answer_key_template.yaml"):
        load_answer_key(tmp_path / "Run01_ANSWER_KEY.yaml")


def test_blank_template_is_refused_without_echoing_content(tmp_path):
    copy = tmp_path / "Run01_ANSWER_KEY.yaml"
    shutil.copy(TEMPLATE, copy)
    with pytest.raises(AnswerKeyProblem, match="FILL IN") as err:
        load_answer_key(copy)
    assert "extraction.character_selector" in str(err.value)


def test_key_needs_rule_keywords(tmp_path):
    bad = tmp_path / "x_ANSWER_KEY.yaml"
    bad.write_text("verdict:\n  chronology_check:\n    planted:\n      - id: P1\n        sentence: s\n"
                   "        keywords: []\n", encoding="utf-8")
    with pytest.raises(AnswerKeyProblem, match="keywords"):
        load_answer_key(bad)


def test_key_accepts_plain_string_entries(tmp_path):
    k = tmp_path / "x_ANSWER_KEY.yaml"
    k.write_text("extraction:\n  character_selector:\n    characters:\n      expected: [Mara Quill]\n",
                 encoding="utf-8")
    loaded = load_answer_key(k)
    entry = loaded["extraction"]["character_selector"]["characters"]["expected"][0]
    assert entry == {"name": "Mara Quill", "aliases": []}


# ---------- name matching ----------

def test_normalize_handles_case_and_diacritics():
    assert normalize("LÚCIA  Fonseca!") == normalize("lucia fonseca")


@pytest.mark.parametrize("item,entry,expected", [
    ("Lucia Fonseca", {"name": "Lúcia Fonseca", "aliases": []}, True),
    ("Salt Archive", {"name": "The Salt Archive", "aliases": []}, True),
    ("World Rule 1: Tides", {"name": "Tides", "aliases": ["Rule 1"]}, True),
    ("Rule 10", {"name": "Masks", "aliases": ["Rule 1"]}, False),
    ("Quillon", {"name": "Mara Quill", "aliases": ["Quill"]}, False),
])
def test_name_matches(item, entry, expected):
    assert name_matches(item, entry) is expected


# ---------- extraction scorer ----------

def test_extraction_perfect(key, steps):
    r = score_extraction(out("chars_perfect.md"), steps["character_selector"], chars_key(key))
    assert r.score == 10 and not r.problem
    assert r.missing == [] and r.invented == [] and r.forbidden == []


def test_extraction_bad(key, steps):
    # Missing Brede and Fonseca (-4), forbidden Kaan (-3), invented Captain Rook (-3).
    r = score_extraction(out("chars_bad.md"), steps["character_selector"], chars_key(key))
    assert r.score == 0
    assert len(r.missing) == 2
    assert r.forbidden == ["Ivo Kaan"]
    assert r.invented == ["Captain Rook"]


def test_extraction_tolerates_fences_aliases_and_repeats(key, steps):
    r = score_extraction(out("chars_fenced.md"), steps["character_selector"], chars_key(key))
    assert r.score == 10
    assert r.duplicates == ["Quill"]


def test_extraction_unparseable_is_zero(key, steps):
    r = score_extraction(out("chars_broken.md"), steps["character_selector"], chars_key(key))
    assert r.score == 0 and "JSON" in r.problem


def test_extraction_wrong_shape_is_zero(key, steps):
    r = score_extraction(out("chars_wrong_shape.md"), steps["character_selector"], chars_key(key))
    assert r.score == 0 and "characters" in r.problem


def test_extraction_two_fields_perfect(key, steps):
    r = score_extraction(out("world_perfect.md"), steps["worldbuilding_selector"], world_key(key))
    assert r.score == 10   # "Rule 3 · Ferries" is on the allowed list: no penalty


def test_extraction_two_fields_bad(key, steps):
    # Missing Pier Nine (-2) and Lanterns (-2); forbidden Night Bazaar (-3).
    r = score_extraction(out("world_bad.md"), steps["worldbuilding_selector"], world_key(key))
    assert r.score == 3
    assert r.forbidden == ["The Night Bazaar"]


def test_extraction_floor_is_zero(key, steps):
    text = json.dumps({"characters": ["A One", "B Two", "C Three", "D Four", "E Five"]})
    assert score_extraction(text, steps["character_selector"], chars_key(key)).score == 0


def test_forbidden_counted_once_per_entry(key, steps):
    text = json.dumps({"characters": ["Mara Quill", "Oskar Brede", "Lúcia Fonseca", "Ivo Kaan", "Kaan"]})
    r = score_extraction(text, steps["character_selector"], chars_key(key))
    assert r.score == 7


@pytest.mark.parametrize("variants", [["Captain Rook", "Capt. Rook"], ["Captain Rook", "Rook"], ["Dr Rook", "Doctor Rook"]])
def test_invented_name_written_two_ways_costs_once(key, steps, variants):
    # Audit B3: one invented person listed under a title and its short form is one invention, not two.
    text = json.dumps({"characters": ["Mara Quill", "Oskar Brede", "Lúcia Fonseca"] + variants})
    r = score_extraction(text, steps["character_selector"], chars_key(key))
    assert r.score == 7
    assert r.invented == [variants[0]]
    assert r.duplicates == [variants[1]]


def test_different_invented_names_each_cost(key, steps):
    text = json.dumps({"characters": ["Mara Quill", "Oskar Brede", "Lúcia Fonseca", "Captain Rook", "Ana Vell"]})
    r = score_extraction(text, steps["character_selector"], chars_key(key))
    assert r.score == 4
    assert r.invented == ["Captain Rook", "Ana Vell"]


# ---------- verdict scorer ----------

def test_overlap():
    planted = "Quill reports to the harbour office every evening."
    assert overlap("Quill reports to the harbour office each evening", planted) >= 0.6
    assert overlap("The tide comes in at dawn.", planted) < 0.6


@pytest.mark.parametrize("caught,confirmed,expected", [(3, 0, 10), (2, 0, 7), (1, 0, 4), (0, 0, 1),
                                                       (1, 2, 2), (0, 3, 0)])
def test_verdict_formula(caught, confirmed, expected):
    assert verdict_score(caught, 3, confirmed) == expected


def test_verdict_perfect(key):
    r = score_verdict(out("verdict_perfect.md"), cc_key(key), "CC-AAA")
    assert r.caught == ["P1", "P2", "P3"] and r.candidates == []
    assert r.score({}) == 10 and r.final({})


def test_verdict_bad(key):
    # P1 caught. P2 quoted but with the wrong rule: not caught, goes to the sheet. One invented report.
    r = score_verdict(out("verdict_bad.md"), cc_key(key), "CC-BBB")
    assert r.caught == ["P1"]
    assert [c.cid for c in r.candidates] == ["CC-BBB #2", "CC-BBB #3"]
    assert "P2" in r.candidates[0].hint and r.candidates[1].hint == ""
    assert r.provisional_score == 4 and not r.final({})
    assert r.score({"CC-BBB #2": True, "CC-BBB #3": True}) == 2
    assert r.score({"CC-BBB #2": False, "CC-BBB #3": True}) == 3


def test_verdict_paraphrased_quote_is_caught(key):
    r = score_verdict(out("verdict_paraphrase.md"), cc_key(key), "CC-CCC")
    assert r.caught == ["P1"] and r.score({}) == 4


def test_verdict_empty_list(key):
    r = score_verdict(out("verdict_empty.md"), cc_key(key), "CC-DDD")
    assert r.caught == [] and r.score({}) == 1 and r.final({})


def test_verdict_unparseable_is_zero(key):
    r = score_verdict(out("verdict_broken.md"), cc_key(key), "CC-EEE")
    assert r.problem and r.score({}) == 0 and r.final({})


def test_verdict_repeat_of_caught_error_is_not_a_false_alarm(key):
    text = json.dumps({"contradictions": [
        {"quote": "Quill reports to the harbour office every evening.", "contradicts": "the Salt Archive"},
        {"quote": "Quill reports to the harbour office every evening", "contradicts": "Salt Archive rule"}]})
    r = score_verdict(text, cc_key(key), "CC-FFF")
    assert r.caught == ["P1"] and r.candidates == [] and r.duplicates == 1


# ---------- false-alarm confirmation sheet ----------

def test_sheet_round_trip(key, tmp_path):
    results = {"CC-BBB": score_verdict(out("verdict_bad.md"), cc_key(key), "CC-BBB"),
               "CC-AAA": score_verdict(out("verdict_perfect.md"), cc_key(key), "CC-AAA")}
    sheet = tmp_path / "sheet.md"
    write_false_alarm_sheet(sheet, "chronology_check", results)
    text = sheet.read_text(encoding="utf-8")
    assert "CC-BBB #2" in text and "CC-BBB #3" in text
    assert "CC-AAA" not in text                       # nothing to confirm for a perfect run
    for planted in cc_key(key)["planted"]:
        assert planted["fact"] not in text            # the key's facts never appear on the sheet
    assert read_false_alarm_sheet(sheet) == {"CC-BBB #2": None, "CC-BBB #3": None}

    filled = text.replace("False alarm? (yes / no):", "False alarm? (yes / no): yes", 1)
    filled = filled.replace("False alarm? (yes / no):\n", "False alarm? (yes / no): no\n", 1)
    sheet.write_text(filled, encoding="utf-8")
    assert read_false_alarm_sheet(sheet) == {"CC-BBB #2": True, "CC-BBB #3": False}


def test_sheet_rewrite_keeps_decisions(key, tmp_path):
    results = {"CC-BBB": score_verdict(out("verdict_bad.md"), cc_key(key), "CC-BBB")}
    sheet = tmp_path / "sheet.md"
    write_false_alarm_sheet(sheet, "chronology_check", results)
    sheet.write_text(sheet.read_text(encoding="utf-8").replace(
        "False alarm? (yes / no):", "False alarm? (yes / no): yes", 1), encoding="utf-8")
    write_false_alarm_sheet(sheet, "chronology_check", results, previous=read_false_alarm_sheet(sheet))
    assert read_false_alarm_sheet(sheet) == {"CC-BBB #2": True, "CC-BBB #3": None}


def test_sheet_rejects_unclear_answers(tmp_path):
    sheet = tmp_path / "sheet.md"
    sheet.write_text("### CC-BBB #2\nFalse alarm? (yes / no): maybe\n", encoding="utf-8")
    with pytest.raises(SheetProblem, match="CC-BBB #2"):
        read_false_alarm_sheet(sheet)


# ---------- whole step, from run records ----------

def _store_with(tmp_path, step, outputs: dict[str, tuple[str, str]]) -> RunStore:
    """outputs: blind_id -> (status, text)."""
    store = RunStore(day=date(2026, 10, 18), root=tmp_path / "runs")
    for n, (blind_id, (status, text)) in enumerate(outputs.items(), start=1):
        path = store.save_output(step, blind_id, text) if text else ""
        store.append(RunRecord(
            run_id=f"r{n}", timestamp="2026-10-18T00:00:00+00:00", step=step.name, model_key="m", model_id="x/y",
            run_number=n, blind_id=blind_id, input_hash="h", output_path=path, input_tokens=1, output_tokens=1,
            reasoning_tokens=0, answer_budget=1, reasoning_budget=0, reasoning_path="", cost_usd=0.0,
            cost_source="test", latency_s=1.0, attempts=1, finish_reason="stop", status=status,
            error_message="HTTP 402" if status == "error" else ""))
    return store


def test_score_step_extraction(key, steps, tmp_path):
    step = steps["character_selector"]
    store = _store_with(tmp_path, step, {
        "CS-AAA": ("ok", out("chars_perfect.md")),
        "CS-BBB": ("ok", out("chars_bad.md")),
        "CS-CCC": ("refused", "I can't help with that."),
        "CS-DDD": ("truncated", '{"characters": ["Mara'),
        "CS-EEE": ("error", ""),
    })
    summary = score_step(step, key, store.dir)
    scores = {r["blind_id"]: r["score"] for r in summary["runs"]}
    assert scores == {"CS-AAA": 10, "CS-BBB": 0, "CS-CCC": 0, "CS-DDD": 0, "CS-EEE": None}
    saved = json.loads((store.dir / "scores_character_selector.json").read_text(encoding="utf-8"))
    assert saved["final"] is True
    assert "model_key" not in json.dumps(saved)        # scores stay blind


def test_score_step_verdict_needs_import(key, steps, tmp_path):
    step = steps["chronology_check"]
    store = _store_with(tmp_path, step, {"CC-AAA": ("ok", out("verdict_perfect.md")),
                                         "CC-BBB": ("ok", out("verdict_bad.md"))})
    summary = score_step(step, key, store.dir)
    assert summary["final"] is False and summary["pending"] == 2
    sheet = Path(summary["sheet"])
    assert sheet.is_file()

    with pytest.raises(SheetProblem, match="2 still blank"):
        score_step(step, key, store.dir, import_sheet=True)

    text = sheet.read_text(encoding="utf-8").replace("False alarm? (yes / no):\n", "False alarm? (yes / no): yes\n")
    sheet.write_text(text, encoding="utf-8")
    summary = score_step(step, key, store.dir, import_sheet=True)
    assert summary["final"] is True
    assert {r["blind_id"]: r["score"] for r in summary["runs"]} == {"CC-AAA": 10, "CC-BBB": 2}


# ---------- the score command ----------

def test_score_command_end_to_end(key, steps, tmp_path, monkeypatch, capsys):
    from eos_bakeoff import cli
    step = steps["chronology_check"]
    store = _store_with(tmp_path, step, {"CC-AAA": ("ok", out("verdict_perfect.md")),
                                         "CC-BBB": ("ok", out("verdict_bad.md"))})
    monkeypatch.setattr(cli, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(cli, "load_answer_key", lambda: key)

    assert cli.main(["score", "--step", "chronology_check"]) == 0
    shown = capsys.readouterr().out
    assert "provisional" in shown and "2 report(s) need your decision" in shown
    assert cli.main(["score", "--step", "chronology_check", "--import"]) == 2   # blanks refused loudly
    assert "still blank" in capsys.readouterr().out
    for planted in cc_key(key)["planted"]:
        assert planted["fact"] not in shown              # key content never printed

    sheet = store.dir / "chronology_check_false_alarms.md"
    sheet.write_text(sheet.read_text(encoding="utf-8").replace(
        "False alarm? (yes / no):\n", "False alarm? (yes / no): no\n"), encoding="utf-8")
    assert cli.main(["score", "--step", "chronology_check", "--import"]) == 0
    assert "decisions applied" in capsys.readouterr().out


def test_score_command_human_step(monkeypatch, capsys):
    from eos_bakeoff import cli
    assert cli.main(["score", "--step", "first_draft"]) == 0
    assert "human review" in capsys.readouterr().out
