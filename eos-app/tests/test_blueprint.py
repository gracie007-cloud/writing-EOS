"""Story Blueprint formula engine (requirements v0.7, FR-DEV-14 to FR-DEV-23, Appendix C).

Every rule here comes from the Notion Story Blueprint Pipeline. Examples are generic. No network, no models.
"""

import pytest
import yaml

from eos_app.blueprint import (TABLES_PATH, CastMap, CoreRating, StageGateError, StoryProfile, StructureRating,
                               TableError, arc_checks, cast_function_map, conflict_fit, gant_skeleton, guardrail_diff,
                               load_tables, needs_antagonist, outcome_type, parse_pillar, pillar_factor, pillar_notation,
                               plot_blueprint_checks, score_cores, score_structures, stage_gate,
                               technology_fallback_flag, who_decides)


@pytest.fixture(scope="module")
def T():
    return load_tables()


# ---------- tables (FR-DEV-23) ----------

def test_tables_load_with_all_nine_cores(T):
    assert len(T.cores) == 9 and set(T.core_pillars) == set(T.cores)
    assert T.version


def test_maxima_follow_the_weights(T):
    assert T.weights["conflict_fit"]["maximum"] == 27
    assert T.weights["structure_fit"]["maximum"] == 36


def test_inconsistent_maximum_is_refused(tmp_path):
    raw = yaml.safe_load(TABLES_PATH.read_text(encoding="utf-8"))
    raw["weights"]["conflict_fit"]["maximum"] = 30
    bad = tmp_path / "t.yaml"
    bad.write_text(yaml.safe_dump(raw, allow_unicode=True), encoding="utf-8")
    with pytest.raises(TableError, match="maximum"):
        load_tables(bad)


def test_unknown_pillar_in_core_map_is_refused(tmp_path):
    raw = yaml.safe_load(TABLES_PATH.read_text(encoding="utf-8"))
    raw["core_pillars"]["Internal"] = ["Belonging", "Happiness"]
    bad = tmp_path / "t.yaml"
    bad.write_text(yaml.safe_dump(raw, allow_unicode=True), encoding="utf-8")
    with pytest.raises(TableError, match="Happiness"):
        load_tables(bad)


# ---------- Pillar factor (FR-DEV-15) ----------

@pytest.mark.parametrize("core, implied, expected", [
    ("Technological", ["Technology", "Purpose"], 3),     # primary and secondary both typical
    ("Interpersonal", ["Belonging"], 3),                 # a single implied Pillar that matches
    ("Technological", ["Purpose", "Belonging"], 2),      # primary matches, secondary does not
    ("Existential", ["Belonging", "Purpose"], 1),        # only a later Pillar matches: loose overlap
    ("Environmental", ["Belonging"], 0),
    ("Internal", [], 0),
])
def test_pillar_factor(T, core, implied, expected):
    assert pillar_factor(core, implied, T) == expected


def test_pillar_factor_refuses_unknown_names(T):
    with pytest.raises(ValueError):
        pillar_factor("Romantic", ["Belonging"], T)
    with pytest.raises(ValueError):
        pillar_factor("Internal", ["Love"], T)


# ---------- Conflict Fit (FR-DEV-1) ----------

def test_conflict_fit_formula(T):
    assert conflict_fit(3, 2, 2, 1, 0, T) == 3 * 3 + 2 * 3 + 2 * 2 + 1
    assert conflict_fit(3, 2, 2, 1, 1, T) == 20 - 3
    assert conflict_fit(3, 3, 3, 3, 0, T) == 27


def test_conflict_fit_refuses_out_of_range(T):
    with pytest.raises(ValueError):
        conflict_fit(4, 0, 0, 0, 0, T)
    with pytest.raises(ValueError):
        conflict_fit(1, 1, 1, 1, -1, T)


