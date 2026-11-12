# Writing EOS

An internal application for writing a novel with a team of models. "EOS" stands for *ecosystem*: about 120 components, each with one job and its own best-fit model, with checks between them. The Author makes every final decision.

## Where it stands

This repository holds the **rule-keeping engine**, tested, and the documents it is built from. It does not yet send a prompt to a model or show a screen; that is the next stage of the build (see the fixes plan, Group D).

| Part | What it does |
|---|---|
| Order of work | Follows the *Narrative Components* database: what runs next, never before its inputs, never past a gate the Author has not approved |
| Model registry and router | Each component's line of experts (Primary, Comparable, Fallback), provider routes, the rule that a checker never judges its own model's work, and the mature-content rules |
| Readiness report | Which components could run today, what an outage would stop, what is still open |
| Story Blueprint formulas | Conflict Fit, Structure Fit and the gates of the Story Blueprint, as code |
| Humanize | Rewrites toward the pen name's voice with dialogue and locked lines protected |
| Shared library | Reads the Author's pools (characters, pen names, genres, themes and more) without changing them |
| Story Bible | The twelve elements and who owns each |

## Layout

```
eos-app/     the engine: eos_app/ (code), config/ (the app's copies of the databases), tests/
docs/        requirements and architecture, proposals, and the fixes implementation plan
roster/      the export of the model roster that config/models.yaml is built from
tools/       the publishing gate that runs before every push
```

## Run it

Python 3.11 or newer.

```bash
cd eos-app
pip install -r requirements.txt
python -m pytest                     # 260 tests; no network, no model calls
python -m eos_app.readiness          # what could run today, and what stands in the way
```

`eos-app/README.md` explains each part and the commands that rebuild the app's copies when a Notion database changes.

## What is not here, on purpose

This repository is public. The Author's own material stays on the Author's computer: the library pools, the bake-off harness with its test pack, worked examples from the Author's books, keys, and anything named as an answer key. `.gitignore` lists them, and `tools/check_public.py` refuses a push that carries any of it.

## Documents

- [Requirements and architecture](docs/WRITING_EOS_REQUIREMENTS_AND_ARCHITECTURE.md)
- [Fixes implementation plan](docs/FIXES_IMPLEMENTATION_PLAN_2026-11-11.md): what the November 2026 audit found, what has been corrected, and what waits on the Author
