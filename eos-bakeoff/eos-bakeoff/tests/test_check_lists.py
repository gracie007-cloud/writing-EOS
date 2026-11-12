"""Audit fixes B1 and B2: the check lists are split into generic and test-pack files, and the test
pack's own table agrees with steps.yaml. No network.
"""

import re

import pytest
import yaml

from eos_bakeoff.config import (CONFIG_DIR, DATA_DIR, TEST_PACK, TEST_PACK_RULES, ConfigError, load_all,
                                load_prose_checks)

GENERIC_KEYS = {"stock_phrases", "injury_vocabulary_limit"}
TEST_PACK_KEYS = {"pov_character", "auto_fail_terms", "victim_names_in_pov_speech", "pov_emotion_words",
                  "dignity_required"}


def read(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# ---------- B1: generic lists apart from one book's rules ----------

def test_slop_config_holds_only_generic_lists():
    assert set(read(CONFIG_DIR / "slop.yaml")) <= GENERIC_KEYS


def test_slop_config_names_nothing_from_the_test_pack():
    slop_text = (CONFIG_DIR / "slop.yaml").read_text(encoding="utf-8").casefold()
    rules = read(TEST_PACK_RULES)
    terms = [rules["pov_character"]] + [t for k, v in rules.items() if isinstance(v, list) for t in v]
    leaked = [t for t in terms if re.search(r"\b" + re.escape(t.casefold()) + r"\b", slop_text)]
    assert leaked == []


def test_test_pack_rules_live_beside_the_test_pack():
    assert TEST_PACK_RULES.parent == DATA_DIR
    assert set(read(TEST_PACK_RULES)) <= TEST_PACK_KEYS


def test_prose_checks_merge_both_files():
    checks = load_prose_checks()
    slop, rules = read(CONFIG_DIR / "slop.yaml"), read(TEST_PACK_RULES)
    assert checks["stock_phrases"] == slop["stock_phrases"]
    assert checks["auto_fail_terms"] == rules["auto_fail_terms"]
    assert checks["pov_character"] == rules["pov_character"]


def test_test_pack_rules_may_not_redefine_generic_lists(tmp_path):
    slop = tmp_path / "slop.yaml"
    slop.write_text("stock_phrases: [\"delve\"]\n", encoding="utf-8")
    rules = tmp_path / "rules.yaml"
    rules.write_text("stock_phrases: [\"something else\"]\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="stock_phrases"):
        load_prose_checks(slop, rules)


def test_generic_file_may_not_hold_book_rules(tmp_path):
    slop = tmp_path / "slop.yaml"
    slop.write_text("auto_fail_terms: [\"x\"]\n", encoding="utf-8")
    rules = tmp_path / "rules.yaml"
    rules.write_text("pov_character: X\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="auto_fail_terms"):
        load_prose_checks(slop, rules)


def test_prose_checks_refuse_an_answer_key_path(tmp_path):
    slop = tmp_path / "slop.yaml"
    slop.write_text("stock_phrases: []\n", encoding="utf-8")
    key = tmp_path / "Run01_ANSWER_KEY.yaml"
    key.write_text("pov_character: X\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="answer key"):
        load_prose_checks(slop, key)


# ---------- B2: the test pack's table matches steps.yaml ----------

def table_rows():
    head = TEST_PACK.read_text(encoding="utf-8").split("\n## A ·", 1)[0]
    rows = {}
    for line in head.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[0] and not set(cells[0]) <= set("-"):
            rows[cells[0]] = re.findall(r"\b([A-E])\b", cells[1])
    return rows


def test_general_prose_row_never_lists_the_mature_brief():
    rows = table_rows()
    general = [v for k, v in rows.items() if k.startswith("Prose Generation")]
    assert general and all("D" not in v for v in general)


def test_table_rows_match_steps_yaml():
    steps = load_all()[1]
    rows = table_rows()
    prose = next(v for k, v in rows.items() if k.startswith("Prose Generation"))
    mature = next(v for k, v in rows.items() if k.startswith("Mature Tier"))
    assert prose == list(steps["first_draft"].sections)
    assert mature == list(steps["first_draft_mature"].sections)
