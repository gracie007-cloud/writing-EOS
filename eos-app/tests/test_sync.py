"""Following the Notion database (D18, fixes plan A2): components.yaml is built from a database export joined with
the app's own inputs table, by a command in this repository."""
import copy

import pytest
import yaml

from eos_app import sync
from eos_app.workflow import COMPONENTS_PATH, load_components


@pytest.fixture(scope="module")
def current():
    return yaml.safe_load(COMPONENTS_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def inputs():
    return sync.load_inputs()


@pytest.fixture()
def rows(current):
    return sync.export_rows(current)


def row(rows, step):
    return next(r for r in rows if r["Step"] == step)


def test_the_shipped_file_is_exactly_what_the_tool_builds(current, inputs, rows, tmp_path):
    rebuilt = sync.build(rows, inputs, version=current["version"])
    assert rebuilt == current
    assert sync.dump(rebuilt) == COMPONENTS_PATH.read_text(encoding="utf-8")        # byte for byte
    out = tmp_path / "export.csv"
    sync.write_export(current, out)                                                 # and through a real CSV file
    assert sync.build(sync.read_export(out), inputs, version=current["version"]) == current


def test_the_export_uses_the_databases_own_columns_and_words(rows):
    assert list(rows[0]) == sync.COLUMNS
    assert row(rows, "33") == {
        "Step": "33", "Component": "Chronology Check 2", "App Name": "Continuity Check", "Flow Order": "87",
        "Phase": "K · Chapters", "Runs": "Per chapter", "Task Type": "Verdict / Check", "Swarm Tier": "Full",
        "Jev Model": "jev-1.14.0", "Author Gate After": "", "Category": "Prose Writing",
        "Frontier Model": "Gemini 4 Argon",
        "Comparable Open-Weight": "None genuinely comparable — least-gap: MiMo-V2.6-Pro (not parity)",
        "Fallback Model": "", "Mature Fallback": "Venice Uncensored"}
    assert row(rows, "PROP-02")["Frontier Model"] == "Deterministic tooling — no LLM"


def test_every_component_has_an_inputs_entry_and_nothing_else_does(current, inputs):
    assert set(inputs) == {c["step"] for c in current["components"]}
    assert inputs["NEW-22"]["modality"] == "Image" and inputs["22.6"]["gate_when_run"] is True
    assert inputs["33"]["judges"] == ["32", "35", "37", "38"]


def test_a_change_in_the_database_is_listed_in_plain_words(current, inputs, rows):
    row(rows, "5")["Frontier Model"] = "Claude Fable 5.1"
    row(rows, "5")["Swarm Tier"] = "Light"
    new = sync.build(rows, inputs, version=current["version"])
    assert sync.differences(current, new) == [
        "Story Pitch (5): candidates {'primary': 'GPT-6.1 Sol', 'comparable': 'MiMo-V2.6-Pro (least-gap — not parity)'} "
        "→ {'primary': 'Claude Fable 5.1', 'comparable': 'MiMo-V2.6-Pro (least-gap — not parity)'}",
        "Story Pitch (5): swarm 'full' → 'light'"]


def test_an_open_weight_primary_is_read_from_the_databases_note(current, inputs, rows):
    aud = row(rows, "NEW-13")
    aud["Frontier Model"], aud["Comparable Open-Weight"] = "None — open-weight primary (Author, 2026-10-22)", "GLM 5.3 Flash"
    assert sync.build(rows, inputs, version=current["version"]) == current          # the same component either way


def test_a_new_database_row_needs_its_inputs_decided_first(inputs, rows):
    rows.append({**rows[-1], "Step": "NEW-99", "App Name": "Something New", "Flow Order": "123"})
    with pytest.raises(sync.SyncError, match="no entry in component_inputs.yaml for: NEW-99"):
        sync.build(rows, inputs)


def test_an_unknown_database_value_is_refused_not_guessed(inputs, rows):
    row(rows, "5")["Task Type"] = "Vibes"
    with pytest.raises(sync.SyncError, match="5: the app has no meaning for the database value 'Vibes'"):
        sync.build(rows, inputs)


def test_a_file_that_is_not_the_export_is_refused(tmp_path):
    f = tmp_path / "roster.csv"
    f.write_text("Model Name,Provider\nKimi K3,Concentrate AI\n", encoding="utf-8")
    with pytest.raises(sync.SyncError, match="not a Narrative Components export"):
        sync.read_export(f)


def test_a_reordered_database_that_breaks_an_input_is_caught(current, inputs, rows):
    brief, picks = row(rows, "22.5"), row(rows, "23")                               # Chapter Brief feeds Plot Picks
    brief["Flow Order"], picks["Flow Order"] = picks["Flow Order"], brief["Flow Order"]
    from eos_app.workflow import check_order, validate
    problems = check_order(validate(sync.build(rows, inputs)))
    assert problems == ["Plot Picks runs before Chapter Brief, which it needs."]
    assert check_order(load_components()) == []
    assert copy.deepcopy(current) == current
