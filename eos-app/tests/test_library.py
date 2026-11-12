"""The shared library (requirements v0.15, FR-LIB, D20), built to the Author's real vault structure.
tests/fixtures/vault mirrors that structure with generic sample notes: character cards with A-K sections and
**field:** lines, subgenre rows that give pen names their style (including multi-entry YA notes), genre
definitions, writing topics, content levels, the conflict-to-structure map, arc entries and their template,
Home and Reference notes, and Archive folders that must be skipped."""

import shutil
from pathlib import Path

import pytest
import yaml

from eos_app.library import (MAP_PATH, Approval, LibraryError, PoolFirstError, body_fields, byline_collisions,
                             candidates_for_role, descriptor, unclassified, import_folder, load_map, load_pool,
                             may_create_character, parse_note, pen_names_for, pools_used_by, prompt_view,
                             write_character, pitches, doctrine, content_levels_for, reviewed, describe_levels,
                             book_needs_mature_tier, check_scene_levels, rank_structures, structure_map,
                             write_arc_entry, source_path, themes_for, theme_fit, term_matches,
                             unrecognised_terms, term_depth, theme_pair, theme_brief, book_theme,
                             profile_gaps, may_promote)
from eos_app.workflow import load_components

VAULT = Path(__file__).parent / "fixtures" / "vault"


@pytest.fixture(scope="module")
def M():
    return load_map()


@pytest.fixture()
def lib(tmp_path, M):
    root = tmp_path / "library"
    for pool, cfg in M.pools.items():
        import_folder(source_path(VAULT, cfg), pool, root, M)
    return root


# ---------- the map ----------

def test_thirteen_pools_named_as_in_the_vault(M):
    assert {c["title"] for c in M.pools.values()} == {
        "Character Pool", "Pen Names Pool", "Narrative Genres Pool", "Story Pitch Pool", "Content Levels",
        "Conflict and Structure Map", "Character Arc and Theme", "Themes in Literature",
        "Character Traits and Personal Strengths", "Character Flaws", "Animal Traits, Strengths and Weaknesses",
        "Character Building (epithet words)", "Character Building - Types of Clothing"}


def test_every_reader_and_writer_is_a_real_component(M):
    steps = load_components().by_step
    for cfg in M.pools.values():
        for st in cfg["read_by"] + cfg["written_by"]:
            assert st in steps, st


def test_pools_used_by_a_component(M):
    assert pools_used_by("6.5", M) == {"reads": ["Character Pool"], "writes": []}
    assert pools_used_by("CD-03b", M) == {"reads": ["Character Traits and Personal Strengths",
                                                    "Animal Traits, Strengths and Weaknesses"], "writes": []}
    assert pools_used_by("CD-11", M) == {"reads": ["Character Flaws"], "writes": ["Character Pool"]}
    assert pools_used_by("CD-10", M) == {"reads": ["Character Building - Types of Clothing"], "writes": []}
    assert "Character Building (epithet words)" not in pools_used_by("6.61", M)["reads"]   # no reader until the Author names one
    assert pools_used_by("3", M) == {"reads": ["Pen Names Pool", "Narrative Genres Pool", "Content Levels"], "writes": []}
    assert pools_used_by("32", M) == {"reads": ["Content Levels"], "writes": []}
    assert pools_used_by("14", M) == {"reads": ["Character Pool", "Conflict and Structure Map", "Themes in Literature"],
                                      "writes": []}                    # drafts the arc entry; the Story Bible finishes it
    assert pools_used_by("19", M)["writes"] == ["Character Arc and Theme"]
    assert "Character Pool" in pools_used_by("10", M)["reads"]          # Worldbuilding takes the pool's setting cards
    assert pools_used_by("13.4", M) == {"reads": [], "writes": []}   # arc entries wait for the structure
    assert pools_used_by("81", M) == {"reads": [], "writes": []}


# ---------- notes ----------

def test_parse_note():
    fm, body = parse_note("---\nname: A\n---\n# A\ntext")
    assert fm == {"name": "A"} and body.startswith("# A")
    assert parse_note("Just text.") == ({}, "Just text.")
    with pytest.raises(LibraryError, match="frontmatter"):
        parse_note("---\nname: [unclosed\n---\nbody")


def test_body_fields():
    f = body_fields("**name:** A\n\n**Best-Fit Tones:** Warm, Dry\n\nplain line\n**root_fear:**   change\n")
    assert f == {"name": "A", "Best-Fit Tones": "Warm, Dry", "root_fear": "change"}


# ---------- import ----------

def test_import_skips_archives_settings_and_non_notes(tmp_path, M):
    root = tmp_path / "library"
    rep = import_folder(VAULT / "Pen Names Pool", "pen_names", root, M)
    assert not any("Archive" in f for f in rep.imported)
    assert rep.skipped == []                                   # the zip folder is excluded before files are looked at
    assert "Sample Authors/sample-database-obsidian/Sample Database/Authors/Sample Pen.md" in rep.imported
    rep = import_folder(VAULT / "Character Pool", "characters", tmp_path / "library", M)
    assert not any(".obsidian" in f for f in rep.imported) and len(rep.imported) == 8


