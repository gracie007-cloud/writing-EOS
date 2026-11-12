# SPEC · Writing EOS Bake-off Harness

## 1 · Purpose
Decide, with evidence, which model should handle each Writing EOS pipeline step. The registry of steps and candidate models lives in Notion (AI Agentic LLM); this harness produces the evidence and exports results that are entered there.

## 2 · Inputs
| File | Use |
|---|---|
| `data/Run01_TestPack.md` | Model-facing test pack, Sections A to E |
| `data/Run01_TestPack_ANSWER_KEY.md` | **Scorer only.** Kept out of the repo's `data/` until Phase 2, then stored in `data/` with the read guard from CLAUDE.md |
| `config/models.yaml` | Candidate models and their access details |
| `config/steps.yaml` | Steps: task type, sections sent, prompt template, output format, scoring method |
| `prompts/*.md` | Prompt templates with `{{SECTION_A}}`-style placeholders |

The test pack is split into sections by its headings: `## A ·`, `## B ·`, `## C ·`, `## D ·`, `## E ·`.

## 3 · Run Loop
For each step and each candidate model:
1. Build the prompt from the template and only the sections listed for that step.
2. Call the model (OpenRouter or the Hugging Face endpoint) with the step's temperature and max tokens.
3. Repeat **three times** with identical input.
4. Record the run (fields listed in CLAUDE.md) to `runs/<YYYY-MM-DD>/runs.jsonl`; save the output verbatim to `runs/<date>/<step>/<blind_id>.md`.
5. Assign a **blind ID** (for example `FD-K7Q`) per run; write the mapping to `runs/<date>/BLIND_MAP.json`.
6. Respect a concurrency limit (default 2) and simple rate-limit backoff.

**Cost:** take token usage from the response; take cost from OpenRouter's generation lookup when available, otherwise compute it from per-token prices in `models.yaml`. `estimate` multiplies expected tokens × prices × runs before anything is sent.

## 4 · Scoring
### 4.1 Structured extraction (automatic)
Selectors must return JSON matching the schema in `steps.yaml`. Compare against the extraction key in the answer key:
- Format fails to parse → 0.
- Otherwise start at 10; −2 per relevant item missing; −3 per invented or forbidden item (for Ch 1, selecting Mattis or the memory market is forbidden).
- Name matching is case-insensitive and tolerant of diacritics.

### 4.2 Verdict / check (automatic, with confirmation)
The checker returns JSON: a list of contradictions, each with the quoted sentence from Section E and the rule it contradicts.
- A planted error counts as **caught** when the returned quote overlaps the planted sentence (at least 60% token overlap) and the stated rule points at the right fact.
- Every other reported contradiction is a **candidate false alarm**, listed in a confirmation sheet for the owner to accept or reject.
- Score = (caught ÷ 3 × 9) + 1 − 1 per confirmed false alarm; floor 0.

### 4.3 Prose (automatic checks, then human review)
Automatic, applied before review:
- **Auto-fail flags** (any one sets Persona Fidelity to 0): the phrase "I remember" in Varga's speech or thought; Varga naming the victim; any of `Mattis`, `M.22`, `Pell`, `Tova`, `market`; emotion words attached to Varga in narration (seed list in `config/slop.yaml`). The lists for these flags live in `data/Run01_rules.yaml`, beside the test pack; `config/slop.yaml` holds only lists true of any book.
- **Slop flags:** count matches from `config/slop.yaml` (generic stock phrases and overused AI vocabulary) and repeated sentence openings (three or more in a row).
- **Mature brief (Section D) dignity checks:** her full name spoken by Ferreira; covering between examinations; the fingertip-dye detail present; listed injury vocabulary absent beyond procedure.

Human review: `sheet` produces a Markdown sheet per step with each output under its blind ID and blank fields for **Prose Level (1–7)**, **Persona Fidelity (0–3)**, and notes. `score --import` reads the completed sheet.
Score = (Level ÷ 7 × 5) + (Fidelity ÷ 3 × 4) + 1 − 0.5 × slop flags; floor 0.

### 4.4 Refusals and truncation
A refusal or truncation scores 0 and is flagged. More than one in three runs disqualifies the model for that step.

## 5 · Reports
`report` prints, per step: model, average score, standard deviation across runs, average cost, average latency, refusals. It applies the **assignment rule**:
- Primary = highest average; a cheaper model within 5% takes Primary.
- Fallback = best open-weight model within 15% of Primary.
- Mature Tier = best `mature_ok` model on Section D.

It exports `results.csv` with columns matching the Notion **Bake-off Runs** database so the owner can import it.

## 6 · Phases and Acceptance Criteria
| Phase | Build | Done When |
|---|---|---|
| **1 · Plumbing** | Config loading, section splitting, prompt builder with the answer-key guard, OpenRouter client, run loop, run records, `estimate` | `run --step first_draft --models <one cheap model> --runs 1` saves an output and a run record with tokens, cost, latency |
| **2 · Automatic scoring** | Extraction and verdict scorers, false-alarm confirmation sheet, tests | Tests pass against hand-made sample outputs, including one perfect and one bad output per scorer |
| **3 · Human review loop** | Prose auto-checks, blind review sheets, sheet import, `report`, CSV export | A full First Draft round across three models produces a review sheet and, after import, a ranked table |
| **4 · Mature tier and sync** | Hugging Face endpoint client (with scale-to-zero cold-start handling); optional Notion write-back | Section D runs only on `mature_ok` models; results appear in Notion Bake-off Runs (optional) |

## 7 · Out of Scope
The Writing EOS app itself; chapter-by-chapter generation; any model fine-tuning.