def ratings(T, top=None, default=(1, 1, 1, 0)):
    """All nine cores at a low default, with chosen cores overridden: top = {core: (source, theme, genre, contra)}."""
    r = {c: CoreRating(*default) for c in T.cores}
    for core, vals in (top or {}).items():
        r[core] = CoreRating(*vals)
    return r


def test_clear_fit(T):
    # Technological: 3*3 + 3*3 (Technology, Purpose) + 3*2 + 2 = 26; Systemic: 2*3 + 1*3 + 2*2 + 2 = 15
    res = score_cores(ratings(T, {"Technological": (3, 3, 2, 0), "Systemic": (2, 2, 2, 0)}), ["Technology", "Purpose"], T)
    assert res.reading == "clear_fit"
    assert res.recommended == "Technological"
    assert res.sheet[0].core == "Technological" and res.sheet[0].total == 26
    assert res.actions == []
    assert res.decided_by == "author"


def test_close_contest_files_the_runner_up(T):
    # Internal: 3*3 + 3*3 (Belonging, Purpose) + 2*2 + 1 = 23; Creational: 3*3 + 3*3 + 1*2 + 1 = 21
    res = score_cores(ratings(T, {"Internal": (3, 2, 1, 0), "Creational": (3, 1, 1, 0)}), ["Belonging", "Purpose"], T)
    assert res.reading == "close_contest"
    assert (res.recommended, res.runner_up, res.gap) == ("Internal", "Creational", 2)
    assert ("file_runner_up", "Creational") in res.actions


def test_tie_goes_to_the_author_with_the_question(T):
    res = score_cores(ratings(T, {"Internal": (3, 2, 1, 0), "Creational": (3, 2, 1, 0)}), ["Belonging", "Purpose"], T)
    assert res.reading == "tie"
    assert res.recommended is None
    assert res.tied == ["Internal", "Creational"]
    assert "lost without" in res.question


def test_weak_material_returns_to_the_braindump_first(T):
    # every core low (best is 11, a tie between two cores); weak is checked before the tie
    res = score_cores(ratings(T, default=(0, 1, 0, 0)), ["Clothing"], T)
    assert res.sheet[0].total < 12
    assert res.reading == "weak"
    assert ("return_to_braindump", None) in res.actions


def test_sheet_records_where_each_factor_came_from(T):
    res = score_cores(ratings(T), ["Belonging"], T)
    assert res.sheet[0].sources == {"source": "rater", "pillar": "code", "theme": "rater", "genre": "rater", "contradictions": "rater"}
    assert res.table_version == T.version


def test_all_nine_cores_must_be_rated(T):
    r = ratings(T)
    del r["Unknown"]
    with pytest.raises(ValueError, match="Unknown"):
        score_cores(r, ["Belonging"], T)


# ---------- antagonist rule (FR-DEV-17) ----------

@pytest.mark.parametrize("core, expected", [("Systemic", True), ("Cultural", True), ("Technological", True),
                                            ("Unknown", True), ("Internal", False), ("Existential", False)])
def test_needs_antagonist(T, core, expected):
    assert needs_antagonist(core, T) is expected


# ---------- Climax Outcome Matrix (FR-DEV-19) ----------

@pytest.mark.parametrize("truth, restored, expected", [(True, True, "Triumph"), (True, False, "Bittersweet"),
                                                       (False, True, "Hollow Victory"), (False, False, "Downfall")])
def test_outcome_matrix(T, truth, restored, expected):
    assert outcome_type(truth, restored, T) == expected


def test_flat_arc_mode(T):
    assert outcome_type(True, False, T, flat_arc=True) == "Flat"


# ---------- Structure Fit (FR-DEV-20; Q10: the Author's map of 21 structures is the standing order) ----------