def test_import_is_byte_identical_and_safe_to_repeat(tmp_path, M):
    src = tmp_path / "vault"
    shutil.copytree(VAULT / "Narrative Genres Pool", src)
    root = tmp_path / "library"
    first = import_folder(src, "genres", root, M)
    note = "YA Genres/ya-list-obsidian/YA Minor Subgenres List/YA Minor Subgenres/Coastal Coming-of-Age.md"
    assert (root / "narrative-genres" / note).read_bytes() == (src / note).read_bytes()
    again = import_folder(src, "genres", root, M)
    assert again.imported == again.updated == again.conflicts == [] and len(again.unchanged) == len(first.imported)
    assert (root / "narrative-genres" / ".import-baseline.json").exists()


def test_a_note_fixed_in_the_vault_is_refreshed(tmp_path, M):
    """The Author repairs a note at the source and re-imports: the library copy follows."""
    src, root = tmp_path / "vault", tmp_path / "library"
    shutil.copytree(VAULT / "Narrative Genres Pool", src)
    import_folder(src, "genres", root, M)
    note = "YA Genres/ya-list-obsidian/YA Minor Subgenres List/YA Minor Subgenres/Coastal Coming-of-Age.md"
    (src / note).write_text((src / note).read_text(encoding="utf-8") + "\nFixed at the source.\n", encoding="utf-8")
    rep = import_folder(src, "genres", root, M)
    assert rep.updated == [note] and rep.conflicts == []
    assert "Fixed at the source." in (root / "narrative-genres" / note).read_text(encoding="utf-8")


def test_a_note_changed_in_both_places_is_left_for_the_author(tmp_path, M):
    src, root = tmp_path / "vault", tmp_path / "library"
    shutil.copytree(VAULT / "Narrative Genres Pool", src)
    import_folder(src, "genres", root, M)
    note = "YA Genres/ya-list-obsidian/YA Minor Subgenres List/YA Minor Subgenres/Coastal Coming-of-Age.md"
    held = root / "narrative-genres" / note
    held.write_text(held.read_text(encoding="utf-8") + "\nEdited in the library.\n", encoding="utf-8")
    (src / note).write_text((src / note).read_text(encoding="utf-8") + "\nEdited in the vault.\n", encoding="utf-8")
    assert import_folder(src, "genres", root, M).conflicts == [note]
    assert "Edited in the library." in held.read_text(encoding="utf-8")       # nothing overwritten silently
    assert import_folder(src, "genres", root, M, overwrite=True).updated == [note]
    assert "Edited in the vault." in held.read_text(encoding="utf-8")


def test_a_note_gone_from_the_vault_is_reported_not_deleted(tmp_path, M):
    src, root = tmp_path / "vault", tmp_path / "library"
    shutil.copytree(VAULT / "Character Pool", src)
    import_folder(src, "characters", root, M)
    old = "Character Pool/character-pool_v1/CHAR-003 Sample Draft.md"
    (src / old).rename(src / "Character Pool/character-pool_v1/CHAR-003 Sample Draft (renamed).md")
    write_character({"name": "Sample Newcomer", "role_in_story": "Ally", "one_line_concept": "Arrives."}, root, M,
                    approval=Approval(gate="G5", by="author"))
    rep = import_folder(src, "characters", root, M)
    assert rep.missing_in_vault == [old]                      # the app's own new/ folder is not counted
    assert (root / "characters" / old).exists()
    assert any("CHAR-003" in p and "two notes" in p for p in load_pool("characters", root, M).problems)


def test_unknown_pool_or_missing_folder_is_refused(tmp_path, M):
    with pytest.raises(LibraryError):
        import_folder(VAULT, "places", tmp_path, M)
    with pytest.raises(LibraryError):
        import_folder(tmp_path / "nowhere", "genres", tmp_path, M)


# ---------- Character Pool ----------

def test_character_cards(lib, M):
    pool = load_pool("characters", lib, M)
    assert sorted(pool.by_id) == ["CHAR-001", "CHAR-002", "CHAR-003", "CHAR-004", "CHAR-005", "CHAR-006"]
    assert pool.ignored == 2                                    # the Home note and the Reference note
    mentor = pool.by_id["CHAR-001"]
    assert mentor.title == "Sample Mentor"
    assert mentor.fields["one_line_concept"] == "A steady hand in a storm."      # from the card body
    assert mentor.fields["want_goal"] == "Keep the harbour safe."
    assert mentor.fields["role_in_story"] == "Mentor" and mentor.fields["animal_nature"].startswith("Heron")
    assert "fusion_sources" not in mentor.fields and "fusion_sources" in mentor.private
    assert mentor.sections["E. Motivation & Arc"].startswith("**want_goal:**")


