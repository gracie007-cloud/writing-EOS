# LLM Identifier for Creative Writing (Proprietary & Open/Near Frontier Models)

A structured, Notion-ready catalog of **62 unique proprietary and open/near-frontier models** spanning text, multimodal, image, video, speech (TTS), music, and sound-design workflows for creative writing and multimedia book production. Designed to populate the Notion database **"LLM Identifier for Creative Writing: Base Models for Fine-Tuning."**

## Dataset Overview

* **Total Unique Models:** 62 (0 duplicate rows)
* **Composition:**
  * **45 Text & Multimodal LLMs:** 7 pre-mapped (`Beam 1.0 501B A23B`, `Claude Fable 5/5.2`, `Claude Opus 5/5.5`, `Claude Sonnet 5.5`, `Claude Haiku 5.5`) + 38 mapped across Google Gemini 2.5–4, OpenAI GPT-5/6, Moonshot Kimi K3/K3.1, Mistral Large 4, Meta Muse, Xiaomi MiMo-V2.6, Tencent HY4, StepFun Step 5, inclusionAI Ling 3.1, xAI Grok 4.7, Alibaba Qwen 3.8, Perplexity Sonar, Inception Mercury 2.5, Upstage Solar Mini 4, MiniMax-M3, and Unbiased Pareto.
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
* **Tag Hygiene:** Fixed minor punctuation typos in the 7 pre-populated `Genres` cells and moved all parenthetical role qualifiers into `Notes`.
* **ID Check:** Verify `Provider Model ID` for `Pareto Latest` (`~unbiased/pareto-latest` carries a leading `~` from the source export).
* **Importing to Notion:** Set `Genre Category`, `Manuscript Format`, `Pen Name`, and `Genres` to **Multi-select**, `Modality` to **Select**, and `Notes` to **Text**.
