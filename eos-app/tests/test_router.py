"""Model registry and router: experts per component, lanes, mature routing, and checkers never judging their own
model's text (D22, P8, P10)."""
from collections import Counter
from dataclasses import replace

import pytest

from eos_app.registry import Registry, candidate_name, least_gap, load_models
from eos_app.router import (RoutingError, choose_checker, choose_writer, experts, load_routing, route,
                            same_model_report, writer_models)
from eos_app.workflow import load_components


@pytest.fixture(scope="module")
def W():
    return load_components()


@pytest.fixture(scope="module")
def R():
    return load_models()


@pytest.fixture(scope="module")
def RT():
    return load_routing()


def model(R, name):
    return [m for m in R.models if m.name == name][0]


def test_the_registry_holds_every_roster_model_with_a_provider(R):
    assert Counter(m.provider for m in R.models) == {"Hugging Face": 153, "Featherless AI": 47, "Concentrate AI": 42,
                                                      "OpenRouter": 25, "Unsloth Desktop": 7, "ElevenLabs": 3,
                                                      "Comfy Cloud": 11}
    assert {m.modality for m in R.models} == {"", "Image", "Video", "Speech", "Music", "Sound", "Speech-to-text"}
    assert len({m.key for m in R.models}) == len(R.models)


def test_mistyped_roster_rows_are_reported_not_guessed(R):
    assert sum("listed twice" in p for p in R.problems) == 5
    assert sum("disagree" in p for p in R.problems) == 5


@pytest.mark.parametrize("cell, name", [
    ("GPT-6.1 Sol", "GPT-6.1 Sol"),
    ("MiMo-V2.6-Pro (least-gap — not parity)", "MiMo-V2.6-Pro"),
    ("None genuinely comparable — least-gap: MiMo-V2.6-Pro (not parity)", "MiMo-V2.6-Pro"),
    ("None — open-weight primary (Author, 2026-10-22)", ""),
])
def test_model_cells_are_read_without_their_notes(cell, name):
    assert candidate_name(cell) == name


def test_spellings_from_both_databases_resolve_to_one_model(R):
    assert R.resolve("MiMo-V2.6-Pro (least-gap — not parity)") is R.resolve("MiMo-2.6-Pro") is model(R, "MiMo-2.6 Pro")
    assert R.resolve("GLM-5.3-Flash") is model(R, "GLM 5.3 Flash")
    assert R.resolve("Kimi  K3") is model(R, "Kimi K3")
    assert least_gap("None genuinely comparable — least-gap: MiMo-V2.6-Pro (not parity)")


def test_every_model_component_has_a_line_of_experts(W, R):
    for c in W.components:
        if c.task_type != "code":
            assert experts(c, R), c.name


def test_experts_run_primary_then_comparable(W, R):
    assert [(s, m.name) for s, m in experts(W.by_step["NEW-14"], R)] == [("primary", "Claude Fable 5.1"), ("comparable", "Kimi K3")]
    assert [(s, m.name) for s, m in experts(W.by_step["NEW-13"], R)] == [("primary", "GLM 5.3 Flash")]   # open-weight primary


def test_each_provider_has_its_route(R, RT):
    assert route(model(R, "Venice Uncensored"), RT) == "openrouter"
    assert route(model(R, "GLM 5.3 Flash"), RT) == "concentrate"
    unsloth = [m for m in R.models if m.provider == "Unsloth Desktop"][0]
    assert route(unsloth, RT) == "unsloth_desktop"


def test_a_checker_steps_past_the_model_that_wrote_the_text(W, R, RT):
    canon = W.by_step["19.3"]                     # Canon Check: MiMo-2.6 Pro, GPT-6.1 Sol, DeepSeek V4 Pro 0813
    assert [m.name for _, m in experts(canon, R)] == ["MiMo-2.6 Pro", "GPT-6.1 Sol", "DeepSeek V4 Pro 0813"]
    assert choose_checker(canon, model(R, "MiMo-2.6 Pro"), R, RT).name == "GPT-6.1 Sol"
    assert choose_checker(canon, model(R, "Gemini 4 Argon"), R, RT).name == "MiMo-2.6 Pro"


def test_mature_text_both_experts_refused_goes_to_venice(W, R, RT):
    cont = W.by_step["33"]
    writer = model(R, "DavidAU/Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic")
    refused = {m.key for _, m in experts(cont, R)}
    assert choose_checker(cont, writer, R, RT, mature=True, refused=refused).name == "Venice Uncensored"
    with pytest.raises(RoutingError):                                # Venice is only for mature text
        choose_checker(cont, writer, R, RT, mature=False, refused=refused)
    with pytest.raises(RoutingError):
        choose_checker(cont, writer, R, RT, mature=True, refused=refused, down={model(R, "Venice Uncensored").key})