def test_core_and_skin(lib, M):
    mentor = load_pool("characters", lib, M).by_id["CHAR-001"]
    assert {"role_in_story", "one_line_concept", "personality_core", "want_goal", "need_internal"} <= set(mentor.core())
    assert {"name", "cluster_universe", "appearance"} & set(mentor.skin()) >= {"name", "cluster_universe"}
    assert "name" not in mentor.core()


def test_incomplete_and_unknown_status_are_problems(lib, M):
    pool = load_pool("characters", lib, M)
    assert pool.by_id["CHAR-004"].missing == ["one_line_concept"]
    assert any("CHAR-004" in p and "one_line_concept" in p for p in pool.problems)
    note = lib / "characters" / "Character Pool" / "character-pool_v1" / "CHAR-007 Odd.md"
    note.write_text("---\ncharacter_id: CHAR-007\nname: Odd\nstatus: Maybe\nrole_in_story: Ally\n---\n"
                    "**one_line_concept:** Odd one.\n\n**status:** Reimagined\n", encoding="utf-8")
    pool = load_pool("characters", lib, M)
    (msg,) = [p for p in pool.problems if "CHAR-007" in p]
    assert "Maybe" in msg and "body says 'Reimagined'" in msg     # a shifted card is named, never guessed at
    assert not pool.by_id["CHAR-007"].offered_to("Project One")


@pytest.mark.parametrize("functions, project, expected", [
    (["Mentor"], "Project One", ["Sample Mentor"]),
    (["Hero"], "Project One", ["Sample Hero"]),                 # "Protagonist (harbour pilot)" fills Hero
    (["Shapeshifter"], "Project One", []),                      # the Rival is assigned to Project Two
    (["Shapeshifter"], "Project Two", ["Sample Rival"]),
    (["Ally"], "Project One", []),                              # the Fusion Draft and the incomplete sketch are never offered
])
def test_pool_match_candidates(lib, M, functions, project, expected):
    pool = load_pool("characters", lib, M)
    assert [e.title for e in candidates_for_role(pool, functions, project)] == expected


def test_free_text_roles_are_listed_and_can_follow_the_matches(lib, M):
    folder = lib / "characters" / "Character Pool" / "character-pool_v1"
    (folder / "CHAR-009 Sample Wanderer.md").write_text(
        "---\ncharacter_id: CHAR-009\nname: Sample Wanderer\nstatus: Reimagined\nrole_in_story: Wandering cartographer\n---\n"
        "**one_line_concept:** Maps what moves.\n", encoding="utf-8")
    pool = load_pool("characters", lib, M)
    assert [e.title for e in unclassified(pool)] == ["Sample Wanderer"]
    assert [e.title for e in candidates_for_role(pool, ["Mentor"], "Project One", include_unclassified=True)] == \
        ["Sample Mentor", "Sample Wanderer"]


def test_setting_cards_go_to_the_world_not_the_cast(lib, M):
    from eos_app.library import settings
    pool = load_pool("characters", lib, M)
    assert [e.title for e in settings(pool)] == ["Sample Harbour"]          # "Setting — a working harbour town"
    assert "Sample Harbour" not in [e.title for e in unclassified(pool)]
    assert "Sample Harbour" not in [e.title for e in candidates_for_role(pool, ["Ally", "Hero", "Mentor"], "Project One",
                                                                        include_unclassified=True)]


def test_pool_before_creation():
    with pytest.raises(PoolFirstError):
        may_create_character(pool_checked=False, fit_found=False)
    with pytest.raises(PoolFirstError):
        may_create_character(pool_checked=True, fit_found=True)
    assert may_create_character(pool_checked=True, fit_found=False) is True


def test_characters_sent_to_a_model_carry_no_private_fields(lib, M):
    view = prompt_view(load_pool("characters", lib, M).by_id["CHAR-001"], M)
    assert "fusion_sources" not in view and "reimagine_record" not in view and "tags" not in view
    assert view["name"] == "Sample Mentor"


# ---------- Pen Names Pool ----------

def test_pen_names_are_built_from_the_subgenre_rows(lib, M):
    pool = load_pool("pen_names", lib, M)
    assert set(pool.by_title) == {"Sample Pen", "Second Pen", "Quiet Pen"}
    sample = pool.by_title["Sample Pen"]
    assert sorted(r["minor_subgenre"] for r in sample.fields["rows"]) == ["Coastal Coming-of-Age", "Harbour Mystery", "Tidal Romance"]
    assert sample.id == "PEN-sample-pen"
    assert any("Quiet Pen" in p and "no subgenre rows" in p for p in pool.problems)
    assert not any("Home" in p for p in pool.problems)                    # a database's home page is not a pen name
    assert pool.by_title["Second Pen"].body.startswith("# Second Pen")     # its note sits outside an Authors folder


