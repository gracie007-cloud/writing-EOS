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


def named(R, name, provider):
    return next(m for m in R.models if m.name == name and m.provider == provider)


def tier_models(R, RT):
    return [m for m in R.models if mature_ok(m, RT)]


GENRE = "Legal Thriller"          # a subgenre the catalogs tag mature-tier models for


def test_the_shipped_registry_is_exactly_what_the_tool_builds_from_the_sources():
    built = registry.build(ROSTER, MATURE, OPEN, PROPRIETARY)
    shipped = yaml.safe_load(registry.MODELS_PATH.read_text(encoding="utf-8"))
    assert built["models"] == shipped["models"] and built["problems"] == shipped["problems"]
    assert "registry.json" not in shipped["source"]       # the 2026-11-14 register is superseded (the Author, 2026-11-25)
    assert not any(m["register_id"] or m["served_context"] for m in shipped["models"])
    assert "pen_names" not in shipped["models"][0]                       # pen names stay outside the app (D10)


def test_every_catalog_model_is_uncensored_on_the_catalogs_provider(R, catalog):
    assert len(catalog) == 91                    # 89 + UnslopNemo and Venice on OpenRouter (2026-11-25)
    for row in catalog:
        rows = [m for m in R.models if m.provider == row["Provider"]
                and row["Provider Model ID"].casefold() in (m.model_id.casefold(), m.name.casefold())]
        assert rows and all(m.uncensored for m in rows), row["Model Name"]


def test_hugging_face_ggufs_are_fine_tune_bases_and_never_called(R, RT, W):
    bases = [m for m in R.models if m.fine_tune_base]
    assert len(bases) == 40 and {m.provider for m in bases} == {"Hugging Face"}
    assert all("fine-tune base" in unusable(m) for m in bases)
    assert not any(mature_ok(m, RT) for m in bases)


def test_mature_text_goes_only_to_an_inference_provider_or_an_aggregator(R, RT):
    tier = [m for m in R.models if mature_ok(m, RT)]
    assert {m.provider for m in tier} == {"Featherless AI", "OpenRouter"}
    local = [m for m in R.models if m.uncensored and m.provider == "Unsloth Desktop"]
    assert len(local) == 8 and not any(mature_ok(m, RT) for m in local)   # local is not in the tier (2026-11-25)


def test_prose_writers_come_from_the_catalogs_genre_tags_not_the_register(W, R, RT):
    draft = W.by_step["32"]
    tagged = {m.name for m in R.for_genre(GENRE)}
    got = [m.name for m in writer_models(draft, R, RT, genre=GENRE, pen_name="any pen name")]
    assert got[0] in tagged and not R.fits                               # no pen-name source until a correct one exists
    assert got.index("Claude Fable 5.1") > max(got.index(n) for n in got if n in tagged)   # experts stay behind


def test_mature_prose_uses_only_the_tier_never_the_stand_ins(W, R, RT):
    draft = W.by_step["32"]
    tier = writer_models(draft, R, RT, genre=GENRE, mature=True)
    assert tier and all(mature_ok(m, RT) for m in tier)
    assert "Claude Fable 5.1" not in {m.name for m in tier}
    assert all(GENRE in m.genres or any(GENRE in x.genres for x in R.routes(m)) for m in tier)


def test_venice_on_openrouter_and_featherless_are_both_used_as_one_model(W, R, RT):
    draft = W.by_step["32"]
    routes = [m for m in writer_models(draft, R, RT, genre="Legal Thriller", mature=True)
              if "venice-edition" in m.model_id.lower() and "GLM" not in m.name]
    assert [m.provider for m in routes] == ["Featherless AI", "OpenRouter"]     # the second route on an outage


def test_unslopnemo_on_openrouter_is_one_model_with_its_featherless_route(R, RT):
    orr = named(R, "TheDrummer: UnslopNemo 12B", "OpenRouter")
    fl = named(R, "TheDrummer/UnslopNemo-12B-v4.1", "Featherless AI")
    assert orr.ident == fl.ident and orr.model_id == "thedrummer/unslopnemo-12b"
    assert mature_ok(orr, RT) and mature_ok(fl, RT)
    assert not named(R, "TheDrummer/UnslopNemo-12B-v4", "Featherless AI").uncensored   # only v4.1 is in the tier


