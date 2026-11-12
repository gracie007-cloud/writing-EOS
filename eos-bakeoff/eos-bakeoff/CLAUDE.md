# CLAUDE.md · Writing EOS Bake-off Harness

## What This Project Is
A small command-line tool that runs the **Writing EOS bake-off**: it sends the same test pack to several language models for each pipeline step, three times each, records cost, latency, and tokens, applies blind IDs, scores what can be scored automatically, and produces review sheets for what a human must score.

It is the **first** Writing EOS codebase. Its prompt templates and model configuration will be reused by the full Writing EOS app later, so keep them clean and data-driven.

Full requirements: `docs/SPEC.md`. Build in the phase order given there.

## The Owner
The owner is not a professional developer. When you finish a task:
- Explain in plain language what you built and how to run it.
- Give the exact command to run.
- Never assume she knows a tool; say what it does in one line.

## Stack (do not change without asking)
- **Python 3.11+**, standard library first.
- Dependencies: `httpx` (HTTP), `pyyaml` (config), `python-dotenv` (keys), `rich` (terminal tables). Nothing else without asking.
- Model access: **OpenRouter** (one API for proprietary and open-weight models) and **Hugging Face Inference Endpoints** (the mature-tier abliterated models).
- Storage: plain files. JSON Lines for run records; Markdown for outputs and review sheets; CSV for result exports. No database.

## Hard Rules
1. **Never send the answer key to a model.** `data/*ANSWER_KEY*` may be read only by the scorer. Enforce this in code: the prompt builder must refuse any path containing `ANSWER_KEY`.
2. **Never send Section E (seeded brief) with Section C (clean brief).** The section map in `config/steps.yaml` is the only source of which sections a step receives.
3. **Secrets live in `.env` only.** Never print, log, or commit keys. Add `.env` to `.gitignore` on day one.
4. **Model IDs live in `config/models.yaml` only.** No model name is hard-coded anywhere else.
5. **Blind IDs.** Review sheets show only blind IDs. The blind-ID-to-model map is written to a separate file the reviewer opens only after scoring.
6. **Mature content** goes only to models flagged `mature_ok: true` in `config/models.yaml`. Refuse to send Section D elsewhere.
7. **Independence rule for any LLM judge:** the judge's family must differ from the family that produced the output being judged, and must not be `anthropic` or `qwen` for Run 01 (they drafted the test material or are drafting fallbacks). Human scoring is the default for prose.
8. **Fail loudly, keep partial results.** A failed call is recorded as a failed run, never silently retried more than twice, never dropped.

## Conventions
- One module per concern: `config.py`, `prompts.py`, `clients.py`, `runner.py`, `scoring.py`, `reports.py`, `cli.py`.
- Every run record includes: run_id, timestamp, step, model_key, run_number, blind_id, input_hash, output_path, input_tokens, output_tokens, cost_usd, latency_s, status (`ok` / `refused` / `truncated` / `error`), error_message.
- Outputs are saved verbatim. Never edit or clean a model's output before saving it.
- Write small tests for scoring functions (`tests/`), using `pytest`.

## Commands (target)
```
python -m eos_bakeoff run --step first_draft            # all candidate models, 3 runs each
python -m eos_bakeoff run --step chronology_check --models gemini4,kimi_k3
python -m eos_bakeoff score --step character_selector   # automatic scoring
python -m eos_bakeoff sheet --step first_draft          # blind human review sheet
python -m eos_bakeoff report                            # results table + CSV export
python -m eos_bakeoff estimate --step first_draft       # projected cost before running
```

## Non-Goals (for now)
No web interface. No Notion writes (CSV export first; Notion sync is Phase 4). No agent frameworks. No parallel execution beyond a simple concurrency limit.