def test_multi_entry_notes_give_each_pen_name_its_own_row(lib, M):
    second = load_pool("pen_names", lib, M).by_title["Second Pen"]
    (row,) = second.fields["rows"]
    assert row["major_subgenre"] == "Adventure" and row["primary_genre"] == "YA"
    assert row["literary_style"] == "Author H fusion — brisk, bright prose"
    assert row["tones"] == "Playful, Hopeful"


@pytest.mark.parametrize("genre, expected", [("Mystery", ["Sample Pen"]), ("adventure", ["Second Pen"]),
                                              ("YA", ["Sample Pen", "Second Pen"]), ("Western", [])])
def test_pen_names_for_a_genre(lib, M, genre, expected):
    assert [p.title for p in pen_names_for(load_pool("pen_names", lib, M), genre)] == expected


@pytest.mark.parametrize("text, expected", [
    ("Author A & Author B fusion — spare, tense prose — short chapters", "spare, tense prose — short chapters"),
    ("Director C - naturalistic light, long takes", "naturalistic light, long takes"),
    ("Work D — fog over water; a single lamp", "fog over water; a single lamp"),
    ("plain description", "plain description"),
])
def test_descriptor(text, expected):
    assert descriptor(text) == expected


def test_models_get_style_descriptions_not_named_people(lib, M, tmp_path):
    view = prompt_view(load_pool("pen_names", lib, M).by_title["Sample Pen"], M)
    styles = " ".join(r["literary_style"] + r["cinematic_style"] + r["book_cover_style"] for r in view["rows"])
    assert "Author A" not in styles and "Director C" not in styles and "spare, tense prose" in styles
    raw = yaml.safe_load(MAP_PATH.read_text(encoding="utf-8"))
    raw["send_named_influences"] = True
    p = tmp_path / "map.yaml"
    p.write_text(yaml.safe_dump(raw, allow_unicode=True), encoding="utf-8")
    M2 = load_map(p)
    view2 = prompt_view(load_pool("pen_names", lib, M2).by_title["Sample Pen"], M2)
    assert any("Author A" in r["literary_style"] for r in view2["rows"])


def test_byline_collisions(lib, M):
    pen = load_pool("pen_names", lib, M).by_title["Sample Pen"]
    hits = byline_collisions(pen, load_pool("characters", lib, M))
    assert {h[0] for h in hits} == {"Sample Mentor", "Sample Rival", "Sample Draft", "Sample Sketch", "Sample Hero", "Sample Harbour"}
    assert {h[1] for h in hits} == {"sample"}


# ---------- Narrative Genres Pool ----------

def test_genre_definitions(lib, M):
    pool = load_pool("genres", lib, M)
    assert set(pool.by_title) == {"Harbour Mystery", "Coastal Coming-of-Age", "No Definition"}
    hm = pool.by_title["Harbour Mystery"]
    assert hm.id == "GEN-literary-fiction-harbour-mystery"
    assert hm.fields["definition"].startswith("Mysteries set in working harbours")
    assert hm.fields["concepts"] == ["Reasoning Concepts and Theories"]
    assert pool.ignored == 1                                    # the list note
    assert any("No Definition" in p and "definition" in p for p in pool.problems)


# ---------- writing back (gate G5 only) ----------

def test_write_character_needs_g5_and_lands_in_new(lib, M):
    new = {"name": "Sample Newcomer", "role_in_story": "Ally", "one_line_concept": "Arrives with the tide."}
    with pytest.raises(LibraryError, match="G5"):
        write_character(new, lib, M, approval=None)
    with pytest.raises(LibraryError, match="G5"):
        write_character(new, lib, M, approval=Approval(gate="G2", by="author"))
    path = write_character(new, lib, M, approval=Approval(gate="G5", by="author"))
    assert path.parent.name == "new"
    entry = load_pool("characters", lib, M).by_title["Sample Newcomer"]
    assert entry.id == "CHAR-007" and entry.fields["status"] == "Ready to Pull"
    with pytest.raises(LibraryError, match="already"):
        write_character(new, lib, M, approval=Approval(gate="G5", by="author"))
    with pytest.raises(LibraryError, match="one_line_concept"):
        write_character({"name": "Half", "role_in_story": "Ally"}, lib, M, approval=Approval(gate="G5", by="author"))


# ---------- Story Pitch Pool ----------

def test_writing_topics_split_into_pitches_and_doctrine(lib, M):
    pool = load_pool("story_pitches", lib, M)
    assert sorted(pool.by_title) == ["Half Idea", "Harbour Lights", "Tide Law"]
    assert pool.ignored == 2                                     # the Home note and the Pitch Type index
    assert [e.title for e in pitches(pool)] == ["Harbour Lights"]
    assert [e.title for e in doctrine(pool)] == ["Tide Law"]     # framework material goes to the Story Bible
    assert pool.by_title["Harbour Lights"].fields["premise"].endswith("a second light?")
    assert any("Half Idea" in p and "premise" in p for p in pool.problems)
    assert "notion_page" not in prompt_view(pool.by_title["Harbour Lights"], M)


