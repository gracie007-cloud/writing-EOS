"""Phase 1 tests: section splitting, prompt building, guards, run records. No network."""

import json
import re
from dataclasses import replace
from datetime import date

import pytest

from eos_bakeoff.clients import CallResult, build_body
from eos_bakeoff.config import ROOT, TEST_PACK, ConfigError, Model, load_all, validate_step
from eos_bakeoff.prompts import (AnswerKeyError, PromptError, build_prompt, check_mature, guard_path,
                                 read_test_pack, split_sections)
from eos_bakeoff.runner import RunStore, classify, new_blind_id, run_step


@pytest.fixture(scope="module")
def setup():
    models, steps = load_all()
    sections = split_sections(read_test_pack(TEST_PACK))
    return models, steps, sections


def test_real_config_loads(setup):
    models, steps, _ = setup
    assert {"first_draft", "chronology_check", "first_draft_mature"} <= set(steps)
    assert all(not m.verified for m in models.values() if m.id and m.id.startswith("VERIFY"))


def test_sections_split(setup):
    _, _, sections = setup
    assert set(sections) == {"A", "B", "C", "D", "E"}
    assert "R.S. Rhys" in sections["A"]
    assert "C/1147" in sections["C"]
    assert "End of test pack" not in sections["E"]
    assert "How the Harness Uses This File" not in "".join(sections.values())
    assert not sections["C"].rstrip().endswith("---")


def test_prompt_uses_only_allowed_sections(setup):
    _, steps, sections = setup
    prompt = build_prompt(steps["first_draft"], sections)
    assert sections["C"] in prompt and sections["B"] in prompt
    assert sections["D"] not in prompt and sections["E"] not in prompt
    assert "{{" not in prompt


def test_selector_placeholders_filled(setup):
    _, steps, sections = setup
    prompt = build_prompt(steps["worldbuilding_selector"], sections)
    assert "locations and rules selector" in prompt
    assert '"world_rules"' in prompt and "{{" not in prompt


def test_chronology_gets_e_not_c(setup):
    _, steps, sections = setup
    prompt = build_prompt(steps["chronology_check"], sections)
    assert sections["E"] in prompt and sections["C"] not in prompt


def test_answer_key_guard():
    with pytest.raises(AnswerKeyError):
        guard_path(ROOT / "data" / "Run01_TestPack_ANSWER_KEY.md")


def test_e_with_c_refused(setup):
    models, steps, sections = setup
    bad = replace(steps["chronology_check"], sections=("A", "B", "C", "E"))
    with pytest.raises(ConfigError):
        validate_step(bad, models)
    with pytest.raises(PromptError):
        build_prompt(bad, sections)


def test_template_cannot_pull_unlisted_section(setup):
    _, steps, sections = setup
    narrowed = replace(steps["first_draft"], sections=("A", "B"))
    with pytest.raises(PromptError):
        build_prompt(narrowed, sections)


def test_mature_guard(setup):
    models, steps, _ = setup
    with pytest.raises(PromptError):
        check_mature(steps["first_draft_mature"], models["gemini4"])
    check_mature(steps["first_draft_mature"], models["custom_abliterated"])
    bad = replace(steps["first_draft_mature"], candidates=("gemini4",))
    with pytest.raises(ConfigError):
        validate_step(bad, models)


def test_unverified_model():
    assert not Model("m", "openrouter", "f", "open", False, id="VERIFY: x/y").verified
    assert Model("m", "openrouter", "f", "open", False, id="x/y").verified


def test_blind_ids_unique_and_shaped():
    taken: set[str] = set()
    ids = {new_blind_id("first_draft", taken) for _ in range(200)}
    assert len(ids) == 200
    assert all(re.fullmatch(r"FD-[A-Z2-9]{3}", i) for i in ids)