def test_prose_writers_use_genre_fine_tunes_and_mature_text_needs_one(W, R, RT):
    draft = W.by_step["32"]
    assert draft.writes_prose and not W.by_step["33"].writes_prose
    assert choose_writer(draft, R, RT, genre="Space Opera").name == "Claude Fable 5.1"      # nothing tagged yet: stand-in
    with pytest.raises(RoutingError):
        writer_models(draft, R, RT, genre="Space Opera", mature=True)
    tuned = replace(model(R, "DavidAU/Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic"), genre="Space Opera")
    reg = Registry(R.version, [tuned] + R.models, {**R.by_key, tuned.key: tuned}, [])
    pick = choose_writer(draft, reg, RT, genre="Space Opera", mature=True)
    assert pick is tuned and route(pick, RT) == "featherless"


def test_no_checker_shares_its_primary_with_what_it_judges(W, R):
    assert same_model_report(W, R) == []        # the 9 checkers and Edit Coach swapped (the Author, 2026-10-22)


def test_every_evaluation_component_has_a_mature_fallback_or_an_open_slot(W):
    evaluators = [c for c in W.components if c.is_evaluation]
    assert len(evaluators) == 21
    assert {c.step for c in evaluators if c.mature_fallback is None} == {"NEW-20", "NEW-25"}   # left open
    assert {c.mature_fallback for c in evaluators if c.mature_fallback} == {"Venice Uncensored"}
    assert all(c.mature_fallback is None for c in W.components if not c.is_evaluation)


def test_editing_tools_run_on_their_own_experts_not_the_genre_fine_tunes(W, R, RT):
    proof, reports, coach = W.by_step["NEW-15"], W.by_step["NEW-16"], W.by_step["NEW-17"]
    assert proof.category == coach.category == "Prose Writing" and not proof.writes_prose
    assert [m.name for m in writer_models(proof, R, RT, genre="Space Opera")] == ["GPT-6 Luna", "GLM 5.3 Flash"]
    assert reports.task_type == "code" and reports.candidates is None
    assert choose_checker(coach, model(R, "Claude Fable 5.1"), R, RT).name == "Kimi K3"    # never on the drafting model


def test_media_components_use_media_models_through_their_providers(W, R, RT):
    cover, narration = W.by_step["NEW-22"], W.by_step["NEW-24"]
    assert cover.makes_media and [m.name for m in writer_models(cover, R, RT)] == ["GPT Image 2", "Ideogram", "Qwen-Image"]
    assert [route(m, RT) for m in writer_models(cover, R, RT)] == ["openrouter", "comfy_cloud", "comfy_cloud"]
    assert [route(m, RT) for m in writer_models(narration, R, RT)] == ["elevenlabs", "openrouter", "featherless"]


def test_mature_media_runs_only_on_open_models_on_comfy_cloud(W, R, RT):
    assert [m.name for m in writer_models(W.by_step["NEW-26"], R, RT, mature=True)] == ["Wan 2.2", "LTX-2"]
    assert [m.name for m in writer_models(W.by_step["NEW-22"], R, RT, mature=True)] == ["Qwen-Image"]
    assert [m.name for m in writer_models(W.by_step["NEW-24"], R, RT, mature=True)] == ["Chatterbox"]
    assert [m.name for m in writer_models(W.by_step["NEW-18"], R, RT, mature=True)] == ["FLUX.2", "Qwen-Image", "Z-Image Turbo"]


def test_sound_effects_has_three_experts_and_mature_work_stays_on_the_open_one(W, R, RT):
    sfx = W.by_step["NEW-28"]
    assert [m.name for m in writer_models(sfx, R, RT)] == ["ElevenLabs Sound Effects", "Stable Audio Open", "Stability Text To Audio"]
    assert [m.name for m in writer_models(sfx, R, RT, mature=True)] == ["Stable Audio Open"]


def test_music_leads_with_lyria_and_keeps_an_open_model_for_mature_work(W, R, RT):
    music = W.by_step["NEW-27"]
    assert [m.name for m in writer_models(music, R, RT)] == ["Lyria 3 Pro", "MiniMax Music 3", "ACE-Step"]
    assert [route(m, RT) for m in writer_models(music, R, RT)] == ["openrouter", "comfy_cloud", "comfy_cloud"]
    assert [m.name for m in writer_models(music, R, RT, mature=True)] == ["ACE-Step"]


def test_media_checkers_run_on_omni_models(W, R):
    for step in ("NEW-20", "NEW-25"):
        assert [m.name for _, m in experts(W.by_step[step], R)] == ["Qwen3.8 Omni Flash", "MiMo-V2-Omni", "Nemotron 3 Nano Omni"]


def test_an_open_mature_fallback_stops_mature_judging_with_a_reason(W, R, RT):
    vcc = W.by_step["NEW-20"]
    assert set(vcc.judges) >= {"NEW-18", "NEW-22", "NEW-26"}
    refused = {m.key for _, m in experts(vcc, R)}
    with pytest.raises(RoutingError, match="still open"):
        choose_checker(vcc, model(R, "GPT Image 2"), R, RT, mature=True, refused=refused)