# ---------- Content Levels ----------

def test_content_levels_are_read_and_zero_is_a_level(lib, M):
    pool = load_pool("content_levels", lib, M)
    assert pool.ignored == 1                                     # the Core index note
    with pytest.raises(LibraryError, match="2 genre paths"):     # same subgenre under Mystery and Thriller
        content_levels_for(pool, "harbour mystery")
    harbour = content_levels_for(pool, "harbour mystery", major="Mystery")
    assert content_levels_for(pool, "Harbour Mystery", major="Thriller").fields["violence"] == 3
    assert (harbour.fields["spice"], harbour.fields["violence"], harbour.fields["swearing"]) == (0, 1, 0)
    assert harbour.missing == [] and harbour.fields["authors"] == "Sample Pen"
    assert not reviewed(harbour)                                 # still the generated suggestion
    assert reviewed(content_levels_for(pool, "Tidal Romance"))
    assert any("Odd Level" in p and "spice" in p for p in pool.problems)
    assert content_levels_for(pool, "Odd Level") is None         # a broken level is never used as a ceiling
    assert content_levels_for(pool, "Ballad") is None            # no mapping: the Author sets levels at Story Setup
    assert describe_levels({"spice": 3}, M) == {"spice": "3 · sensual, closed door"}


def test_mature_tier_and_ceiling(lib, M):
    pool = load_pool("content_levels", lib, M)
    harbour = content_levels_for(pool, "Harbour Mystery", major="Mystery").fields
    tidal = content_levels_for(pool, "Tidal Romance").fields
    assert book_needs_mature_tier(tidal, M) and not book_needs_mature_tier(harbour, M)
    calm = check_scene_levels({"spice": 1, "violence": 1, "swearing": 0}, harbour, M)
    assert calm.tier == "standard" and calm.over_ceiling == [("spice", 1, 0)]
    hot = check_scene_levels({"spice": 4, "violence": 1}, tidal, M)
    assert hot.tier == "mature" and hot.mature_axes == ["spice"] and hot.over_ceiling == []


# ---------- Conflict and Structure Map ----------

def test_structures_ranked_core_first_then_modifiers(lib, M):
    pool = load_pool("conflict_map", lib, M)
    assert pool.ignored == 2                                     # the Axis index and the structure reverse index
    story = {"Conflict Core": "Internal", "Intensity": "Severe", "Inevitability": ["Avoidable"]}
    ranked = rank_structures(pool, story)
    assert [r.structure for r in ranked] == ["Spiral Sample", "Story Circle Sample", "Ladder Sample"]
    assert (ranked[0].core, ranked[0].best, ranked[0].situational) == ("best", 1, 1)
    assert ranked[2].core == "situational"


# ---------- Character Arc and Theme ----------

def test_arc_entries_skip_the_template(lib, M):
    pool = load_pool("arc_themes", lib, M)
    assert list(pool.by_title) == ["Sample Mentor"]
    assert pool.ignored == 2                                     # the blank template and the Home note


def test_write_arc_entry_needs_the_arc_gate(lib, M):
    entry = {"character_name": "Sample Hero", "theme": "Courage", "basic_information": "Adult pilot",
             "relationships": ["Sample Mentor"], "character_arc": "From doubt to command"}
    with pytest.raises(LibraryError, match="Story Bible lock"):
        write_arc_entry(entry, "Project One", lib, M, approval=None)
    path = write_arc_entry(entry, "Project One", lib, M, approval=Approval(gate="Story Bible lock", by="author"))
    assert path.parent.name == "Project One" and path.parent.parent.name == "new"
    text = path.read_text(encoding="utf-8")
    assert "## Theme in Literature\nCourage" in text and "- [[Sample Mentor]]" in text
    pool = load_pool("arc_themes", lib, M)
    assert pool.by_title["Sample Hero"].fields["theme"] == "Courage"
    with pytest.raises(LibraryError, match="already"):
        write_arc_entry(entry, "Project One", lib, M, approval=Approval(gate="Story Bible lock", by="author"))
    with pytest.raises(LibraryError, match="character_arc"):
        write_arc_entry({"character_name": "Half", "theme": "Duty"}, "Project One", lib, M,
                        approval=Approval(gate="Story Bible lock", by="author"))



def test_near_duplicate_names_within_a_primary_genre(lib, M):
    extra = lib / "narrative-genres" / "extra"
    extra.mkdir()
    note = '---\ntype: {t}\nprimary_genre: "{p}"\n---\n\n# {n}\n\n## Definition\nA sample.\n'
    (extra / "Harbour Mysteries.md").write_text(note.format(t="minor-subgenre", p="Literary Fiction", n="Harbour Mysteries"), encoding="utf-8")
    (extra / "Harbour-Mystery.md").write_text(note.format(t="ya-minor-subgenre", p="YA", n="Harbour-Mystery"), encoding="utf-8")
    problems = [p for p in load_pool("genres", lib, M).problems if "near-duplicate" in p]
    assert problems == ["near-duplicate names in Literary Fiction: Harbour Mysteries / Harbour Mystery; "
                        "keep one spelling in your vault"]       # the YA entry of the same name is its own genre


