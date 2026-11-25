# LLM Identifier for Creative Writing (Open-Weight & Fine-Tuned Models)

A structured, Notion-ready catalog of **68 unique open-weight base and fine-tuned models** evaluated for creative writing across manuscript formats, modalities, pen names, genre categories, and subgenres. Designed to populate the Notion database **"LLM Identifier for Creative Writing: Base Models for Fine-Tuning."**

## Dataset Overview

* **Total Unique Models:** 68 (deduplicated from 88 raw rows; 19 duplicate rows and 1 blank trailing row removed)
* **Composition:**
  * **43 Fine-Tuned Models:** 23 pre-mapped (typos fixed and standardized) + 20 researched from Hugging Face model cards and community discussions
  * **25 Open-Weight Base/Foundation Models:** 1 pre-mapped (`Command A`) + 24 mapped across text, vision, omni-modal, audio (TTS), and image-generation workflows
* **Providers Covered:** Concentrate AI, Featherless AI, Hugging Face (local GGUF/MLX/VL), OpenRouter, Unsloth Desktop, and Comfy Cloud

## Column Schema

| Column | Description |
| :--- | :--- |
| `Model Name` | Display or repository name of the model. |
| `Can Run Locally` | Local deployment feasibility (`Yes` / `No`). |
| `Comparable Equivalent Model` | Reference equivalent model, if applicable. |
| `Fallback Model` | Designated fallback model, if applicable. |
| `Fine-Tuned Model` | Whether the model is a fine-tune (`Yes` / `No`). |
| `Genre Category` | High-level creative writing category (Categories A–H). Uses `/` inside labels so Notion splits multiple categories cleanly on import. |
| `Genres` | Standardized, comma-separated subgenre tags (cleaned for Notion Multi-Select). |
| `Manuscript Format` | Best-fit deliverable formats (e.g., `Novel`, `Series`, `Codex`, `Audiobook`, `Graphic Novel`). |
| `Modality` | Model I/O type (`Text-to-Text`, `Image-Text-to-Text`, `Image-Video-Text-to-Text`, `Omni (Text-Image-Audio)`, `Text-to-Speech (Audio)`, `Text-to-Image`). |
| `Notes` | Preserved role qualifiers (e.g., `series architecture`, `visual OCR`, `spec-sheet mode`) plus quantization, template, and behavioral notes. |
| `Open-Weights Model` | Whether model weights are publicly downloadable (`Yes` / `No`). |
| `Open/Near Frontier Model` | Frontier-tier indicator (`Yes` / `No`). |
| `Pen Name` | Mapped house author persona(s) aligned with each model's genre and stylistic strengths. |
| `Provider` | Primary host or aggregator (`Concentrate AI`, `Featherless AI`, `Hugging Face`, `OpenRouter`, `Unsloth Desktop`, `Comfy Cloud`). |
| `Provider Model ID` | Exact model ID used by the hosting provider. |
| `Via Aggregator` | Available via model aggregator (`Yes` / `No`). |
| `Via Inference Providers` | Available via hosted inference API (`Yes` / `No`). |

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

## Special & Non-Prose Models

* **Audiobook / TTS:** `Chatterbox` (`ResembleAI/chatterbox`) — Text-to-Speech with zero-shot voice cloning and paralinguistic tags for audiobook production.
* **Book Covers & Visual Art:** `Z-Image-Turbo Text to Image` — 6B distilled image generator for covers, character sheets, and worldbuilding references.
* **Technical / Code Assistants:** `DavidAU/Qwen3-53B-A3B-2507-TOTAL-RECALL-v2-MASTER-CODER` and `North Mini Code` — intended for technical specs, fictional code/terminals, and LitRPG stat mechanics rather than primary prose.
* **Testing / Benchmark Only:** `ggml-org/stories15M_MOE` (36.4M) and `Tinyllama-15M-stories` (15.2M) — TinyStories toy models for pipeline testing, not publishable manuscripts.

## Data Cleanup, Overlaps & Notion Import Notes

* **Deduplication:** Removed 19 duplicate entries and 1 empty trailing row from the source export.
* **Cross-File Overlaps:** Four models also appear in the companion **Abliterated & Uncensored** CSV (`DavidAU/Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B`, `Naphula/Goetia-26B-A4B-v1.6`, `Naphula/Goetia-26B-A4B-v1.7`, and `nightmedia/Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess`). Skip or merge these if importing both CSVs into the same Notion database.
* **Tag Hygiene:** Fixed spelling and punctuation errors (`Galactice Empire`, `Conspirarcy Fiction`, `Children's’ Literature`, unclosed parentheses, trailing commas, and within-row duplicates) and extracted all parenthetical role qualifiers into the `Notes` column.
* **Importing to Notion:** Set `Genre Category`, `Manuscript Format`, `Pen Name`, and `Genres` to **Multi-select**, `Modality` to **Select**, and `Notes` to **Text**.