# A generic slice of a Conflict and Structure Map: {structure: {(axis, value): best | situational}}.
FITS = {
    "Hero's Journey": {("Conflict Core", "Internal"): "situational", ("Inevitability", "Avoidable"): "best"},
    "Save the Cat": {("Conflict Core", "Interpersonal"): "best", ("Inevitability", "Avoidable"): "best",
                     ("Novelty", "Unusual"): "best", ("Novelty", "Ordinary"): "situational"},
    "Fichtean Curve": {("Conflict Core", "Technological"): "best", ("Inevitability", "Unavoidable"): "best",
                       ("Inevitability", "Conditional"): "situational", ("Novelty", "Unusual"): "best"},
    "Freytag's Pyramid": {("Conflict Core", "Existential"): "best", ("Inevitability", "Unavoidable"): "best"},
    "Dan Harmon's Story Circle": {("Conflict Core", "Internal"): "best", ("Novelty", "Ordinary"): "best",
                                  ("Inevitability", "Conditional"): "situational"},
    "Kishōtenketsu": {("Conflict Core", "Internal"): "best", ("Inevitability", "Unavoidable"): "situational",
                      ("Novelty", "Inexplicable"): "best", ("Novelty", "Ordinary"): "situational"},
}


def all_ratings(T, value=2, **over):
    r = {name: StructureRating(value, value, value) for name in T.structures}
    r.update(over)
    return r


def story_of(**kw):
    base = dict(outcome="Bittersweet", inevitability="Unavoidable", novelty="Unusual", temporal_root="Historical",
                core="Technological")
    return StoryProfile(**{**base, **kw})


def test_all_21_structures_are_scored(T):
    assert len(T.structures) == 21 and T.three_act == "Three-Act Structure"
    assert len(score_structures(story_of(), all_ratings(T), T, FITS).sheet) == 21


def test_inevitability_and_novelty_come_from_the_map(T):
    rows = {r.structure: r for r in score_structures(story_of(), all_ratings(T), T, FITS).sheet}
    f = rows["Fichtean Curve"]
    assert (f.core_fit, f.outcome, f.inevitability, f.novelty) == ("best", 1, 3, 3)   # outcome Any scores 1
    h = rows["Hero's Journey"]
    assert (h.inevitability, h.novelty) == (0, 1)      # listed only under Avoidable; no view on novelty at all
    assert rows["Save the Cat"].novelty == 3 and rows["Save the Cat"].inevitability == 0
    assert all(r.sources["inevitability"] == "map" and r.sources["outcome"] == "code" for r in rows.values())


def test_the_core_decides_first(T):
    # Hero's Journey totals more (28 against 24) but is no fit for a Technological core; Fichtean leads.
    res = score_structures(story_of(), all_ratings(T, **{"Hero's Journey": StructureRating(3, 3, 3)}), T, FITS)
    rows = {r.structure: r for r in res.sheet}
    assert rows["Hero's Journey"].total == 28 and rows["Fichtean Curve"].total == 24
    assert res.sheet[0].structure == "Fichtean Curve" and res.recommended == "Fichtean Curve"
    assert not res.three_act and res.decided_by == "author"


def test_three_act_when_nothing_beats_18(T):
    res = score_structures(story_of(outcome="Flat"), all_ratings(T, 0), T, FITS)
    assert res.sheet[0].total <= 18
    assert res.three_act and res.recommended == "Three-Act Structure"


def test_kishotenketsu_flag_sends_back_to_stage0(T):
    story = story_of(outcome="Flat", inevitability="Avoidable", novelty="Ordinary", core="Internal")
    res = score_structures(story, all_ratings(T, 1, **{"Kishōtenketsu": StructureRating(3, 3, 3)}), T, FITS)
    assert res.recommended == "Kishōtenketsu" and res.kishotenketsu_flag
    assert ("kishotenketsu_send_back", None) in res.actions


def test_story_circle_special_rules(T):
    base = dict(inevitability="Conditional", novelty="Ordinary", core="Internal")
    with_residual = score_structures(story_of(outcome="Triumph", temporal_root="Cyclical", residual_unmet=True, **base),
                                     all_ratings(T), T, FITS)
    without = score_structures(story_of(outcome="Triumph", temporal_root="Historical", residual_unmet=False, **base),
                               all_ratings(T), T, FITS)
    a = {r.structure: r for r in with_residual.sheet}["Dan Harmon's Story Circle"]
    b = {r.structure: r for r in without.sheet}["Dan Harmon's Story Circle"]
    assert (a.outcome, a.inevitability) == (3, 3)      # exact with a Cyclical root
    assert (b.outcome, b.inevitability) == (2, 2)      # Triumph without a residual Unmet; the map's situational fit