# ---------- Themes in Literature ----------

LF_MYSTERY = {"primary_genre": "Literary Fiction", "secondary_genre": "Contemporary Literary Fiction",
              "major_subgenre": "Mystery", "minor_subgenre": "Harbour Mystery"}
YA_MYSTERY = {"primary_genre": "YA", "secondary_genre": "Contemporary Literary Fiction",
              "major_subgenre": "Mystery", "minor_subgenre": "Coastal Coming-of-Age"}


def test_the_themes_spreadsheets_are_imported_and_read(lib, M):
    for name in M.pools["themes"]["tables"]:
        assert (lib / "themes" / Path(name).name).exists()            # named files land flat in the pool folder
    pool = load_pool("themes", lib, M)
    assert [e.title for e in pool.entries] == ["Action", "Belonging", "Loyalty", "Revenge", "Rivalry"]
    action = pool.by_title["Action"]
    assert action.id == "THEME-action" and action.fields["good_fit"] == ["Adventure", "Thriller"]
    assert pool.by_title["Belonging"].fields["not_ideal"] == []       # a lone dash means none
    assert action.fields["definition"] == "Stories driven by deeds."
    assert action.fields["complementary_theme"] == "Revenge"
    assert pool.problems == []


def test_genre_terms_follow_the_lists_shorthand(M):
    cfg = M.pools["themes"]
    assert term_matches("Contemporary", LF_MYSTERY, cfg)               # Contemporary Literary Fiction
    assert term_depth("Contemporary", LF_MYSTERY, cfg) == 2 and term_depth("Mystery", LF_MYSTERY, cfg) == 3
    assert term_depth("YA — Coming-of-Age", YA_MYSTERY, cfg) == 4
    assert term_matches("YA — Coming-of-Age", YA_MYSTERY, cfg)          # broad level and narrow name both match
    assert not term_matches("YA — Coming-of-Age", LF_MYSTERY, cfg)
    assert term_matches("Children's Literature (Picture Books)",
                        {"primary_genre": "Children's Literature", "minor_subgenre": "Picture Books"}, cfg)
    assert term_matches("Science Fiction — Dystopian", {"primary_genre": "Literary Fiction", "secondary_genre":
                        "Science Fiction", "major_subgenre": "Adventure", "minor_subgenre": "Dystopian Fiction"}, cfg)
    assert term_matches("Nonfiction", {"primary_genre": "Biography", "minor_subgenre": "Collective Biography"}, cfg)


def test_theme_suggestions_for_a_book(lib, M):
    pool = load_pool("themes", lib, M)
    fits = {f.theme: f.fit for f in themes_for(pool, LF_MYSTERY)}
    assert fits == {"Belonging": "good", "Loyalty": "good", "Action": "open", "Revenge": "open", "Rivalry": "mixed"}
    assert [f.theme for f in themes_for(pool, LF_MYSTERY)][:2] == ["Belonging", "Loyalty"]   # good fits first
    ya = {f.theme: f for f in themes_for(pool, YA_MYSTERY)}
    assert ya["Loyalty"].fit == "good"               # good for Mystery outweighs not ideal for YA: the more specific wins
    assert ("not_ideal", "YA") in ya["Loyalty"].reasons and ("good", "Mystery") in ya["Loyalty"].reasons
    picture = {"primary_genre": "Children's Literature", "minor_subgenre": "Picture Books"}
    assert theme_fit(pool.by_title["Action"], picture).fit == "not_ideal"


def test_unrecognised_genre_terms_are_listed(lib, M):
    out = unrecognised_terms(load_pool("themes", lib, M), load_pool("genres", lib, M))
    assert "Cyberwestern" in out and "Mystery" not in out and "Contemporary" not in out


def test_arc_entry_themes_come_from_the_list(lib, M):
    themes = load_pool("themes", lib, M)
    ok = Approval(gate="Story Bible lock", by="author")
    entry = {"character_name": "Sample Pilot", "theme": "belonging", "character_arc": "From outsider to crew"}
    path = write_arc_entry(entry, "Project One", lib, M, approval=ok, themes=themes)
    assert "theme: Belonging" in path.read_text(encoding="utf-8")     # written in the list's spelling
    with pytest.raises(LibraryError, match="Themes in Literature"):
        write_arc_entry({**entry, "character_name": "Sample Other", "theme": "Courage"}, "Project One", lib, M,
                        approval=ok, themes=themes)


