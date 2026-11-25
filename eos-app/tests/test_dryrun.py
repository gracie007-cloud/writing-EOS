"""The dry run of the first slice (fixes plan D1): seven prompts from allowed inputs only, the models the router
picks, a stop at all three gates, verified endpoints, and nothing sent."""
import json
import socket

import pytest

from eos_app import dryrun as dr
from eos_app.clients import build_request, load_endpoints
from eos_app.library import import_folder, load_map, source_path
from eos_app.prompts import (AnswerKeyError, PromptError, build_prompt, check_agent, load_agents)
from eos_app.workflow import load_components

from test_library import VAULT

STAND_INS = {"genre_path": {"primary_genre": "Literary Fiction", "secondary_genre": "Contemporary Literary Fiction",
                            "major_subgenre": "Mystery", "minor_subgenre": "Harbour Mystery"},
             "pen_name": "Sample Pen", "manuscript_type": "Novel"}
AUTHOR = {"braindump": "A lighthouse log goes missing the night a boat is lost.",
          "brainstorm": "Belonging; quiet and tense; an ending like a door left open.", "manuscript_type": "Novel"}
FAKE_KEY = "sk-or-v1-" + "x" * 40


@pytest.fixture(scope="module")
def M():
    return load_map()


@pytest.fixture(scope="module")
def lib(tmp_path_factory, M):
    root = tmp_path_factory.mktemp("lib") / "library"
    for pool, cfg in M.pools.items():
        import_folder(source_path(VAULT, cfg), pool, root, M)
    return root


@pytest.fixture(scope="module")
def run(tmp_path_factory, lib):
    project = tmp_path_factory.mktemp("project")
    mp = pytest.MonkeyPatch()
    mp.setenv("OPENROUTER_API_KEY", FAKE_KEY)
    mp.setenv("CONCENTRATE_API_KEY", FAKE_KEY)

    def no_network(*a, **k):
        raise AssertionError("the dry run opened a network connection")
    mp.setattr(socket.socket, "connect", no_network)
    try:
        summary = dr.dry_run(project, library_root=lib, author=AUTHOR, assumed=STAND_INS)
    finally:
        mp.undo()
    return project, summary


def test_the_slice_is_story_pitch_and_everything_it_needs_in_flow_order():
    w = load_components()
    assert [c.step for c in dr.slice_for(w, "5")] == ["1", "2", "4.1", "3", "NEW-13", "3.5", "5"]


def test_every_agent_asks_only_for_what_its_component_may_have(M):
    w, agents = load_components(), load_agents()
    assert set(agents) == {"1", "2", "4.1", "3", "NEW-13", "3.5", "5"}
    assert [p for a in agents.values() for p in check_agent(a, w, M)] == []


def test_an_input_the_component_may_not_have_is_refused(M):
    w, a = load_components(), load_agents()["1"]
    from dataclasses import replace
    from eos_app.prompts import Input
    bad = replace(a, inputs=a.inputs + (Input("library.characters", "Character Pool"), Input("step.3", "Pen name")))
    problems = check_agent(bad, w, M)
    assert any("characters" in p for p in problems) and any("step 3" in p for p in problems)


def test_seven_prompts_three_gate_stops_and_nothing_sent(run):
    project, s = run
    assert (s["prompts"], s["calls"], s["gate_stops"]) == (7, 11, 3)
    events = json.loads((project / "dry-run.json").read_text(encoding="utf-8"))
    assert events["prompts"] == 7
    page = (project / "dry-run.html").read_text(encoding="utf-8")
    order = [h for h in __import__("re").findall(r"<h2>([^<]+)</h2>", page)]
    assert order == ["Idea Intake", "Story Setup", "Stop · Author confirms manuscript type", "Genre Pack Builder",
                     "Pen Name and Style", "Stop · Author picks the pen name", "Target Audience", "Premise Adapter",
                     "Stop · Author approves the adapted premise", "Story Pitch"]
    records = [json.loads(x) for f in (project / "runs").glob("*/runs.jsonl") for x in f.read_text().splitlines()]
    assert len(records) == 11 and {r["status"] for r in records} == {"not sent"}
    assert len(list((project / "prompts" / "dry-run").glob("*.md"))) == 7


def test_the_models_come_from_the_router_on_concentrate_with_verified_endpoints(run):
    _, s = run
    calls = {step: c for step, _, c in s["steps"]}
    assert calls["1"] == [("writer", "Claude Fable 5.1", "concentrate"), ("cross-check", "Kimi K3", "concentrate")]
    # Target Audience: GLM 5.3 Flash's catalog Fallback, MiMo V2.6 Flash, gives the Full tier its cross-check
    assert calls["NEW-13"] == [("writer", "GLM 5.3 Flash", "concentrate"), ("cross-check", "MiMo V2.6 Flash", "concentrate")]
    ep = load_endpoints()
    assert ep["concentrate"].url == "https://api.concentrate.ai/v1/chat/completions"
    assert ep["featherless"].url == "https://api.featherless.ai/v1/chat/completions"
    assert ep["openrouter"].url == "https://openrouter.ai/api/v1/chat/completions"


def test_the_cost_is_estimated_and_nothing_is_left_open(run):
    _, s = run
    assert s["cost_usd_max"] is not None and 0 < s["cost_usd_max"] < 1
    assert s["open_items"] == []


def test_no_key_ever_reaches_a_prompt_a_request_or_a_record(run):
    project, _ = run
    for f in project.rglob("*"):
        if f.is_file():
            assert FAKE_KEY not in f.read_text(encoding="utf-8")
    req = build_request(load_endpoints()["concentrate"], "concentrate", "gpt-6.1-sol", "hi", 0.2, 10)
    assert req["headers"]["Authorization"] == "Bearer ${CONCENTRATE_API_KEY}"


def test_the_library_slice_is_chosen_for_the_book_and_stand_ins_are_marked(run):
    project, s = run
    pen = (project / "prompts" / "dry-run" / "06-premise_adapter.md").read_text(encoding="utf-8")
    assert "Sample Pen" in pen and "Second Pen" not in pen          # only the pen name taken at the gate
    assert s["stand_ins"]["pen_name"] == "Sample Pen"
    assert "(stand-in for the dry run)" in (project / "dry-run.html").read_text(encoding="utf-8")


def test_an_answer_key_path_is_refused(lib, tmp_path):
    with pytest.raises(AnswerKeyError):
        dr.dry_run(tmp_path, library_root=lib, author=AUTHOR, author_paths=[tmp_path / "Run01_ANSWER_KEY.yaml"],
                   assumed=STAND_INS)


def test_a_key_in_the_material_stops_the_prompt(lib, M):
    a = load_agents()["1"]
    with pytest.raises(PromptError, match="provider key"):
        build_prompt(a, author={"braindump": "notes " + FAKE_KEY}, outputs={}, decisions={}, pools={}, lmap=M)


def test_over_budget_an_optional_block_is_left_out_and_recorded(lib, M):
    from dataclasses import replace
    from eos_app.library import load_pool
    a = replace(load_agents()["1"], context_budget_tokens=600)
    pools = {"story_pitches": load_pool("story_pitches", lib, M)}
    built = build_prompt(a, author={"braindump": "x " * 400, "brainstorm": "y " * 200}, outputs={}, decisions={},
                         pools=pools, lmap=M)
    assert built.tokens <= 600 and [x[0] for x in built.left_out][0].startswith("Story Pitch Pool")
    with pytest.raises(PromptError, match="required parts alone"):
        build_prompt(replace(a, context_budget_tokens=50), author={"braindump": "x " * 400}, outputs={},
                     decisions={}, pools=pools, lmap=M)