def test_structure_tie_lists_both(T):
    fits = {"Story Grid": {("Conflict Core", "Systemic"): "best"}, "Four-Act Structure": {("Conflict Core", "Systemic"): "best"}}
    res = score_structures(story_of(core="Systemic"), all_ratings(T, 3), T, fits)
    assert res.sheet[0].total == res.sheet[1].total == 24
    assert res.recommended is None and res.tied == ["Four-Act Structure", "Story Grid"]


def test_structure_ratings_and_names_are_checked(T):
    story = story_of()
    with pytest.raises(ValueError):
        score_structures(story, all_ratings(T, 4), T, FITS)
    r = all_ratings(T)
    del r["Save the Cat"]
    with pytest.raises(ValueError, match="Save the Cat"):
        score_structures(story, r, T, FITS)
    with pytest.raises(TableError, match="Cloud Structure"):
        score_structures(story, all_ratings(T), T, {"Cloud Structure": {}})


# ---------- Vacancy Rule (FR-DEV-21) ----------

def test_cast_function_map(T):
    cm = cast_function_map(
        required=["Hero", "Mentor", "Herald", "Shadow / Antagonist"],
        assignments={"Hero": ["[Protagonist]"], "Mentor": ["[Mentor]"], "Herald": ["[Mentor]"]},
        characters=["[Protagonist]", "[Mentor]", "[Minor character]"], tables=T)
    assert isinstance(cm, CastMap)
    assert cm.statuses["Hero"] == "Filled" and cm.statuses["Herald"] == "Filled"
    assert cm.statuses["Shadow / Antagonist"] == "Vacant (create)"
    assert cm.statuses["Trickster"] == "Not required"
    assert cm.cut_or_merge == ["[Minor character]"]
    assert ("send_to_pool", "Shadow / Antagonist") in cm.actions
    assert cm.warnings == []          # one character may hold two functions


def test_split_function_needs_a_reason(T):
    kw = dict(required=["Hero", "Ally"], characters=["[Protagonist]", "[Supporting character A]", "[Supporting character B]"], tables=T)
    a = {"Hero": ["[Protagonist]"], "Ally": ["[Supporting character A]", "[Supporting character B]"]}
    assert any("Ally" in w for w in cast_function_map(assignments=a, **kw).warnings)
    assert cast_function_map(assignments=a, split_reasons={"Ally": "Twins who act as one"}, **kw).warnings == []


def test_three_functions_on_one_character_is_flagged(T):
    cm = cast_function_map(required=["Hero", "Mentor", "Herald", "Ally"],
                           assignments={"Hero": ["[Protagonist]"], "Mentor": ["[Mentor]"], "Herald": ["[Mentor]"], "Ally": ["[Mentor]"]},
                           characters=["[Protagonist]", "[Mentor]"], tables=T)
    assert any("[Mentor]" in w for w in cm.warnings)


def test_unknown_archetype_is_refused(T):
    with pytest.raises(ValueError):
        cast_function_map(required=["Sidekick"], assignments={}, characters=[], tables=T)


# ---------- stage gates and the guardrail (FR-DEV-22, FR-DEV-5) ----------

def test_characters_wait_for_the_naming_system(T):
    stage_gate("characters", {"conflict_seed", "naming_system"}, T)
    with pytest.raises(StageGateError, match="naming_system"):
        stage_gate("characters", {"conflict_seed"}, T)


