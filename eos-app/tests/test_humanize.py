"""Humanize (requirements v0.8, FR-HU-1 to FR-HU-9). No network: the model is a fake callable."""

import pytest

from eos_app.humanize import (HumanizeFailed, HumanizeSettings, ProtectedSpanError, build_request, check,
                              clean_output, load_config, measure, protect, recommend, restore, humanize)


@pytest.fixture(scope="module")
def C():
    return load_config()


ROBOTIC = ("She walked to the door. She opened the door slowly. She looked into the room. "
           "It was clear that something was wrong. This was a moment of truth. "
           "Furthermore, the air was thick with tension. She couldn't help but shiver. ") * 3

NATURAL = ("The door stuck. She shouldered it, once, twice, and on the third try it gave with a crack "
           "that sent plaster dust drifting across the hall like flour from a dropped sack. Nobody. "
           "Just the clock, and the smell of oranges going soft in a bowl nobody had emptied since spring.")


# ---------- settings and config ----------

def test_config_loads(C):
    assert set(C.strengths) == {"light", "balanced", "strong"}
    assert C.limits["max_passes"] == 3
    assert "a testament to" in C.stock_phrases


def test_settings_are_checked(C):
    with pytest.raises(ValueError):
        HumanizeSettings(strength="extreme").validate(C)
    with pytest.raises(ValueError):
        HumanizeSettings(passes=4).validate(C)
    with pytest.raises(ValueError):
        HumanizeSettings(english_variant="martian").validate(C)
    with pytest.raises(ValueError):
        HumanizeSettings(em_dash="never").validate(C)
    HumanizeSettings().validate(C)


# ---------- protected spans (FR-HU-3) ----------

def test_dialogue_and_locks_are_masked_and_restored():
    text = 'He paused. "Not tonight," she said. The rain kept on. I will not go back.'
    p = protect(text, locked=["I will not go back."])
    assert '"Not tonight,"' not in p.masked and "I will not go back." not in p.masked
    assert len(p.spans) == 2
    assert restore(p.masked, p) == text


def test_curly_and_single_quote_dialogue():
    text = "“Wait,” he said. ‘I don’t know,’ she said."
    p = protect(text, single_quote_dialogue=True)
    assert len(p.spans) == 2
    assert "don’t" not in p.masked
    assert restore(p.masked, p) == text


def test_dialogue_protection_can_be_turned_off():
    p = protect('"Go," she said.', protect_dialogue=False)
    assert p.spans == {} and p.masked == '"Go," she said.'


def test_restore_refuses_a_lost_or_repeated_span():
    p = protect('A. "Stay," he said. B.')
    token = next(iter(p.spans))
    with pytest.raises(ProtectedSpanError):
        restore(p.masked.replace(token, ""), p)
    with pytest.raises(ProtectedSpanError):
        restore(p.masked + " " + token, p)


def test_text_that_already_contains_a_token_shape_is_refused():
    with pytest.raises(ValueError):
        protect("A note ⟦P1⟧ left in the text.")


# ---------- the request (FR-HU-2, FR-HU-4) ----------

def test_request_carries_settings_route_and_voice(C):
    s = HumanizeSettings(strength="strong", english_variant="british", em_dash="remove_narration",
                         voice_notes="Close third person, past tense, dry humour.")
    req = build_request("She ran.", s, C, target_words=120)
    system = req.messages[0]["content"]
    assert req.temperature == C.strengths["strong"]["temperature"]
    assert req.task_type == "prose" and req.agent == "edit_actions.humanize" and req.tier == "standard"
    assert "Close third person" in system and "British spelling" in system
    assert "108" in system and "132" in system           # ±10% of 120 words
    assert "⟦" in system                             # the placeholder rule
    assert "tapestry" in system                          # the stock-phrase list
    assert "detector" not in system.lower()
    assert req.messages[1]["content"].endswith("She ran.")


def test_mature_passage_routes_to_the_mature_tier(C):
    assert build_request("x", HumanizeSettings(mature=True), C, 10).tier == "mature"


# ---------- clean-up (FR-HU-5) ----------

def test_clean_output_strips_markup_and_preamble_but_keeps_italics(C):
    raw = "Here is the rewritten text:\n\n## Scene\n**She** ran. *Too late*, she thought.\n- item\n```x```"
    out = clean_output(raw, HumanizeSettings(), C)
    assert out.startswith("Scene")
    assert "**" not in out and "##" not in out and "```" not in out and "- item" not in out
    assert "*Too late*" in out


def test_em_dash_policy_applies_to_narration_only(C):
    p = protect('He stopped — listened. "Wait — no," she said.')
    out = clean_output(p.masked, HumanizeSettings(em_dash="remove_narration"), C)
    final = restore(out, p)
    assert final.startswith("He stopped, listened.")
    assert '"Wait — no,"' in final                    # dialogue untouched


