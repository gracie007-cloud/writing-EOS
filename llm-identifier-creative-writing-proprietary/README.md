# LLM Identifier for Creative Writing (Proprietary & Open/Near Frontier Models)

A structured, Notion-ready catalog of **63 unique proprietary and open/near-frontier models** spanning text, multimodal, image, video, speech (TTS), music, and sound-design workflows for creative writing and multimedia book production. Designed to populate the Notion database **"LLM Identifier for Creative Writing: Proprietary & Open/Near Frontier Models."**

## Dataset Overview

* **Total Unique Models:** 63 (0 duplicate rows)
* **Composition:**
  * **46 Text & Multimodal LLMs:** 7 pre-mapped (`Beam 1.0 501B A23B`, `Claude Fable 5/5.2`, `Claude Opus 5/5.5`, `Claude Sonnet 5.5`, `Claude Haiku 5.5`) + 39 mapped across Google Gemini 2.5–4, OpenAI GPT-5/6, Moonshot Kimi K3/K3.1 Pro, Mistral Large 4, Meta Muse, Xiaomi MiMo-V2.6, Tencent HY4, StepFun Step 5, inclusionAI Ling 3.1, xAI Grok 4.7, Alibaba Qwen 3.8, Perplexity Sonar, Inception Mercury 2.5, Upstage Solar Mini 4, MiniMax-M3, NVIDIA Nemotron Lightning 3.5 (added 25 November 2026), and Unbiased Pareto.
  * **17 Multimedia Production Models:** 5 Image (`FLUX.2 Pro`, `GPT Image 2`, `Ideogram v4`, `Nano Banana Pro`, `Qwen-Image 3.0`), 5 Video (`FLUX 3 Video`, `LTX-2.5`, `Seedance 2.5`, `Wan 3.0 T2V/I2V`), 2 Speech/TTS (`Fish Audio S2 Pro`, `Gemini 3.1 Flash TTS Preview`), 3 Music (`ACE-Step 1.5`, `Lyria 3 Pro Preview`, `MiniMax Music 3`), and 2 Sound/SFX (`Stable Audio 2.5`, `Stability Audio 2.5 Inpainting`).
* **Providers Covered:** Concentrate AI, OpenRouter, and Comfy Cloud

## Column Schema

| Column | Description |
| :--- | :--- |
| `Model Name` | Display name of the model. |
| `Can Run Locally` | Local deployment feasibility (`Yes` / `No`). |
| `Comparable Equivalent Model` | Reference open/equivalent model, if applicable. |
| `Fallback Model` | Designated fallback model, if applicable. |
| `Genre Category` | High-level creative writing category (Categories A–H). Uses `/` inside labels for clean Notion Multi-Select splitting. |
| `Genres` | Standardized, comma-separated subgenre or production-role tags. |
| `Manuscript Format` | Best-fit deliverable formats (e.g., `Novel`, `Series`, `Audiobook`, `Graphic Novel`, `Screenplay`). |
| `Modality` | Model I/O type (`Text-to-Text`, `Image-Text-to-Text`, `Image-Video-Audio-Text-to-Text`, `Omni`, `Image`, `Video`, `Speech`, `Music`, `Sound`). |
| `Notes` | Preserved role qualifiers plus context-window, pricing/speed tier, and production notes. |
| `Open/Near Frontier Model` | Open-frontier indicator (`Yes` / `No`). |
| `Pen Name` | Mapped house author persona(s) or production role (`All Pen Names (Visual Art & Covers / Book Trailers / Audio & Trailers / Audiobook Production)`). |
| `Proprietary Model` | Proprietary indicator (`Yes` / `No`). |
| `Provider` | Primary host or aggregator (`Concentrate AI`, `OpenRouter`, `Comfy Cloud`). |
| `Provider Model ID` | Exact API/provider model identifier. |
| `Via Aggregator` | Available via model aggregator (`Yes` / `No`). |
| `Via Inference Providers` | Available via hosted inference API (`Yes` / `No`). |

## Data Cleanup & Notion Import Notes

* **Schema Fixes:** Corrected a column shift on `FLUX 3 Video Image-to-Video` (`Video` moved from `Manuscript Format` to `Modality`), trimmed trailing whitespace on `Mistral Large 4`, and normalized double spaces in `Fallback Model` (`Kimi K3`).
* **Pairings (25 November 2026):** Comparable and Fallback cells that named `Kimi K3.1` now name `Kimi K3.1 Pro`, and Claude Haiku 5.5's Comparable is `Nemotron Lightning 3.5 30B A3B`. Both columns are now text, not select.
* **Tag Hygiene:** Fixed minor punctuation typos in the 7 pre-populated `Genres` cells and moved all parenthetical role qualifiers into `Notes`.
* **ID Check:** `Pareto Latest` is `~unbiased/pareto-latest`; the leading `~` is part of OpenRouter's ID (confirmed 25 November 2026).
* **Importing to Notion:** Set `Genre Category`, `Manuscript Format`, `Pen Name`, and `Genres` to **Multi-select**, `Modality` to **Select**, and `Notes` to **Text**.

## In the Writing EOS app

* **File:** `proprietary_models.csv` (UTF-8, Notion's column names)
* **Exported:** 25 November 2026, from the database's table view, sorted by Model Name.
* **Cleanup:** Notion's export markup was removed: bold tags around one name and backslash escapes (`\~`, `\<`, `\$`). Multi-select columns are comma-separated, and checkboxes are `Yes` / `No`.

### What the app does with it

The registry build (`python -m eos_app.registry … --proprietary <this file>`, see `eos-app/README.md`) folds it in the same way as the open-weight catalog, **without** marking anything uncensored:

| Provider | Rows | In the app |
| :--- | :--- | :--- |
| Concentrate AI | 37 | 28 were already in the roster and get genre tags. 9 routes the roster lacked are added: Claude Fable 5 and 5.2, Gemini 4 Carbon, Hydrogen and Neon, Kimi K3.1 Pro and Pro Highspeed, Nemotron Lightning 3.5 30B A3B, and Qwen3.8 Omni Flash (a second route beside its OpenRouter one). |
| OpenRouter | 13 | 12 were already in the roster and get genre tags, and Fish Audio S2 Pro gets its ID (`fish-audio/s2-pro`). Gemini 3.1 Flash TTS Preview and Lyria 3 Pro Preview are added as media models. |
| Comfy Cloud | 13 | Image, video, music and sound workflows, each with its ID (the workflow name). The ones the roster also lists match it; the rest (for example FLUX.2 Pro and Qwen-Image 3.0) are added. *Narrative Components* names them for the media components (2026-11-25). |

A model this catalog adds counts as frontier when either checkbox is ticked.

### Media models

This catalog is where the Author keeps every media model (2026-11-25), so the build adds its media rows with their type (Image, Video, Music, Sound, Speech) instead of reporting them.

### Pareto Latest

Its ID is `~unbiased/pareto-latest`, with the leading tilde: that is OpenRouter's ID for it (confirmed by the Author, 2026-11-25).

### Columns

The columns match the open-weight catalog's, except that **Proprietary Model** (checkbox) replaces Open-Weights Model and Fine-Tuned Model. Modality adds **Image-Video-Audio-Text-to-Text** and **Omni (Text-Image-Video-Audio)**, which the app treats as text models.

The Pen Name column stays in this folder. It is never copied into `eos-app/` (D10).