def test_stage_gates(T):
    stage_gate("stage1", {"conflict_seed", "naming_system", "character_seeds"}, T)
    with pytest.raises(StageGateError, match="plot_blueprint"):
        stage_gate("stage2", {"conflict_seed", "character_seeds"}, T)
    with pytest.raises(StageGateError, match="arc_blueprint"):
        stage_gate("stage3", {"plot_blueprint"}, T)
    with pytest.raises(ValueError):
        stage_gate("stage9", set(), T)


def test_guardrail_diff(T):
    before = {"core": "Technological", "pillars": ["Worker · Purpose: Threatened (Technological)"], "want": "Keep the job", "point_of_impact": "Purpose"}
    after = dict(before, pillars=["Worker · Belonging: Threatened (Natural)"], want="Find a new crew")
    assert guardrail_diff(before, after, T) == ["pillars"]


# ---------- Stage 2 checks (FR-DEV-19) ----------

def test_oscillation_is_counted(T):
    path = ["Protection", "Disruption", "Resistance", "Negotiation", "Resistance", "Negotiation", "Collapse", "Acceptance", "Integration"]
    res = arc_checks([1, 2, 3, 4, 5, 6, 7], path, "Triumph", T)
    assert res.oscillations == 1 and res.warnings == [] and res.errors == []


def test_positive_arc_without_collapse_is_warned(T):
    res = arc_checks([1, 2, 3, 4, 5, 6, 7], ["Protection", "Disruption", "Resistance", "Negotiation", "Acceptance", "Integration"], "Bittersweet", T)
    assert any("Collapse" in w for w in res.warnings)


def test_plot_ring_only_moves_forward(T):
    res = arc_checks([1, 2, 3, 2, 4], ["Protection"], "Downfall", T)
    assert res.errors


def test_gant_skeleton_follows_the_conversion_table(T):
    bp = {"pillar_history": "Lost a home in a fire", "pillar_profile": "Shelter & Safety: Secure (Technological)",
          "want": "Keep the new house", "point_of_impact": "Shelter & Safety", "peak_intensity": "Severe",
          "possible_endings": "Home kept / Home lost"}
    sk = gant_skeleton(bp, T)
    assert ("Ghost", "pillar_history", "Lost a home in a fire") in sk[0]
    assert any(c == "Want activated" for c, _, _ in sk[3])
    assert any(c == "Climax Outcome Matrix" for c, _, _ in sk[6])
    lie = [v for c, f, v in sk[1] if c == "Lie"][0]
    assert "Lost a home" in lie and "Shelter" in lie


# ---------- Pillar notation and the Technology fallback (FR-DEV-18) ----------

def test_pillar_notation_round_trip(T):
    text = pillar_notation("Victims", "Shelter & Safety", "Unmet", "Technological", T)
    assert text == "Victims · Shelter & Safety: Unmet (Technological)"
    assert parse_pillar(text, T) == ("Victims", "Shelter & Safety", "Unmet", "Technological")
    with pytest.raises(ValueError):
        pillar_notation("Victims", "Shelter & Safety", "Gone", "Natural", T)


def test_technology_fallback_flag(T):
    states = [("[Protagonist]", "Technology", "Threatened", "Technological")]
    assert technology_fallback_flag(states, natural_fallback=False)
    assert technology_fallback_flag(states, natural_fallback=True) is None
    assert technology_fallback_flag([("[Protagonist]", "Belonging", "Threatened", "Natural")], natural_fallback=False) is None


# ---------- Stage 1 quality checks (FR-DEV-6, FR-DEV-17) ----------

def good_blueprint():
    return {"core": "Technological", "point_of_impact": {"pillar": "Purpose", "state": "Threatened", "level": "Technological"},
            "specificity": "Only the protagonist still knows how the old machines work.",
            "resonance": "match", "intensity": {"opening": "Mild", "peak": "Severe"}, "shape": "standard",
            "antagonist_role": {"function": "Replaces the workers", "requirements": "A face for the system", "source": "Pool match"},
            "trope_audit": [{"element": "The rebel engineer", "treatment": "subverted"},
                            {"element": "The heartless company", "treatment": "deepened"},
                            {"element": "The last-minute fix", "treatment": "justified"}]}