def test_suggestions_carry_definitions_and_pairs(lib, M):
    pool = load_pool("themes", lib, M)
    belonging = next(f for f in themes_for(pool, LF_MYSTERY) if f.theme == "Belonging")
    assert belonging.definition == "The need to be part of a group."
    pair = theme_pair(pool, "belonging", LF_MYSTERY)
    assert (pair.partner, pair.intersection) == ("Loyalty", "Loyalty keeps the group whole.")
    assert pair.partner_fit.fit == "good"                              # the partner's own fit for this book
    assert theme_pair(pool, "Action", LF_MYSTERY).partner_fit.fit == "open"


def test_models_get_definitions_and_pairs_not_fit_lists(lib, M):
    brief = theme_brief(load_pool("themes", lib, M), ["Rivalry"], LF_MYSTERY)
    assert brief == [{"theme": "Rivalry", "type": "Canon", "definition": "Two people measured against each other.",
                      "pairs_with": "Loyalty", "how_they_intersect": "Rivals test each other's loyalties."}]


def test_the_three_spreadsheets_must_line_up(lib, M):
    folder = lib / "themes"
    defs = folder / "Theme in Literature - Themes in Literature List.csv"
    defs.write_text("Theme in Literature,Definitions,Theme Type\nAction,Deeds.,Motif\nBelonging,Group.,Canon\n"
                    "Loyalty,Faith.,Canon\nRevenge,Harm.,Canon\nCourage,Facing fear.,Canon\n", encoding="utf-8")
    comp = folder / "Theme in Literature - Complementary Theme.csv"
    comp.write_text(comp.read_text(encoding="utf-8-sig").replace("Rivalry,Loyalty", "Rivalry,Hope"), encoding="utf-8")
    problems = load_pool("themes", lib, M).problems
    assert "Theme in Literature - Themes in Literature List.csv: Courage isn't in " \
           "Theme in Literature - Literary Genres and Theme.csv" in problems
    assert "Theme in Literature - Themes in Literature List.csv: has no row for Rivalry" in problems
    assert "Rivalry: missing definition, theme_type" in problems
    assert "Rivalry: its complementary theme 'Hope' isn't in the list" in problems


def test_themes_are_canon_or_motif(lib, M):
    pool = load_pool("themes", lib, M)
    assert pool.by_title["Action"].fields["theme_type"] == "Motif"
    assert [f.theme for f in themes_for(pool, LF_MYSTERY, theme_type="Canon")] == ["Belonging", "Loyalty", "Rivalry", "Revenge"]
    defs = lib / "themes" / "Theme in Literature - Themes in Literature List.csv"
    defs.write_text(defs.read_text(encoding="utf-8-sig").replace("Rivalry,Two people measured against each other.,Canon",
                                                                 "Rivalry,Two people measured against each other.,Major"), encoding="utf-8")
    assert "Rivalry: theme type 'Major' is not one of Canon, Motif" in load_pool("themes", lib, M).problems


def test_the_books_theme_must_be_canon(lib, M):
    pool = load_pool("themes", lib, M)
    assert book_theme(pool, "belonging", LF_MYSTERY).fit == "good"
    with pytest.raises(LibraryError, match="Motif theme; the book's theme must be a Canon theme"):
        book_theme(pool, "Action", LF_MYSTERY)


def test_a_lead_characters_arc_carries_a_canon_theme(lib, M):
    themes = load_pool("themes", lib, M)
    ok = Approval(gate="Story Bible lock", by="author")
    entry = {"character_name": "Sample Lead", "theme": "Action", "character_arc": "From flight to stand"}
    with pytest.raises(LibraryError, match="lead character's arc carries a Canon theme"):
        write_arc_entry(entry, "Project One", lib, M, approval=ok, themes=themes, lead=True)
    assert write_arc_entry({**entry, "character_name": "Sample Support"}, "Project One", lib, M, approval=ok,
                           themes=themes).exists()                    # a supporting arc may carry a Motif


def test_a_pool_card_is_a_launchpad_not_the_final_profile(lib, M):
    card = load_pool("characters", lib, M).by_id["CHAR-001"].fields
    gaps = profile_gaps(card, M)
    assert gaps["age"] == "CD-09" and gaps["ghost"] == "CD-03a"      # each gap names the stage that owes it
    with pytest.raises(LibraryError, match="isn't complete yet"):
        may_promote(card, M)
    developed = {k: "filled" for k in M.pools["characters"]["profile_required"]}
    assert profile_gaps(developed, M) == {} and may_promote(developed, M)



def test_what_the_author_left_open_is_never_filled():
    from eos_app.library import settled_open
    card = {"open_questions_/_notes": "The deputy is uncast. THE ORIGIN IS SETTLED-OPEN BY DESIGN: it stays unexplained. "
                                      "The accent is open."}
    assert settled_open(card) == ["THE ORIGIN IS SETTLED-OPEN BY DESIGN: it stays unexplained."]
    assert settled_open({"name": "Sample"}) == []