@pytest.mark.parametrize("result,expected", [
    (CallResult("Chapter text " * 100, 10, 10, 0.1, "openrouter", "stop", 1.0, 1), "ok"),
    (CallResult("Chapter text", 10, 10, 0.1, "openrouter", "length", 1.0, 1), "truncated"),
    (CallResult("I'm sorry, but I can't write this.", 10, 10, 0.0, "openrouter", "stop", 1.0, 1), "refused"),
    (CallResult("", 10, 0, 0.0, "openrouter", "stop", 1.0, 1), "refused"),
    (CallResult(None, None, None, None, None, None, 0.0, 3, error="HTTP 500"), "error"),
])
def test_classify(result, expected):
    assert classify(result) == expected


def test_request_body_budgets():
    body = build_body("x/y", "hi", 0.85, 6000, 4000)
    assert body["max_tokens"] == 10000
    assert body["reasoning"] == {"max_tokens": 4000, "exclude": False}
    assert "reasoning" not in build_body("x/y", "hi", 0.2, 800, 0)


def test_steps_carry_thinking_budget(setup):
    _, steps, _ = setup
    step = steps["first_draft"]
    assert step.reasoning_max_tokens == 4000
    assert step.request_max_tokens == step.max_tokens + 4000


class FakeClient:
    def __init__(self):
        self.calls = 0
        self.budgets = []

    def chat(self, model_id, prompt, temperature, max_tokens, reasoning_max_tokens=0):
        self.calls += 1
        self.budgets.append((max_tokens, reasoning_max_tokens))
        if self.calls == 2:
            return CallResult(None, None, None, None, None, None, 0.5, 3, error="HTTP 503: busy")
        if self.calls == 3:
            return CallResult("Intake\n\nThe trolley", 1200, 10000, 0.05, "openrouter", "length", 9.0, 1,
                              reasoning="Planning scene one…", reasoning_tokens=9990)
        return CallResult("Intake\n\nThe trolley came down at 05:40.  \r\n", 1200, 900, 0.0123,
                          "openrouter", "stop", 2.5, 1, generation_id="gen-1",
                          reasoning="Plan: four scenes.", reasoning_tokens=300)


def test_run_step_records_everything(setup, tmp_path):
    models, steps, sections = setup
    step = steps["first_draft"]
    model = replace(models["gemini4"], id="google/test-model")
    store = RunStore(day=date(2026, 10, 17), root=tmp_path / "runs")
    prompt = build_prompt(step, sections)

    client = FakeClient()
    records = run_step(step, [model], prompt, 3, client, store, concurrency=1)

    assert len(records) == 3
    assert client.budgets == [(step.max_tokens, step.reasoning_max_tokens)] * 3
    assert sorted(r.status for r in records) == ["error", "ok", "truncated"]
    truncated = next(r for r in records if r.status == "truncated")
    assert truncated.output_path   # partial text kept
    assert (tmp_path / truncated.reasoning_path).read_text(encoding="utf-8") == "Planning scene one…"
    assert truncated.reasoning_tokens == 9990
    lines = store.records_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    required = {"run_id", "timestamp", "step", "model_key", "run_number", "blind_id", "input_hash",
                "output_path", "input_tokens", "output_tokens", "cost_usd", "latency_s", "status",
                "error_message"}
    for line in lines:
        assert required <= set(json.loads(line))
    ok = next(r for r in records if r.status == "ok")
    saved = (tmp_path / ok.output_path).read_bytes().decode("utf-8")
    assert saved == "Intake\n\nThe trolley came down at 05:40.  \r\n"   # verbatim
    mapping = json.loads(store.blind_map_path.read_text(encoding="utf-8"))
    assert {r.blind_id for r in records} == set(mapping)
    assert all(v["model_key"] == "gemini4" for v in mapping.values())


def test_estimate_survives_a_non_utf8_console():
    # A Windows console using cp1252 cannot show "≈"; the command must still finish.
    import os
    import subprocess
    import sys
    env = dict(os.environ, PYTHONIOENCODING="cp1252", PYTHONUTF8="0")
    r = subprocess.run([sys.executable, "-m", "eos_bakeoff", "estimate", "--step", "first_draft"],
                       cwd=ROOT, env=env, capture_output=True)
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")[-400:]
    assert b"Estimate" in r.stdout
