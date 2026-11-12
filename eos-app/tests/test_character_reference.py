"""The Author's character reference pools (2026-10-22): traits and strengths, flaws, animal natures, epithet words
and clothing, read from spreadsheets and a Word document with the standard library."""
import zipfile
from pathlib import Path

import pytest

from eos_app.library import (is_scaffolding, animal_traits, epithet_slots, import_folder, load_map, load_pool,
                             sections_about, source_path, synonyms, words, LibraryError)
from eos_app.office import OfficeError, read_docx, read_xlsx

VAULT = Path(__file__).parent / "fixtures" / "vault"
POOLS = ["character_traits", "character_flaws", "animal_natures", "epithet_words", "clothing"]


@pytest.fixture(scope="module")
def M():
    return load_map()


@pytest.fixture()
def lib(tmp_path, M):
    root = tmp_path / "library"
    for pool in POOLS:
        rep = import_folder(source_path(VAULT, M.pools[pool]), pool, root, M)
        assert rep.problems == [], (pool, rep.problems)          # binary files are not read as text
    return root


def test_every_reference_pool_loads_clean(lib, M):
    for pool in POOLS:
        p = load_pool(pool, lib, M)
        assert p.entries and p.problems == [], (pool, p.problems)


def test_traits_and_strengths_keep_their_kind(lib, M):
    p = load_pool("character_traits", lib, M)
    assert words(p, "trait") == ["Brave", "Curious", "Stubborn"]          # the sheet's header row is not a word
    assert words(p, "strength") == ["Adaptable", "Loyal"]


def test_flaws_carry_the_synonyms_the_author_listed(lib, M):
    p = load_pool("character_flaws", lib, M)
    assert words(p, "flaw") == ["Arrogant", "Cowardly", "Jealous"]
    assert synonyms(p, "arrogant") == ["Haughty", "Proud"]
    assert synonyms(p, "Cowardly") == []


def test_animal_natures_group_strengths_and_weaknesses(lib, M):
    p = load_pool("animal_natures", lib, M)
    assert [e.title for e in p.entries] == ["Lion", "Otter"]
    assert animal_traits(p, "otter") == {"strengths": ["Playful"], "weaknesses": ["Disorganised", "Easily Bored"]}
    with pytest.raises(LibraryError):
        animal_traits(p, "Owl")


def test_epithet_words_fill_three_slots(lib, M):
    slots = epithet_slots(load_pool("epithet_words", lib, M))
    assert slots == {"descriptor": ["crazed", "pale"], "noun": ["doctor", "tyrant"], "domain": ["of Death", "of the Stars"]}


def test_clothing_document_splits_into_sections_at_two_empty_paragraphs(lib, M):
    p = load_pool("clothing", lib, M)
    assert [e.title for e in p.entries] == ["Clothing can be grouped by setting.",
                                            "Layered garments can conceal what a character carries.",
                                            "Uniforms signal rank and belonging."]
    assert "Formal wear" in p.entries[0].body                             # a single empty paragraph stays inside
    assert [e.id for e in sections_about(p, "conceal", "secrets")] == ["CLOTH-02"]


def _xlsx(path, rows):
    S = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    cells = "".join(f'<row r="{n}">' + "".join(f'<c r="{chr(65 + i)}{n}" t="inlineStr"><is><t>{v}</t></is></c>'
                                               for i, v in enumerate(r) if v) + "</row>" for n, r in enumerate(rows, 1))
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("xl/workbook.xml", f'<workbook xmlns="{S}" xmlns:r="{R}"><sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels", f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/worksheet" Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr("xl/worksheets/sheet1.xml", f'<worksheet xmlns="{S}"><sheetData>{cells}</sheetData></worksheet>')


def test_inline_text_cells_are_read_and_blank_cells_left_out(tmp_path):
    f = tmp_path / "t.xlsx"
    _xlsx(f, [["Animal", "Strength"], ["", "Calm"]])
    assert read_xlsx(f) == {"Sheet1": [{"A": "Animal", "B": "Strength"}, {"B": "Calm"}]}


def test_a_repeated_word_and_an_unknown_synonym_row_are_problems(tmp_path, M):
    folder = tmp_path / "library" / M.pools["character_flaws"]["folder"]
    folder.mkdir(parents=True)
    S = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    def sheet(rows):
        return f'<worksheet xmlns="{S}"><sheetData>' + "".join(
            f'<row r="{n}">' + "".join(f'<c r="{chr(65 + i)}{n}" t="inlineStr"><is><t>{v}</t></is></c>' for i, v in enumerate(r) if v)
            + "</row>" for n, r in enumerate(rows, 1)) + "</sheetData></worksheet>"
    with zipfile.ZipFile(folder / "Character Flaws.xlsx", "w") as z:
        z.writestr("xl/workbook.xml", f'<workbook xmlns="{S}" xmlns:r="{R}"><sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/><sheet name="Sheet2" sheetId="2" r:id="rId2"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels", f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="{R}/worksheet" Target="worksheets/sheet2.xml"/></Relationships>')
        z.writestr("xl/worksheets/sheet1.xml", sheet([["Character Flaws"], ["Vain"], ["Vain"]]))
        z.writestr("xl/worksheets/sheet2.xml", sheet([["Petty", "Small", "Spiteful"]]))
    probs = load_pool("character_flaws", tmp_path / "library", M).problems
    assert any("Vain is listed twice" in p for p in probs)
    assert any("Petty has synonyms but isn't in the flaw list" in p for p in probs)


def test_a_file_that_is_not_an_office_file_is_refused(tmp_path):
    f = tmp_path / "not.xlsx"
    f.write_text("plain text", encoding="utf-8")
    with pytest.raises(OfficeError):
        read_xlsx(f)
    with pytest.raises(OfficeError):
        read_docx(f)


def test_the_knowledge_base_pools_are_scaffolding_and_the_others_are_not(M):
    assert all(is_scaffolding(p, M) for p in POOLS)
    assert not any(is_scaffolding(p, M) for p in M.pools if p not in POOLS)
