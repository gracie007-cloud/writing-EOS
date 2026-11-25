> **Superseded (2026-11-25).** The Author found this 14 November register incorrect. The app no longer reads it (nor `registry.json` or `routing.json`); models come only from the Notion databases (the roster *LLM Identifier - Master List* and the three *LLM Identifier for Creative Writing* catalogs). Kept for reference until the Author says to delete it.

# Verification log: model register, 14 November 2026

Every model ID was checked live against the Hugging Face API (`/api/models/{id}`) and the Featherless AI API (`/v1/models/{id}`) on 14 November 2026. The Notion database "LLM Identifier for Creative Writing" and the Google Drive model documents were treated as scaffolding: each claim below was checked, not copied.

## Roster

- 87 models: 77 prose writers (W01 to W77) and 10 component specialists (C01 to C10).
- W70 to W77 are the eight models added to the Drive folder on 14 November 2026. They are numbered after the existing models so that no existing ID changes.
- Removed: `DavidAU/ERNIE-21B-A3B-GLM-4.7-Flash-Thinking`, at the owner's instruction. Its Hugging Face repo also no longer resolves (HTTP 401).
- Not in the roster: `DavidAU/ERNIE-21B-A3B-Thinking-Gemini-3-Pro-High-Reasoning-V2` (listed in Notion; Hugging Face repo does not resolve), `DavidAU/Qwen3-VL-8B-GLM-4.7-Flash-Heretic-Uncensored-Thinking` and `DavidAU/Qwen3.5-21B-GLM-4.7-Flash-Deckard-Heretic-Uncensored-Thinking` (listed in Notion and served by Featherless, but there is no Drive profile for either).

## Inference providers

| Provider | Models | Notes |
| --- | --- | --- |
| Featherless AI | 77 | Default. Model ID equals the Hugging Face repo, except W64 (see below). |
| Local, Unsloth Desktop | 8 | W01 to W07 (Gemma-4 E2B and E4B DECKARD) and W42 (FREAKSTORM-6B). Not served by Featherless. |
| Local, GGUF from Hugging Face | 2 | W68 (`ArliAI/Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1-GGUF`) and W69 (`DavidAU/LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF`). Not served by Featherless. |
| OpenRouter (secondary) | 3 | W50 `thedrummer/unslopnemo-12b`, W56 `thedrummer/cydonia-24b-v4.1`, W57 `cognitivecomputations/dolphin-mistral-24b-venice-edition`. All three are also on Featherless. |

- W64 Legion 70B: Featherless serves `e-n-v-y/Legion-V2.1-LLaMa-70B-Elarablated-v0.8-hf`, not `e-n-v-y/Legion-V2.1-LLaMa-70B-Elarablated-v0.8`. Both repos exist on Hugging Face. Concurrency cost 4.
- Served context differs from the context the model cards claim. Featherless serves Llama-3 8B models at 8,192 tokens (W59 to W63, C05), Gemma-2 9B at 16,384 (W26, W27) and everything else at 32,768. Cards claiming 128K, 256K or 1M native context (for example W45, W50, W52, W59, W61, C09) are capped at the served figure. The app must size requests to `served_context_tokens`.
- Featherless serves the Qwen3.6 12B, 21B and 9B shrinks (W74 to W77) under model class `qwen3_5-27b`, concurrency cost 2, the same as the 27B models.

## Notion database corrections (applied 14 November 2026)

The Notion database "LLM Identifier for Creative Writing" was corrected in place so it matches this register:

- W57 `dphn/Dolphin-Mistral-24B-Venice-Edition`: provider set to Featherless AI (OpenRouter kept as secondary).
- W42 FREAKSTORM-6B: "Via Inference Providers" unticked, "Can Run Locally" ticked.
- Hathor v0.9 row: Provider Model ID corrected (it held the Stheno 3.3 GGUF ID).
- Genre spellings aligned with the Genre Matrix (Love Triangle Romance, Epic Quest Fantasy, Dark/Rogue Epic Fantasy, Moral Tales, and others).
- New row added for W69 (LFM2.5-2.6B NEO-MAX).
- Left for the owner to delete: the two ERNIE rows for models no longer in the roster.

## Errors found in the Drive model folder

- The Google Doc titled "IggyLux/MN-VelvetCafe-RP-12B-V2" profiles `EldritchLabs/MN-Crimson-Cafe-12B`, a merge of VelvetCafe with Crimson-Constellation. The register uses the Crimson-Cafe repo (W55), which Featherless serves.
- Genre names in the documents that are not in the Genre Matrix were not used as genres (for example Absurdist Fiction, Creepypasta, Dark Academia, Erotic Horror). They appear on the model cards as cross-genre roles.
