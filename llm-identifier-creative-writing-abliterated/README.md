# LLM Identifier for Creative Writing: Abliterated & Uncensored Models

The repository's copy of the Notion database **"🎾 LLM Identifier for Creative Writing: Abliterated & Uncensored Models"**: **91 rows, 90 distinct models**, all uncensored or abliterated, each evaluated for creative writing across manuscript formats, pen names, genre categories and subgenres. Dolphin Mistral 24B Venice Edition appears twice, once per route (Featherless AI and OpenRouter). UnslopNemo 12B v4.1 is listed on OpenRouter; its Featherless AI route comes from the 14 November register (W50), and the app uses both.

This catalog is the source of the Writing EOS app's **mature tier** (requirement P10, decision D33). The app's registry build reads it (see `eos-app/README.md`), marks every model in it uncensored, and takes its genre tags.

* **File:** `abliterated_models.csv` (UTF-8, one header row, Notion's column names)
* **Last updated:** 25 November 2026, in step with the Notion database

## What the app does with each row

| Provider in the row | Rows | In the mature tier? | Why |
| :--- | :--- | :--- | :--- |
| Featherless AI | 61 | Yes | An inference provider: called directly. |
| OpenRouter | 2 | Yes | An aggregator: a second route to a model also on Featherless AI. |
| Hugging Face | 20 | No | GGUF files kept as **bases for later fine-tuning** ("Via Inference Providers" unticked). Recorded, never called. |
| Unsloth Desktop | 8 | No | Local models. Local inference and fine-tuning are not planned for now (hardware). |

The rule (the Author, 25 November 2026): the mature tier is the uncensored models that an inference provider or an aggregator serves.

## Column schema

| Column | Description |
| :--- | :--- |
| `Model Name` | Model repository name (`org/model-name`). |
| `Provider Model ID` | The ID the provider serves it under. For OpenRouter, the OpenRouter slug (e.g. `thedrummer/unslopnemo-12b`). |
| `Open-Weights Model` | Weights publicly downloadable (`Yes` / `No`). |
| `Fine-Tuned Model` | The model is a fine-tune (`Yes` / `No`). |
| `Via Inference Providers` | Served by a hosted inference provider (`Yes` / `No`). `No` on a Hugging Face row means a GGUF fine-tune base. |
| `Via Aggregator` | Reachable through an aggregator such as OpenRouter (`Yes` / `No`). |
| `Provider` | The route this row describes: `Featherless AI`, `OpenRouter`, `Hugging Face` or `Unsloth Desktop`. |
| `Can Run Locally` | Local deployment is feasible (`Yes` / `No`). |
| `Comparable Equivalent Model` | Reference equivalent model, if any (`N/A` otherwise). |
| `Fallback Model` | Designated fallback model, if any. |
| `Genre Category` | Categories A to H (below). Several are comma-separated. |
| `Manuscript Format` | Best-fit deliverable formats (e.g. `Novel`, `Novella`, `Short Story`, `Series`, `Codex`, `Graphic Novel`). |
| `Pen Name` | House author personas aligned with the model's genres and style. |
| `Genres` | Comma-separated subgenre tags, spelled as in the Genre Matrix. |
| `Notes` | Role qualifiers (e.g. `outlining`, `vignettes`), sampling, context and guardrail notes. |

## Genre categories

The Notion database spells the labels without spaces around the slashes (`Category A: Dark Fantasy/Gothic/Horror & Grimdark`); this file keeps the spaced spelling below. The app reads only the letter.

* **Category A:** Dark Fantasy / Gothic Horror & Grimdark
* **Category B:** High-End Literary Prose / Complex Drama / Poetry & Atmospheric Narrative
* **Category C:** Romance / Erotica / Character Drama & Manga/Graphic Novels
* **Category D:** Speculative Fiction / Sci-Fi / Cyberpunk & LitRPG
* **Category E:** Humor / Satire / Slice-of-Life / Cozy & Children's/Middle Grade
* **Category F:** Mystery / Noir Crime / Espionage & High-Stakes Thrillers
* **Category G:** Epic Fantasy / Wuxia/Xianxia / Historical Adventure & Mythic Sagas
* **Category H:** Nonfiction / Essays / Biography / Memoir / Travel & Self-Help

## Allowed manuscript formats

`Anthology`, `Audiobook`, `Biography`, `Book Proposal`, `Chapter Book`, `Codex`, `Comic Book`, `Essay`, `Graphic Novel`, `Memoir`, `Novel`, `Novella`, `Screenplay`, `Self-Help`, `Series`, `Short Story`, `Theatrical Script`, `Trilogy`, `Unfinished Manuscript`

## Change log

* **25 November 2026.** Two OpenRouter routes added, in Notion and here:
  * `TheDrummer/UnslopNemo-12B-v4.1` as OpenRouter `thedrummer/unslopnemo-12b` (served by Parasail, 1,024,000-token context). OpenRouter's listing links these weights; the 14 November register (W50) verified the same model on Featherless AI. Its genres, pen names and categories come from the register; its manuscript formats are inferred from its long context.
  * `cognitivecomputations/Dolphin-Mistral-24B-Venice-Edition` as OpenRouter `cognitivecomputations/dolphin-mistral-24b-venice-edition` (listed as "Venice: Uncensored", served by Venice, 128K context). The same weights as the Featherless row `dphn/Dolphin-Mistral-24B-Venice-Edition` (register W57). Its other columns copy that row.
  * The four duplicate rows in Notion were removed, so the database and this file now agree row for row.
  * This file moved from `llm-identifer-creative-writing-abliterated/.csv` (misspelled folder, nameless file) to its current path.
* **24 November 2026.** First export: 89 unique models, deduplicated from 93 raw rows. Spelling and punctuation in `Genres` corrected, within-row duplicate tags merged, and role qualifiers moved to `Notes` so Notion multi-select tags stay clean.

## Importing to Notion

Import the CSV into Notion and set `Genre Category`, `Manuscript Format` and `Pen Name` to **Multi-select**, `Notes` and `Genres` to **Text**, and the Yes/No columns to **Checkbox**.
