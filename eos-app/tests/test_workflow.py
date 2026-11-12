"""Order of work (requirements v0.10, FR-FLOW, D17, D18): the app follows the Notion database Narrative Components."""

import copy

import pytest
import yaml

from eos_app.blueprint import load_tables
from eos_app.workflow import (COMPONENTS_PATH, OrderError, chapter_loop, check_order, display_name, gates,
                              jev_role, load_components, next_to_run, run_plan, validate)


@pytest.fixture(scope="module")
def W():
    return load_components()


@pytest.fixture(scope="module")
def T():
    return load_tables()


def raw():
    return yaml.safe_load(COMPONENTS_PATH.read_text(encoding="utf-8"))


# ---------- the registry ----------

def test_all_123_components_load(W):
    assert len(W.components) == 123
    assert len({c.step for c in W.components}) == 123
    assert len({c.name for c in W.components}) == 123


def test_flow_order_is_1_to_122_and_word_count_has_none(W):
    orders = sorted(c.flow_order for c in W.components if c.flow_order is not None)
    assert orders == list(range(1, 123))
    assert W.by_step["PROP-02"].flow_order is None


def test_shipped_order_has_no_missing_inputs(W):
    assert check_order(W) == []


def test_phases_run_in_order(W):
    seq = [c.phase for c in W.ordered() if c.phase != "All"]
    letters = "ABCDEFGHIJKLMN"
    assert [letters.index(p) for p in seq] == sorted(letters.index(p) for p in seq)


def test_naming_rules_come_before_any_character_is_named(W):
    assert W.by_step["10.1"].flow_order < W.by_step["6.61"].flow_order < W.by_step["16"].flow_order


# ---------- names (D18) ----------

def test_writer_view_shows_the_plain_name_and_engine_view_the_database_row(W):
    c = W.by_step["33"]
    assert display_name(c, "writer") == "Continuity Check"
    assert display_name(c, "engine") == "33 · Chronology Check 2"


@pytest.mark.parametrize("step, name", [("19", "Story Bible Builder"), ("7", "Character Seeds"),
                                        ("27.5", "Character State"), ("13", "Character Arc"),
                                        ("36", "Character Changes Log"), ("37", "Polish")])
def test_plain_names(W, step, name):
    assert W.by_step[step].name == name


def test_plain_names_carry_no_codes(W):
    for c in W.components:
        assert "(" not in c.name and not any(ch.isdigit() for ch in c.name), c.name
        for code in ("GANT", "X1", "X2", "Triad", "CD-", "NEW-", "PROP-"):
            assert code not in c.name, c.name


# ---------- validation refuses broken orders (FR-FLOW-6) ----------

def test_an_order_that_runs_a_step_before_its_input_is_refused(W):
    bad = copy.deepcopy(W)
    a, b = bad.by_step["22.5"], bad.by_step["23"]           # Chapter Brief must come before Plot Picks
    a.flow_order, b.flow_order = b.flow_order, a.flow_order
    problems = check_order(bad)
    assert problems and "Plot Picks" in problems[0] and "Chapter Brief" in problems[0]


@pytest.mark.parametrize("mutate, message", [
    (lambda d: d["components"][1].update(name=d["components"][0]["name"]), "name"),
    (lambda d: d["components"][0].update(phase="Z"), "phase"),
    (lambda d: d["components"][0].update(runs="sometimes"), "runs"),
    (lambda d: d["components"][5].update(needs=["99.9"]), "99.9"),
    (lambda d: d["components"][7].update(flow_order=200), "Flow Order"),
])
def test_validation(mutate, message):
    d = raw()
    mutate(d)
    with pytest.raises(OrderError, match=message):
        validate(d)


# ---------- what runs next ----------

def test_first_steps(W):
    names = [c.name for c in next_to_run(W, done=set())]
    assert names[0] == "Idea Intake"
    assert "Story Pitch" not in names                       # needs the adapted premise first