def test_em_dash_keep_leaves_them(C):
    assert "—" in clean_output("He stopped — listened.", HumanizeSettings(em_dash="keep"), C)


# ---------- measures (FR-HU-6) ----------

def test_measures_tell_robotic_from_natural(C):
    a, b = measure(ROBOTIC, C), measure(NATURAL, C)
    assert a.stock_phrases > b.stock_phrases
    assert a.copula_openers >= 2 and b.copula_openers == 0
    assert a.sentence_spread < b.sentence_spread
    assert 0 < b.lexical_variety <= 100
    assert a.words > 0 and a.sentences > 0
    assert -50 < a.reading_ease < 130 and b.grade_level > a.grade_level


def test_measure_counts_em_dashes_and_lists_phrases(C):
    m = measure("The weight of it — all of it. A testament to nothing.", C)
    assert m.em_dashes == 1
    assert set(m.phrases_found) == {"the weight of", "a testament to"}


# ---------- recommendation by code (FR-HU-7) ----------

def test_recommend_strong_for_robotic_text(C):
    s, reason = recommend(ROBOTIC, C)
    assert s.strength == "strong" and reason


def test_recommend_light_for_natural_text(C):
    s, _ = recommend(NATURAL, C)
    assert s.strength == "light" and s.passes == 1


def test_one_stock_phrase_in_a_short_scene_is_not_strong(C):
    text = ("The first ferry left at six. By twenty to, the queue already reached the ticket hut, and the gulls had "
            "found the bread van. [Protagonist] showed a pass at the barrier and checked the timetable against the one "
            "in their pocket. The times matched. The wind off the water held steady from the east. Along the pier the "
            "lamps were still lit, though the sky had gone grey. [Protagonist] felt the weight of the morning settle, "
            "step by step. At the end of the pier, [Mentor] was already waiting with two coffees and the morning paper.")
    s, reason = recommend(text, C)
    assert s.strength == "balanced"
    assert reason.startswith("1 stock phrase or summary opener in ")


# ---------- checks (FR-HU-8) ----------

def test_check_flags_drift_names_and_new_tells(C):
    original = "Mara crossed the yard to the old well. " * 10
    shorter = "Someone crossed. A testament to the yard."
    res = check(original, shorter, C, terms=["Mara"])
    assert any("Mara" in e for e in res.errors)
    assert any("words" in e.lower() for e in res.errors)          # drift above the fail line
    assert any("stock phrase" in w.lower() for w in res.warnings)


def test_check_passes_a_faithful_rewrite(C):
    original = "Mara crossed the yard to the old well, and the bucket rattled."
    result = "Mara crossed the yard to the old well. The bucket rattled on its chain."
    res = check(original, result, C, terms=["Mara"])
    assert res.errors == []


# ---------- the whole action (FR-HU-1, FR-HU-9) ----------

def test_humanize_runs_passes_and_keeps_protected_spans(C):
    calls = []

    def fake_model(req):
        calls.append(req)
        body = req.messages[1]["content"].split("\n\n", 1)[1]
        return "Here is the revised text:\n" + body.replace("Furthermore, ", "")

    text = 'Furthermore, Mara waited. "Not yet," she said. She waited more.'
    res = humanize(text, HumanizeSettings(passes=2), fake_model, C, locked=["She waited more."], terms=["Mara"])
    assert len(calls) == 2
    assert res.text == 'Mara waited. "Not yet," she said. She waited more.'
    assert res.before.stock_phrases == 1 and res.after.stock_phrases == 0
    assert res.status == "suggestion" and res.decided_by == "author"
    assert res.errors == []
    assert res.passes_run == 2
    assert res.inputs["settings"]["passes"] == 2


def test_a_lost_span_is_retried_then_fails_to_the_fallback(C):
    attempts = []

    def bad_model(req):
        attempts.append(1)
        return "Mara waited."          # drops the dialogue token every time

    with pytest.raises(HumanizeFailed):
        humanize('Mara waited. "Not yet," she said.', HumanizeSettings(), bad_model, C)
    assert len(attempts) == 1 + C.limits["retries"]


def test_a_retry_that_succeeds_is_used(C):
    replies = iter(["Mara waited.", None])

    def flaky(req):
        r = next(replies)
        return r if r is not None else req.messages[1]["content"].split("\n\n", 1)[1]

    res = humanize('Mara waited. "Not yet," she said.', HumanizeSettings(), flaky, C)
    assert '"Not yet,"' in res.text and res.retries == 1


def test_too_long_or_empty_text_is_refused(C):
    with pytest.raises(ValueError):
        humanize("", HumanizeSettings(), lambda r: "", C)
    with pytest.raises(ValueError, match="scene by scene"):
        humanize("word " * 5000, HumanizeSettings(), lambda r: "", C)
