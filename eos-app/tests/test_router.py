"""Model registry and router: experts per component, lanes, mature routing, and checkers never judging their own
model's text (D22, P8, P10)."""
from collections import Counter
from dataclasses import replace

import pytest

from eos_app.registry import Registry, RegistryError, candidate_name, least_gap, load_models
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
    # the roster, with the models the three Notion catalogs and the register add (D33)
    assert Counter(m.provider for m in R.models) == {"Hugging Face": 166, "Featherless AI": 83, "Concentrate AI": 50,
                                                      "OpenRouter": 25, "Unsloth Desktop": 8, "ElevenLabs": 3,
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
    assert choose_writer(draft, R, RT, genre="Epistolary Cookery").name == "Claude Fable 5.1"   # nothing fitted: stand-in
    with pytest.raises(RoutingError, match="no mature-tier model is fitted to Epistolary Cookery"):
        writer_models(draft, R, RT, genre="Epistolary Cookery", mature=True)
    tuned = replace(model(R, "DavidAU/Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic"),
                    genres=("Epistolary Cookery",))
    reg = Registry(R.version, [tuned] + R.models, {**R.by_key, tuned.key: tuned}, [])
    pick = choose_writer(draft, reg, RT, genre="Epistolary Cookery", mature=True)
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


# ---------- corrections of 2026-11-12 (fixes plan B1, B2, B4, B9, B10) ----------

def also_on(R, name, provider, model_id):
    """The registry with one more roster row: the same model on a second provider."""
    m = model(R, name)
    twin = replace(m, key=f"{provider.lower().replace(' ', '-')}-{model_id}", provider=provider, model_id=model_id)
    return Registry(R.version, R.models + [twin], {**R.by_key, twin.key: twin}, []), twin


def test_a_model_with_no_provider_id_is_never_chosen(W, R, RT):
    cover = W.by_step["NEW-22"]                             # GPT Image 2 has an ID; Ideogram and Qwen-Image do not yet
    assert choose_writer(cover, R, RT).name == "GPT Image 2"
    with pytest.raises(RoutingError, match="Ideogram has no provider model ID yet"):
        choose_writer(cover, R, RT, down={model(R, "GPT Image 2").key})
    with pytest.raises(RoutingError, match="FLUX.2 has no provider model ID yet"):
        choose_writer(W.by_step["NEW-18"], R, RT)


def test_an_outage_is_met_by_the_same_model_on_another_provider_first(W, R, RT):
    tropes = W.by_step["NEW-14"]                            # Claude Fable 5.1, then Kimi K3; both on Concentrate AI
    with pytest.raises(RoutingError, match="Concentrate AI, which is down"):
        choose_writer(tropes, R, RT, down_providers={"Concentrate AI"})
    reg, twin = also_on(R, "Claude Fable 5.1", "OpenRouter", "anthropic/claude-fable-5.1")
    assert [(m.name, m.provider) for m in writer_models(tropes, reg, RT)] == [
        ("Claude Fable 5.1", "Concentrate AI"), ("Claude Fable 5.1", "OpenRouter"), ("Kimi K3", "Concentrate AI")]
    assert choose_writer(tropes, reg, RT).provider == "Concentrate AI"
    assert choose_writer(tropes, reg, RT, down_providers={"Concentrate AI"}) is twin      # same model, other route


def test_a_checker_never_judges_its_own_model_on_another_route(W, R, RT):
    canon = W.by_step["19.3"]                               # MiMo-2.6 Pro, GPT-6.1 Sol, DeepSeek V4 Pro 0813
    reg, twin = also_on(R, "MiMo-2.6 Pro", "OpenRouter", "xiaomi/mimo-2.6-pro")
    assert twin.ident == model(R, "MiMo-2.6 Pro").ident and twin.key != model(R, "MiMo-2.6 Pro").key
    assert choose_checker(canon, twin, reg, RT).name == "GPT-6.1 Sol"                         # the writer's model, skipped
    assert choose_checker(canon, model(R, "GPT-6.1 Sol"), reg, RT, down_providers={"Concentrate AI"}) is twin


def test_a_tagged_fine_tune_leads_and_the_components_experts_stay_as_the_safety_net(W, R, RT):
    draft = W.by_step["32"]
    tuned = replace(model(R, "DavidAU/Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic"),
                    genres=("Epistolary Cookery",))
    others = [m for m in R.models if m.ident != tuned.ident]                 # the same model on no other route
    reg = Registry(R.version, [tuned] + others, {m.key: m for m in [tuned] + others}, [])
    assert [m.name for m in writer_models(draft, reg, RT, genre="Epistolary Cookery")] == [tuned.name, "Claude Fable 5.1",
                                                                                              "Kimi K3"]
    assert choose_writer(draft, reg, RT, genre="Epistolary Cookery", down={tuned.key}).name == "Claude Fable 5.1"
    assert writer_models(draft, reg, RT, genre="Epistolary Cookery", mature=True) == [tuned]   # never the stand-ins


def test_a_model_on_a_provider_outside_the_lane_is_not_called(W, R, RT):
    tropes = W.by_step["NEW-14"]
    moved = [replace(m, provider="Hugging Face") if m.name == "Kimi K3" else m for m in R.models]
    reg = Registry(R.version, moved, {m.key: m for m in moved}, [])
    assert [m.name for m in writer_models(tropes, reg, RT)] == ["Claude Fable 5.1"]           # Kimi K3 left the general lane
    moved = [replace(m, provider="Hugging Face") if m.name in ("Kimi K3", "Claude Fable 5.1") else m for m in R.models]
    with pytest.raises(RoutingError, match="general-lane provider"):
        writer_models(tropes, Registry(R.version, moved, {m.key: m for m in moved}, []), RT)


def test_a_media_component_only_takes_models_that_make_what_it_makes(W, R, RT):
    cover = W.by_step["NEW-22"]
    assert cover.modality == "Image" and W.by_step["NEW-27"].modality == "Music"
    with pytest.raises(RoutingError, match="makes music, but GPT Image 2 makes image"):
        writer_models(replace(cover, modality="Music"), R, RT)


def test_two_models_that_read_alike_are_told_apart_or_refused(R):
    assert R.resolve("Command A").provider == "Concentrate AI" and R.resolve("Command A+").provider == "OpenRouter"
    assert R.resolve("command-a") is R.resolve("Command A")                                   # an exact provider ID
    with pytest.raises(RegistryError, match="could mean Command A or Command A\\+"):
        R.resolve("CommandA")
