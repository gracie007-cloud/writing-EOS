"""The mature tier (P10, D33): the Abliterated & Uncensored Models catalog, the 2026-11-14 register and its routing
table, joined with the roster; mature text only on an inference provider or aggregator; fine-tune bases never called.
Pen names are taken from routing.json at run time, never written here (D10)."""
import csv
import json
from pathlib import Path

import pytest
import yaml

from eos_app import registry
from eos_app.readiness import report
from eos_app.registry import load_models
from eos_app.router import (RoutingError, choose_checker, experts, load_routing, mature_ok, unusable,
                            writer_models)
from eos_app.workflow import load_components

ROOT = Path(__file__).resolve().parents[2]
ROSTER = ROOT / "roster" / "LLM Identifier export.csv"
MATURE = ROOT / "llm-identifier-creative-writing-abliterated" / "abliterated_models.csv"
REGISTER, ROUTING = ROOT / "registry.json", ROOT / "routing.json"
OPEN = ROOT / "llm-identifier-creative-writing-open-weight" / "open_weight_models.csv"
PROPRIETARY = ROOT / "llm-identifier-creative-writing-proprietary" / "proprietary_models.csv"


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
def catalog():
    with open(MATURE, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def table():
    return json.loads(ROUTING.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ids():
    return {w["id"]: w["hf_repo"] for w in json.loads(REGISTER.read_text(encoding="utf-8"))["models"]}


def named(R, name, provider):
    return next(m for m in R.models if m.name == name and m.provider == provider)


def subgenre(row):
    return row["minor_subgenre"] or row["major_subgenre"]


def mature_led_row(table, ids, R, RT):
    """A routing-table row whose first lead writer is in the mature tier: its pen name, subgenre and that model."""
    tier = {m.name for m in R.models if mature_ok(m, RT)}
    row = next(r for r in table if r["lead_writer"] and ids[r["lead_writer"][0]["model"]] in tier)
    return row["pen_name"], subgenre(row), ids[row["lead_writer"][0]["model"]]


def test_the_shipped_registry_is_exactly_what_the_tool_builds_from_the_sources():
    built = registry.build(ROSTER, MATURE, REGISTER, OPEN, PROPRIETARY)
    shipped = yaml.safe_load(registry.MODELS_PATH.read_text(encoding="utf-8"))
    assert built["models"] == shipped["models"] and built["problems"] == shipped["problems"]
    assert len(registry.load_fits()) == 538                              # one per Genre Matrix row with a model
    assert "pen_names" not in shipped["models"][0]                       # pen names stay outside the app (D10)


def test_every_catalog_model_is_uncensored_on_the_catalogs_provider(R, catalog):
    assert len(catalog) == 91                    # 89 + UnslopNemo and Venice on OpenRouter (2026-11-25)
    for row in catalog:
        rows = [m for m in R.models if m.provider == row["Provider"]
                and row["Provider Model ID"].casefold() in (m.model_id.casefold(), m.name.casefold())]
        assert rows and all(m.uncensored for m in rows), row["Model Name"]


def test_hugging_face_ggufs_are_fine_tune_bases_and_never_called(R, RT, W):
    bases = [m for m in R.models if m.fine_tune_base]
    assert len(bases) == 42 and {m.provider for m in bases} == {"Hugging Face"}
    assert all("fine-tune base" in unusable(m) for m in bases)
    assert not any(mature_ok(m, RT) for m in bases)


def test_mature_text_goes_only_to_an_inference_provider_or_an_aggregator(R, RT):
    tier = [m for m in R.models if mature_ok(m, RT)]
    assert {m.provider for m in tier} == {"Featherless AI", "OpenRouter"}
    local = [m for m in R.models if m.uncensored and m.provider == "Unsloth Desktop"]
    assert len(local) == 8 and not any(mature_ok(m, RT) for m in local)   # local is not in the tier (2026-11-25)


def test_the_registers_writers_for_the_pen_name_lead_in_its_order(W, R, RT, table, ids):
    draft = W.by_step["32"]
    rows = [r for r in table if len(r["lead_writer"]) > 2]
    pen, genre = rows[0]["pen_name"], subgenre(rows[0])
    leads = [ids[x["model"]] for r in table if r["pen_name"] == pen and subgenre(r) == genre for x in r["lead_writer"]]
    got = [m.name for m in writer_models(draft, R, RT, genre=genre, pen_name=pen)]
    assert [n for n in got if n in leads] == list(dict.fromkeys(leads))  # the register's order, routes beside each
    assert got.index(leads[-1]) < got.index("Claude Fable 5.1")         # the component's experts stay behind


def test_mature_prose_uses_only_the_tier_never_the_stand_ins(W, R, RT, table, ids):
    draft = W.by_step["32"]
    pen, genre, lead = mature_led_row(table, ids, R, RT)
    tier = writer_models(draft, R, RT, genre=genre, pen_name=pen, mature=True)
    assert tier and all(mature_ok(m, RT) for m in tier)
    assert "Claude Fable 5.1" not in {m.name for m in tier}
    assert tier[0].name == lead                                          # the register's first lead writer


def test_venice_on_openrouter_and_featherless_are_both_used_as_one_model(W, R, RT):
    draft = W.by_step["32"]
    routes = [m for m in writer_models(draft, R, RT, genre="Legal Thriller", mature=True)
              if "venice-edition" in m.model_id.lower() and "GLM" not in m.name]
    assert [m.provider for m in routes] == ["Featherless AI", "OpenRouter"]     # the second route on an outage


def test_unslopnemo_on_openrouter_is_one_model_with_its_featherless_route(R, RT):
    orr = named(R, "TheDrummer: UnslopNemo 12B", "OpenRouter")
    fl = named(R, "TheDrummer/UnslopNemo-12B-v4.1", "Featherless AI")
    assert orr.ident == fl.ident and orr.model_id == "thedrummer/unslopnemo-12b"
    assert mature_ok(orr, RT) and mature_ok(fl, RT) and fl.served_context == 32768
    assert not named(R, "TheDrummer/UnslopNemo-12B-v4", "Featherless AI").uncensored   # only v4.1 is in the tier


def test_a_text_component_with_no_mature_expert_hands_the_passage_to_the_tier(W, R, RT, table, ids):
    edit = W.by_step["NEW-15"]                                          # Proofreader: general lane, text
    assert not any(mature_ok(m, RT) for _, m in experts(edit, R))
    with pytest.raises(RoutingError, match="give its subgenre"):
        writer_models(edit, R, RT, mature=True)
    pen, genre, lead = mature_led_row(table, ids, R, RT)
    picked = writer_models(edit, R, RT, genre=genre, pen_name=pen, mature=True)
    assert picked[0].name == lead and all(mature_ok(m, RT) for m in picked)


def test_venice_uncensored_never_judges_text_its_own_model_wrote(W, R, RT):
    dolphin = named(R, "dphn/Dolphin-Mistral-24B-Venice-Edition", "Featherless AI")
    venice = named(R, "Venice Uncensored", "OpenRouter")
    assert venice.ident == dolphin.ident                                # one model, two routes (P8)
    cont = W.by_step["33"]
    refused = {m.key for _, m in experts(cont, R)}
    with pytest.raises(RoutingError, match="Venice Uncensored wrote the text"):
        choose_checker(cont, dolphin, R, RT, mature=True, refused=refused)


def test_a_mistyped_roster_row_takes_the_name_the_newer_sources_give_it(R):
    row = named(R, "DavidAU/Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking", "Featherless AI")
    assert row.register_id == "W41" and "Space Opera" in row.genres
    assert any("Qwen3-VL-12B-Thinking-Brainstorm20x-NEO-MAX-GGUF" in p and "renamed" in p for p in R.problems)


def test_readiness_sizes_the_mature_tier(W, R, RT):
    rep = report(W, R, RT)
    # Sonar Deep Research joins (roster ticks it uncensored; the proprietary catalog gave it genres)
    assert rep["mature_models"] == 64 and dict(rep["mature_tier"]) == {"Featherless AI": 63, "OpenRouter": 3}
    assert rep["fine_tune_bases"] == 42


def test_the_open_weight_catalog_adds_routes_and_ids_but_not_the_uncensored_mark(R):
    with open(OPEN, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 68
    cydonia = named(R, "TheDrummer:Cydonia-24b-v4.1", "Featherless AI")
    assert cydonia.model_id == "TheDrummer/Cydonia-24B-v4.1" and not cydonia.fine_tune_base
    assert named(R, "Chatterbox", "Featherless AI").model_id == "ResembleAI/chatterbox"   # an empty ID filled
    assert any("Z-Image-Turbo Text to Image" in p and "not added" in p for p in R.problems)  # media: reported only
    tiefighter = named(R, "KoboldAI/LLaMA2-13B-TiefighterLR", "Featherless AI")              # markup stripped
    assert not tiefighter.uncensored


def test_the_proprietary_catalog_adds_concentrate_routes_and_reports_unmatched_media(R):
    with open(PROPRIETARY, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 62
    for name in ("Claude Fable 5", "Claude Fable 5.2", "Gemini 4 Neon", "Kimi K3.1 Pro", "Qwen3.8 Omni Flash"):
        m = named(R, name, "Concentrate AI")
        assert m.frontier and not m.uncensored and m.genres
    omni = [m.provider for m in R.models if m.name == "Qwen3.8 Omni Flash"]
    assert sorted(omni) == ["Concentrate AI", "OpenRouter"]                       # a second route to one model
    assert named(R, "Fish Audio S2 Pro", "OpenRouter").model_id == "fish-audio/s2-pro"   # an empty ID filled
    assert sum("proprietary catalog" in p and "not added" in p for p in R.problems) == 14  # media: reported only