def test_good_plot_blueprint_passes(T):
    assert plot_blueprint_checks(good_blueprint(), T) == []


@pytest.mark.parametrize("change, expected", [
    ({"core": ["Technological", "Internal"]}, "exactly one Conflict Core"),
    ({"point_of_impact": {"pillar": "Purpose"}}, "point of impact"),
    ({"specificity": "One reason. And another."}, "one sentence"),
    ({"resonance": ""}, "Resonance"),
    ({"intensity": {"opening": "Severe", "peak": "Mild"}}, "Peak"),
    ({"antagonist_role": None}, "Antagonist Role"),
    ({"trope_audit": [{"element": "x", "treatment": "ignored"}]}, "trope audit"),
])
def test_plot_blueprint_failures(T, change, expected):
    bp = good_blueprint()
    bp.update(change)
    assert any(expected.lower() in f.lower() for f in plot_blueprint_checks(bp, T))


def test_siege_shape_may_keep_peak_level(T):
    bp = good_blueprint()
    bp.update(intensity={"opening": "Severe", "peak": "Severe"}, shape="siege")
    assert plot_blueprint_checks(bp, T) == []


# ---------- who decides (FR-AU-3, FR-AU-4) ----------

@pytest.mark.parametrize("kind, expected", [
    ("core_pick", "author"), ("outcome", "author"), ("structure", "author"), ("cast_map", "author"),
    ("return_to_braindump", "agent_may_settle"), ("file_runner_up", "agent_may_settle"),
    ("kishotenketsu_send_back", "agent_may_settle"), ("send_to_pool", "agent_may_settle"),
    ("something_new", "author"),
])
def test_who_decides(T, kind, expected):
    assert who_decides(kind, T) == expected


# ---------- calibration (FR-DEV-8) ----------

def test_weights_come_from_the_tables(tmp_path):
    raw = yaml.safe_load(TABLES_PATH.read_text(encoding="utf-8"))
    raw["weights"]["conflict_fit"].update(source=4, maximum=30)
    p = tmp_path / "t.yaml"
    p.write_text(yaml.safe_dump(raw, allow_unicode=True), encoding="utf-8")
    t2 = load_tables(p)
    assert conflict_fit(3, 0, 0, 0, 0, t2) == 12


# ---------- next Ghost and provenance (FR-DEV-19, FR-DEV-23) ----------

def test_unmet_pillar_at_the_denouement_becomes_the_next_ghost(T):
    res = arc_checks([1, 2, 3], ["Protection", "Collapse"], "Bittersweet", T,
                     denouement_unmet=["[Protagonist] · Belonging: Unmet (Natural)"])
    assert res.next_ghost == ["[Protagonist] · Belonging: Unmet (Natural)"]
    assert res.actions == [("record_next_ghost", res.next_ghost)]
    assert who_decides("record_next_ghost", T) == "agent_may_settle"


def test_results_record_their_inputs(T):
    res = score_cores(ratings(T), ["Belonging"], T)
    assert res.inputs["implied_pillars"] == ["Belonging"]
    assert res.inputs["ratings"]["Internal"] == {"source": 1, "theme": 1, "genre": 1, "contradictions": 0}
    story = StoryProfile(outcome="Triumph", inevitability="Avoidable", novelty="Ordinary", temporal_root="Situational")
    sres = score_structures(story, all_ratings(T), T, FITS)
    assert sres.inputs["story"]["outcome"] == "Triumph" and sres.table_version == T.version
    assert all(row.sources["outcome"] == "code" and row.sources["cast_shape"] == "rater" and
               row.sources["novelty"] == "map" for row in sres.sheet)


def test_technology_flag_says_intensity_should_rise(T):
    msg = technology_fallback_flag([("[Town]", "Technology", "Unmet", "Technological")], natural_fallback=False)
    assert "Intensity should rise" in msg and "[Town]" in msg
