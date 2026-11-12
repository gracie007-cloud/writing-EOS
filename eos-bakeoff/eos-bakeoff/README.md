# Writing EOS · Bake-off Harness (Starter Kit)

This folder is a **specification**, not finished code. Claude Code builds the harness from it.

## Before You Start (one time)
1. **Python 3.11 or newer.** Check with `python --version` in a terminal.
2. **Put this folder somewhere outside OneDrive and outside your Obsidian vault**, for example `C:\Users\soray\Projects\eos-bakeoff`. Code folders and cloud sync do not mix well.
3. **Create a file named `.env`** in this folder containing:
   ```
   OPENROUTER_API_KEY=your-key-here
   HF_TOKEN=your-hugging-face-token
   HF_ENDPOINT_CUSTOM=
   HF_ENDPOINT_BASELINE=
   ```
   Never share or upload this file.
4. **Verify model IDs.** Open `config/models.yaml`. Every `id` starts with `VERIFY:`. Look each model up on openrouter.ai/models, replace the placeholder with the exact slug, and fill in the prices. If a model is not available, delete its entry.
5. **Keep the answer key out of this folder for now.** `Run01_TestPack_ANSWER_KEY.md` is added in Phase 2, when the scorer exists.

## Building With Claude Code
Open a terminal in this folder, start Claude Code, and give it this first instruction:

> Read CLAUDE.md and docs/SPEC.md. Build Phase 1 only. Before writing code, show me your plan in plain language and wait for my approval. When Phase 1 works, run its acceptance test using the cheapest model in config/models.yaml with one run, and show me the output file and the run record.

Then, one phase at a time:

> Build Phase 2 as described in docs/SPEC.md. I have put the answer key in data/. Write the tests first, then the scorers.

> Build Phase 3.

> Build Phase 4.

## Phase 1 · Built 2026-10-17
Before the first real call: put `OPENROUTER_API_KEY=your-key` in a file named `.env` next to this README, and replace the `VERIFY:` placeholder for at least one model in `config/models.yaml`.
```
python -m eos_bakeoff estimate --step first_draft                       # cost before sending (sends nothing)
python -m eos_bakeoff run --step first_draft --models gemini4 --runs 1  # Phase 1 acceptance test
python -m pytest                                                        # automatic checks, no network
```
Outputs land in `runs/<date>/<step>/` under blind IDs; one line per call in `runs/<date>/runs.jsonl`; `BLIND_MAP.json` stays closed until scoring.

## First Real Round (after Phase 3)
```
python -m eos_bakeoff estimate --step first_draft
python -m eos_bakeoff run --step first_draft
python -m eos_bakeoff sheet --step first_draft
```
Score the review sheet **without opening BLIND_MAP.json**, then:
```
python -m eos_bakeoff score --step first_draft --import
python -m eos_bakeoff report
```

## Files
| File | Purpose |
|---|---|
| `CLAUDE.md` | Rules Claude Code follows in this project |
| `docs/SPEC.md` | What to build, phase by phase, with acceptance criteria |
| `config/models.yaml` | Candidate models (verify before use) |
| `config/steps.yaml` | Which steps, which sections, which scoring |
| `config/slop.yaml` | Generic slop phrase lists (true of any book) |
| `data/Run01_rules.yaml` | This test pack's own auto-fail rules (its characters and planted terms) |
| `prompts/` | Prompt templates, reusable by the future app |
| `data/Run01_TestPack.md` | The model-facing test pack |

## Phase 2 · Built 2026-10-17 · Automatic scoring

**The answer key.** The scorer reads `data/Run01_ANSWER_KEY.yaml`, a YAML version of the Notion answer key
(SPEC §2 names a `.md` key; the scorer needs the answers in fields, so this file replaces it).

1. Copy `docs/answer_key_template.yaml` to `data/Run01_ANSWER_KEY.yaml`.
2. Replace every `FILL IN` with the answers from Notion. The comments in the template explain each field.
3. The file name is git-ignored and refused by the prompt builder. Only `eos_bakeoff/scoring.py` reads it,
   and its error messages name fields, never answers.

**Scoring a step.**

```
python -m eos_bakeoff score --step character_selector
python -m eos_bakeoff score --step worldbuilding_selector
python -m eos_bakeoff score --step chronology_check
python -m eos_bakeoff score --step chronology_check --import
```

- Selectors (SPEC §4.1): 10 points, −2 per expected name missing, −3 per forbidden or invented name, never
  below 0. A wrapping ```json fence is accepted; any other text around the JSON scores 0.
- Chronology check (SPEC §4.2): a planted error is caught when the quote shares at least 60% of its words with
  the planted sentence and the stated rule mentions one of that error's `keywords`. Every other report goes on
  `runs/<date>/chronology_check_false_alarms.md`; type `yes` or `no` on each, then run `score --import`.
  Scores stay marked provisional until every report has an answer.
- Refused or truncated runs score 0 (SPEC §4.4). Failed calls (for example out of credits) are not scored; re-run them.
- Scores are saved to `runs/<date>/scores_<step>.json` under blind IDs. Use `--date YYYY-MM-DD` to score an older day.
