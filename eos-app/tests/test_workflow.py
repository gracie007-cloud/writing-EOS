"""Order of work (requirements v0.10, FR-FLOW, D17, D18): the app follows the Notion database Narrative Components."""

import copy

import pytest
import yaml

from eos_app.blueprint import load_tables
from eos_app.workflow import (COMPONENTS_PATH, OrderError, chapter_loop, check_order, display_name, gates,
                              is_chapter_gate, jev_role, load_components, next_to_run, run_plan, validate,
                              waiting_on)


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
    (lambda d: d["components"][1]["candidates"].update(frontier="GPT-6.1 Sol"), "primary, comparable and fallback"),
    (lambda d: d["components"][1].update(modality="Image"), "media component"),
    (lambda d: next(c for c in d["components"] if c["step"] == "NEW-22").pop("modality"), "media component"),
    (lambda d: d["components"][1].update(gate_when_run=True), "no gate"),
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
    done, ok = {"1", "2", "4.1", "3", "4", "NEW-02", "3.5"}, {"2", "3", "3.5"}      # three gates approved
    names = [c.name for c in next_to_run(W, done=done, approved=ok)]
    assert names[:2] == ["Fact Base", "Target Audience"]
    assert "Story Pitch" not in names                       # reads the Reader Contract
    assert "Conflict Scoring" not in names                  # needs the pitch
    names = [c.name for c in next_to_run(W, done=done | {"NEW-13"}, approved=ok)]
    assert "Story Pitch" in names


def test_audience_pitch_and_tropes_are_separate_components_on_their_own_models(W):
    aud, pitch, tropes = W.by_step["NEW-13"], W.by_step["5"], W.by_step["NEW-14"]
    assert "NEW-13" in pitch.needs and aud.flow_order < pitch.flow_order

    assert {"5", "NEW-13", "19"} <= set(tropes.needs)       # after the Story Bible lock: characters and world complete
    assert aud.candidates == {"primary": "GLM 5.3 Flash", "comparable": None}       # the Author chose the open model
    assert tropes.candidates["primary"] == "Claude Fable 5.1" and pitch.candidates["primary"] == "GPT-6.1 Sol"


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
            assert c.candidates and c.candidates["primary"] and set(c.candidates) <= {"primary", "comparable", "fallback"}


# ---------- Author gates stop the queue (FR-FLOW-3) ----------

def test_nothing_past_a_gate_is_offered_until_the_author_approves_it(W):
    done = {"1", "NEW-03", "2"}                                # Story Setup is finished; its gate is not approved
    assert next_to_run(W, done) == []
    held = waiting_on(W, W.by_step["4.1"], done)
    assert [(g.name, g.gate_after) for g, _ in held] == [("Story Setup", "Author confirms manuscript type")]
    assert [c.name for c in next_to_run(W, done, approved={"2"})] == ["Genre Pack Builder"]


def test_a_gate_does_not_hold_back_its_own_component_or_anything_before_it(W):
    assert [c.name for c in next_to_run(W, done=set())] == ["Idea Intake", "Fact Base"]
    assert waiting_on(W, W.by_step["2"], done={"1"}) == []


def test_the_recipe_gate_applies_only_when_a_recipe_was_built(W):
    recipe, brief = W.by_step["22.6"], W.by_step["22.5"]
    assert recipe.gate_when_run and recipe.runs == "on_demand"
    book = {g.step for g, _ in gates(W) if not is_chapter_gate(W, g)} - {"22.6"}
    assert not any(g.step == "22.6" for g, _ in waiting_on(W, brief, done=set(), approved=book, chapter=1))
    assert [g.name for g, _ in waiting_on(W, brief, done={"22.6"}, approved=book, chapter=1)] == ["Recipe Builder"]


def test_the_whole_book_stops_at_every_gate(W):
    """Run the book with two chapters, approving a gate only when the queue has stopped at it."""
    done, approved, stops, chapters = set(), set(), [], (1, 2)
    book_gates = [g for g, _ in gates(W) if not is_chapter_gate(W, g) and not g.gate_when_run]
    lock = next(g for g, _ in gates(W) if is_chapter_gate(W, g))
    per_chapter = [c for c in chapter_loop(W) if c.runs == "per_chapter"]

    def run_book():
        while True:
            nxt = next_to_run(W, done, approved)
            if nxt:
                done.add(nxt[0].step)
                continue
            waiting = [g for g in book_gates if g.step in done and g.step not in approved]
            if not waiting:
                return
            approved.add(waiting[0].step)                   # the queue was empty: this is a real stop
            stops.append(waiting[0].gate_after)

    run_book()                                              # everything up to the chapters
    assert "21.2" in approved and "NEW-12" not in done      # the outline is approved; finishing has not started
    for ch in chapters:
        while nxt := next_to_run(W, done, approved, chapter=ch):
            done.add((nxt[0].step, ch))
        assert ("36", ch) not in done                       # the canon update waits for this chapter's lock (FR-FLOW-4)
        approved.add((lock.step, ch))
        stops.append(f"{lock.gate_after} · chapter {ch}")
        while nxt := next_to_run(W, done, approved, chapter=ch):
            done.add((nxt[0].step, ch))
        assert all((c.step, ch) in done for c in per_chapter)
    done.update(c.step for c in per_chapter)                # every chapter has finished each per-chapter step
    approved.add(lock.step)                                 # every chapter is locked
    run_book()
    assert all(c.step in done for c in W.ordered() if c.runs == "sequence")
    assert len(stops) == len(book_gates) + len(chapters) == 20
    assert stops[:3] == ["Author confirms manuscript type", "Author picks the pen name", "Author approves the adapted premise"]


def test_planning_runs_ahead_but_drafting_waits_for_the_previous_chapters_lock(W):
    book = {g.step for g, _ in gates(W) if not is_chapter_gate(W, g)}
    done = {c.step for c in W.ordered() if c.runs == "sequence" and c.phase < "K"}
    for _ in range(40):                                     # run chapter 2 as far as it will go
        nxt = next_to_run(W, done, approved=book, chapter=2)
        if not nxt:
            break
        done.add((nxt[0].step, 2))
    assert ("22.5", 2) in done and ("28", 2) in done        # Chapter Brief and Character Notes: planned ahead
    assert ("32", 2) not in done                            # First Draft waits (FR-GEN-5)
    held = waiting_on(W, W.by_step["32"], done, approved=book, chapter=2)
    assert [(g.gate_after, ch) for g, ch in held] == [("Chapter lock (Author)", 1)]
    assert "First Draft" in [c.name for c in next_to_run(W, done, approved=book | {("38", 1)}, chapter=2)]
