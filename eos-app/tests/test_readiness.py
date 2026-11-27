"""Readiness report (fixes plan B1, B2, B3, B7, B8, B11): which components could run today, and why the rest could
not. Nothing here calls a model."""
from dataclasses import replace

import pytest

from eos_app.readiness import component_readiness, render, report, stopped_by_outage
from eos_app.registry import Registry, load_models
from eos_app.router import load_routing
from eos_app.workflow import chapter_loop, load_components


@pytest.fixture(scope="module")
def W():
    return load_components()


@pytest.fixture(scope="module")
def R():
    return load_models()


@pytest.fixture(scope="module")
def RT():
    return load_routing()


@pytest.fixture(scope="module")
def rep(W, R, RT):
    return report(W, R, RT)


def names(rep, state):
    return [r.name for r in rep["components"] if r.state == state]


def test_every_component_has_a_state(rep):
    assert rep["counts"] == {"ready": 117, "code": 6}


def test_media_components_run_now_their_models_have_ids(rep):
    # the media models carry Comfy Cloud and OpenRouter IDs from the proprietary catalog (2026-11-25)
    assert names(rep, "blocked") == []


def test_target_audience_has_its_cross_check_from_the_catalog_pairing(rep):
    # GLM 5.3 Flash's Fallback in the catalogs (MiMo V2.6 Flash) is its second expert: decision 5 closed
    assert names(rep, "degraded") == []


def test_a_component_running_on_a_later_expert_is_degraded(W, R, RT):
    no_id = [replace(m, model_id="") if m.name == "Claude Fable 5.1" else m for m in R.models]
    reg = Registry(R.version, no_id, {m.key: m for m in no_id}, [])
    r = component_readiness(W.by_step["NEW-14"], W, reg, RT)
    assert r.state == "degraded"
    assert r.reasons == ("Claude Fable 5.1 has no provider model ID yet, so it would run on Kimi K3",
                         "the Full tier cross-checks with a second expert, and it has one")


def test_a_ready_component_still_says_what_it_lacks(rep):
    cover = next(r for r in rep["components"] if r.name == "Cover Art")
    assert cover.state == "ready"
    assert cover.notes == ()
    interview = next(r for r in rep["components"] if r.name == "Character Interview")
    assert "nothing checks its work" in interview.notes


def test_one_provider_going_down_is_counted_component_by_component(W, R, RT, rep):
    stopped = rep["outage"]["Concentrate AI"]
    per_chapter = {c.step for c in chapter_loop(W)}
    assert len(stopped) == 105 and sum(c.step in per_chapter for c in stopped) == 17
    assert [len(rep["outage"][p]) for p in ("OpenRouter", "Featherless AI", "Comfy Cloud")] == [0, 0, 5]
    # media is called on Comfy Cloud first (the Author, 2026-11-25), so these have no expert elsewhere; Sound Effects
    # falls back to ElevenLabs SFX v3 (the Author, 2026-11-27)
    assert [c.name for c in rep["outage"]["Comfy Cloud"]] == ["Visual References", "Map Maker", "Interior Art",
                                                              "Marketing Visuals", "Trailer Video"]
    # a second route for the two workhorse models keeps their components running
    twins = [replace(m, key=f"openrouter-{m.model_id}", provider="OpenRouter")
             for m in R.models if m.name in ("Claude Fable 5.1", "Kimi K3")]
    reg = Registry(R.version, R.models + twins, {m.key: m for m in R.models + twins}, [])
    assert len(stopped_by_outage(W, reg, RT, "Concentrate AI")) < 105 - 40


def test_open_items_are_named(rep, W):
    text = render(rep, W)
    assert not rep["jev_in_roster"] and "Jev (typesafe/jev-1.14) has no row in the roster" in text
    assert "Mature Fallback still open (2): Visual Consistency Check, Narration Check" in text
    assert "Writers nothing checks (4): Character Interview, Proofread, Music, Sound Effects" in text
    # D33: text hands mature passages to the tier; the media components now have open models for them
    assert "No route for mature material" not in text
    assert ("Mature tier: 62 models, 64 routes (Featherless AI 62, OpenRouter 2), fitted to 212 subgenres · "
            "40 fine-tune bases recorded, never called") in text
    assert "Concentrate AI: 105 components (17 of them run in every chapter)" in text