def test_adaptation_regenerates_the_skin(lib, M):
    from eos_app.library import skin_carried_over
    card = load_pool("characters", lib, M).by_id["CHAR-001"].fields
    developed = {k: "filled" for k in M.pools["characters"]["profile_required"]}
    developed |= {"cluster_universe": card["cluster_universe"], "recurring_motif": "A ship's bell"}
    assert skin_carried_over(developed, card, M) == ["cluster_universe"]
    with pytest.raises(LibraryError, match="Skin hasn't been regenerated"):
        may_promote(developed, M, card=card)
    assert may_promote(developed, M, card=card, kept=["cluster_universe"])      # kept with the Author's approval


def test_an_uncast_relationship_sends_the_role_to_pool_match(lib, M):
    ok = Approval(gate="Story Bible lock", by="author")
    entry = {"character_name": "Sample Keeper", "theme": "Duty", "character_arc": "From holding on to handing over",
             "relationships": ["[[Sample Mentor]]", "A deputy, not yet cast"]}
    from eos_app.library import uncast_roles
    assert uncast_roles(entry["relationships"], lib, M) == ["A deputy, not yet cast"]   # R6: back to Pool Match
    with pytest.raises(LibraryError, match="Character Pool Match"):
        write_arc_entry(entry, "Project One", lib, M, approval=ok)
    entry["relationships"] = ["[[Sample Mentor]]", "[[Sample Hero|the deputy]]"]
    assert write_arc_entry(entry, "Project One", lib, M, approval=ok).exists()


# ---------- Story Bible elements from the themes workbook ----------

def test_the_workbook_is_read_from_its_folder(tmp_path, M):
    rep = import_folder(source_path(VAULT, M.pools["themes"]), "themes", tmp_path, M)
    assert len(rep.imported) == len(M.pools["themes"]["tables"]) and rep.problems == []


def test_a_named_file_in_a_hidden_data_folder_is_read(tmp_path, M):
    hidden = tmp_path / "vault" / ".plugin-data"
    hidden.mkdir(parents=True)
    names = list(M.pools["themes"]["tables"])
    folder = VAULT / M.pools["themes"]["source_folder"]
    for n in names:
        (hidden / n).write_bytes((folder / n).read_bytes())
    (hidden / "cache.mdc").write_text("plugin cache", encoding="utf-8")
    rep = import_folder([hidden / n for n in names], "themes", tmp_path / "library", M)
    assert len(rep.imported) == len(names) and not any("cache" in f for f in rep.imported)
    assert not (tmp_path / "library" / "themes" / ".plugin-data").exists()       # named files land flat


def test_every_sheet_joins_the_same_themes(lib, M):
    pool = load_pool("themes", lib, M)
    assert pool.problems == []
    action = pool.by_title["Action"].fields
    assert action["world_merps"]["Military"] == "Action: military"
    assert action["colours"]["Hexadecimal Code #8"] == "#FF0000"
    assert action["structure_good"] == ["Fichtean Curve", "Three-Act Structure"]


def test_worldbuilding_works_under_the_approved_approach(lib, M):
    from eos_app.library import world_approaches, world_brief
    pool = load_pool("themes", lib, M)
    assert world_approaches(M) == ["Components", "G.R.A.P.E.S.", "M.E.R.P.S."]
    brief = world_brief(pool, ["Belonging", "Rivalry"], "Components", M)
    assert brief["aspects"]["Movement and Travel"] == [("Belonging", "Belonging: movement and travel"),
                                                       ("Rivalry", "Rivalry: movement and travel")]
    assert set(brief["layout"]) == {"Physical Environment", "Social Structure", "Economic Systems",
                                    "Technology and Magic", "Culture and Beliefs", "History and Lore"}
    with pytest.raises(LibraryError, match="not a worldbuilding approach"):
        world_brief(pool, ["Belonging"], "Hexagon", M)


def test_theme_structure_fit_is_shown_beside_the_scores(lib, M):
    from eos_app.library import theme_structure_fit, unknown_structures
    pool = load_pool("themes", lib, M)
    fit = theme_structure_fit(pool, ["Action", "Belonging"], ["Fichtean Curve", "Save the Cat", "Kishōtenketsu", "Story Grid"])
    assert fit["Fichtean Curve"] == [("Action", "good"), ("Belonging", "not_ideal")]
    assert fit["Save the Cat"] == [("Action", "situational"), ("Belonging", "open")]
    assert fit["Kishōtenketsu"][0] == ("Action", "not_ideal") and fit["Story Grid"][0] == ("Action", "open")
    from eos_app.blueprint import load_tables
    assert unknown_structures(pool, load_tables().structures) == ["Cloud Structure"]


def test_voice_colour_and_timeline_rows(lib, M):
    from eos_app.library import theme_aspects
    pool = load_pool("themes", lib, M)
    assert theme_aspects(pool, "loyalty", "dialogue_voice")["Narrative Voice"] == "Loyalty: narrative voice"
    assert theme_aspects(pool, "Revenge", "timeline")["Flashbacks"] == "Revenge: flashbacks"
    assert theme_aspects(pool, "Action", "colours")["Complementary Colors"] == "Red & Aqua"

