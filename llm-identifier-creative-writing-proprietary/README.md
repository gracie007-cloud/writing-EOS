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
| OpenRouter | 13 | 12 were already in the roster and get genre tags, and Fish Audio S2 Pro gets its ID (`fish-audio/s2-pro`). Gemini 3.1 Flash TTS Preview and Lyria 3 Pro Preview are added as media models. |
| Comfy Cloud | 13 | Image, video, music and sound workflows, each with its ID (the workflow name). The ones the roster also lists match it; the rest (for example FLUX.2 Pro and Qwen-Image 3.0) are added. *Narrative Components* names them for the media components (2026-11-25). |

A model this catalog adds counts as frontier when either checkbox is ticked.

### Media models

This catalog is where the Author keeps every media model (2026-11-25), so the build adds its media rows with their type (Image, Video, Music, Sound, Speech) instead of reporting them.

### Pareto Latest

Its ID is `~unbiased/pareto-latest`, with the leading tilde: that is OpenRouter's ID for it (confirmed by the Author, 2026-11-25).

## Columns

The columns match the open-weight catalog's, except that **Proprietary Model** (checkbox) replaces Open-Weights Model and Fine-Tuned Model. Modality adds **Image-Video-Audio-Text-to-Text** and **Omni (Text-Image-Video-Audio)**, which the app treats as text models.

The Pen Name column stays in this folder. It is never copied into `eos-app/` (D10).