def test_a_text_component_with_no_mature_expert_hands_the_passage_to_the_tier(W, R, RT):
    edit = W.by_step["NEW-15"]                                          # Proofreader: general lane, text
    assert not any(mature_ok(m, RT) for _, m in experts(edit, R))
    with pytest.raises(RoutingError, match="give its subgenre"):
        writer_models(edit, R, RT, mature=True)
    picked = writer_models(edit, R, RT, genre=GENRE, mature=True)
    assert picked and all(mature_ok(m, RT) for m in picked)


def test_venice_uncensored_never_judges_text_its_own_model_wrote(W, R, RT):
    dolphin = named(R, "dphn/Dolphin-Mistral-24B-Venice-Edition", "Featherless AI")
    venice = named(R, "Venice Uncensored", "OpenRouter")
    assert venice.ident == dolphin.ident                                # one model, two routes (P8)
    cont = W.by_step["33"]
    refused = {m.key for _, m in experts(cont, R)}
    judge = choose_checker(cont, dolphin, R, RT, mature=True, refused=refused)
    assert judge.ident != dolphin.ident                                 # never Venice on either route
    assert judge.name == dolphin.comparable == "DavidAU/Dolphin-Mistral-GLM-4.7-Flash-24B-Venice-Edition-Thinking-Uncensored"


def test_the_catalogs_pair_each_model_with_a_comparable_and_a_fallback(R):
    haiku = named(R, "Claude Haiku 5.5", "Concentrate AI")
    assert haiku.fallback == "GPT-6 Luna"                               # the proprietary catalog (2026-11-25)
    # the Author's pairings of 2026-11-25: Kimi K3.1 is Kimi K3.1 Pro; Haiku's comparable is Nemotron Lightning 3.5
    assert named(R, "Gemini 4 Argon", "Concentrate AI").fallback == "Kimi K3.1 Pro"
    assert haiku.comparable == "Nemotron Lightning 3.5 30B A3B"
    assert named(R, "Kimi K3.1 Pro", "Concentrate AI").fallback == "Step 5 Preview"
    assert not any("names no model" in p for p in R.problems)


def test_the_corrected_qwen3_vl_row_is_the_32b_model_featherless_serves(R):
    row = named(R, "DavidAU/Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking", "Featherless AI")
    assert "Space Opera" in row.genres and row.uncensored
    assert not any("renamed" in p for p in R.problems)          # corrected in Notion (2026-11-25), nothing to rename


def test_readiness_sizes_the_mature_tier(W, R, RT):
    rep = report(W, R, RT)
    assert rep["mature_models"] == 62 and dict(rep["mature_tier"]) == {"Featherless AI": 62, "OpenRouter": 2}
    assert "Sonar Deep Research" not in {m.name for m in tier_models(R, RT)}       # not uncensored in Notion
    assert rep["fine_tune_bases"] == 40


def test_the_open_weight_catalog_adds_routes_and_ids_but_not_the_uncensored_mark(R):
    with open(OPEN, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 68
    cydonia = named(R, "TheDrummer:Cydonia-24b-v4.1", "Featherless AI")
    assert cydonia.model_id == "TheDrummer/Cydonia-24B-v4.1" and not cydonia.fine_tune_base
    assert named(R, "Chatterbox", "Featherless AI").model_id == "ResembleAI/chatterbox"   # an empty ID filled
    assert named(R, "Z-Image-Turbo Text to Image", "Comfy Cloud").modality == "Image"       # the roster names it now
    tiefighter = named(R, "KoboldAI/LLaMA2-13B-TiefighterLR", "Featherless AI")              # markup stripped
    assert not tiefighter.uncensored


def test_the_proprietary_catalog_adds_concentrate_routes_and_its_media_models(R):
    with open(PROPRIETARY, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 63                                       # + Nemotron Lightning 3.5 30B A3B (2026-11-25)
    for name in ("Claude Fable 5", "Claude Fable 5.2", "Gemini 4 Neon", "Kimi K3.1 Pro", "Qwen3.8 Omni Flash"):
        m = named(R, name, "Concentrate AI")
        assert m.frontier and not m.uncensored and m.genres
    omni = [m.provider for m in R.models if m.name == "Qwen3.8 Omni Flash"]
    assert sorted(omni) == ["Concentrate AI", "OpenRouter"]                       # a second route to one model
    assert named(R, "Fish Audio S2 Pro", "OpenRouter").model_id == "fish-audio/s2-pro"   # an empty ID filled
    assert not any("not added" in p for p in R.problems)                 # every media model is added (2026-11-25)
    assert named(R, "FLUX.2 Pro", "Comfy Cloud").modality == "Image"
