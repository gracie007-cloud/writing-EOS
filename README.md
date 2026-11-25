# Writing EOS

An internal application for writing a novel with a team of models. "EOS" stands for *ecosystem*: about 120 components, each with one job and its own best-fit model, with checks between them. The Author makes every final decision.

## Where it stands

This repository holds the **rule-keeping engine**, tested, and the documents it is built from. It builds the prompts of the first stretch of work and shows them on a page, but it does not yet send a prompt to a model: the **dry run** of that slice is done, and the first live run waits on the Author's word and a spending cap (fixes plan, D1).

| Part | What it does |
|---|---|
| Order of work | Follows the *Narrative Components* database: what runs next, never before its inputs, never past a gate the Author has not approved |
| Model registry and router | Each component's line of experts (Primary, Comparable, Fallback), provider routes, the rule that a checker never judges its own model's work, and the mature tier: 64 uncensored models on Featherless AI and OpenRouter, chosen by the book's pen name and subgenre (D33) |
| Readiness report | Which components could run today, what an outage would stop, what is still open |
| Story Blueprint formulas | Conflict Fit, Structure Fit and the gates of the Story Blueprint, as code |
| Dry run | Builds the prompts of Idea Intake through Story Pitch from their allowed inputs, picks their models, stops at the three gates, prices the run, and sends nothing |
| Humanize | Rewrites toward the pen name's voice with dialogue and locked lines protected |
| Shared library | Reads the Author's pools (characters, pen names, genres, themes and more) without changing them |
| Story Bible | The twelve elements and who owns each |

## Layout

```
eos-app/         the engine: eos_app/ (code), config/ (the app's copies of the databases), tests/
eos-bakeoff/     the bake-off harness that tests models on a step, with its test pack
canvas-source/   the front end: the design canvas's 19 boards, copied from the live canvas on 25 November 2026
experiments/     worked examples
docs/            requirements and architecture, proposals, reports and the fixes implementation plan
roster/          the export of the model roster LLM Identifier
llm-identifier-creative-writing-abliterated/   the mature catalog (Notion: Abliterated & Uncensored Models)
llm-identifier-creative-writing-open-weight/   the open-weight catalog (Notion: Open-Weight & Fine-Tuned Models)
llm-identifier-creative-writing-proprietary/   the proprietary catalog (Notion: Proprietary & Open/Near Frontier Models)
llm-identifier-creative-writing/               204 GGUF bases for later fine-tuning; not called by the app
llm-identifier-creative-writing-base-models/   the README for that catalog
registry.json, routing.json                    the model register and its pen name routing table (2026-11-14)
REGISTER.md, VERIFICATION.md                   the same register to read, and how it was verified
tools/           the gate that runs before every push
```

`eos-app/config/models.yaml` is built from the roster, the three catalogs and `registry.json`; the app reads
`routing.json` where it is. See `eos-app/README.md`, *Models and routing*.

## Run it

Python 3.11 or newer.

```bash
cd eos-app
pip install -r requirements.txt
python -m pytest                     # 284 tests; no network, no model calls
python -m eos_app.readiness          # what could run today, and what stands in the way
python -m eos_app.dryrun --help      # the first slice, built and priced, nothing sent

cd ../eos-bakeoff/eos-bakeoff
python -m pytest                     # the harness's own 74 tests
```

`eos-app/README.md` explains each part and the commands that rebuild the app's copies when a Notion database changes.

## Private, and what is still left out

This repository is **private** (since 2026-11-12): the harness, the worked examples and the canvas source name the Author's book. Three things are still never stored here: keys (`.env`), the real answer key, and the library pools, whose master copy is the Author's Obsidian vault.

`tools/check_public.py` runs before every push. It refuses keys and those paths, and it keeps the app itself generic: no name from the Author's library may appear in `eos-app/` or the requirements (decision D10). **Before this repository is ever made public again**, read the note at the top of that file.

## Documents

- [Requirements and architecture](docs/WRITING_EOS_REQUIREMENTS_AND_ARCHITECTURE.md)
- [Fixes implementation plan](docs/FIXES_IMPLEMENTATION_PLAN_2026-11-11.md): what the November 2026 audit found, what has been corrected, and what waits on the Author
