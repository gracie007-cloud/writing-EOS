# LLM Identifier for Creative Writing: Open-Weight & Fine-Tuned Models

The repository's copy of the Notion database **"♣️ LLM Identifier for Creative Writing: Open-Weight & Fine-Tuned Models"**: **68 models**, open-weight and fine-tuned, each mapped to genre categories, subgenres, manuscript formats and pen names. It is the non-mature counterpart of `../llm-identifier-creative-writing-abliterated/`.

* **File:** `open_weight_models.csv` (UTF-8, Notion's column names)
* **Exported:** 25 November 2026, from the database's table view. Notion's export markup was removed: bold tags around two names and backslash escapes (`\_`, `\[`). Multi-select columns are comma-separated; checkboxes are `Yes` / `No`.

## What the app does with it

The registry build (`python -m eos_app.registry … --open <this file>`, see `eos-app/README.md`) folds it in as it does the mature catalog, **without** marking anything uncensored:

| Provider | Rows | In the app |
| :--- | :--- | :--- |
| Featherless AI | 25 | Called. A route the roster lacked is added (e.g. Cydonia 24B, Crimson Cafe 12B, Tiefighter 13B, Hathor 8B on Featherless). |
| Concentrate AI | 13 | Already in the roster; genre tags added. |
| OpenRouter | 8 | Already in the roster; genre tags added. |
| Hugging Face | 20 | **Fine-tune bases**: "Via Inference Providers" is unticked, so they are recorded and never called. |
| Unsloth Desktop | 1 | Local; not used while local work waits. |
| Comfy Cloud | 1 | Z-Image Turbo. Not added: its "Provider Model ID" reads like a workflow name, and the roster already lists Z-Image Turbo without an ID. Confirm the ID in the roster. |

Its genre tags join each model's, so the prose lane can pick these models for a book's subgenre. An ID the roster left empty is filled from here (Chatterbox: `ResembleAI/chatterbox`), which gives audiobook narration a second provider beside ElevenLabs.

## Columns

As the Abliterated catalog's, plus **Open/Near Frontier Model** (checkbox) and **Modality** (Text-to-Text, Image-Text-to-Text, Image-Video-Text-to-Text, Omni, Text-to-Speech, Text-to-Image). Text modalities are text models to the app; Text-to-Speech is Speech and Text-to-Image is Image.
