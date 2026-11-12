"""The Story Bible's twelve elements (requirements §4.4, FR-SB-3, D26)."""

import pytest

from eos_app.library import load_map
from eos_app.story_bible import BibleError, check_bible, load_bible
from eos_app.workflow import load_components


@pytest.fixture(scope="module")
def B():
    return load_bible()


def test_the_structure_is_sound(B):
    assert check_bible(B, load_components(), load_map()) == []


def test_twelve_elements_in_the_standard_order(B):
    assert [e.title for e in B.elements] == [
        "Title and Logline", "Synopsis", "Characters", "Setting and World-Building", "Plot and Structure",
        "Themes and Symbolism", "Dialogue and Voice", "Visual References", "Timeline", "Research and References",
        "Glossary", "Appendices"]


def test_worldbuilding_is_part_of_the_bible_and_its_approach_is_the_authors(B):
    world = B.element("world")
    assert "10" in world.filled_by and "10.5" in world.filled_by          # Worldbuilding and World Check
    assert world.approach["proposed_by"] == "10" and world.approach["decided_by"] == "author"
    assert B.elements_filled_by("10") == ["Setting and World-Building", "Visual References"]


def test_the_existing_registers_live_inside_the_elements(B):
    held = {r for e in B.elements for r in e.registers}
    assert {"Characters", "Arc", "Relationships", "Secrets and knowledge", "Naming", "Style card", "World rules",
            "Locations", "Objects", "Plot threads", "Premise and Blueprints", "Creative Reserve"} <= held


def test_a_broken_structure_is_reported(B):
    from dataclasses import replace
    bad = replace(B, elements=[replace(B.elements[0], filled_by=["99.9"])] + B.elements[1:])
    assert "Title and Logline: unknown component 99.9" in check_bible(bad, load_components(), load_map())
    with pytest.raises(BibleError):
        B.element("nowhere")