def test_next_steps_follow_inputs(W):
    done = {"1", "2", "4.1", "3", "4", "NEW-02", "3.5"}
    names = [c.name for c in next_to_run(W, done=done)]
    assert names[:2] == ["Fact Base", "Target Audience"]
    assert "Story Pitch" not in names                       # reads the Reader Contract
    assert "Conflict Scoring" not in names                  # needs the pitch
    names = [c.name for c in next_to_run(W, done=done | {"NEW-13"})]
    assert "Story Pitch" in names


def test_audience_pitch_and_tropes_are_separate_components_on_their_own_models(W):
    aud, pitch, tropes = W.by_step["NEW-13"], W.by_step["5"], W.by_step["NEW-14"]
    assert "NEW-13" in pitch.needs and aud.flow_order < pitch.flow_order

    assert {"5", "NEW-13", "19"} <= set(tropes.needs)       # after the Story Bible lock: characters and world complete
    assert aud.candidates == {"frontier": None, "open_weight": "GLM 5.3 Flash", "primary": "open_weight"}
    assert tropes.candidates["frontier"] == "Claude Fable 5.1" and pitch.candidates["frontier"] == "GPT-6.1 Sol"


def test_the_reader_contract_comes_right_after_the_pen_name_and_feeds_the_intake(W):
    aud = W.by_step["NEW-13"]
    assert aud.flow_order == W.by_step["3"].flow_order + 1 and aud.phase == "A"
    for reader in ("4", "NEW-02", "3.5", "5"):                 # Writing Guide, POV and Reader, Premise Adapter, Story Pitch
        assert "NEW-13" in W.by_step[reader].needs and W.by_step[reader].flow_order > aud.flow_order


def test_on_demand_and_cross_cutting_are_not_queued(W):
    names = {c.name for c in next_to_run(W, done=set())}
    assert "Brainstorm" not in names and "Story Advisor" not in names


def test_chapter_loop_matches_the_chapter_pipeline(W):
    assert [c.name for c in chapter_loop(W)] == [
        "Chapter Brief", "Plot Picks", "Cast Picks", "World Picks", "Scene Plan", "Setting Notes",
        "Character State", "Character Notes", "Timeline Check", "Scene Plan Fix", "First Draft",
        "Continuity Check", "Voice and Style Check", "Rewrite", "Polish", "Character Changes Log", "Chapter Summary"]


def test_canon_updates_come_after_the_chapter_lock(W):
    lock = next(g for g in gates(W) if g[1] == "Chapter lock (Author)")
    assert W.by_step["37"].flow_order < lock[0].flow_order < W.by_step["36"].flow_order


def test_story_bible_lock_is_after_the_second_opinion(W):
    g = next(g for g in gates(W) if "Story Bible lock" in g[1])
    assert g[0].name == "Canon Second Opinion"


# ---------- how each component runs: Swarm Tier and Jev (D18) ----------

def test_run_plan(W):
    assert run_plan(W.by_step["33"]) == {"models": 2, "cross_check": True, "jev": "settles"}       # a check
    assert run_plan(W.by_step["32"]) == {"models": 1, "cross_check": False, "jev": "advises"}      # the draft
    assert run_plan(W.by_step["PROP-02"]) == {"models": 0, "cross_check": False, "jev": "none"}    # code


def test_jev_settles_only_what_agents_may_settle(W, T):
    check = W.by_step["30"]                                  # Timeline Check: jev settles
    assert jev_role(check, "return_to_braindump", T) == "settles"
    assert jev_role(check, "core_pick", T) == "recommends"   # always the Author's
    assert jev_role(W.by_step["32"], "file_runner_up", T) == "recommends"   # an advising component
    assert jev_role(W.by_step["PROP-02"], "file_runner_up", T) is None


def test_every_model_component_has_candidates_and_code_has_none(W):
    for c in W.components:
        if c.task_type == "code":
            assert c.candidates is None and c.swarm == "none"
        else:
            assert c.candidates and (c.candidates["frontier"] or c.candidates.get("primary") == "open_weight" and c.candidates["open_weight"])
