# LLM Identifier for Creative Writing (Abliterated & Uncensored Models)

A structured, Notion-ready catalog of **89 unique open-weights and fine-tuned LLMs** evaluated for creative writing across manuscript formats, pen names, genre categories, and subgenres. Designed to populate the Notion database **"LLM Identifier for Creative Writing: Base Models for Fine-Tuning."**

## Dataset Overview

* **Total Unique Models:** 89 (deduplicated from 93 raw rows; 4 exact duplicates removed)
* **Providers Covered:** Featherless AI, Hugging Face (local GGUF/VL), and Unsloth Desktop
* **Coverage:** 69 pre-mapped models (cleaned and standardized) + 20 Hugging Face models researched from model cards and community discussions

## Column Schema

| Column | Description |
| :--- | :--- |
| `Model Name` | Full model repository name (`org/model-name`). |
| `Provider Model ID` | Identifier used by the hosting provider or aggregator. |
| `Open-Weights Model` | Whether model weights are publicly downloadable (`Yes` / `No`). |
| `Fine-Tuned Model` | Whether the model is a fine-tune (`Yes` / `No`). |
| `Via Inference Providers` | Available via hosted inference API (`Yes` / `No`). |
| `Via Aggregator` | Available via model aggregator (`Yes` / `No`). |
| `Provider` | Primary host (`Featherless AI`, `Hugging Face`, `Unsloth Desktop`). |
| `Can Run Locally` | Local deployment feasibility (`Yes` / `No`). |
| `Comparable Equivalent Model` | Reference equivalent model, if applicable. |
| `Fallback Model` | Designated fallback model, if applicable. |
| `Genre Category` | High-level creative writing category (Categories A–H). Uses `/` inside labels so Notion splits multiple categories cleanly on import. |
| `Manuscript Format` | Best-fit deliverable formats (e.g., `Novel`, `Novella`, `Short Story`, `Series`, `Codex`, `Graphic Novel`). |
| `Pen Name` | Mapped house author persona(s) aligned with each model's genre and stylistic strengths. |
| `Genres` | Standardized, comma-separated subgenre tags (cleaned for Notion Multi-Select). |
| `Notes` | Preserved role qualifiers (e.g., `outlining`, `vignettes`, `visual evidence`, `push-caveat`) plus sampling, context, and guardrail notes. |

## Genre Categories

* **Category A:** Dark Fantasy / Gothic Horror & Grimdark
* **Category B:** High-End Literary Prose / Complex Drama / Poetry & Atmospheric Narrative
* **Category C:** Romance / Erotica / Character Drama & Manga/Graphic Novels
* **Category D:** Speculative Fiction / Sci-Fi / Cyberpunk & LitRPG
* **Category E:** Humor / Satire / Slice-of-Life / Cozy & Children's/Middle Grade
* **Category F:** Mystery / Noir Crime / Espionage & High-Stakes Thrillers
* **Category G:** Epic Fantasy / Wuxia/Xianxia / Historical Adventure & Mythic Sagas
* **Category H:** Nonfiction / Essays / Biography / Memoir / Travel & Self-Help

## Allowed Manuscript Formats

`Anthology`, `Audiobook`, `Biography`, `Book Proposal`, `Chapter Book`, `Codex`, `Comic Book`, `Essay`, `Graphic Novel`, `Memoir`, `Novel`, `Novella`, `Screenplay`, `Self-Help`, `Series`, `Short Story`, `Theatrical Script`, `Trilogy`, `Unfinished Manuscript`

## Data Cleanup & Notion Import Notes

* **Deduplication:** Removed 4 duplicate entries present in the source export (`Dolphin-Mistral-GLM-4.7-Flash-24B`, `ERNIE-21B-A3B-Claude-4.5-High-OPUS`, `gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe`, and `gemma-4-E4B-it-The-DECKARD-V2-Strong`).
* **Tag Hygiene:** Spelling and punctuation errors in the original `Genres` column were corrected, within-row duplicate tags were merged, and parenthetical role qualifiers were moved to the `Notes` column to prevent fragmented Multi-Select tags in Notion.
* **Importing to Notion:** Import the `.csv` directly into Notion and set `Genre Category`, `Manuscript Format`, `Pen Name`, and `Genres` to **Multi-select** properties and `Notes` to **Text**.
