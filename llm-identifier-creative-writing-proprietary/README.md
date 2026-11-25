# LLM Identifier for Creative Writing: Proprietary & Open/Near Frontier Models

This is the repository's copy of the Notion database **"🎡 LLM Identifier for Creative Writing: Proprietary & Open/Near Frontier Models"**. It holds **62 models**: 45 proprietary, 13 open or near frontier, and 4 ticked as both. Each is mapped to genre categories, subgenres, manuscript formats and pen names. It complements `../llm-identifier-creative-writing-open-weight/` and `../llm-identifier-creative-writing-abliterated/`.

* **File:** `proprietary_models.csv` (UTF-8, Notion's column names)
* **Exported:** 25 November 2026, from the database's table view, sorted by Model Name.
* **Cleanup:** Notion's export markup was removed: bold tags around one name and backslash escapes (`\~`, `\<`, `\$`). Multi-select columns are comma-separated, and checkboxes are `Yes` / `No`.

## What the app does with it

The registry build (`python -m eos_app.registry … --proprietary <this file>`, see `eos-app/README.md`) folds it in the same way as the open-weight catalog, **without** marking anything uncensored:

| Provider | Rows | In the app |
| :--- | :--- | :--- |
| Concentrate AI | 36 | 28 were already in the roster and get genre tags. 8 routes the roster lacked are added: Claude Fable 5 and 5.2, Gemini 4 Carbon, Hydrogen and Neon, Kimi K3.1 Pro and Pro Highspeed, and Qwen3.8 Omni Flash (a second route beside its OpenRouter one). |
| OpenRouter | 13 | 12 were already in the roster and get genre tags, and Fish Audio S2 Pro gets its ID (`fish-audio/s2-pro`). Gemini 3.1 Flash TTS Preview is reported, not added: the roster lists "Gemini 3.1 Flash TTS" with no ID. |
| Comfy Cloud | 13 | Reported, not added. These are media workflows named for newer versions than the roster's ID-less rows (for example FLUX.2 Pro vs FLUX.2, Seedance 2.5 vs 2.0, Wan 3.0 vs 2.2, LTX-2.5 vs LTX-2). Say which roster row each one replaces. |

A model this catalog adds counts as frontier when either checkbox is ticked.

### Two side effects

* **Sonar Deep Research enters the mature tier.** The roster ticks Uncensored for it, and this catalog gives it genre tags, so it now qualifies on OpenRouter. If that tick was not meant, untick it in the roster.
* **Pareto Latest keeps its leading tilde.** Its ID, `~unbiased/pareto-latest`, is an OpenRouter "latest" alias. The Notes column asks whether the tilde is a typo, so confirm it on OpenRouter.

## Columns

The columns match the open-weight catalog's, except that **Proprietary Model** (checkbox) replaces Open-Weights Model and Fine-Tuned Model. Modality adds **Image-Video-Audio-Text-to-Text** and **Omni (Text-Image-Video-Audio)**, which the app treats as text models.

The Pen Name column stays in this folder. It is never copied into `eos-app/` (D10).
