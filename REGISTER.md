# Pen Name and Fine-Tuned Model Assignment Register

**For:** Claude Code, building the Writing EOS app · **Data verified:** 14 November 2026 · **Roster:** 87 models (77 prose writers, 10 component specialists) · 44 pen names · 739 Genre Matrix rows

The register answers one question: **for this pen name, in this subgenre, which models should write, and in what role?** It is organised pen name first. Each pen name has one table with one row per Genre Matrix path, and the models that serve that path sit in the row, grouped by role and ordered by fit. A separate Model reference tab holds one card per model: what it is, how to call it, its context limit and what not to use it for.

Machine-readable copies: `routing.json` (one record per pen name and genre path, the same data as the routing tables) and `registry.json` (per-model data, inference details and assignments).

## How to use it

1. Open the tab with the pen name (alphabetical).
2. Find the row whose Secondary Genre, Major Subgenre and Minor Subgenre match the project. These come straight from the pen name's Genre Matrix sheet; the Primary Genre is stated above each table.
3. Read across: **Lead writers** draft the book. **Short-form and conditional writers** handle scenes, vignettes and short stories, or work only under the stated condition. **Layer and component specialists** support a lead writer: planning, worldbuilding, series continuity, evidence reading, technical accuracy. **Strong adjacent fits** are good but unranked alternatives.
4. Look up any model ID (W01–W77, C01–C10) in the "Models used for this pen name" table under the routing table, or on its card in the Model reference tab.

## Reading a cell

- `W57 #1` means model W57, and this subgenre is **number 1 on W57's own best-fit list** (its strongest genre). Within a cell, models are ordered by that number, so the first model listed is the one for which this subgenre is most central. The number describes the model's specialisation; it is not a ranking of pen names.
- Text in brackets is the usage note from the model's source document, for example `(Short)` = short pieces only, `(Directed)` = needs an explicit, detailed brief, `(conditional: Directed)` = use only when that condition is met, `(Planning layer)` = plans for another writer rather than drafting.
- For component specialists (C01–C10) the bracket starts with the component they provide: `C04 #1 (Planning, Outlining)`.
- `whole Major level` or `whole Secondary level` means the model fits every subgenre beneath that level, so it appears on each of those rows.
- `—` means no model in the roster fills that role for that path. Rows with no model at all are listed under the table rather than shown empty.

## Coverage

538 of 739 Genre Matrix rows have at least one model; 491 have a lead writer. Every one of the 1,500 assignments in the source documents maps to an existing Genre Matrix row; none were dropped or renamed.

Pen names with no model on any row (6): Amos Trevelyan, Beatrix Holm, June Callender, Maud Ellery, Odessa Marchetti, Ruth Calloway. Their Genre Matrix sheets are nonfiction (essay, biography, autobiography, travel, self-help) and lyric and formal poetry, which none of the 87 profiled models was assessed for. August Reinhardt (drama) and Callum Reid (poetry) are only lightly covered.

| Pen name | Genre Matrix rows | With a lead writer | With any model | With no model |
| --- | --- | --- | --- | --- |
| AJ Solomon | 5 | 5 | 5 | 0 |
| Amos Trevelyan | 9 | 0 | 0 | 9 |
| Anais Amaris | 2 | 2 | 2 | 0 |
| Anya Amara | 4 | 2 | 3 | 1 |
| August Reinhardt | 17 | 1 | 2 | 15 |
| Avery Lee | 7 | 3 | 5 | 2 |
| Bastien Benoit | 17 | 5 | 8 | 9 |
| Beatrix Holm | 8 | 0 | 0 | 8 |
| Bree Beaumont | 5 | 4 | 4 | 1 |
| Callum Reid | 5 | 1 | 1 | 4 |
| Carys Cassian | 9 | 5 | 6 | 3 |
| Cassidy Cavendish | 13 | 4 | 6 | 7 |
| CeeCee Chestervale | 12 | 1 | 2 | 10 |
| Ch'an Lee | 51 | 51 | 51 | 0 |
| Christine Leigh | 55 | 55 | 55 | 0 |
| D'Annie de Leon | 6 | 6 | 6 | 0 |
| Deon D'Arcy | 68 | 67 | 68 | 0 |
| Drew D'Angelo | 9 | 2 | 6 | 3 |
| Ellis Leigh | 30 | 12 | 18 | 12 |
| Eulalie Rowland | 1 | 1 | 1 | 0 |
| Gabby Gabriel | 8 | 4 | 4 | 4 |
| Gabriel Varenne | 9 | 9 | 9 | 0 |
| Gia Graceville | 5 | 1 | 2 | 3 |
| Gigi Gable | 5 | 1 | 3 | 2 |
| H.J. Hakimi | 10 | 10 | 10 | 0 |
| Hanif J. Hakimi | 17 | 7 | 8 | 9 |
| June Callender | 6 | 0 | 0 | 6 |
| K.K. Kenyatta | 9 | 8 | 8 | 1 |
| Kai Koan | 7 | 6 | 6 | 1 |
| Laurent Levesque | 4 | 4 | 4 | 0 |
| MJ Montrose | 32 | 18 | 22 | 10 |
| Marcel Moreau | 17 | 6 | 7 | 10 |
| Maud Ellery | 18 | 0 | 0 | 18 |
| Mimi Montclair | 4 | 1 | 1 | 3 |
| Naomi McNamara | 19 | 15 | 16 | 3 |
| Noelle Noir | 41 | 22 | 30 | 11 |
| O. O'Sullivan-Oz | 3 | 1 | 1 | 2 |
| Odessa Marchetti | 7 | 0 | 0 | 7 |
| R.S. Raphael | 41 | 32 | 35 | 6 |
| R.S. Rhys | 85 | 76 | 79 | 6 |
| Remy Raphael | 25 | 25 | 25 | 0 |
| Ria Garcia Reyes | 13 | 5 | 6 | 7 |
| Ruth Calloway | 7 | 0 | 0 | 7 |
| Sebastian V. Somerset | 14 | 13 | 13 | 1 |

## Inference

Featherless AI is the default provider. Each model card gives the exact model ID to send, the context the provider actually serves and the concurrency cost. Size every request to the **served** context, not the native context a model card claims: Featherless serves Llama-3 8B models at 8,192 tokens, Gemma-2 9B at 16,384 and everything else at 32,768.

## Verification, 14 November 2026

Every model ID was checked live against the Hugging Face API (`/api/models/{id}`) and the Featherless AI API (`/v1/models/{id}`) on 14 November 2026. The Notion database "LLM Identifier for Creative Writing" and the Google Drive model documents were treated as scaffolding: each claim below was checked, not copied.

### Roster

- 87 models: 77 prose writers (W01 to W77) and 10 component specialists (C01 to C10).
- W70 to W77 are the eight models added to the Drive folder on 14 November 2026. They are numbered after the existing models so that no existing ID changes.
- Removed: `DavidAU/ERNIE-21B-A3B-GLM-4.7-Flash-Thinking`, at the owner's instruction. Its Hugging Face repo also no longer resolves (HTTP 401).
- Not in the roster: `DavidAU/ERNIE-21B-A3B-Thinking-Gemini-3-Pro-High-Reasoning-V2` (listed in Notion; Hugging Face repo does not resolve), `DavidAU/Qwen3-VL-8B-GLM-4.7-Flash-Heretic-Uncensored-Thinking` and `DavidAU/Qwen3.5-21B-GLM-4.7-Flash-Deckard-Heretic-Uncensored-Thinking` (listed in Notion and served by Featherless, but there is no Drive profile for either).

### Inference providers

| Provider | Models | Notes |
| --- | --- | --- |
| Featherless AI | 77 | Default. Model ID equals the Hugging Face repo, except W64 (see below). |
| Local, Unsloth Desktop | 8 | W01 to W07 (Gemma-4 E2B and E4B DECKARD) and W42 (FREAKSTORM-6B). Not served by Featherless. |
| Local, GGUF from Hugging Face | 2 | W68 (`ArliAI/Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1-GGUF`) and W69 (`DavidAU/LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF`). Not served by Featherless. |
| OpenRouter (secondary) | 3 | W50 `thedrummer/unslopnemo-12b`, W56 `thedrummer/cydonia-24b-v4.1`, W57 `cognitivecomputations/dolphin-mistral-24b-venice-edition`. All three are also on Featherless. |

- W64 Legion 70B: Featherless serves `e-n-v-y/Legion-V2.1-LLaMa-70B-Elarablated-v0.8-hf`, not `e-n-v-y/Legion-V2.1-LLaMa-70B-Elarablated-v0.8`. Both repos exist on Hugging Face. Concurrency cost 4.
- Served context differs from the context the model cards claim. Featherless serves Llama-3 8B models at 8,192 tokens (W59 to W63, C05), Gemma-2 9B at 16,384 (W26, W27) and everything else at 32,768. Cards claiming 128K, 256K or 1M native context (for example W45, W50, W52, W59, W61, C09) are capped at the served figure. The app must size requests to `served_context_tokens`.
- Featherless serves the Qwen3.6 12B, 21B and 9B shrinks (W74 to W77) under model class `qwen3_5-27b`, concurrency cost 2, the same as the 27B models.

### Notion database corrections (applied 14 November 2026)

The Notion database "LLM Identifier for Creative Writing" was corrected in place so it matches this register:

- W57 `dphn/Dolphin-Mistral-24B-Venice-Edition`: provider set to Featherless AI (OpenRouter kept as secondary).
- W42 FREAKSTORM-6B: "Via Inference Providers" unticked, "Can Run Locally" ticked.
- Hathor v0.9 row: Provider Model ID corrected (it held the Stheno 3.3 GGUF ID).
- Genre spellings aligned with the Genre Matrix (Love Triangle Romance, Epic Quest Fantasy, Dark/Rogue Epic Fantasy, Moral Tales, and others).
- New row added for W69 (LFM2.5-2.6B NEO-MAX).
- Left for the owner to delete: the two ERNIE rows for models no longer in the roster.

### Errors found in the Drive model folder

- The Google Doc titled "IggyLux/MN-VelvetCafe-RP-12B-V2" profiles `EldritchLabs/MN-Crimson-Cafe-12B`, a merge of VelvetCafe with Crimson-Constellation. The register uses the Crimson-Cafe repo (W55), which Featherless serves.
- Genre names in the documents that are not in the Genre Matrix were not used as genres (for example Absurdist Fiction, Creepypasta, Dark Academia, Erotic Horror). They appear on the model cards as cross-genre roles.

# Routing · AJ Solomon to Ch'an Lee

One table per pen name: each row is a Genre Matrix path, followed by the models for that path, grouped by role. `#n` is where that subgenre sits on the model's own best-fit list. See the Overview tab for the full key.

## AJ Solomon

Primary Genre: Literary Fiction · 5 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Western | American Renaissance Literature | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Western | Cultural History | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Western | Fiction with a Strong Sense of Place | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Western | Revisionist Western | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W56 #5 | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Western | Western Drama | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | W26 #6 (Voice pastiche; Jack Schaefer style) | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W56 | `Cydonia-24B-v4.1` | The roster's Dungeon Master | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Amos Trevelyan

Primary Genre: Nonfiction · 9 Genre Matrix rows

No model in the roster is assigned to any of this pen name's Genre Matrix rows.

## Anais Amaris

Primary Genre: Literary Fiction · 2 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Adventure | Speculative Historical Fiction | W71 #1 (Polaris lineage) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W16 #2 · W19 #2 · W40 #3 · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W12 #4 · W23 #4 · W72 #4 · W45 #6 | — | C03 #3 (Worldbuilding, Divergence planning) · C06 #3 (Worldbuilding, Divergence planning) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Adventure | Epic Poetry | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C03 | `LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL` | Pocket scope planner | Featherless AI (32,768 tokens) |
| C06 | `Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking` | Early-alpha wide-lens planner | Featherless AI (32,768 tokens) |
| W12 | `Goetia-26B-A4B-v1.6` | Broad-knowledge literary workhorse | Featherless AI (32,768 tokens) |
| W16 | `Gemma3-27B-it-vl-Polaris-HI16-Heretic-Uncensored-INSTRUCT` | Literary reasoning writer | Featherless AI (32,768 tokens) |
| W19 | `gemma-3-12b-it-vl-Gemini-3-Pro-Preview-Heretic-Uncensored-Thinking` | Timeline-sweep writer | Featherless AI (32,768 tokens) |
| W23 | `gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking` | Puzzle and timeline reasoner | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W45 | `Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess` | Book-scale writer-thinker | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Anya Amara

Primary Genre: Literary Fiction, YA, YA (Graphic Novel) · 4 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Adventure | Coming-of-Age Epic | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W52 #3 (Episodic use) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Romance | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Science Fiction (Sci-Fi) | Horror | Apocalyptic | — | W62 #7 (Short-form) | — | C03 (Worldbuilding, Transition planning) · C06 (Worldbuilding, Transition planning) |

**Rows with no model (1):** Fantasy > Romance > Mythopoeia

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C03 | `LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL` | Pocket scope planner | Featherless AI (32,768 tokens) |
| C06 | `Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking` | Early-alpha wide-lens planner | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W52 | `UnslopNemo-12B-v3` | Prose stylist with a bad memory | Featherless AI (32,768 tokens) |
| W62 | `L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` | Dark-bias scene writer | Featherless AI (8,192 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## August Reinhardt

Primary Genre: Drama · 17 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Drama | Romantic Comedy | — | W68 #2 | W06 #1 (Christina Lauren style) | — | C05 (Premise generation, Premises) · W05 (short-form writer, Short-form) · W26 (short-form writer) |
| Drama | Tragicomedy | — | — | W44 #2 (Short) | — | — |

**Rows with no model (15):** Drama > Absurdist Drama; Drama > Black Comedy; Drama > Classical Tragedy; Drama > Comedy of Manners; Drama > Documentary Theatre; Drama > Epic Theatre; Drama > Farce; Drama > History Play; Drama > Melodrama; Drama > Modern Tragedy; Drama > Morality Play; Drama > Musical Theatre; Drama > Mystery Play; Drama > Revenge Tragedy; Drama > Satirical

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W44 | `Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` | Pocket attitude storyteller | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |

## Avery Lee

Primary Genre: Literary Fiction, YA, YA (Graphic Novel) · 7 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Comedy | Cozy Fiction | W52 #4 | W69 #2 · W02 #3 (Vignettes) · W01 #5 (Vignettes) · W26 #5 (Short) · W06 #10 (Whimsical vignettes) | — | — |
| Fantasy | Comedy | Animal Fiction | — | W04 #4 (Jack London style) · W05 #4 (Jack London style) · W06 #6 · W03 | — | — |
| Fantasy | Comedy | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Science Fiction (Sci-Fi) | Comedy | Parody | — | W02 #4 (Light; Mark Twain style) · W44 #5 (Short) | — | — |
| Science Fiction (Sci-Fi) | Thriller | Noir Fiction | W31 #1 (Terse default) · W71 #3 (Uncensored) | W66 #4 (Short) | — | W33 |

**Rows with no model (2):** Fantasy > Comedy > Mythopoeia; Fantasy > Comedy > Satirical Fantasy

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| W01 | `gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Edge voice sketcher | Local (Unsloth Desktop) |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W31 | `Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking` | Dual-mind arguer | Featherless AI (32,768 tokens) |
| W33 | `Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking` | Philip K | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W44 | `Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` | Pocket attitude storyteller | Featherless AI (32,768 tokens) |
| W52 | `UnslopNemo-12B-v3` | Prose stylist with a bad memory | Featherless AI (32,768 tokens) |
| W66 | `Llama-3.2-3B-Instruct-uncensored` | 3B abliteration, second build | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |
| W69 | `LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF` | Cozy series engine | Local (GGUF from Hugging Face) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |

## Bastien Benoit

Primary Genre: Literary Fiction · 17 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Adventure | Epic Sagas | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W12 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | C09 #2 (Series continuity) · C03 #4 (Worldbuilding, Multi-generational structure) · C06 #4 (Worldbuilding, Multi-generational structure) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Fantasy | Adventure | Asian-Inspired-Oriental Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Cosmic Nautical Metafiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Mystery | Occult Detective | W60 #2 · W41 #7 (Visual arcana: grimoire OCR, ritual-site imagery) · W46 #8 | — | — | — |
| Fantasy | Mystery | Paranormal Cozy Mystery | — | W63 #5 | — | — |
| Fantasy | Mystery | Supernatural Mystery | W49 #8 | — | — | — |
| Fantasy | Thriller | Supernatural Thriller | — | — | C02 #6 (Planning, Rules and reveal schedule) | — |
| Fantasy | Mystery | Cozy Witch Mysteries | — | W63 #5 | — | — |

**Rows with no model (9):** Fantasy > Mystery > Fantasy Noir; Fantasy > Mystery > Gaslamp Fantasy; Fantasy > Thriller > Magical Political Intrigue; Fantasy > Mystery > Magical Realism Fantasy; Fantasy > Mystery > Paranormal Mystery; Fantasy > Mystery > Spiritual-Mystical Fiction; Fantasy > Mystery > Supernatural Noir; Fantasy > Mystery > Urban Fantasy Mystery; Fantasy > Mystery > Paranormal Cozy Mysteries with Animals

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C02 | `LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL` | Pocket hybrid planner | Featherless AI (32,768 tokens) |
| C03 | `LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL` | Pocket scope planner | Featherless AI (32,768 tokens) |
| C06 | `Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking` | Early-alpha wide-lens planner | Featherless AI (32,768 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W12 | `Goetia-26B-A4B-v1.6` | Broad-knowledge literary workhorse | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W41 | `Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` | Wide-lens visual analyst | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W60 | `Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning` | Structured dark planner-writer | Featherless AI (8,192 tokens) |
| W63 | `Hathor_Tahsin-L3-8B-v0.85` | Persona engine | Featherless AI (8,192 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Beatrix Holm

Primary Genre: Nonfiction · 8 Genre Matrix rows

No model in the roster is assigned to any of this pen name's Genre Matrix rows.

## Bree Beaumont

Primary Genre: Literary Fiction, YA, YA (Graphic Novel) · 5 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Romance | Poetry-Prose Hybrid | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Science Fiction (Sci-Fi) | Thriller | Faustian Saga | W14 #4 | W47 #3 (Short) · W15 #5 · W46 #7 (Short) | — | W70 (The bargain as ongoing RP) |
| Fantasy | Horror | Folk Horror | W10 #3 | W42 #4 · W66 #5 (Short) | — | W41 (Ritual-site analysis) · W43 (short-form writer, Short) · W49 · W60 |

**Rows with no model (1):** Science Fiction (Sci-Fi) > Romance > YA Dystopian Romance

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| W10 | `gemma-4-31B-it-Grand-Horror-X-INTENSE-HERETIC-UNCENSORED-Thinking` | Full-intensity horror | Featherless AI (32,768 tokens) |
| W14 | `Goetia-26B-A4B-v1.3-Absolute-Heretic-ARA` | Transgressive specialist | Featherless AI (32,768 tokens) |
| W15 | `Shadow-Siren-26B-A4B` | Dark-seduction character engine | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W41 | `Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` | Wide-lens visual analyst | Featherless AI (32,768 tokens) |
| W42 | `Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B` | Horror-tainted engine | Local (Unsloth Desktop) |
| W43 | `Qwen3-Horror-Instruct-Uncensored-262K-ctx-4B` | Pocket horror engine | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W60 | `Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning` | Structured dark planner-writer | Featherless AI (8,192 tokens) |
| W66 | `Llama-3.2-3B-Instruct-uncensored` | 3B abliteration, second build | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |
| W70 | `Rocinante-X-12B-v1-Heretic-Uncensored` | Long-session character engine | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Callum Reid

Primary Genre: Poetry · 5 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Narrative & Epic Poetry | Dramatic Monologue | — | W31 #8 (Combative speaker) | W01 #1 (Short) · W04 #1 · W05 #1 · W28 #2 (Short) · W06 #3 · W07 #4 (Unhinged mode) · W26 #4 · W03 | C01 #4 (Planning, Structural support) | W77 (short-form writer, Unhinged speaker, short) |

**Rows with no model (4):** Narrative & Epic Poetry > Ballad; Narrative & Epic Poetry > Heroic Epic; Narrative & Epic Poetry > Mock Epic; Narrative & Epic Poetry > Narrative Poetry

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| W01 | `gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Edge voice sketcher | Local (Unsloth Desktop) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W07 | `gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Manic escalation wildcard | Local (Unsloth Desktop) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W28 | `Qwen3.5-4B-Deckard-HERETIC-UNCENSORED-Thinking` | Pocket DECKARD | Featherless AI (32,768 tokens) |
| W31 | `Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking` | Dual-mind arguer | Featherless AI (32,768 tokens) |
| W77 | `Qwen3.6-9B-Heretic-Uncensored-Thinking-Sweet-Madness` | Surrealist instrument | Featherless AI (32,768 tokens) |

## Carys Cassian

Primary Genre: Literary Fiction, YA, YA (Graphic Novel) · 9 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Science Fiction | Adventure | Speculative Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W46 #4 (Black Mirror-style anthology) | — | C05 #1 (Premise generation, Premises and twist shorts) · C09 #4 (Series continuity, Anthology-series planning) · C02 #5 (Premise generation, Premise stress-testing) · W38 #8 (Ethical-dilemma episode structure) | — |
| Contemporary Literary Fiction | Adventure | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Historical Fiction | Adventure | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Fantasy | Adventure | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Science Fiction (Sci-Fi) | Adventure | Dystopian | — | — | — | C01 (Planning, YA resistance planning) |
| Contemporary Literary Fiction | Thriller | Psychological Thriller-Suspense | W48 #2 | W07 #3 (Unreliable-narrator mode) · W62 #3 | C05 #4 (Planning, Short) | W47 |

**Rows with no model (3):** Fantasy > Adventure > Mythopoeia; Fantasy > Adventure > Mythology Retold; Fantasy > Horror > Religious Fiction

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| C02 | `LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL` | Pocket hybrid planner | Featherless AI (32,768 tokens) |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W07 | `gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Manic escalation wildcard | Local (Unsloth Desktop) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W38 | `Qwen3.5-9B-Star-Trek-TNG-DS9-Heretic-Uncensored-Thinking` | Star Trek canon voice | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W48 | `Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus` | Vivid crime and horror scene writer | Featherless AI (32,768 tokens) |
| W62 | `L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` | Dark-bias scene writer | Featherless AI (8,192 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Cassidy Cavendish

Primary Genre: Literary Fiction (Adult Comics), YA, YA (Graphic Novel) · 13 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Thriller | Crime Noir | W13 #5 | W65 #2 (Short) · W02 #5 (conditional: Directed dark vignettes) · W62 #5 (Short-form) | — | — |
| Contemporary Literary Fiction | Mystery | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Historical Fiction | Mystery | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Science Fiction (Sci-Fi) | Mystery | Dystopian | — | — | — | C01 (Planning, YA resistance planning) |
| Historical Fiction | Adventure | Dystopian | — | — | — | C01 (Planning, YA resistance planning) |
| Contemporary Literary Fiction | Thriller | Crime Fiction | W48 #1 (Vivid mode) · W73 #1 (Generalist) · W74 #1 · W09 #6 · W20 #6 (Forensic-heavy) | W37 #3 (Scene level; deduction carried implicitly) · W36 #4 (Scene level; deduction carried implicitly) | — | — |

**Rows with no model (7):** Contemporary Literary Fiction > Horror > Supernatural Horror; Contemporary Literary Fiction > Mystery > Amateur Sleuth; Contemporary Literary Fiction > Mystery > Mystery-Detective; Fantasy > Mystery > Mythopoeia; Historical Fiction > Adventure > Mythopoeia; Historical Fiction > Mystery > Mythopoeia; Contemporary Literary Fiction > Mystery > Spies

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W09 | `gemma-4-31B-it-Mystery-Fine-Tune-HERETIC-UNCENSORED-Thinking` | Fair-play mystery specialist | Featherless AI (32,768 tokens) |
| W13 | `Goetia-26B-A4B-v1.7` | Dark-craft and suspense build | Featherless AI (32,768 tokens) |
| W20 | `gemma-3-12b-it-vl-Deepseek-v3.1-Heretic-Uncensored-Thinking` | Investigation writer | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W36 | `Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` | 9B direct-delivery workhorse | Featherless AI (32,768 tokens) |
| W37 | `Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` | 9B direct-delivery flagship | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W48 | `Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus` | Vivid crime and horror scene writer | Featherless AI (32,768 tokens) |
| W62 | `L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` | Dark-bias scene writer | Featherless AI (8,192 tokens) |
| W65 | `Llama-3.2-3B-Instruct-abliterated` | Clean 3B abliteration | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## CeeCee Chestervale

Primary Genre: Children's Literature, Literary Fiction · 12 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Comedy | Cozy Fiction | W52 #4 | W69 #2 · W02 #3 (Vignettes) · W01 #5 (Vignettes) · W26 #5 (Short) · W06 #10 (Whimsical vignettes) | — | — |
| Fantasy | Comedy | Literary Nonsense | — | — | — | W03 (short-form writer, Children's register) · W04 (short-form writer) · W05 (short-form writer) · W26 (short-form writer) · W44 (short-form writer, The drift suits it) |

**Rows with no model (10):** Contemporary Literary Fiction > Adventure > Chapter Books; Contemporary Literary Fiction > Adventure > Children's Story; Contemporary Literary Fiction > Comedy > Contemporary Middle Grade; Contemporary Literary Fiction > Adventure > Early Readers; Contemporary Literary Fiction > Adventure > Middle Grade; Contemporary Literary Fiction > Adventure > Middle-Grade Contemporary Adventure; Fantasy > Adventure > Middle-Grade Fantasy; Contemporary Literary Fiction > Mystery > Middle-Grade Mystery; Contemporary Literary Fiction > Adventure > Picture Books; Contemporary Literary Fiction > Comedy > School Stories

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| W01 | `gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Edge voice sketcher | Local (Unsloth Desktop) |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W44 | `Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` | Pocket attitude storyteller | Featherless AI (32,768 tokens) |
| W52 | `UnslopNemo-12B-v3` | Prose stylist with a bad memory | Featherless AI (32,768 tokens) |
| W69 | `LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF` | Cozy series engine | Local (GGUF from Hugging Face) |

## Ch'an Lee

Primary Genre: Literary Fiction, Literary Fiction (Adult Comics) · 51 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Fantasy | Adventure | Adventure Fantasy | W56 #1 · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W11 #5 (Run interactively) | — | — | — |
| Fantasy | Adventure | Angel Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Arthurian Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Dark/Rogue Epic Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W14 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W64 #4 | — | — | — |
| Fantasy | Adventure | Demon Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Dragon Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Elves & Fae Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Epic Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Epic Quest Fantasy | W56 #1 · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W11 #5 (Run interactively) | — | C09 #2 (Series continuity) | — |
| Fantasy | Adventure | Epic Sagas | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W12 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | C09 #2 (Series continuity) · C03 #4 (Worldbuilding, Multi-generational structure) · C06 #4 (Worldbuilding, Multi-generational structure) | — |
| Fantasy | Adventure | Exploration Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W50 #3 · W51 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W19 #4 (Reads maps) | — | — | C03 (Worldbuilding, Map logic) · W49 |
| Fantasy | Adventure | Folklore-Inspired Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | C03 (Worldbuilding) · C06 (Worldbuilding) |
| Fantasy | Adventure | Ghost Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Gods & Goddesses Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Heroic Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | High Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W12 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Historical Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Literary Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W12 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Low Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Magic | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Martial Arts Fiction (Wuxia) | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Metaphysical & Visionary | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Metaphysical Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Modern Mythological Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Mythic Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Mythic Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Nautical Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W50 #3 · W51 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W49 |
| Fantasy | Adventure | Norse & Viking Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Oriental Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Philosphical Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Portal Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Psychic Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Revisionist Fairy Tales | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Science Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Silkpunk | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Social Justice Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Space Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Steampunk | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | C03 (Worldbuilding, Era consistency) · C06 (Worldbuilding, Era consistency) |
| Fantasy | Adventure | Steampunk Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Superhero | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | C05 (Premise generation, Concepts) · W61 (layer specialist, Worldbuilding) |
| Fantasy | Adventure | Superhero Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Survival Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Sword & Sorcery | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W56 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Urban Fantasy | W70 #1 (Investigator held across a long case) · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W47 #7 (Character-driven) | — | — | C07 (Evidence reading, Evidence triage) · C08 (Evidence reading, Evidence work) · W28 (short-form writer, Character scenes with visual evidence) · W36 (short-form writer, Character scenes) · W37 (short-form writer, Character scenes) · W46 (Investigator stories) |
| Fantasy | Adventure | Urban Mythopoeia | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Vampire Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W42 (short-form writer, Non-romance mode) · W43 (short-form writer, Non-romance) · W62 (short-form writer, Non-romance) |
| Fantasy | Adventure | Werewolf & Shifter Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Witch & Wizard Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Wuxia Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Adventure | Xianxia Fantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Erotic Manga | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C03 | `LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL` | Pocket scope planner | Featherless AI (32,768 tokens) |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| C06 | `Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking` | Early-alpha wide-lens planner | Featherless AI (32,768 tokens) |
| C07 | `Qwen3.5-2B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Pocket evidence reader | Featherless AI (32,768 tokens) |
| C08 | `Qwen3.5-4B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Complete small pipeline | Featherless AI (32,768 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W11 | `Pantheon-Reasoning-31B-1.1` | Plot-architecture writer | Featherless AI (32,768 tokens) |
| W12 | `Goetia-26B-A4B-v1.6` | Broad-knowledge literary workhorse | Featherless AI (32,768 tokens) |
| W14 | `Goetia-26B-A4B-v1.3-Absolute-Heretic-ARA` | Transgressive specialist | Featherless AI (32,768 tokens) |
| W19 | `gemma-3-12b-it-vl-Gemini-3-Pro-Preview-Heretic-Uncensored-Thinking` | Timeline-sweep writer | Featherless AI (32,768 tokens) |
| W28 | `Qwen3.5-4B-Deckard-HERETIC-UNCENSORED-Thinking` | Pocket DECKARD | Featherless AI (32,768 tokens) |
| W36 | `Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` | 9B direct-delivery workhorse | Featherless AI (32,768 tokens) |
| W37 | `Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` | 9B direct-delivery flagship | Featherless AI (32,768 tokens) |
| W42 | `Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B` | Horror-tainted engine | Local (Unsloth Desktop) |
| W43 | `Qwen3-Horror-Instruct-Uncensored-262K-ctx-4B` | Pocket horror engine | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W50 | `UnslopNemo-12B-v4.1` | Anti-slop workhorse | Featherless AI (32,768 tokens) |
| W51 | `UnslopNemo-12B-v4` | Backup to UnslopNemo v4 | Featherless AI (32,768 tokens) |
| W56 | `Cydonia-24B-v4.1` | The roster's Dungeon Master | Featherless AI (32,768 tokens) |
| W61 | `Llama-3.3-8B-Thinking-Gemini-Flash-11000x-128k` | Systems and scope planner | Featherless AI (8,192 tokens) |
| W62 | `L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` | Dark-bias scene writer | Featherless AI (8,192 tokens) |
| W64 | `Legion-V2.1-LLaMa-70B-Elarablated-v0.8` | Dark-literary heavyweight | Featherless AI (32,768 tokens) |
| W70 | `Rocinante-X-12B-v1-Heretic-Uncensored` | Long-session character engine | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

# Routing · Christine Leigh to Eulalie Rowland

One table per pen name: each row is a Genre Matrix path, followed by the models for that path, grouped by role. `#n` is where that subgenre sits on the model's own best-fit list. See the Overview tab for the full key.

## Christine Leigh

Primary Genre: Literary Fiction · 55 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Drama | Psychological Realism | W72 #10 (Dark side of realism) | — | — | — |
| Contemporary Literary Fiction | Romance | African American Literature | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Beach Reads | W53 #1 · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W26 #1 | — | — |
| Contemporary Literary Fiction | Romance | Christian Literature | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Contemporary Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W37 #5 · W36 #6 | — | — | — |
| Contemporary Literary Fiction | Romance | Contemporary Women's Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W68 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W54 #4 | — | — | W70 (Relationship-driven) |
| Contemporary Literary Fiction | Romance | Cross-Cultural Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W54 #5 | — | — | — |
| Historical Fiction | Romance | Cultural Heritage Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | East Asian Historical Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Edwardian Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Romance | Erotic Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W27 #1 · W71 #4 (conditional: Directed) · W74 #4 (conditional: Directed) · W26 #7 (conditional: Directed; Nin and Miller style) | — | W46 (conditional, Directed) |
| Historical Fiction | Romance | Erotic Literature | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W64 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W27 #3 (Period manners, formal craft) | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Romance | Erotic Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W27 #2 · W70 #4 (conditional: Directed) · W26 #7 (conditional: Directed) | — | W47 (conditional, Directed) |
| Fantasy | Romance | Fairy Tales | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W03 (short-form writer) · W04 (short-form writer) · W05 (short-form writer) |
| Contemporary Literary Fiction | Romance | Fairy Tales Retellings | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W03 (short-form writer) · W04 (short-form writer) · W05 (short-form writer) · W26 (short-form writer) · W44 (short-form writer, Crooked retellings) |
| Historical Fiction | Romance | Family Saga | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W55 #4 · W12 #6 | — | C09 #1 (Series continuity, Series architecture) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Romance | Feel-Good Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W52 #4 · W54 #4 | W69 #4 | — | — |
| Science Fiction | Romance | Futuristic Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Historical Fiction | Romance | Generational Stories | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W12 #6 | — | W19 #5 (Structural work) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Gothic Romance | W55 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W14 #4 (Pushed dark) · W47 #5 | W42 #7 (conditional: Dark mode only) · W70 #8 (Short-form) | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Historical Christian Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Historical Drama | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) · W40 · W72 |
| Historical Fiction | Romance | Historical Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W55 #5 | — | — | W26 (short-form writer) · W30 (Period prose. Secondary Genre level; whole Secondary level) · W36 (short-form writer, Period scenes) · W37 (short-form writer, Period scenes) |
| Contemporary Literary Fiction | Romance | Inspirational Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | LGBTQ+ Literature | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W54 #5 | — | — | — |
| Historical Fiction | Romance | Literary Fiction Set in the Past | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) · W40 |
| Contemporary Literary Fiction | Romance | Literary Romance | W54 #1 · W68 #1 · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W36 #2 · W30 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W37 #7 | — | — | — |
| Historical Fiction | Romance | Medieval Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Fantasy | Romance | Modern Fairy Tales | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Multi-Cultural Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Historical Fiction | Romance | Multi-Generational Saga | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W55 #4 | — | C09 #1 (Series continuity, Series architecture) · W19 #5 (Structural work) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Romance | New Adult Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W53 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W49 #6 | W26 #1 · W70 #4 (conditional: Directed) | — | — |
| Contemporary Literary Fiction | Romance | New Adult Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W49 #6 | W26 #1 | — | — |
| Fantasy | Romance | Paranormal Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W55 #3 · W70 #3 (Dark mode) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W47 #4 (Dark) · W68 #4 | W63 #1 · W15 #5 (Dark end) | — | W46 |
| Historical Fiction | Romance | Pastoral Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Period Drama | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Regency Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W12 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W55 #5 | — | — | W26 (short-form writer) · W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Romance | Romantic Drama | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W36 #2 · W54 #2 · W30 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W37 #7 | — | — | — |
| Contemporary Literary Fiction | Romance | Romantic Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Historical Fiction | Romance | Romantic Literature | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Romance | Romantic Social Commentary | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Historical Fiction | Romance | Romanticism | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Science Fiction | Romance | Science Fiction Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Sensual Romance | W53 #1 · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W49 #6 | W26 #1 · W27 #4 · W70 #4 (conditional: Directed) | — | — |
| Contemporary Literary Fiction | Romance | Small Town Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Science Fiction | Romance | Speculative Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Spiritual-Religious Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W33 #10 (Gnostic mode) | — | — | — |
| Contemporary Literary Fiction | Romance | Sweet Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Upmarket Women's Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 |
| Historical Fiction | Romance | Upstairs-Downstairs Drama | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W55 #4 | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Fantasy | Romance | Urban Fantasy Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W63 #4 | — | — |
| Historical Fiction | Romance | Victorian Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W12 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W55 #5 | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Victorian Literature | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W12 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Victorian/Regency Period Drama | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Romance | Women's Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W37 #5 · W36 #6 | — | — | — |

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W12 | `Goetia-26B-A4B-v1.6` | Broad-knowledge literary workhorse | Featherless AI (32,768 tokens) |
| W14 | `Goetia-26B-A4B-v1.3-Absolute-Heretic-ARA` | Transgressive specialist | Featherless AI (32,768 tokens) |
| W15 | `Shadow-Siren-26B-A4B` | Dark-seduction character engine | Featherless AI (32,768 tokens) |
| W19 | `gemma-3-12b-it-vl-Gemini-3-Pro-Preview-Heretic-Uncensored-Thinking` | Timeline-sweep writer | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W27 | `Dirty-Muse-Writer-v01-Uncensored-Erotica-NSFW` | Explicit-literary specialist | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W33 | `Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking` | Philip K | Featherless AI (32,768 tokens) |
| W36 | `Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` | 9B direct-delivery workhorse | Featherless AI (32,768 tokens) |
| W37 | `Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` | 9B direct-delivery flagship | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W42 | `Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B` | Horror-tainted engine | Local (Unsloth Desktop) |
| W44 | `Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` | Pocket attitude storyteller | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W52 | `UnslopNemo-12B-v3` | Prose stylist with a bad memory | Featherless AI (32,768 tokens) |
| W53 | `UnslopNemo-12B-v1` | Obedient synopsis executor | Featherless AI (32,768 tokens) |
| W54 | `MN-Violet-Lotus-12B` | Emotional-intelligence specialist | Featherless AI (32,768 tokens) |
| W55 | `MN-Crimson-Cafe-12B` | Atmospheric ensemble storyteller | Featherless AI (32,768 tokens) |
| W63 | `Hathor_Tahsin-L3-8B-v0.85` | Persona engine | Featherless AI (8,192 tokens) |
| W64 | `Legion-V2.1-LLaMa-70B-Elarablated-v0.8` | Dark-literary heavyweight | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |
| W69 | `LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF` | Cozy series engine | Local (GGUF from Hugging Face) |
| W70 | `Rocinante-X-12B-v1-Heretic-Uncensored` | Long-session character engine | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## D'Annie de Leon

Primary Genre: Literary Fiction, Literary Fiction (Adult Comics) · 6 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Romance | Highlander Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Pirate Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Royalty Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Viking Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Western Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Romance | Erotica | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W27 #3 | — | — |

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| W27 | `Dirty-Muse-Writer-v01-Uncensored-Erotica-NSFW` | Explicit-literary specialist | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Deon D'Arcy

Primary Genre: Literary Fiction · 68 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Hybrid Drama | Social Realism | — | — | — | W40 |
| Contemporary Literary Fiction | Romance | African American Literature | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Beach Reads | W53 #1 · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W26 #1 | — | — |
| Contemporary Literary Fiction | Romance | Christian Literature | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Contemporary Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W37 #5 · W36 #6 | — | — | — |
| Contemporary Literary Fiction | Romance | Contemporary Women's Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W68 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W54 #4 | — | — | W70 (Relationship-driven) |
| Contemporary Literary Fiction | Romance | Cross-Cultural Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W54 #5 | — | — | — |
| Contemporary Literary Fiction | Romance | Domestic Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W40 |
| Contemporary Literary Fiction | Romance | Erotic Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W27 #1 · W71 #4 (conditional: Directed) · W74 #4 (conditional: Directed) · W26 #7 (conditional: Directed; Nin and Miller style) | — | W46 (conditional, Directed) |
| Contemporary Literary Fiction | Romance | Erotic Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W27 #2 · W70 #4 (conditional: Directed) · W26 #7 (conditional: Directed) | — | W47 (conditional, Directed) |
| Fantasy | Romance | Fairy Tales | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W03 (short-form writer) · W04 (short-form writer) · W05 (short-form writer) |
| Contemporary Literary Fiction | Romance | Fairy Tales Retellings | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W03 (short-form writer) · W04 (short-form writer) · W05 (short-form writer) · W26 (short-form writer) · W44 (short-form writer, Crooked retellings) |
| Contemporary Literary Fiction | Romance | Feel-Good Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W52 #4 · W54 #4 | W69 #4 | — | — |
| Contemporary Literary Fiction | Romance | Feminist Literature | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W67 #4 | — | — | — |
| Contemporary Literary Fiction | Romance | Inspirational Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | LGBTQ+ Literature | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W54 #5 | — | — | — |
| Contemporary Literary Fiction | Romance | Literary Romance | W54 #1 · W68 #1 · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W36 #2 · W30 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W37 #7 | — | — | — |
| Fantasy | Romance | Modern Fairy Tales | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Multi-Cultural Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | New Adult Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W53 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W49 #6 | W26 #1 · W70 #4 (conditional: Directed) | — | — |
| Contemporary Literary Fiction | Romance | New Adult Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W49 #6 | W26 #1 | — | — |
| Fantasy | Romance | Paranormal Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W55 #3 · W70 #3 (Dark mode) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W47 #4 (Dark) · W68 #4 | W63 #1 · W15 #5 (Dark end) | — | W46 |
| Contemporary Literary Fiction | Romance | Romantic Drama | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W36 #2 · W54 #2 · W30 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W37 #7 | — | — | — |
| Contemporary Literary Fiction | Romance | Romantic Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Romantic Social Commentary | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Sensual Romance | W53 #1 · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W49 #6 | W26 #1 · W27 #4 · W70 #4 (conditional: Directed) | — | — |
| Contemporary Literary Fiction | Romance | Small Town Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Spiritual-Religious Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W33 #10 (Gnostic mode) | — | — | — |
| Contemporary Literary Fiction | Romance | Sweet Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Upmarket Women's Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 |
| Fantasy | Romance | Urban Fantasy Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W63 #4 | — | — |
| Fantasy | Romance | Cozy Fantasy Monster Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Romance | Cozy Fantasy Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W50 #4 | — | — | — |
| Fantasy | Romance | Angel Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Romance | Demon Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W47 #3 (Short) · W15 #5 · W46 #7 (Short) | — | W70 (The bargain as ongoing RP) |
| Fantasy | Romance | Ghost Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Romance | Greek Mythology Romantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Romance | Psychic Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Romance | Romantasy | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W68 #4 | W63 #3 | — | — |
| Fantasy | Romance | Time Travel Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Romance | Vampire Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W55 #3 · W70 #3 (Dark mode) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W47 #4 (Dark) | W15 #3 | — | W46 |
| Fantasy | Romance | Werewolf & Shifter Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W63 #2 | — | W47 · W70 |
| Fantasy | Romance | Witch & Wizard Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W63 #4 | — | — |
| Contemporary Literary Fiction | Romance | Women's Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W37 #5 · W36 #6 | — | — | — |
| Contemporary Literary Fiction | Romance | Amish Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Amnesia Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Beach Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Billionaire Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Clean & Wholesome Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Cowboy Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Dark Romance | W47 #1 · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W14 #2 · W70 #2 (12B pick) · W46 #3 (Planned arc) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W15 #1 · W66 #2 (Short) · W71 #4 (conditional: Directed) · W74 #4 (conditional: Directed) · W27 #5 · W62 #6 (Short-form, directed) · W42 #7 (conditional: Dark mode only) · W49 #7 (Short) · W43 #8 (Dark mode, short) | — | C09 (Series continuity, Arc compounding across a series) · W48 (short-form writer, Short-form) |
| Contemporary Literary Fiction | Romance | Firefighter Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Gambling Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Holiday Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Love Triangle Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W54 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W53 #4 | — | — | — |
| Contemporary Literary Fiction | Romance | Mafia Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W47 #2 · W70 #2 (12B pick) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W15 #2 · W27 #5 | — | W46 |
| Contemporary Literary Fiction | Romance | Medical Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W36 · W37 |
| Contemporary Literary Fiction | Romance | Military Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Multi-cultural Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Multicultural & Interracial Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Political Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W57 #4 · W16 #6 | — | — | — |
| Contemporary Literary Fiction | Romance | Second Chance Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W54 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W53 #4 | — | — | — |
| Contemporary Literary Fiction | Romance | Secret Baby Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Sports Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Spy Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Vacation Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W53 #4 | — | — | — |
| Contemporary Literary Fiction | Romance | Wedding Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Romance | Workplace Romance | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W14 | `Goetia-26B-A4B-v1.3-Absolute-Heretic-ARA` | Transgressive specialist | Featherless AI (32,768 tokens) |
| W15 | `Shadow-Siren-26B-A4B` | Dark-seduction character engine | Featherless AI (32,768 tokens) |
| W16 | `Gemma3-27B-it-vl-Polaris-HI16-Heretic-Uncensored-INSTRUCT` | Literary reasoning writer | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W27 | `Dirty-Muse-Writer-v01-Uncensored-Erotica-NSFW` | Explicit-literary specialist | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W33 | `Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking` | Philip K | Featherless AI (32,768 tokens) |
| W36 | `Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` | 9B direct-delivery workhorse | Featherless AI (32,768 tokens) |
| W37 | `Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` | 9B direct-delivery flagship | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W42 | `Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B` | Horror-tainted engine | Local (Unsloth Desktop) |
| W43 | `Qwen3-Horror-Instruct-Uncensored-262K-ctx-4B` | Pocket horror engine | Featherless AI (32,768 tokens) |
| W44 | `Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` | Pocket attitude storyteller | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W48 | `Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus` | Vivid crime and horror scene writer | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W50 | `UnslopNemo-12B-v4.1` | Anti-slop workhorse | Featherless AI (32,768 tokens) |
| W52 | `UnslopNemo-12B-v3` | Prose stylist with a bad memory | Featherless AI (32,768 tokens) |
| W53 | `UnslopNemo-12B-v1` | Obedient synopsis executor | Featherless AI (32,768 tokens) |
| W54 | `MN-Violet-Lotus-12B` | Emotional-intelligence specialist | Featherless AI (32,768 tokens) |
| W55 | `MN-Crimson-Cafe-12B` | Atmospheric ensemble storyteller | Featherless AI (32,768 tokens) |
| W57 | `Dolphin-Mistral-24B-Venice-Edition` | Utility infielder | Featherless AI (32,768 tokens) |
| W62 | `L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` | Dark-bias scene writer | Featherless AI (8,192 tokens) |
| W63 | `Hathor_Tahsin-L3-8B-v0.85` | Persona engine | Featherless AI (8,192 tokens) |
| W66 | `Llama-3.2-3B-Instruct-uncensored` | 3B abliteration, second build | Featherless AI (32,768 tokens) |
| W67 | `ERNIE-21B-A3B-Claude-4.5-High-OPUS-Thinking` | Philosopher twin | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |
| W69 | `LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF` | Cozy series engine | Local (GGUF from Hugging Face) |
| W70 | `Rocinante-X-12B-v1-Heretic-Uncensored` | Long-session character engine | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Drew D'Angelo

Primary Genre: YA, YA (Graphic Novel) · 9 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Fantasy | Horror | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Science Fiction (Sci-Fi) | Thriller | Dystopian | — | — | — | C01 (Planning, YA resistance planning) |
| Fantasy | Horror | Dystopian | — | — | — | C01 (Planning, YA resistance planning) |
| Science Fiction (Sci-Fi) | Thriller | Space Opera | W12 #5 · W41 #6 (Series-scale politics) | — | C09 #3 (Series continuity, Series politics) · C03 #7 (Series continuity, Continuity) · C06 #7 (Series continuity, Continuity) | — |
| Science Fiction (Sci-Fi) | Thriller | Dystopian | — | — | — | C01 (Planning, YA resistance planning) |
| Science Fiction (Sci-Fi) | Thriller | Alien Science Fiction | — | — | — | W38 (Truly foreign minds) |

**Rows with no model (3):** Fantasy > Horror > Mythopoeia; Fantasy > Horror > Dark Fantasy; Fantasy > Thriller > YA Academy Fantasy

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| C03 | `LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL` | Pocket scope planner | Featherless AI (32,768 tokens) |
| C06 | `Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking` | Early-alpha wide-lens planner | Featherless AI (32,768 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W12 | `Goetia-26B-A4B-v1.6` | Broad-knowledge literary workhorse | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W38 | `Qwen3.5-9B-Star-Trek-TNG-DS9-Heretic-Uncensored-Thinking` | Star Trek canon voice | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W41 | `Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` | Wide-lens visual analyst | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |

## Ellis Leigh

Primary Genre: Literary Fiction · 30 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Fantasy | Comedy | Animal Fiction | — | W04 #4 (Jack London style) · W05 #4 (Jack London style) · W06 #6 · W03 | — | — |
| Contemporary Literary Fiction | Comedy | Chick-Lit | W53 #3 | — | — | — |
| Contemporary Literary Fiction | Comedy | Cozy Fiction | W52 #4 | W69 #2 · W02 #3 (Vignettes) · W01 #5 (Vignettes) · W26 #5 (Short) · W06 #10 (Whimsical vignettes) | — | — |
| Contemporary Literary Fiction | Comedy | Culinary Fiction | — | W52 #5 (Literary vignettes) | — | — |
| Contemporary Literary Fiction | Comedy | Dark Comedy | W53 #5 (Light side) | W44 #2 (Short) · W07 #5 (Palahniuk and Landy styles) | — | W75 (short-form writer, Malfunctioning-machine kind) · W76 (short-form writer, Non-sequitur kind) · W77 (short-form writer, Absurdist kind) |
| Fantasy | Comedy | Fable | W45 #5 · W67 #5 | W02 #2 (Short) · W01 #3 (Short) · W04 #3 (Moore and Gaiman; Andersen styles) · W05 #3 · W44 #3 (conditional: Twisted mode) · W06 #5 · W07 #8 (Dark mode; Moore and Gaiman style) · W03 | — | — |
| Contemporary Literary Fiction | Comedy | General Literary Fiction | W30 #1 · W71 #1 (Polaris lineage) · W40 #2 · W16 #3 (Enright and Ishiguro style) · W12 #6 · W72 #9 | W69 #5 | — | — |
| Contemporary Literary Fiction | Comedy | Horror Comedy | — | W43 #4 (Dark) · W07 #5 (Palahniuk and Landy styles) | — | W42 (short-form writer, The thinking voice is darkly funny by default) · W44 (short-form writer, Short) |
| Contemporary Literary Fiction | Comedy | Lighthearted Women's Fiction | W53 #3 | — | — | — |
| Contemporary Literary Fiction | Comedy | Metafiction | W71 #3 · W08 #4 · W32 #4 · W33 #6 · W31 #7 (Self-aware argument) | W29 #4 (Short) · W28 #5 (Short) | — | W30 |
| Contemporary Literary Fiction | Comedy | Moral Tales | W45 #5 · W67 #5 | W02 #2 (Short) · W01 #3 (Short) · W04 #3 · W05 #3 · W44 #3 (conditional: Twisted mode) · W06 #5 · W07 #8 (Dark mode) · W03 | — | — |
| Contemporary Literary Fiction | Comedy | Parody | — | W02 #4 (Light; Mark Twain style) · W44 #5 (Short) | — | — |
| Contemporary Literary Fiction | Comedy | Romantic Comedy | W68 #2 | W06 #1 (Christina Lauren style) | — | C05 (Premise generation, Premises) · W05 (short-form writer, Short-form) · W26 (short-form writer) |
| Contemporary Literary Fiction | Comedy | Satire | W31 #3 · W32 #4 · W53 #5 (Light side) | W02 #4 (Light vignettes) | — | W29 |
| Fantasy | Comedy | Cozy Fantasy | — | W69 #2 | — | — |
| Contemporary Literary Fiction | Comedy | Satirical Fiction | W08 #4 | — | — | — |
| Contemporary Literary Fiction | Comedy | Slice-of-Life Fiction | W52 #1 · W68 #3 · W70 #6 (Character mode) · W30 #7 (Literary mode) | W26 #2 (Vignettes) · W02 #3 (Vignettes) · W01 #5 (Vignettes) · W49 #5 (Short) · W69 #5 · W44 #6 (Off-kilter vignettes; anchor the tone with a system prompt) | — | W03 (short-form writer, Vignettes) · W04 (short-form writer, Vignettes) · W05 (short-form writer, Vignettes) |
| Contemporary Literary Fiction | Comedy | Tragicomedy | — | W44 #2 (Short) | — | — |

**Rows with no model (12):** Contemporary Literary Fiction > Drama > Realism; Contemporary Literary Fiction > Comedy > Contemporary Fiction with Cultural Themes; Contemporary Literary Fiction > Comedy > Cultural Narrative; Contemporary Literary Fiction > Comedy > Education Fiction; Fantasy > Comedy > Fantasy of Manners; Contemporary Literary Fiction > Comedy > Farce; Contemporary Literary Fiction > Comedy > Irish Literature; Fantasy > Comedy > Mannerpunk; Contemporary Literary Fiction > Comedy > Post-Modern Fiction; Contemporary Literary Fiction > Comedy > Post-Modernism; Fantasy > Comedy > Satirical Fantasy; Contemporary Literary Fiction > Comedy > Social Commentary

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| W01 | `gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Edge voice sketcher | Local (Unsloth Desktop) |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W07 | `gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Manic escalation wildcard | Local (Unsloth Desktop) |
| W08 | `gemma-4-31B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Voice-and-ideas flagship | Featherless AI (32,768 tokens) |
| W12 | `Goetia-26B-A4B-v1.6` | Broad-knowledge literary workhorse | Featherless AI (32,768 tokens) |
| W16 | `Gemma3-27B-it-vl-Polaris-HI16-Heretic-Uncensored-INSTRUCT` | Literary reasoning writer | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W28 | `Qwen3.5-4B-Deckard-HERETIC-UNCENSORED-Thinking` | Pocket DECKARD | Featherless AI (32,768 tokens) |
| W29 | `Qwen3.5-9B-Claude-4.6-Opus-Deckard-V4.2-Uncensored-Heretic-Thinking` | 9B DECKARD thinker on a multimodal base | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W31 | `Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking` | Dual-mind arguer | Featherless AI (32,768 tokens) |
| W32 | `Qwen3.5-21B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking` | Mid-size DECKARD flagship | Featherless AI (32,768 tokens) |
| W33 | `Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking` | Philip K | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W42 | `Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B` | Horror-tainted engine | Local (Unsloth Desktop) |
| W43 | `Qwen3-Horror-Instruct-Uncensored-262K-ctx-4B` | Pocket horror engine | Featherless AI (32,768 tokens) |
| W44 | `Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` | Pocket attitude storyteller | Featherless AI (32,768 tokens) |
| W45 | `Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess` | Book-scale writer-thinker | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W52 | `UnslopNemo-12B-v3` | Prose stylist with a bad memory | Featherless AI (32,768 tokens) |
| W53 | `UnslopNemo-12B-v1` | Obedient synopsis executor | Featherless AI (32,768 tokens) |
| W67 | `ERNIE-21B-A3B-Claude-4.5-High-OPUS-Thinking` | Philosopher twin | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |
| W69 | `LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF` | Cozy series engine | Local (GGUF from Hugging Face) |
| W70 | `Rocinante-X-12B-v1-Heretic-Uncensored` | Long-session character engine | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W75 | `Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop` | Word-slip instrument | Featherless AI (32,768 tokens) |
| W76 | `Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking` | Logic-drift instrument | Featherless AI (32,768 tokens) |
| W77 | `Qwen3.6-9B-Heretic-Uncensored-Thinking-Sweet-Madness` | Surrealist instrument | Featherless AI (32,768 tokens) |

## Eulalie Rowland

Primary Genre: Literary Fiction · 1 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Adventure | Historical Adventure | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W19 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W56 #6 | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| W19 | `gemma-3-12b-it-vl-Gemini-3-Pro-Preview-Heretic-Uncensored-Thinking` | Timeline-sweep writer | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W56 | `Cydonia-24B-v4.1` | The roster's Dungeon Master | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

# Routing · Gabby Gabriel to Naomi McNamara

One table per pen name: each row is a Genre Matrix path, followed by the models for that path, grouped by role. `#n` is where that subgenre sits on the model's own best-fit list. See the Overview tab for the full key.

## Gabby Gabriel

Primary Genre: Literary Fiction, YA, YA (Graphic Novel) · 8 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Comedy | Beach Reads | W53 #1 | W26 #1 | — | — |
| Contemporary Literary Fiction | Comedy | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Contemporary Literary Fiction | Comedy | Cozy Fiction | W52 #4 | W69 #2 · W02 #3 (Vignettes) · W01 #5 (Vignettes) · W26 #5 (Short) · W06 #10 (Whimsical vignettes) | — | — |
| Contemporary Literary Fiction | Comedy | Romantic Comedy | W68 #2 | W06 #1 (Christina Lauren style) | — | C05 (Premise generation, Premises) · W05 (short-form writer, Short-form) · W26 (short-form writer) |

**Rows with no model (4):** Contemporary Literary Fiction > Comedy > Slice-of-Life; Contemporary Literary Fiction > Comedy > Slice-of-Life; Contemporary Literary Fiction > Horror > Slice-of-Life; Contemporary Literary Fiction > Thriller > Tragicomic

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| W01 | `gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Edge voice sketcher | Local (Unsloth Desktop) |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W52 | `UnslopNemo-12B-v3` | Prose stylist with a bad memory | Featherless AI (32,768 tokens) |
| W53 | `UnslopNemo-12B-v1` | Obedient synopsis executor | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |
| W69 | `LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF` | Cozy series engine | Local (GGUF from Hugging Face) |

## Gabriel Varenne

Primary Genre: Literary Fiction · 9 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Romance | Gothic Romance | W55 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W14 #4 (Pushed dark) · W47 #5 | W42 #7 (conditional: Dark mode only) · W70 #8 (Short-form) | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Highlander Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Historical Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W55 #5 | — | — | W26 (short-form writer) · W30 (Period prose. Secondary Genre level; whole Secondary level) · W36 (short-form writer, Period scenes) · W37 (short-form writer, Period scenes) |
| Historical Fiction | Romance | Medieval Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Pirate Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Regency Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W12 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W55 #5 | — | — | W26 (short-form writer) · W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Royalty Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Viking Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Romance | Western Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| W12 | `Goetia-26B-A4B-v1.6` | Broad-knowledge literary workhorse | Featherless AI (32,768 tokens) |
| W14 | `Goetia-26B-A4B-v1.3-Absolute-Heretic-ARA` | Transgressive specialist | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W36 | `Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` | 9B direct-delivery workhorse | Featherless AI (32,768 tokens) |
| W37 | `Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` | 9B direct-delivery flagship | Featherless AI (32,768 tokens) |
| W42 | `Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B` | Horror-tainted engine | Local (Unsloth Desktop) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W55 | `MN-Crimson-Cafe-12B` | Atmospheric ensemble storyteller | Featherless AI (32,768 tokens) |
| W70 | `Rocinante-X-12B-v1-Heretic-Uncensored` | Long-session character engine | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Gia Graceville

Primary Genre: YA, YA (Graphic Novel) · 5 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Romance | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Contemporary Literary Fiction | Romance | Dystopian | — | — | — | C01 (Planning, YA resistance planning) |

**Rows with no model (3):** Contemporary Literary Fiction > Romance > Adult Comics; Contemporary Literary Fiction > Romance > Manga; Contemporary Literary Fiction > Thriller > Gender Queer

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |

## Gigi Gable

Primary Genre: YA, YA (Graphic Novel) · 5 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Romance | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |
| Contemporary Literary Fiction | Romance | Dystopian | — | — | — | C01 (Planning, YA resistance planning) |
| Contemporary Literary Fiction | Thriller | Culinary Fiction | — | W52 #5 (Literary vignettes) | — | — |

**Rows with no model (2):** Contemporary Literary Fiction > Romance > Adult Comics; Contemporary Literary Fiction > Romance > Manga

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W52 | `UnslopNemo-12B-v3` | Prose stylist with a bad memory | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |

## H.J. Hakimi

Primary Genre: Literary Fiction · 10 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Science Fiction (Sci-Fi) | Adventure | Speculative Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W46 #4 (Black Mirror-style anthology) | — | C05 #1 (Premise generation, Premises and twist shorts) · C09 #4 (Series continuity, Anthology-series planning) · C02 #5 (Premise generation, Premise stress-testing) · W38 #8 (Ethical-dilemma episode structure) | — |
| Historical Fiction | Adventure | Dieselpunk | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | C03 (Worldbuilding, Era consistency) · C06 (Worldbuilding, Era consistency) · W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Adventure | Historical Adventure | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W19 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W56 #6 | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Adventure | Historical Epic Drama | W12 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W16 #2 (Dumas and Hugo style) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Adventure | Historical Naval Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W56 #4 | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Adventure | Middle Eastern Historical Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Adventure | Nautical Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W56 #6 | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Adventure | Period Piece | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W12 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Adventure | Speculative Historical Fiction | W71 #1 (Polaris lineage) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W16 #2 · W19 #2 · W40 #3 · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W12 #4 · W23 #4 · W72 #4 · W45 #6 | — | C03 #3 (Worldbuilding, Divergence planning) · C06 #3 (Worldbuilding, Divergence planning) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Adventure | War Fiction | W73 #1 (Generalist) · W71 #3 · W74 #3 · W41 #4 (Visual operations: recon imagery, terrain, timelines) | W26 #6 (Voice pastiche) | — | W30 (Period prose. Secondary Genre level; whole Secondary level) · W36 (short-form writer, Combat scenes) · W37 (short-form writer, Combat scenes) |

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C02 | `LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL` | Pocket hybrid planner | Featherless AI (32,768 tokens) |
| C03 | `LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL` | Pocket scope planner | Featherless AI (32,768 tokens) |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| C06 | `Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking` | Early-alpha wide-lens planner | Featherless AI (32,768 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W12 | `Goetia-26B-A4B-v1.6` | Broad-knowledge literary workhorse | Featherless AI (32,768 tokens) |
| W16 | `Gemma3-27B-it-vl-Polaris-HI16-Heretic-Uncensored-INSTRUCT` | Literary reasoning writer | Featherless AI (32,768 tokens) |
| W19 | `gemma-3-12b-it-vl-Gemini-3-Pro-Preview-Heretic-Uncensored-Thinking` | Timeline-sweep writer | Featherless AI (32,768 tokens) |
| W23 | `gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking` | Puzzle and timeline reasoner | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W36 | `Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` | 9B direct-delivery workhorse | Featherless AI (32,768 tokens) |
| W37 | `Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` | 9B direct-delivery flagship | Featherless AI (32,768 tokens) |
| W38 | `Qwen3.5-9B-Star-Trek-TNG-DS9-Heretic-Uncensored-Thinking` | Star Trek canon voice | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W41 | `Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` | Wide-lens visual analyst | Featherless AI (32,768 tokens) |
| W45 | `Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess` | Book-scale writer-thinker | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W56 | `Cydonia-24B-v4.1` | The roster's Dungeon Master | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Hanif J. Hakimi

Primary Genre: Literary Fiction · 17 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Science Fiction | Adventure | Speculative Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W46 #4 (Black Mirror-style anthology) | — | C05 #1 (Premise generation, Premises and twist shorts) · C09 #4 (Series continuity, Anthology-series planning) · C02 #5 (Premise generation, Premise stress-testing) · W38 #8 (Ethical-dilemma episode structure) | — |
| Historical Fiction | Drama | Multi-Generational Family Saga | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | C09 #1 (Series continuity, Series architecture) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Drama | Psychological Realism | W72 #10 (Dark side of realism) | — | — | — |
| Contemporary Literary Fiction | Drama | Regional Fiction | W40 #8 | — | — | — |
| Contemporary Literary Fiction | Drama | Social Drama | W72 #10 (Dark side of realism) | — | — | W40 |
| Historical Fiction | Drama | Social History | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Drama | Social Realism | — | — | — | W40 |
| Contemporary Literary Fiction | Drama | Southern Fiction | W40 #8 | — | — | — |

**Rows with no model (9):** Contemporary Literary Fiction > Drama > Medical/Health Issues; Contemporary Literary Fiction > Drama > Mental Health Fiction; Contemporary Literary Fiction > Drama > Realism; Contemporary Literary Fiction > Drama > Realist Fiction; Contemporary Literary Fiction > Drama > Social Criticism; Contemporary Literary Fiction > Drama > Social Justice Fiction; Contemporary Literary Fiction > Drama > Street Lit; Contemporary Literary Fiction > Drama > Tragedy; Contemporary Literary Fiction > Drama > Urban Fiction

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C02 | `LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL` | Pocket hybrid planner | Featherless AI (32,768 tokens) |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W38 | `Qwen3.5-9B-Star-Trek-TNG-DS9-Heretic-Uncensored-Thinking` | Star Trek canon voice | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## June Callender

Primary Genre: Nonfiction · 6 Genre Matrix rows

No model in the roster is assigned to any of this pen name's Genre Matrix rows.

## K.K. Kenyatta

Primary Genre: Literary Fiction, Literary Fiction (Adult Comics) · 9 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Thriller | Mystery Thriller | W73 #1 (Generalist) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 | — | C02 #1 (Planning, Hybrid planning) · C05 #3 (Premise generation, Premise and plan layer) · W35 #5 (Clue logic) · W34 #7 (Planning layer) · W59 #7 (Planning layer) | C01 (Planning, Beat sheets) · W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Thriller | Alternate History | W16 #1 · W19 #1 · W71 #1 (Polaris lineage) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #2 · W41 #3 (Visual what-if from period maps and photographs) · W12 #4 · W23 #4 · W40 #4 (Divergence at literary weight) · W18 #5 · W72 #5 · W08 #6 (Historical-figure voice) · W45 #6 | — | C03 #1 (Planning) · C06 #1 (Worldbuilding, What-if planning; verify the chains) · C10 #7 (Worldbuilding, Rigorous what-if; every downstream consequence traced) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Thriller | Aviation Thriller | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Thriller | Courtly Intrigue | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | C02 (Planning) · W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Thriller | Crime Noir | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W13 #5 | W65 #2 (Short) · W02 #5 (conditional: Directed dark vignettes) · W62 #5 (Short-form) | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Thriller | Espionage Thriller | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W58 #4 · W13 #6 · W22 #6 · W24 #6 | — | — | C02 (Planning, Operations planning) · W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Thriller | Historical Legal Drama | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Thriller | Historical Thrillers | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | C03 (Planning) · C06 (Worldbuilding, Timeline verification, with cross-checking) · W30 (Period prose. Secondary Genre level; whole Secondary level) |

**Rows with no model (1):** Contemporary Literary Fiction > Thriller > Underground Comix

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| C02 | `LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL` | Pocket hybrid planner | Featherless AI (32,768 tokens) |
| C03 | `LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL` | Pocket scope planner | Featherless AI (32,768 tokens) |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| C06 | `Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking` | Early-alpha wide-lens planner | Featherless AI (32,768 tokens) |
| C10 | `Qwen3.5-27B-Claude-4.6-OS-INSTRUCT` | Clean 27B chief analyst | Featherless AI (32,768 tokens) |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W08 | `gemma-4-31B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Voice-and-ideas flagship | Featherless AI (32,768 tokens) |
| W12 | `Goetia-26B-A4B-v1.6` | Broad-knowledge literary workhorse | Featherless AI (32,768 tokens) |
| W13 | `Goetia-26B-A4B-v1.7` | Dark-craft and suspense build | Featherless AI (32,768 tokens) |
| W16 | `Gemma3-27B-it-vl-Polaris-HI16-Heretic-Uncensored-INSTRUCT` | Literary reasoning writer | Featherless AI (32,768 tokens) |
| W18 | `Gemma-3-27b-it-Gemini-Deep-Reasoning` | Premium fair-play mystery reasoner | Featherless AI (32,768 tokens) |
| W19 | `gemma-3-12b-it-vl-Gemini-3-Pro-Preview-Heretic-Uncensored-Thinking` | Timeline-sweep writer | Featherless AI (32,768 tokens) |
| W22 | `gemma-3-12b-it-vl-Polaris-GLM-4.7-Flash-VAR-Thinking-Instruct-Heretic-Uncensored` | Hybrid scheme-and-puzzle writer | Featherless AI (32,768 tokens) |
| W23 | `gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking` | Puzzle and timeline reasoner | Featherless AI (32,768 tokens) |
| W24 | `gemma-3-12b-it-vl-GLM-4.7-Flash-INSTRUCT-Thinking-Hybrid-Heretic-Uncensored` | Switchable mechanism writer | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W34 | `Qwen3.5-9B-Claude-4.6-OS-Auto-Variable-THINKING` | Adaptive clean analyst | Featherless AI (32,768 tokens) |
| W35 | `Qwen3.5-9B-Claude-4.6-HighIQ-THINKING-HERETIC-UNCENSORED` | 9B precision deducer | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W41 | `Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` | Wide-lens visual analyst | Featherless AI (32,768 tokens) |
| W45 | `Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess` | Book-scale writer-thinker | Featherless AI (32,768 tokens) |
| W58 | `Dolphin-Mistral-GLM-4.7-Flash-24B-Venice-Edition-Thinking-Uncensored` | Dark-operations planner-writer | Featherless AI (32,768 tokens) |
| W59 | `Llama3.3-8B-Instruct-Thinking-Claude-4.5-Opus-High-Reasoning` | Technical spec writer | Featherless AI (8,192 tokens) |
| W62 | `L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` | Dark-bias scene writer | Featherless AI (8,192 tokens) |
| W65 | `Llama-3.2-3B-Instruct-abliterated` | Clean 3B abliteration | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Kai Koan

Primary Genre: Literary Fiction · 7 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Mystery | Philosophical Fiction | W08 #1 · W32 #1 · W67 #1 · W71 #3 | W29 #1 (Short to mid-length) · W28 #3 (Short) · W04 #8 (Short-form) · W06 #9 (Short-form sketches) | — | — |
| Historical Fiction | Fantasy | Historical Magical Realism | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Fantasy | Historical Mythological Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Fantasy | Magical Realist Historical Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Fantasy | Mythological Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Fantasy | Adventure | Lit RPG/Gamelit | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |

**Rows with no model (1):** Contemporary Literary Fiction > Fantasy > Magical Realism

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W08 | `gemma-4-31B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Voice-and-ideas flagship | Featherless AI (32,768 tokens) |
| W28 | `Qwen3.5-4B-Deckard-HERETIC-UNCENSORED-Thinking` | Pocket DECKARD | Featherless AI (32,768 tokens) |
| W29 | `Qwen3.5-9B-Claude-4.6-Opus-Deckard-V4.2-Uncensored-Heretic-Thinking` | 9B DECKARD thinker on a multimodal base | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W32 | `Qwen3.5-21B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking` | Mid-size DECKARD flagship | Featherless AI (32,768 tokens) |
| W67 | `ERNIE-21B-A3B-Claude-4.5-High-OPUS-Thinking` | Philosopher twin | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Laurent Levesque

Primary Genre: Literary Fiction · 4 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Drama | Cultural History | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Adventure | Epic Poetry | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Drama | Multi-generational Family Saga | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | C09 #1 (Series continuity, Series architecture) · C03 #4 (Worldbuilding, Multi-generational structure) · C06 #4 (Series continuity, Generation maps and inheritance ledgers) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Drama | Social History | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C03 | `LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL` | Pocket scope planner | Featherless AI (32,768 tokens) |
| C06 | `Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking` | Early-alpha wide-lens planner | Featherless AI (32,768 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## MJ Montrose

Primary Genre: Literary Fiction · 32 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Thriller | Assassination Thriller | W58 #2 | — | — | W39 (layer specialist, Operational planning) · W47 |
| Contemporary Literary Fiction | Thriller | Conspiracy Fiction | W71 #2 (Reasoning) · W58 #3 · W57 #4 · W21 #5 · W35 #7 (Evidence chain; OCRs documents) · W33 #9 (Paranoia mode: the conspiracy may be real and the narrator ill) | — | C01 #3 (Planning, Web-building) · C02 #3 (Planning, Web and span) · C10 #4 (Evidence reading, The full web; document OCR across 256K) · C03 #5 (Worldbuilding, Scope mode) · C06 #5 (Worldbuilding, Scope mode: the reach of the cover-up) · C09 #5 (Series continuity, Series-spanning webs) · W61 #8 (Planning layer) | W31 (Argumentative evidence chains) |
| Contemporary Literary Fiction | Thriller | Conspiracy Thriller | W41 #2 (Visual surveillance webs: video, OCR'd documents, maps) · W58 #3 · W22 #4 · W13 #6 · W24 #6 · W39 #6 (The dirty web and its cover-up) | — | C04 #4 (Planning, Web outlining) | W47 · W60 |
| Contemporary Literary Fiction | Thriller | Courtroom Drama | W57 #1 · W31 #2 (Argues both sides in one mind) | — | — | — |
| Contemporary Literary Fiction | Thriller | Domestic Noir | W73 #2 (Uncensored) · W48 #6 · W72 #10 (Dark side of realism) | W65 #2 (Short) · W62 #4 · W37 #6 (Scene level) · W36 #7 (Scene level) | — | C02 (Planning) · W31 (Terse intimate threat) · W39 (Planned intimate threats) · W46 · W49 · W60 |
| Contemporary Literary Fiction | Thriller | Espionage Fiction | — | — | — | C02 (Planning, Operations planning) |
| Contemporary Literary Fiction | Thriller | FBI Agents | W20 #6 | — | — | — |
| Contemporary Literary Fiction | Thriller | Financial Thriller | W21 #3 · W57 #3 · W58 #6 (Dark end) | — | — | C10 (Planning, Scheme mechanics) · W35 (Scheme logic) |
| Contemporary Literary Fiction | Thriller | Heist Fiction | W22 #1 · W58 #1 · W24 #2 · W71 #2 (Reasoning) · W25 #3 · W17 #4 · W21 #4 (Tech-forward) | — | C04 #1 (Planning, Outlining) · C01 #2 (Planning, Scheme design) · C02 #2 (Planning, Full job plan) · C10 #3 (Planning, Master plan, contingency trees) · W39 #3 (The full criminal plan, including the violent contingencies) · C08 #5 (Light scene drafting, Plan and light scene) · W23 #6 (Cunning-planning end) · W35 #6 (Planning layer) · W59 #7 (Planning layer) · W61 #8 (Planning layer) | C07 (Planning, Quick plan checks) · C09 (Series continuity, Crew continuity across a series) · W31 (layer specialist, Terse job briefs) · W41 (Multi-site surveillance) |
| Contemporary Literary Fiction | Thriller | Legal Drama | W31 #2 (Argues both sides) | — | — | — |
| Contemporary Literary Fiction | Thriller | Legal Thriller | W57 #1 · W58 #6 (Dark end) | — | — | — |
| Contemporary Literary Fiction | Thriller | Literary Thriller | W13 #1 · W30 #2 · W16 #6 | — | — | — |
| Contemporary Literary Fiction | Thriller | Medical Thriller | W71 #2 (Reasoning) · W20 #4 · W39 #5 (Dark medicine at clinical accuracy) | — | C08 #3 (Light scene drafting, Triage and scene) · C07 #4 (Evidence reading, Pocket triage; reads scans) · W34 #4 (Clinical layer; reads medical imaging) · W35 #4 (Diagnostic layer; reads medical imaging) · C10 #5 (Evidence reading, Clinical reasoning; reads medical imaging) · W59 #6 (Technical layer) | W48 · W60 |
| Contemporary Literary Fiction | Thriller | Military Thriller | W41 #4 (Visual operations) · W20 #5 | — | — | — |
| Contemporary Literary Fiction | Thriller | Mystery Thriller | W73 #1 (Generalist) · W74 #3 | — | C02 #1 (Planning, Hybrid planning) · C05 #3 (Premise generation, Premise and plan layer) · W35 #5 (Clue logic) · W34 #7 (Planning layer) · W59 #7 (Planning layer) | C01 (Planning, Beat sheets) |
| Contemporary Literary Fiction | Thriller | Organized Crime | W47 #2 | — | — | W62 (short-form writer) |
| Contemporary Literary Fiction | Thriller | Political Commentary | — | — | — | W72 |
| Contemporary Literary Fiction | Thriller | Political Fiction | — | — | — | W72 |
| Contemporary Literary Fiction | Thriller | Political Intrigue | — | — | — | W38 (Frontier politics) |
| Contemporary Literary Fiction | Thriller | Psychological Thriller-Suspense | W48 #2 | W07 #3 (Unreliable-narrator mode) · W62 #3 | C05 #4 (Planning, Short) | W47 |
| Contemporary Literary Fiction | Thriller | Serial Killers | W73 #2 (Uncensored) · W41 #8 (Visual pattern across cases) | W39 #4 (Pattern and forensics; reads crime-scene imagery) · W48 #7 (Scene level) | W60 #6 (Procedural planning) | C01 (Planning, Pattern planning) · C02 (Planning, Pattern logic) · W42 (short-form writer) · W43 (short-form writer, Scene level) · W62 (short-form writer) |
| Contemporary Literary Fiction | Thriller | Thriller-Suspense | W73 #1 (Generalist) · W74 #1 · W37 #2 (Pacing) · W36 #5 (Pacing) | — | — | — |

**Rows with no model (10):** Contemporary Literary Fiction > Thriller > International Thriller; Contemporary Literary Fiction > Thriller > International-Espionage Thriller; Contemporary Literary Fiction > Thriller > Literary Espionage; Contemporary Literary Fiction > Thriller > Political Thriller; Contemporary Literary Fiction > Thriller > Romantic Suspense; Contemporary Literary Fiction > Thriller > Spy Fiction; Contemporary Literary Fiction > Thriller > Terrorism Thriller; Contemporary Literary Fiction > Thriller > Theological Thriller; Contemporary Literary Fiction > Thriller > Vigilante Justice; Contemporary Literary Fiction > Thriller > War Thriller

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| C02 | `LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL` | Pocket hybrid planner | Featherless AI (32,768 tokens) |
| C03 | `LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL` | Pocket scope planner | Featherless AI (32,768 tokens) |
| C04 | `Gemma-3-1B-it-GLM-4.7-Flash-Heretic-Uncensored-Thinking` | Pocket planner | Featherless AI (32,768 tokens) |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| C06 | `Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking` | Early-alpha wide-lens planner | Featherless AI (32,768 tokens) |
| C07 | `Qwen3.5-2B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Pocket evidence reader | Featherless AI (32,768 tokens) |
| C08 | `Qwen3.5-4B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Complete small pipeline | Featherless AI (32,768 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| C10 | `Qwen3.5-27B-Claude-4.6-OS-INSTRUCT` | Clean 27B chief analyst | Featherless AI (32,768 tokens) |
| W07 | `gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Manic escalation wildcard | Local (Unsloth Desktop) |
| W13 | `Goetia-26B-A4B-v1.7` | Dark-craft and suspense build | Featherless AI (32,768 tokens) |
| W16 | `Gemma3-27B-it-vl-Polaris-HI16-Heretic-Uncensored-INSTRUCT` | Literary reasoning writer | Featherless AI (32,768 tokens) |
| W17 | `Gemma3-27B-it-vl-GLM-4.7-Uncensored-Heretic-Deep-Reasoning` | Deep-reasoning mechanism writer | Featherless AI (32,768 tokens) |
| W20 | `gemma-3-12b-it-vl-Deepseek-v3.1-Heretic-Uncensored-Thinking` | Investigation writer | Featherless AI (32,768 tokens) |
| W21 | `gemma-3-12b-it-vl-GPT-5.1-High-Heretic-Uncensored-Thinking` | Scheme designer | Featherless AI (32,768 tokens) |
| W22 | `gemma-3-12b-it-vl-Polaris-GLM-4.7-Flash-VAR-Thinking-Instruct-Heretic-Uncensored` | Hybrid scheme-and-puzzle writer | Featherless AI (32,768 tokens) |
| W23 | `gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking` | Puzzle and timeline reasoner | Featherless AI (32,768 tokens) |
| W24 | `gemma-3-12b-it-vl-GLM-4.7-Flash-INSTRUCT-Thinking-Hybrid-Heretic-Uncensored` | Switchable mechanism writer | Featherless AI (32,768 tokens) |
| W25 | `gemma-3-12b-it-vl-GLM-4.7-Flash-Heretic-Uncensored-Thinking` | Mechanism-depth thinker | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W31 | `Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking` | Dual-mind arguer | Featherless AI (32,768 tokens) |
| W33 | `Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking` | Philip K | Featherless AI (32,768 tokens) |
| W34 | `Qwen3.5-9B-Claude-4.6-OS-Auto-Variable-THINKING` | Adaptive clean analyst | Featherless AI (32,768 tokens) |
| W35 | `Qwen3.5-9B-Claude-4.6-HighIQ-THINKING-HERETIC-UNCENSORED` | 9B precision deducer | Featherless AI (32,768 tokens) |
| W36 | `Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` | 9B direct-delivery workhorse | Featherless AI (32,768 tokens) |
| W37 | `Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` | 9B direct-delivery flagship | Featherless AI (32,768 tokens) |
| W38 | `Qwen3.5-9B-Star-Trek-TNG-DS9-Heretic-Uncensored-Thinking` | Star Trek canon voice | Featherless AI (32,768 tokens) |
| W39 | `Qwen3.5-27B-Claude-4.6-OS-Auto-Variable-Heretic-Uncensored-Thinking` | Uncensored 27B dark analyst | Featherless AI (32,768 tokens) |
| W41 | `Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` | Wide-lens visual analyst | Featherless AI (32,768 tokens) |
| W42 | `Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B` | Horror-tainted engine | Local (Unsloth Desktop) |
| W43 | `Qwen3-Horror-Instruct-Uncensored-262K-ctx-4B` | Pocket horror engine | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W48 | `Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus` | Vivid crime and horror scene writer | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W57 | `Dolphin-Mistral-24B-Venice-Edition` | Utility infielder | Featherless AI (32,768 tokens) |
| W58 | `Dolphin-Mistral-GLM-4.7-Flash-24B-Venice-Edition-Thinking-Uncensored` | Dark-operations planner-writer | Featherless AI (32,768 tokens) |
| W59 | `Llama3.3-8B-Instruct-Thinking-Claude-4.5-Opus-High-Reasoning` | Technical spec writer | Featherless AI (8,192 tokens) |
| W60 | `Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning` | Structured dark planner-writer | Featherless AI (8,192 tokens) |
| W61 | `Llama-3.3-8B-Thinking-Gemini-Flash-11000x-128k` | Systems and scope planner | Featherless AI (8,192 tokens) |
| W62 | `L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` | Dark-bias scene writer | Featherless AI (8,192 tokens) |
| W65 | `Llama-3.2-3B-Instruct-abliterated` | Clean 3B abliteration | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Marcel Moreau

Primary Genre: Literary Fiction, Literary Fiction (Adult Comics) · 17 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Drama | War Fiction | W73 #1 (Generalist) · W71 #3 · W74 #3 · W41 #4 (Visual operations: recon imagery, terrain, timelines) | W26 #6 (Voice pastiche) | — | W30 (Period prose. Secondary Genre level; whole Secondary level) · W36 (short-form writer, Combat scenes) · W37 (short-form writer, Combat scenes) |
| Contemporary Literary Fiction | Drama | Psychological Realism | W72 #10 (Dark side of realism) | — | — | — |
| Contemporary Literary Fiction | Drama | Regional Fiction | W40 #8 | — | — | — |
| Contemporary Literary Fiction | Drama | Social Drama | W72 #10 (Dark side of realism) | — | — | W40 |
| Contemporary Literary Fiction | Drama | Social Realism | — | — | — | W40 |
| Contemporary Literary Fiction | Drama | Southern Fiction | W40 #8 | — | — | — |
| Contemporary Literary Fiction | Romance | Satire | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W31 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W32 #4 · W53 #5 (Light side) | W02 #4 (Light vignettes) | — | W29 |

**Rows with no model (10):** Contemporary Literary Fiction > Drama > Medical/Health Issues; Contemporary Literary Fiction > Drama > Mental Health Fiction; Contemporary Literary Fiction > Drama > Realism; Contemporary Literary Fiction > Drama > Realist Fiction; Contemporary Literary Fiction > Drama > Social Criticism; Contemporary Literary Fiction > Drama > Social Justice Fiction; Contemporary Literary Fiction > Drama > Street Lit; Contemporary Literary Fiction > Drama > Tragedy; Contemporary Literary Fiction > Drama > Urban Fiction; Contemporary Literary Fiction > Drama > Realistic Fiction

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W29 | `Qwen3.5-9B-Claude-4.6-Opus-Deckard-V4.2-Uncensored-Heretic-Thinking` | 9B DECKARD thinker on a multimodal base | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W31 | `Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking` | Dual-mind arguer | Featherless AI (32,768 tokens) |
| W32 | `Qwen3.5-21B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking` | Mid-size DECKARD flagship | Featherless AI (32,768 tokens) |
| W36 | `Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` | 9B direct-delivery workhorse | Featherless AI (32,768 tokens) |
| W37 | `Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` | 9B direct-delivery flagship | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W41 | `Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` | Wide-lens visual analyst | Featherless AI (32,768 tokens) |
| W53 | `UnslopNemo-12B-v1` | Obedient synopsis executor | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Maud Ellery

Primary Genre: Poetry · 18 Genre Matrix rows

No model in the roster is assigned to any of this pen name's Genre Matrix rows.

## Mimi Montclair

Primary Genre: Literary Fiction, YA · 4 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Western | Coming-of-Age | W68 #5 · W30 #7 (Literary mode) | W26 #2 (Vignettes) | — | W40 (Literary mode) |

**Rows with no model (3):** Contemporary Literary Fiction > Western > Canadian Literature; Contemporary Literary Fiction > Western > Counterculture Literature; Contemporary Literary Fiction > Western > Environmental Literature

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |

## Naomi McNamara

Primary Genre: Literary Fiction (New Adult) · 19 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Horror | Dramatic Monologue | W31 #8 (Combative speaker) | W01 #1 (Short) · W04 #1 · W05 #1 · W28 #2 (Short) · W06 #3 · W07 #4 (Unhinged mode) · W26 #4 · W03 | C01 #4 (Planning, Structural support) | W77 (short-form writer, Unhinged speaker, short) |
| Contemporary Literary Fiction | Horror | Existential Fiction | W67 #3 · W08 #5 · W23 #5 (Idea side) · W32 #8 · W33 #8 | W65 #4 (Short) · W28 #7 (Short) · W29 #7 (Short) · W04 #8 (Short-form) | — | W76 (short-form writer, Passages) · W77 (short-form writer, The void rendered literally) |
| Contemporary Literary Fiction | Horror | Ghost Story | W74 #1 · W46 #2 | W49 #2 (Short) · W76 #3 (Short passages, unreliable perception) | — | — |
| Historical Fiction | Horror | Gothic Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #1 · W71 #3 (Uncensored) · W30 #5 (Atmospheric) | — | W60 #1 (Structured) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Horror | Gothic Horror | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #1 · W10 #2 · W46 #2 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | W49 #2 (Short) · W66 #5 (Short) · W43 #7 (Short) · W26 #8 (conditional: Atmospheric, directed) | W60 #1 (Structured) | W30 (Period prose. Secondary Genre level; whole Secondary level) · W48 (short-form writer, Short-form) |
| Historical Fiction | Romance | Gothic Romance | W55 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W14 #4 (Pushed dark) · W47 #5 | W42 #7 (conditional: Dark mode only) · W70 #8 (Short-form) | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Mystery | Gothic Romantic Mystery | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W55 #3 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W47 #5 | W15 #4 | — | W28 (short-form writer, Short, character-driven) · W29 (short-form writer, Short) · W30 (Period prose. Secondary Genre level; whole Secondary level) · W32 (The DECKARD voice in the haunted register) |
| Contemporary Literary Fiction | Horror | Horror Mystery | W48 #4 · W46 #8 · W49 #8 | — | — | — |
| Contemporary Literary Fiction | Horror | Psychological Gothic | W64 #2 · W10 #4 · W13 #4 | — | — | — |
| Contemporary Literary Fiction | Horror | Psychotropic Literature | W33 #7 | W77 #4 (Short passages, deep) · W76 #5 (Short passages, mid-trip) | W75 #5 (Short passages, structured fever) | — |
| Contemporary Literary Fiction | Horror | Slasher | W10 #1 · W48 #3 (Planned) | W42 #1 · W07 #2 (Short-form) · W43 #2 (Short-form) · W62 #2 · W49 #3 (conditional: Directed) | — | — |
| Contemporary Literary Fiction | Horror | Southern Gothic | W64 #1 · W30 #5 (Atmospheric) | W66 #5 (Short) | — | W42 (short-form writer) · W43 (short-form writer) · W47 · W62 (short-form writer, Short-form) |
| Contemporary Literary Fiction | Horror | Surreal Literature | — | W77 #1 (Short passages) · W76 #2 (Short passages, transitional) · W65 #4 (Short) · W75 #4 (Short passages, mild) | — | W33 |
| Contemporary Literary Fiction | Horror | Transgressional Fiction | W73 #2 (Uncensored) · W14 #5 (At scale) | W07 #1 · W44 #1 (Short-form) · W62 #1 · W65 #1 (Short) · W66 #1 (Short) · W02 #5 (conditional: Directed dark vignettes) · W01 #6 (conditional: Directed dark monologues, short-form) · W43 #6 (Short-form) · W05 #8 (Short-form) · W42 #8 · W47 #8 (conditional: Directed) | C04 #3 (Light scene drafting, Short-form, directed) · C01 #5 (Planning, Dark planning) · C07 #5 (Light scene drafting, Short-form; needs explicit direction) · C08 #6 (Light scene drafting, Short-form; needs explicit direction) · W60 #7 (Structured) | W04 (short-form writer, Short-form) · W26 (short-form writer, Short-form) · W28 (short-form writer, Short-form; needs explicit direction) · W29 (short-form writer, Short-form; needs explicit direction) · W30 (short-form writer, Short-form; needs explicit direction) · W31 (short-form writer, Short-form) · W32 (short-form writer, Short-form) · W39 (layer specialist, Structured) · W48 (short-form writer, Short-form, directed) · W49 (short-form writer, Short-form, directed) · W70 (short-form writer, Short-form, pushed) · W75 (short-form writer, Short-form, pushed) |
| Historical Fiction | Horror | Victorian Era Horror | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W10 #2 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Horror | Victorian Gothic | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |

**Rows with no model (3):** Fantasy > Horror > Gothic Fantasy; Contemporary Literary Fiction > Horror > Modern Gothic Fiction; Contemporary Literary Fiction > Horror > Psychological Drama

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| C04 | `Gemma-3-1B-it-GLM-4.7-Flash-Heretic-Uncensored-Thinking` | Pocket planner | Featherless AI (32,768 tokens) |
| C07 | `Qwen3.5-2B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Pocket evidence reader | Featherless AI (32,768 tokens) |
| C08 | `Qwen3.5-4B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Complete small pipeline | Featherless AI (32,768 tokens) |
| W01 | `gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Edge voice sketcher | Local (Unsloth Desktop) |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W07 | `gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Manic escalation wildcard | Local (Unsloth Desktop) |
| W08 | `gemma-4-31B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Voice-and-ideas flagship | Featherless AI (32,768 tokens) |
| W10 | `gemma-4-31B-it-Grand-Horror-X-INTENSE-HERETIC-UNCENSORED-Thinking` | Full-intensity horror | Featherless AI (32,768 tokens) |
| W13 | `Goetia-26B-A4B-v1.7` | Dark-craft and suspense build | Featherless AI (32,768 tokens) |
| W14 | `Goetia-26B-A4B-v1.3-Absolute-Heretic-ARA` | Transgressive specialist | Featherless AI (32,768 tokens) |
| W15 | `Shadow-Siren-26B-A4B` | Dark-seduction character engine | Featherless AI (32,768 tokens) |
| W23 | `gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking` | Puzzle and timeline reasoner | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W28 | `Qwen3.5-4B-Deckard-HERETIC-UNCENSORED-Thinking` | Pocket DECKARD | Featherless AI (32,768 tokens) |
| W29 | `Qwen3.5-9B-Claude-4.6-Opus-Deckard-V4.2-Uncensored-Heretic-Thinking` | 9B DECKARD thinker on a multimodal base | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W31 | `Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking` | Dual-mind arguer | Featherless AI (32,768 tokens) |
| W32 | `Qwen3.5-21B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking` | Mid-size DECKARD flagship | Featherless AI (32,768 tokens) |
| W33 | `Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking` | Philip K | Featherless AI (32,768 tokens) |
| W39 | `Qwen3.5-27B-Claude-4.6-OS-Auto-Variable-Heretic-Uncensored-Thinking` | Uncensored 27B dark analyst | Featherless AI (32,768 tokens) |
| W42 | `Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B` | Horror-tainted engine | Local (Unsloth Desktop) |
| W43 | `Qwen3-Horror-Instruct-Uncensored-262K-ctx-4B` | Pocket horror engine | Featherless AI (32,768 tokens) |
| W44 | `Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` | Pocket attitude storyteller | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W48 | `Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus` | Vivid crime and horror scene writer | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W55 | `MN-Crimson-Cafe-12B` | Atmospheric ensemble storyteller | Featherless AI (32,768 tokens) |
| W60 | `Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning` | Structured dark planner-writer | Featherless AI (8,192 tokens) |
| W62 | `L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` | Dark-bias scene writer | Featherless AI (8,192 tokens) |
| W64 | `Legion-V2.1-LLaMa-70B-Elarablated-v0.8` | Dark-literary heavyweight | Featherless AI (32,768 tokens) |
| W65 | `Llama-3.2-3B-Instruct-abliterated` | Clean 3B abliteration | Featherless AI (32,768 tokens) |
| W66 | `Llama-3.2-3B-Instruct-uncensored` | 3B abliteration, second build | Featherless AI (32,768 tokens) |
| W67 | `ERNIE-21B-A3B-Claude-4.5-High-OPUS-Thinking` | Philosopher twin | Featherless AI (32,768 tokens) |
| W70 | `Rocinante-X-12B-v1-Heretic-Uncensored` | Long-session character engine | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |
| W75 | `Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop` | Word-slip instrument | Featherless AI (32,768 tokens) |
| W76 | `Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking` | Logic-drift instrument | Featherless AI (32,768 tokens) |
| W77 | `Qwen3.6-9B-Heretic-Uncensored-Thinking-Sweet-Madness` | Surrealist instrument | Featherless AI (32,768 tokens) |

# Routing · Noelle Noir to R.S. Rhys

One table per pen name: each row is a Genre Matrix path, followed by the models for that path, grouped by role. `#n` is where that subgenre sits on the model's own best-fit list. See the Overview tab for the full key.

## Noelle Noir

Primary Genre: Literary Fiction, Literary Fiction (Adult Comics) · 41 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Mystery | Allegory | W71 #1 (F451 lineage) · W32 #2 · W45 #4 · W67 #5 · W40 #6 · W72 #7 | W29 #5 (Short to mid-length) · W04 #7 · W05 #7 (Short-form) · W28 #8 (Short) · W06 #9 (Short-form sketches) | — | — |
| Contemporary Literary Fiction | Mystery | Amateur Sleuth Mystery | W20 #3 · W51 #4 · W50 #5 · W09 #6 | — | — | W03 (short-form writer) · W04 (short-form writer) · W05 (short-form writer) |
| Contemporary Literary Fiction | Mystery | Cozy Mystery | — | W69 #1 · W49 #5 (Short) · W48 #8 (Short) | C04 #5 (Light scene drafting, Formula drafting) | W68 (Whimsical variants) |
| Contemporary Literary Fiction | Mystery | Crime Fiction | W48 #1 (Vivid mode) · W73 #1 (Generalist) · W74 #1 · W09 #6 · W20 #6 (Forensic-heavy) | W37 #3 (Scene level; deduction carried implicitly) · W36 #4 (Scene level; deduction carried implicitly) | — | — |
| Contemporary Literary Fiction | Mystery | Detective Stories | W48 #1 (Vivid mode) · W20 #3 · W09 #6 | W37 #3 (Scene level) · W36 #4 (Scene level) | — | — |
| Contemporary Literary Fiction | Mystery | Hard-boiled Fiction | W31 #1 (Terse default is the genre's register) | W66 #4 (Short) · W62 #5 (Short-form) | — | — |
| Contemporary Literary Fiction | Mystery | Legal Social Commentary | W57 #2 | — | — | — |
| Contemporary Literary Fiction | Mystery | Literary Mystery | W30 #2 · W09 #3 · W18 #3 | — | — | W28 (short-form writer, Character-weighted) · W29 · W32 (Ideas-weighted) · W72 |
| Contemporary Literary Fiction | Mystery | Mystery-Suspense Fiction | W09 #1 · W13 #2 | — | — | — |
| Contemporary Literary Fiction | Mystery | Neo-Noir | W13 #5 | W65 #2 (Short) · W66 #4 (Short) · W15 #6 (Femme-fatale leads) | — | W33 |
| Contemporary Literary Fiction | Mystery | Philosophical Fiction | W08 #1 · W32 #1 · W67 #1 · W71 #3 | W29 #1 (Short to mid-length) · W28 #3 (Short) · W04 #8 (Short-form) · W06 #9 (Short-form sketches) | — | — |
| Contemporary Literary Fiction | Mystery | Philosophical Mystery | W11 #1 · W32 #2 · W23 #3 · W18 #4 · W08 #5 · W46 #6 (RP-framed, interactive) · W47 #6 (RP-framed) · W70 #7 (RP-framed, interactive quests (12B tier)) | W29 #3 (RP-framed, short) | — | — |
| Contemporary Literary Fiction | Mystery | Police Procedural | W20 #1 · W31 #5 (Terse, on the record) | — | C07 #2 (Evidence reading, Evidence triage from photos and documents) · C08 #2 (Light scene drafting, Evidence and scene) · W35 #3 (Deduction layer: evidence, inference, conclusion) | — |
| Contemporary Literary Fiction | Mystery | Post-Modern Literature | — | W77 #6 (Short, fractured) | — | W33 · W76 (short-form writer, Fragments) |
| Contemporary Literary Fiction | Mystery | Psychological Fiction | W30 #4 · W31 #4 (Dual-voice, unreliable) · W33 #5 (Unreliable narrator) | — | — | — |
| Contemporary Literary Fiction | Mystery | Psychological Mystery | W09 #3 · W18 #3 · W11 #4 · W33 #5 (Unreliable narrator) | — | — | — |
| Contemporary Literary Fiction | Mystery | Romantic Comedy Mystery | W50 #5 · W70 #5 (Banter) | W68 #6 (conditional: Whimsical cozy variants only) | — | — |
| Contemporary Literary Fiction | Mystery | Small-Town Life | W52 #2 | — | — | W03 (short-form writer) · W04 (short-form writer) · W05 (short-form writer) |
| Contemporary Literary Fiction | Mystery | Spiritual Fiction | W33 #10 (Gnostic mode) | — | — | — |
| Contemporary Literary Fiction | Mystery | Stream-of-Consciousness | — | W77 #3 (Short passages) | — | — |
| Contemporary Literary Fiction | Mystery | True Crime | W20 #2 (Reads case photos and documents) · W48 #5 (Fictionalized) · W41 #8 (Visual pattern across cases) | W65 #3 (Short) | — | W62 (short-form writer) |
| Contemporary Literary Fiction | Mystery | Village Mystery | W50 #5 | W69 #1 | — | W03 (short-form writer) · W04 (short-form writer) · W05 (short-form writer) |
| Contemporary Literary Fiction | Mystery | Whimsical Mystery | W50 #1 · W51 #2 · W49 #4 · W70 #5 (Banter) | W02 #1 (Vignette) · W69 #3 · W01 #4 (Vignette) · W44 #4 (Very short) · W04 #5 (Short) · W05 #5 (Short) · W26 #5 (Short) · W68 #6 (conditional: Whimsical cozy variants only) · W06 #7 (Short) · W48 #8 (Short) · W03 (Short) | — | C05 (Planning, Short) · W32 (Wit available on direction) |
| Contemporary Literary Fiction | Mystery | Whodunit | W09 #2 · W18 #2 · W23 #2 · W11 #3 · W22 #3 | — | C01 #1 (Planning, Clue planning) · C04 #2 (Planning, Clue planning) · W35 #5 (Clue logic; fair-play audit) · C09 #8 (Series continuity, Fair-play clue ledger across books) | — |
| Contemporary Literary Fiction | Mystery | Bookstory Cozy Mystery | — | W69 #1 | — | — |
| Contemporary Literary Fiction | Mystery | Christian Cozy Mystery | — | W69 #1 | — | — |
| Contemporary Literary Fiction | Mystery | Cozy Mystery with Animals | — | W69 #1 | — | W70 (The animal companion as an RP character) |
| Contemporary Literary Fiction | Mystery | Culinary Cozy Mystery | — | W69 #1 | — | — |
| Contemporary Literary Fiction | Mystery | Standard Cozy Mystery | — | W69 #1 | — | — |
| Contemporary Literary Fiction | Thriller | Crime Noir | W13 #5 | W65 #2 (Short) · W02 #5 (conditional: Directed dark vignettes) · W62 #5 (Short-form) | — | — |

**Rows with no model (11):** Contemporary Literary Fiction > Mystery > Culinary Mysteries; Contemporary Literary Fiction > Mystery > Family Drama; Contemporary Literary Fiction > Mystery > Indigenous Fiction; Contemporary Literary Fiction > Mystery > Literary Drama; Contemporary Literary Fiction > Mystery > Literature of Suburban Change; Contemporary Literary Fiction > Mystery > Memory Exploration; Contemporary Literary Fiction > Mystery > Modernist Fiction; Contemporary Literary Fiction > Mystery > Mystery Detective; Contemporary Literary Fiction > Mystery > Private Investigator Story; Contemporary Literary Fiction > Mystery > Religious Mystery; Contemporary Literary Fiction > Mystery > Crafts & Hobbies Cozy Mystery

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| C04 | `Gemma-3-1B-it-GLM-4.7-Flash-Heretic-Uncensored-Thinking` | Pocket planner | Featherless AI (32,768 tokens) |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| C07 | `Qwen3.5-2B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Pocket evidence reader | Featherless AI (32,768 tokens) |
| C08 | `Qwen3.5-4B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Complete small pipeline | Featherless AI (32,768 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W01 | `gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Edge voice sketcher | Local (Unsloth Desktop) |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W08 | `gemma-4-31B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Voice-and-ideas flagship | Featherless AI (32,768 tokens) |
| W09 | `gemma-4-31B-it-Mystery-Fine-Tune-HERETIC-UNCENSORED-Thinking` | Fair-play mystery specialist | Featherless AI (32,768 tokens) |
| W11 | `Pantheon-Reasoning-31B-1.1` | Plot-architecture writer | Featherless AI (32,768 tokens) |
| W13 | `Goetia-26B-A4B-v1.7` | Dark-craft and suspense build | Featherless AI (32,768 tokens) |
| W15 | `Shadow-Siren-26B-A4B` | Dark-seduction character engine | Featherless AI (32,768 tokens) |
| W18 | `Gemma-3-27b-it-Gemini-Deep-Reasoning` | Premium fair-play mystery reasoner | Featherless AI (32,768 tokens) |
| W20 | `gemma-3-12b-it-vl-Deepseek-v3.1-Heretic-Uncensored-Thinking` | Investigation writer | Featherless AI (32,768 tokens) |
| W22 | `gemma-3-12b-it-vl-Polaris-GLM-4.7-Flash-VAR-Thinking-Instruct-Heretic-Uncensored` | Hybrid scheme-and-puzzle writer | Featherless AI (32,768 tokens) |
| W23 | `gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking` | Puzzle and timeline reasoner | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W28 | `Qwen3.5-4B-Deckard-HERETIC-UNCENSORED-Thinking` | Pocket DECKARD | Featherless AI (32,768 tokens) |
| W29 | `Qwen3.5-9B-Claude-4.6-Opus-Deckard-V4.2-Uncensored-Heretic-Thinking` | 9B DECKARD thinker on a multimodal base | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W31 | `Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking` | Dual-mind arguer | Featherless AI (32,768 tokens) |
| W32 | `Qwen3.5-21B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking` | Mid-size DECKARD flagship | Featherless AI (32,768 tokens) |
| W33 | `Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking` | Philip K | Featherless AI (32,768 tokens) |
| W35 | `Qwen3.5-9B-Claude-4.6-HighIQ-THINKING-HERETIC-UNCENSORED` | 9B precision deducer | Featherless AI (32,768 tokens) |
| W36 | `Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` | 9B direct-delivery workhorse | Featherless AI (32,768 tokens) |
| W37 | `Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` | 9B direct-delivery flagship | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W41 | `Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` | Wide-lens visual analyst | Featherless AI (32,768 tokens) |
| W44 | `Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` | Pocket attitude storyteller | Featherless AI (32,768 tokens) |
| W45 | `Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess` | Book-scale writer-thinker | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W48 | `Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus` | Vivid crime and horror scene writer | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W50 | `UnslopNemo-12B-v4.1` | Anti-slop workhorse | Featherless AI (32,768 tokens) |
| W51 | `UnslopNemo-12B-v4` | Backup to UnslopNemo v4 | Featherless AI (32,768 tokens) |
| W52 | `UnslopNemo-12B-v3` | Prose stylist with a bad memory | Featherless AI (32,768 tokens) |
| W57 | `Dolphin-Mistral-24B-Venice-Edition` | Utility infielder | Featherless AI (32,768 tokens) |
| W62 | `L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` | Dark-bias scene writer | Featherless AI (8,192 tokens) |
| W65 | `Llama-3.2-3B-Instruct-abliterated` | Clean 3B abliteration | Featherless AI (32,768 tokens) |
| W66 | `Llama-3.2-3B-Instruct-uncensored` | 3B abliteration, second build | Featherless AI (32,768 tokens) |
| W67 | `ERNIE-21B-A3B-Claude-4.5-High-OPUS-Thinking` | Philosopher twin | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |
| W69 | `LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF` | Cozy series engine | Local (GGUF from Hugging Face) |
| W70 | `Rocinante-X-12B-v1-Heretic-Uncensored` | Long-session character engine | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |
| W76 | `Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking` | Logic-drift instrument | Featherless AI (32,768 tokens) |
| W77 | `Qwen3.6-9B-Heretic-Uncensored-Thinking-Sweet-Madness` | Surrealist instrument | Featherless AI (32,768 tokens) |

## O. O'Sullivan-Oz

Primary Genre: Literary Fiction, YA · 3 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Science Fiction | Adventure | Speculative Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W46 #4 (Black Mirror-style anthology) | — | C05 #1 (Premise generation, Premises and twist shorts) · C09 #4 (Series continuity, Anthology-series planning) · C02 #5 (Premise generation, Premise stress-testing) · W38 #8 (Ethical-dilemma episode structure) | — |

**Rows with no model (2):** Fantasy > Hybrid Adventure > Magical Realism; Fantasy > Hybrid Adventure > Mythological Fiction

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C02 | `LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL` | Pocket hybrid planner | Featherless AI (32,768 tokens) |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W38 | `Qwen3.5-9B-Star-Trek-TNG-DS9-Heretic-Uncensored-Thinking` | Star Trek canon voice | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Odessa Marchetti

Primary Genre: Nonfiction · 7 Genre Matrix rows

No model in the roster is assigned to any of this pen name's Genre Matrix rows.

## R.S. Raphael

Primary Genre: Literary Fiction · 41 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Mystery | Philosophical Fiction | W08 #1 · W32 #1 · W67 #1 · W71 #3 | W29 #1 (Short to mid-length) · W28 #3 (Short) · W04 #8 (Short-form) · W06 #9 (Short-form sketches) | — | — |
| Fantasy | Horror | Alternate Reality Fantasy | W33 #3 | — | — | W38 (Mirror-universe mode) |
| Science Fiction | Horror | Anti-Utopian Fiction | W45 #1 · W71 #1 (F451 lineage) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W72 #2 · W33 #4 | — | — | — |
| Science Fiction | Horror | Biopunk | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W17 #5 · W57 #5 · W25 #6 | — | — | W39 (Engineered plagues) |
| Science Fiction | Horror | Contemporary Speculative Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W46 #4 (Anthology pieces) | — | C05 #1 (Premise generation, Premises and twist shorts) | — |
| Science Fiction | Horror | Cosmic Horror | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W10 #5 | W42 #5 | — | — |
| Historical Fiction | Horror | Dark Romanticism | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W55 #2 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Horror | Dramatic Monologue | W31 #8 (Combative speaker) | W01 #1 (Short) · W04 #1 · W05 #1 · W28 #2 (Short) · W06 #3 · W07 #4 (Unhinged mode) · W26 #4 · W03 | C01 #4 (Planning, Structural support) | W77 (short-form writer, Unhinged speaker, short) |
| Fantasy | Horror | Dystopian Fantasy | — | — | — | W72 |
| Science Fiction | Horror | Eco-Dystopian | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W42 (short-form writer) · W43 (short-form writer) |
| Contemporary Literary Fiction | Horror | Existential Fiction | W67 #3 · W08 #5 · W23 #5 (Idea side) · W32 #8 · W33 #8 | W65 #4 (Short) · W28 #7 (Short) · W29 #7 (Short) · W04 #8 (Short-form) | — | W76 (short-form writer, Passages) · W77 (short-form writer, The void rendered literally) |
| Fantasy | Horror | Faustian Saga | W14 #4 | W47 #3 (Short) · W15 #5 · W46 #7 (Short) | — | W70 (The bargain as ongoing RP) |
| Fantasy | Horror | Folk Horror | W10 #3 | W42 #4 · W66 #5 (Short) | — | W41 (Ritual-site analysis) · W43 (short-form writer, Short) · W49 · W60 |
| Contemporary Literary Fiction | Horror | Ghost Story | W74 #1 · W46 #2 | W49 #2 (Short) · W76 #3 (Short passages, unreliable perception) | — | — |
| Science Fiction | Horror | Gothic Cyberpunk | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | — |
| Historical Fiction | Horror | Gothic Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #1 · W71 #3 (Uncensored) · W30 #5 (Atmospheric) | — | W60 #1 (Structured) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Horror | Gothic Horror | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #1 · W10 #2 · W46 #2 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | W49 #2 (Short) · W66 #5 (Short) · W43 #7 (Short) · W26 #8 (conditional: Atmospheric, directed) | W60 #1 (Structured) | W30 (Period prose. Secondary Genre level; whole Secondary level) · W48 (short-form writer, Short-form) |
| Fantasy | Horror | Grimdark Fantasy | W14 #1 · W73 #2 (Uncensored) · W64 #4 | W66 #3 (Short-form) · W42 #6 (Short-form) · W62 #8 (Short-form) | W39 #8 (Strategic layer: the war's logic, not its prose) | W41 (Campaign maps) · W43 (short-form writer, Short-form) · W47 (short-form writer, Short-form) · W60 (short-form writer, Short-form) |
| Fantasy | Horror | Horror Fantasy | — | W42 #2 (Graphic and body horror) | — | — |
| Contemporary Literary Fiction | Horror | Horror Mystery | W48 #4 · W46 #8 · W49 #8 | — | — | — |
| Fantasy | Horror | Monster | W10 #6 (Erotic horror, x-rated) | W43 #1 (Body horror) · W42 #2 (Graphic and body horror) · W75 #6 (Short, dissociative machine or mirror mode) | — | — |
| Fantasy | Horror | Occult | W13 #3 | W42 #4 · W43 #5 (Short) | W60 #3 (Structured) | C08 (Planning, Clue chains; artifact images) |
| Fantasy | Horror | Occult Mystery | W60 #2 · W41 #7 (Visual arcana) | — | — | W48 |
| Contemporary Literary Fiction | Horror | Psychological Gothic | W64 #2 · W10 #4 · W13 #4 | — | — | — |
| Contemporary Literary Fiction | Horror | Psychological Horror | W46 #1 (Second-person) · W49 #1 (Planned) · W74 #1 (Atmospheric dread) · W48 #2 · W64 #2 · W10 #4 | W07 #3 (Unreliable-narrator mode) · W42 #3 (Tainted mode) · W43 #3 (Unreliable narrator) · W62 #3 · W76 #4 (Short passages, dissociative) | — | W60 |
| Contemporary Literary Fiction | Horror | Psychotropic Literature | W33 #7 | W77 #4 (Short passages, deep) · W76 #5 (Short passages, mid-trip) | W75 #5 (Short passages, structured fever) | — |
| Science Fiction | Horror | Science Fiction Horror | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | — |
| Contemporary Literary Fiction | Horror | Slasher | W10 #1 · W48 #3 (Planned) | W42 #1 · W07 #2 (Short-form) · W43 #2 (Short-form) · W62 #2 · W49 #3 (conditional: Directed) | — | — |
| Contemporary Literary Fiction | Horror | Southern Gothic | W64 #1 · W30 #5 (Atmospheric) | W66 #5 (Short) | — | W42 (short-form writer) · W43 (short-form writer) · W47 · W62 (short-form writer, Short-form) |
| Fantasy | Horror | Supernatural Fiction | W13 #3 | — | — | — |
| Contemporary Literary Fiction | Horror | Surreal Literature | — | W77 #1 (Short passages) · W76 #2 (Short passages, transitional) · W65 #4 (Short) · W75 #4 (Short passages, mild) | — | W33 |
| Contemporary Literary Fiction | Horror | Transgressional Fiction | W73 #2 (Uncensored) · W14 #5 (At scale) | W07 #1 · W44 #1 (Short-form) · W62 #1 · W65 #1 (Short) · W66 #1 (Short) · W02 #5 (conditional: Directed dark vignettes) · W01 #6 (conditional: Directed dark monologues, short-form) · W43 #6 (Short-form) · W05 #8 (Short-form) · W42 #8 · W47 #8 (conditional: Directed) | C04 #3 (Light scene drafting, Short-form, directed) · C01 #5 (Planning, Dark planning) · C07 #5 (Light scene drafting, Short-form; needs explicit direction) · C08 #6 (Light scene drafting, Short-form; needs explicit direction) · W60 #7 (Structured) | W04 (short-form writer, Short-form) · W26 (short-form writer, Short-form) · W28 (short-form writer, Short-form; needs explicit direction) · W29 (short-form writer, Short-form; needs explicit direction) · W30 (short-form writer, Short-form; needs explicit direction) · W31 (short-form writer, Short-form) · W32 (short-form writer, Short-form) · W39 (layer specialist, Structured) · W48 (short-form writer, Short-form, directed) · W49 (short-form writer, Short-form, directed) · W70 (short-form writer, Short-form, pushed) · W75 (short-form writer, Short-form, pushed) |
| Historical Fiction | Horror | Victorian Era Horror | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W10 #2 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Horror | Victorian Gothic | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Fantasy | Horror | Weird Fiction | W13 #3 · W10 #5 | W75 #1 (Short) · W42 #5 · W43 #5 (Short) · W77 #5 (Short, fragmentary) · W07 #6 (Short-form) · W76 #6 (Short passages, drifting) | W60 #3 (Structured) | W46 · W49 (short-form writer, Short-form) · W62 (short-form writer, Short-form) |

**Rows with no model (6):** Fantasy > Horror > Creepy-Cozy Horror; Fantasy > Horror > Dark Fantasy; Fantasy > Horror > Gothic Fantasy; Contemporary Literary Fiction > Horror > Modern Gothic Fiction; Contemporary Literary Fiction > Horror > Psychological Drama; Fantasy > Horror > Urban Mythic

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| C04 | `Gemma-3-1B-it-GLM-4.7-Flash-Heretic-Uncensored-Thinking` | Pocket planner | Featherless AI (32,768 tokens) |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| C07 | `Qwen3.5-2B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Pocket evidence reader | Featherless AI (32,768 tokens) |
| C08 | `Qwen3.5-4B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Complete small pipeline | Featherless AI (32,768 tokens) |
| W01 | `gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Edge voice sketcher | Local (Unsloth Desktop) |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W07 | `gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Manic escalation wildcard | Local (Unsloth Desktop) |
| W08 | `gemma-4-31B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Voice-and-ideas flagship | Featherless AI (32,768 tokens) |
| W10 | `gemma-4-31B-it-Grand-Horror-X-INTENSE-HERETIC-UNCENSORED-Thinking` | Full-intensity horror | Featherless AI (32,768 tokens) |
| W13 | `Goetia-26B-A4B-v1.7` | Dark-craft and suspense build | Featherless AI (32,768 tokens) |
| W14 | `Goetia-26B-A4B-v1.3-Absolute-Heretic-ARA` | Transgressive specialist | Featherless AI (32,768 tokens) |
| W15 | `Shadow-Siren-26B-A4B` | Dark-seduction character engine | Featherless AI (32,768 tokens) |
| W17 | `Gemma3-27B-it-vl-GLM-4.7-Uncensored-Heretic-Deep-Reasoning` | Deep-reasoning mechanism writer | Featherless AI (32,768 tokens) |
| W23 | `gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking` | Puzzle and timeline reasoner | Featherless AI (32,768 tokens) |
| W25 | `gemma-3-12b-it-vl-GLM-4.7-Flash-Heretic-Uncensored-Thinking` | Mechanism-depth thinker | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W28 | `Qwen3.5-4B-Deckard-HERETIC-UNCENSORED-Thinking` | Pocket DECKARD | Featherless AI (32,768 tokens) |
| W29 | `Qwen3.5-9B-Claude-4.6-Opus-Deckard-V4.2-Uncensored-Heretic-Thinking` | 9B DECKARD thinker on a multimodal base | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W31 | `Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking` | Dual-mind arguer | Featherless AI (32,768 tokens) |
| W32 | `Qwen3.5-21B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking` | Mid-size DECKARD flagship | Featherless AI (32,768 tokens) |
| W33 | `Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking` | Philip K | Featherless AI (32,768 tokens) |
| W38 | `Qwen3.5-9B-Star-Trek-TNG-DS9-Heretic-Uncensored-Thinking` | Star Trek canon voice | Featherless AI (32,768 tokens) |
| W39 | `Qwen3.5-27B-Claude-4.6-OS-Auto-Variable-Heretic-Uncensored-Thinking` | Uncensored 27B dark analyst | Featherless AI (32,768 tokens) |
| W41 | `Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` | Wide-lens visual analyst | Featherless AI (32,768 tokens) |
| W42 | `Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B` | Horror-tainted engine | Local (Unsloth Desktop) |
| W43 | `Qwen3-Horror-Instruct-Uncensored-262K-ctx-4B` | Pocket horror engine | Featherless AI (32,768 tokens) |
| W44 | `Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` | Pocket attitude storyteller | Featherless AI (32,768 tokens) |
| W45 | `Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess` | Book-scale writer-thinker | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W48 | `Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus` | Vivid crime and horror scene writer | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W55 | `MN-Crimson-Cafe-12B` | Atmospheric ensemble storyteller | Featherless AI (32,768 tokens) |
| W57 | `Dolphin-Mistral-24B-Venice-Edition` | Utility infielder | Featherless AI (32,768 tokens) |
| W60 | `Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning` | Structured dark planner-writer | Featherless AI (8,192 tokens) |
| W62 | `L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` | Dark-bias scene writer | Featherless AI (8,192 tokens) |
| W64 | `Legion-V2.1-LLaMa-70B-Elarablated-v0.8` | Dark-literary heavyweight | Featherless AI (32,768 tokens) |
| W65 | `Llama-3.2-3B-Instruct-abliterated` | Clean 3B abliteration | Featherless AI (32,768 tokens) |
| W66 | `Llama-3.2-3B-Instruct-uncensored` | 3B abliteration, second build | Featherless AI (32,768 tokens) |
| W67 | `ERNIE-21B-A3B-Claude-4.5-High-OPUS-Thinking` | Philosopher twin | Featherless AI (32,768 tokens) |
| W70 | `Rocinante-X-12B-v1-Heretic-Uncensored` | Long-session character engine | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |
| W75 | `Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop` | Word-slip instrument | Featherless AI (32,768 tokens) |
| W76 | `Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking` | Logic-drift instrument | Featherless AI (32,768 tokens) |
| W77 | `Qwen3.6-9B-Heretic-Uncensored-Thinking-Sweet-Madness` | Surrealist instrument | Featherless AI (32,768 tokens) |

## R.S. Rhys

Primary Genre: Literary Fiction · 85 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Science Fiction | Adventure | Adventure Science Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Horror | Alternate Reality Fantasy | W33 #3 | — | — | W38 (Mirror-universe mode) |
| Science Fiction | Horror | Anti-Utopian Fiction | W45 #1 · W71 #1 (F451 lineage) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W72 #2 · W33 #4 | — | — | — |
| Science Fiction | Horror | Biopunk | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W17 #5 · W57 #5 · W25 #6 | — | — | W39 (Engineered plagues) |
| Science Fiction | Thriller | Climate Fiction (Cli-Fi) | W61 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W41 #5 (Satellite and drone evidence) | — | C05 #2 (Premise generation, Concept layer) · W34 #5 (Science layer) · W59 #5 (Science layer) · C10 #6 (Technical verification, Systems modelling) | W72 |
| Science Fiction | Horror | Contemporary Speculative Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W46 #4 (Anthology pieces) | — | C05 #1 (Premise generation, Premises and twist shorts) | — |
| Science Fiction | Horror | Cosmic Horror | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W10 #5 | W42 #5 | — | — |
| Science Fiction | Thriller | Cyberpunk | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W17 #2 · W25 #2 · W24 #3 · W22 #5 | — | — | W33 · W34 (Clean systems) · W41 (Visual network interfaces) · W59 (Clean) · W61 (Clean) · W70 (short-form writer, Character scenes) |
| Historical Fiction | Horror | Dark Romanticism | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W55 #2 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Contemporary Literary Fiction | Horror | Dramatic Monologue | W31 #8 (Combative speaker) | W01 #1 (Short) · W04 #1 · W05 #1 · W28 #2 (Short) · W06 #3 · W07 #4 (Unhinged mode) · W26 #4 · W03 | C01 #4 (Planning, Structural support) | W77 (short-form writer, Unhinged speaker, short) |
| Fantasy | Horror | Dystopian Fantasy | — | — | — | W72 |
| Science Fiction | Thriller | Dystopian Fiction | W45 #1 · W71 #1 (F451 lineage) · W72 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #2 (Chapter scale) · W09 #4 (Resistance narratives) · W33 #4 (Petty, bureaucratic police state) · W32 #7 (Chapter-scale; the ideology argues with itself) · W40 #7 (Chapter-scale) | — | C03 #6 (Worldbuilding, World-system planning) · C06 #6 (Worldbuilding, World-system planning) · C09 #7 (Series continuity, World-system drift across books) | — |
| Science Fiction | Horror | Eco-Dystopian | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W42 (short-form writer) · W43 (short-form writer) |
| Science Fiction | Thriller | Eco-Thriller | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #2 (Reasoning) · W20 #4 · W41 #5 (Satellite and drone evidence) · W39 #7 (Weaponized environment) | — | W61 #2 (Countermeasure planning) · C08 #3 (Light scene drafting, Triage and scene) · C07 #4 (Evidence reading, Pocket triage; reads contamination maps) · W35 #4 (Diagnostic layer) · W34 #5 (Science layer) · W59 #5 (Science layer) · C10 #6 (Technical verification, Systems modelling) | C05 (Premise generation, Concepts) · W48 (short-form writer, Disaster scenes) · W49 |
| Contemporary Literary Fiction | Horror | Existential Fiction | W67 #3 · W08 #5 · W23 #5 (Idea side) · W32 #8 · W33 #8 | W65 #4 (Short) · W28 #7 (Short) · W29 #7 (Short) · W04 #8 (Short-form) | — | W76 (short-form writer, Passages) · W77 (short-form writer, The void rendered literally) |
| Fantasy | Horror | Faustian Saga | W14 #4 | W47 #3 (Short) · W15 #5 · W46 #7 (Short) | — | W70 (The bargain as ongoing RP) |
| Science Fiction | Adventure | Feminist Science Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Horror | Folk Horror | W10 #3 | W42 #4 · W66 #5 (Short) | — | W41 (Ritual-site analysis) · W43 (short-form writer, Short) · W49 · W60 |
| Science Fiction | Romance | Futuristic Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Horror | Ghost Story | W74 #1 · W46 #2 | W49 #2 (Short) · W76 #3 (Short passages, unreliable perception) | — | — |
| Science Fiction | Horror | Gothic Cyberpunk | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | — |
| Historical Fiction | Horror | Gothic Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #1 · W71 #3 (Uncensored) · W30 #5 (Atmospheric) | — | W60 #1 (Structured) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Horror | Gothic Horror | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #1 · W10 #2 · W46 #2 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | W49 #2 (Short) · W66 #5 (Short) · W43 #7 (Short) · W26 #8 (conditional: Atmospheric, directed) | W60 #1 (Structured) | W30 (Period prose. Secondary Genre level; whole Secondary level) · W48 (short-form writer, Short-form) |
| Fantasy | Horror | Grimdark Fantasy | W14 #1 · W73 #2 (Uncensored) · W64 #4 | W66 #3 (Short-form) · W42 #6 (Short-form) · W62 #8 (Short-form) | W39 #8 (Strategic layer: the war's logic, not its prose) | W41 (Campaign maps) · W43 (short-form writer, Short-form) · W47 (short-form writer, Short-form) · W60 (short-form writer, Short-form) |
| Science Fiction | Adventure | Hard Sci-Fi | W34 #1 · W35 #1 · W59 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W39 #2 (Dark mode: the physics of what kills) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W60 #5 (Dark mode) | — | C10 #1 (Evidence reading, Full engineering; reads schematics) | — |
| Fantasy | Horror | Horror Fantasy | — | W42 #2 (Graphic and body horror) | — | — |
| Contemporary Literary Fiction | Horror | Horror Mystery | W48 #4 · W46 #8 · W49 #8 | — | — | — |
| Science Fiction | Adventure | Metaphysical Speculative Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Science Fiction | Adventure | Military Sci-Fi | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | W38 #5 (Ethical mode: strategy with conscience) | C10 (Planning, Campaign planning) · W34 (layer specialist, Planning tables) · W35 (Tactical reasoning) · W59 · W61 |
| Fantasy | Horror | Monster | W10 #6 (Erotic horror, x-rated) | W43 #1 (Body horror) · W42 #2 (Graphic and body horror) · W75 #6 (Short, dissociative machine or mirror mode) | — | — |
| Science Fiction | Thriller | Near-Future Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | C05 #2 (Premise generation, Concept layer) | W33 · W72 |
| Science Fiction | Adventure | Near-Future Sci-Fi | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W59 #4 · W61 #7 | W36 #3 (Scene level) · W37 #4 (Scene level) | W34 #6 (Plausibility layer) | — |
| Fantasy | Horror | Occult | W13 #3 | W42 #4 · W43 #5 (Short) | W60 #3 (Structured) | C08 (Planning, Clue chains; artifact images) |
| Fantasy | Horror | Occult Mystery | W60 #2 · W41 #7 (Visual arcana) | — | — | W48 |
| Science Fiction | Adventure | Post-Apocalyptic | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W62 #7 (Short-form) | — | C03 (Worldbuilding, Transition planning) · C06 (Worldbuilding, Transition planning) |
| Science Fiction | Adventure | Post-Cyberpunk | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W17 #2 · W25 #2 · W24 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Horror | Psychological Gothic | W64 #2 · W10 #4 · W13 #4 | — | — | — |
| Contemporary Literary Fiction | Horror | Psychological Horror | W46 #1 (Second-person) · W49 #1 (Planned) · W74 #1 (Atmospheric dread) · W48 #2 · W64 #2 · W10 #4 | W07 #3 (Unreliable-narrator mode) · W42 #3 (Tainted mode) · W43 #3 (Unreliable narrator) · W62 #3 · W76 #4 (Short passages, dissociative) | — | W60 |
| Contemporary Literary Fiction | Horror | Psychotropic Literature | W33 #7 | W77 #4 (Short passages, deep) · W76 #5 (Short passages, mid-trip) | W75 #5 (Short passages, structured fever) | — |
| Science Fiction | Horror | Science Fiction Horror | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | — |
| Science Fiction | Romance | Science Fiction Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Horror | Slasher | W10 #1 · W48 #3 (Planned) | W42 #1 · W07 #2 (Short-form) · W43 #2 (Short-form) · W62 #2 · W49 #3 (conditional: Directed) | — | — |
| Science Fiction | Adventure | Social Science Fiction | W71 #1 (F451 lineage) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W45 #2 · W38 #3 (The alien society as ethical mirror) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W40 #5 · W67 #6 · W72 #6 · W32 #7 (Chapter-scale) | — | — | — |
| Science Fiction | Adventure | Solarpunk | W61 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Horror | Southern Gothic | W64 #1 · W30 #5 (Atmospheric) | W66 #5 (Short) | — | W42 (short-form writer) · W43 (short-form writer) · W47 · W62 (short-form writer, Short-form) |
| Science Fiction | Adventure | Space Opera | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W12 #5 · W41 #6 (Series-scale politics) | — | C09 #3 (Series continuity, Series politics) · C03 #7 (Series continuity, Continuity) · C06 #7 (Series continuity, Continuity) | — |
| Science Fiction | Adventure | Speculative Biology | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Science Fiction | Adventure | Speculative Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W46 #4 (Black Mirror-style anthology) | — | C05 #1 (Premise generation, Premises and twist shorts) · C09 #4 (Series continuity, Anthology-series planning) · C02 #5 (Premise generation, Premise stress-testing) · W38 #8 (Ethical-dilemma episode structure) | — |
| Science Fiction | Romance | Speculative Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Science Fiction | Romance | Alien Romance | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Fantasy | Horror | Supernatural Fiction | W13 #3 | — | — | — |
| Contemporary Literary Fiction | Horror | Surreal Literature | — | W77 #1 (Short passages) · W76 #2 (Short passages, transitional) · W65 #4 (Short) · W75 #4 (Short passages, mild) | — | W33 |
| Science Fiction | Adventure | Synthwave | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Science Fiction | Thriller | Techno-Thriller | W17 #1 · W24 #1 · W25 #1 · W39 #1 (Dark schemes; reads schematics) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W21 #2 · W22 #2 · W71 #2 (Reasoning) · W60 #4 (Dark schemes) · W58 #5 | — | C10 #2 (Technical verification, Full systems design) · W34 #2 (Systems layer) · W35 #2 (Systems layer; plan with thinking on, write with it off) · W59 #2 (Spec-sheet mode) · C07 #3 (Light scene drafting, Quick systems and continuity checks between drafting passes) · C02 #4 (Worldbuilding, Systems and timeline) · C08 #4 (Light scene drafting, Systems check and scene) · W61 #4 (Operations roadmap) · W23 #6 (Cunning-planning end) · W31 #6 (Terse specs) | C01 (Planning, Checklists) · C09 (Series continuity, Systems continuity across a series) · W32 (layer specialist, Philosophy layer only) |
| Science Fiction | Adventure | Telepathic Science Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Science Fiction | Adventure | Time Travel | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #2 (Reasoning) · W08 #3 · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W46 #5 (Romantic or dark) · W38 #6 (Trek rules of time travel) | — | C05 #5 (Premise generation) · W32 #5 (Paradox as philosophy) · C09 #6 (Series continuity, Paradox ledger across books) · C03 #8 (Planning, Paradox auditing) · C06 #8 (Technical verification, Paradox chains; least safe use here, verify) · W35 #8 (Paradox resolution) · W59 #8 (Paradox planning) | C10 (Series continuity, Paradox ledgers) · W29 (Philosophical mode) · W33 |
| Contemporary Literary Fiction | Horror | Transgressional Fiction | W73 #2 (Uncensored) · W14 #5 (At scale) | W07 #1 · W44 #1 (Short-form) · W62 #1 · W65 #1 (Short) · W66 #1 (Short) · W02 #5 (conditional: Directed dark vignettes) · W01 #6 (conditional: Directed dark monologues, short-form) · W43 #6 (Short-form) · W05 #8 (Short-form) · W42 #8 · W47 #8 (conditional: Directed) | C04 #3 (Light scene drafting, Short-form, directed) · C01 #5 (Planning, Dark planning) · C07 #5 (Light scene drafting, Short-form; needs explicit direction) · C08 #6 (Light scene drafting, Short-form; needs explicit direction) · W60 #7 (Structured) | W04 (short-form writer, Short-form) · W26 (short-form writer, Short-form) · W28 (short-form writer, Short-form; needs explicit direction) · W29 (short-form writer, Short-form; needs explicit direction) · W30 (short-form writer, Short-form; needs explicit direction) · W31 (short-form writer, Short-form) · W32 (short-form writer, Short-form) · W39 (layer specialist, Structured) · W48 (short-form writer, Short-form, directed) · W49 (short-form writer, Short-form, directed) · W70 (short-form writer, Short-form, pushed) · W75 (short-form writer, Short-form, pushed) |
| Science Fiction | Adventure | Utopian Fiction | W71 #1 (F451 lineage) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W45 #2 · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W61 #6 · W67 #6 · W38 #7 · W40 #7 (Chapter-scale) · W72 #8 | — | C03 #6 (Worldbuilding, World-system planning) · C06 #6 (Worldbuilding, World-system planning) · C09 #7 (Series continuity, World-system drift across books) | — |
| Science Fiction | Adventure | AI Science Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W08 #2 · W29 #2 · W33 #2 · W32 #3 · W71 #3 · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W24 #5 · W25 #5 · W17 #6 · W21 #6 | W28 #4 (Short) | — | W38 (The android question) |
| Science Fiction | Adventure | Alien Invasion | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Science Fiction | Adventure | Clone Science Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W59 |
| Science Fiction | Adventure | Colonization | W41 #1 (Visual worldbuilding: terrain, orbital plots, decades-long colony arcs) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W19 #3 · W59 #3 (Technical support) · W71 #3 · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W38 #4 (Frontier-station register) · W18 #5 · W61 #5 | — | C03 #2 (Worldbuilding audits) · C06 #2 (Evidence reading, Worldbuilding; reads terrain imagery) · W34 #3 (Mission planning) | C10 (Planning, Mission architecture) |
| Science Fiction | Adventure | Corporate Science Fiction | W21 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W57 #5 | — | W61 #3 (Strategy layer) | C05 (Premise generation, Premise layer) · C10 (Planning, Strategy at depth) · W33 (Simulation-adjacent) · W34 (layer specialist, Strategy documents) · W35 (layer specialist, Strategy memos) · W39 (Hostile takeovers as warfare) · W59 |
| Science Fiction | Adventure | First Contact | W38 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #2 · W19 #3 · W71 #3 · W18 #5 | — | — | — |
| Science Fiction | Adventure | Galactic Empire | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W12 #5 · W41 #6 (Series-scale politics; star charts and fleet dispositions) | — | C09 #3 (Series continuity, Series politics) · C03 #7 (Series continuity, Continuity) · C06 #7 (Series continuity, Continuity) | — |
| Science Fiction | Adventure | Genetic Engineering | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W17 #5 · W25 #6 | — | — | C10 (Planning, Bioethics and mechanism) · W34 (Bioethics and mechanism) · W35 (Mechanism and ethics) · W38 · W59 · W61 |
| Science Fiction | Adventure | Hard Science Fiction | W34 #1 · W35 #1 · W59 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #2 (Reasoning) · W17 #3 · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W24 #4 · W25 #4 · W12 #5 | — | C10 #1 (Technical verification, Full engineering) | W61 (Systems) |
| Science Fiction | Adventure | Metaphysical Science Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Science Fiction | Adventure | Military Marine Science Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Science Fiction | Adventure | Mutant Science Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Science Fiction | Adventure | Pirate Science Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W56 #6 | — | — | — |
| Science Fiction | Adventure | Robot & Android Science Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W08 #2 · W29 #2 · W33 #2 · W32 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W24 #5 · W25 #5 · W17 #6 · W21 #6 | W28 #4 (Short) | — | — |
| Science Fiction | Adventure | Space Exploration | W41 #1 (Visual worldbuilding) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W38 #2 · W74 #2 · W19 #3 · W59 #3 (Technical support) · W71 #3 · W61 #5 | W36 #3 (Scene level) · W37 #4 (Scene level) | C03 #2 (Worldbuilding audits) · C06 #2 (Worldbuilding) · W34 #3 (Mission planning) | C10 (Planning, Mission architecture) |
| Science Fiction | Adventure | Space Fleet | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Science Fiction | Adventure | Virtual Reality | W33 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W24 #5 · W25 #5 | — | — | — |
| Historical Fiction | Horror | Victorian Era Horror | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W10 #2 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Horror | Victorian Gothic | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Fantasy | Horror | Weird Fiction | W13 #3 · W10 #5 | W75 #1 (Short) · W42 #5 · W43 #5 (Short) · W77 #5 (Short, fragmentary) · W07 #6 (Short-form) · W76 #6 (Short passages, drifting) | W60 #3 (Structured) | W46 · W49 (short-form writer, Short-form) · W62 (short-form writer, Short-form) |
| Science Fiction | Mystery | Cozy Sci-Fi | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W50 #4 · W51 #4 | — | — | — |

**Rows with no model (6):** Fantasy > Horror > Creepy-Cozy Horror; Fantasy > Horror > Dark Fantasy; Fantasy > Horror > Gothic Fantasy; Contemporary Literary Fiction > Horror > Modern Gothic Fiction; Contemporary Literary Fiction > Horror > Psychological Drama; Fantasy > Horror > Urban Mythic

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| C02 | `LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL` | Pocket hybrid planner | Featherless AI (32,768 tokens) |
| C03 | `LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL` | Pocket scope planner | Featherless AI (32,768 tokens) |
| C04 | `Gemma-3-1B-it-GLM-4.7-Flash-Heretic-Uncensored-Thinking` | Pocket planner | Featherless AI (32,768 tokens) |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| C06 | `Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking` | Early-alpha wide-lens planner | Featherless AI (32,768 tokens) |
| C07 | `Qwen3.5-2B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Pocket evidence reader | Featherless AI (32,768 tokens) |
| C08 | `Qwen3.5-4B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Complete small pipeline | Featherless AI (32,768 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| C10 | `Qwen3.5-27B-Claude-4.6-OS-INSTRUCT` | Clean 27B chief analyst | Featherless AI (32,768 tokens) |
| W01 | `gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Edge voice sketcher | Local (Unsloth Desktop) |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W07 | `gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Manic escalation wildcard | Local (Unsloth Desktop) |
| W08 | `gemma-4-31B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Voice-and-ideas flagship | Featherless AI (32,768 tokens) |
| W09 | `gemma-4-31B-it-Mystery-Fine-Tune-HERETIC-UNCENSORED-Thinking` | Fair-play mystery specialist | Featherless AI (32,768 tokens) |
| W10 | `gemma-4-31B-it-Grand-Horror-X-INTENSE-HERETIC-UNCENSORED-Thinking` | Full-intensity horror | Featherless AI (32,768 tokens) |
| W12 | `Goetia-26B-A4B-v1.6` | Broad-knowledge literary workhorse | Featherless AI (32,768 tokens) |
| W13 | `Goetia-26B-A4B-v1.7` | Dark-craft and suspense build | Featherless AI (32,768 tokens) |
| W14 | `Goetia-26B-A4B-v1.3-Absolute-Heretic-ARA` | Transgressive specialist | Featherless AI (32,768 tokens) |
| W15 | `Shadow-Siren-26B-A4B` | Dark-seduction character engine | Featherless AI (32,768 tokens) |
| W17 | `Gemma3-27B-it-vl-GLM-4.7-Uncensored-Heretic-Deep-Reasoning` | Deep-reasoning mechanism writer | Featherless AI (32,768 tokens) |
| W18 | `Gemma-3-27b-it-Gemini-Deep-Reasoning` | Premium fair-play mystery reasoner | Featherless AI (32,768 tokens) |
| W19 | `gemma-3-12b-it-vl-Gemini-3-Pro-Preview-Heretic-Uncensored-Thinking` | Timeline-sweep writer | Featherless AI (32,768 tokens) |
| W20 | `gemma-3-12b-it-vl-Deepseek-v3.1-Heretic-Uncensored-Thinking` | Investigation writer | Featherless AI (32,768 tokens) |
| W21 | `gemma-3-12b-it-vl-GPT-5.1-High-Heretic-Uncensored-Thinking` | Scheme designer | Featherless AI (32,768 tokens) |
| W22 | `gemma-3-12b-it-vl-Polaris-GLM-4.7-Flash-VAR-Thinking-Instruct-Heretic-Uncensored` | Hybrid scheme-and-puzzle writer | Featherless AI (32,768 tokens) |
| W23 | `gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking` | Puzzle and timeline reasoner | Featherless AI (32,768 tokens) |
| W24 | `gemma-3-12b-it-vl-GLM-4.7-Flash-INSTRUCT-Thinking-Hybrid-Heretic-Uncensored` | Switchable mechanism writer | Featherless AI (32,768 tokens) |
| W25 | `gemma-3-12b-it-vl-GLM-4.7-Flash-Heretic-Uncensored-Thinking` | Mechanism-depth thinker | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W28 | `Qwen3.5-4B-Deckard-HERETIC-UNCENSORED-Thinking` | Pocket DECKARD | Featherless AI (32,768 tokens) |
| W29 | `Qwen3.5-9B-Claude-4.6-Opus-Deckard-V4.2-Uncensored-Heretic-Thinking` | 9B DECKARD thinker on a multimodal base | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W31 | `Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking` | Dual-mind arguer | Featherless AI (32,768 tokens) |
| W32 | `Qwen3.5-21B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking` | Mid-size DECKARD flagship | Featherless AI (32,768 tokens) |
| W33 | `Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking` | Philip K | Featherless AI (32,768 tokens) |
| W34 | `Qwen3.5-9B-Claude-4.6-OS-Auto-Variable-THINKING` | Adaptive clean analyst | Featherless AI (32,768 tokens) |
| W35 | `Qwen3.5-9B-Claude-4.6-HighIQ-THINKING-HERETIC-UNCENSORED` | 9B precision deducer | Featherless AI (32,768 tokens) |
| W36 | `Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` | 9B direct-delivery workhorse | Featherless AI (32,768 tokens) |
| W37 | `Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` | 9B direct-delivery flagship | Featherless AI (32,768 tokens) |
| W38 | `Qwen3.5-9B-Star-Trek-TNG-DS9-Heretic-Uncensored-Thinking` | Star Trek canon voice | Featherless AI (32,768 tokens) |
| W39 | `Qwen3.5-27B-Claude-4.6-OS-Auto-Variable-Heretic-Uncensored-Thinking` | Uncensored 27B dark analyst | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W41 | `Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` | Wide-lens visual analyst | Featherless AI (32,768 tokens) |
| W42 | `Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B` | Horror-tainted engine | Local (Unsloth Desktop) |
| W43 | `Qwen3-Horror-Instruct-Uncensored-262K-ctx-4B` | Pocket horror engine | Featherless AI (32,768 tokens) |
| W44 | `Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` | Pocket attitude storyteller | Featherless AI (32,768 tokens) |
| W45 | `Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess` | Book-scale writer-thinker | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W48 | `Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus` | Vivid crime and horror scene writer | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W50 | `UnslopNemo-12B-v4.1` | Anti-slop workhorse | Featherless AI (32,768 tokens) |
| W51 | `UnslopNemo-12B-v4` | Backup to UnslopNemo v4 | Featherless AI (32,768 tokens) |
| W55 | `MN-Crimson-Cafe-12B` | Atmospheric ensemble storyteller | Featherless AI (32,768 tokens) |
| W56 | `Cydonia-24B-v4.1` | The roster's Dungeon Master | Featherless AI (32,768 tokens) |
| W57 | `Dolphin-Mistral-24B-Venice-Edition` | Utility infielder | Featherless AI (32,768 tokens) |
| W58 | `Dolphin-Mistral-GLM-4.7-Flash-24B-Venice-Edition-Thinking-Uncensored` | Dark-operations planner-writer | Featherless AI (32,768 tokens) |
| W59 | `Llama3.3-8B-Instruct-Thinking-Claude-4.5-Opus-High-Reasoning` | Technical spec writer | Featherless AI (8,192 tokens) |
| W60 | `Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning` | Structured dark planner-writer | Featherless AI (8,192 tokens) |
| W61 | `Llama-3.3-8B-Thinking-Gemini-Flash-11000x-128k` | Systems and scope planner | Featherless AI (8,192 tokens) |
| W62 | `L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` | Dark-bias scene writer | Featherless AI (8,192 tokens) |
| W64 | `Legion-V2.1-LLaMa-70B-Elarablated-v0.8` | Dark-literary heavyweight | Featherless AI (32,768 tokens) |
| W65 | `Llama-3.2-3B-Instruct-abliterated` | Clean 3B abliteration | Featherless AI (32,768 tokens) |
| W66 | `Llama-3.2-3B-Instruct-uncensored` | 3B abliteration, second build | Featherless AI (32,768 tokens) |
| W67 | `ERNIE-21B-A3B-Claude-4.5-High-OPUS-Thinking` | Philosopher twin | Featherless AI (32,768 tokens) |
| W70 | `Rocinante-X-12B-v1-Heretic-Uncensored` | Long-session character engine | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |
| W75 | `Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop` | Word-slip instrument | Featherless AI (32,768 tokens) |
| W76 | `Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking` | Logic-drift instrument | Featherless AI (32,768 tokens) |
| W77 | `Qwen3.6-9B-Heretic-Uncensored-Thinking-Sweet-Madness` | Surrealist instrument | Featherless AI (32,768 tokens) |

# Routing · Remy Raphael to Sebastian V. Somerset

One table per pen name: each row is a Genre Matrix path, followed by the models for that path, grouped by role. `#n` is where that subgenre sits on the model's own best-fit list. See the Overview tab for the full key.

## Remy Raphael

Primary Genre: Literary Fiction · 25 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Contemporary Literary Fiction | Adventure | Bildungsroman | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W68 #5 | — | — | W72 |
| Contemporary Literary Fiction | Adventure | City Life | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | W52 #5 (Literary vignettes) | — | — |
| Contemporary Literary Fiction | Adventure | Cityscapes | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | Cultural Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | Diaspora Literature | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | Eco-Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | Environmental Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | Immigrant Literature | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W67 #4 | — | — | — |
| Contemporary Literary Fiction | Adventure | Intellectual Adventure | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W11 #2 · W23 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W16 #4 · W22 #5 | — | — | — |
| Contemporary Literary Fiction | Adventure | Literary Realism | W40 #1 (Treat output as a draft) · W71 #1 (Polaris lineage) · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W16 #3 · W72 #3 · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W12 #6 · W30 #6 | — | — | — |
| Contemporary Literary Fiction | Adventure | Military Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W20 #5 | — | — | — |
| Contemporary Literary Fiction | Adventure | Modernist Literature | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | Naturalism | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | W40 |
| Contemporary Literary Fiction | Adventure | Philosophical Adventure | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W67 #2 · W45 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W23 #5 (Idea side) | — | — | — |
| Contemporary Literary Fiction | Adventure | Philosophical Literary Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W45 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | Post-Colonial Literature | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W67 #4 | — | — | — |
| Contemporary Literary Fiction | Adventure | Psychological Adventure | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W11 #4 | — | — | — |
| Contemporary Literary Fiction | Adventure | Robinsonade | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W56 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | Romantic Adventure | W36 #1 (Fast-paced; no reasoning pause between beats) · W37 #1 (Fast-paced; no pause between beats) · W51 #1 · W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W50 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W49 #4 | W06 #2 | — | W70 (Banter under adrenaline) |
| Contemporary Literary Fiction | Adventure | Small Town & Rural | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W52 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W70 #6 (Character mode) | W26 #2 (Vignettes) | — | — |
| Contemporary Literary Fiction | Adventure | Sports Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | Survival Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W56 #3 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | TV, Movie, Video Game Adaptations | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | Urban Life | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |
| Contemporary Literary Fiction | Adventure | Zen or Buddhist Fiction | W73 #1 (Generalist: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W67 #2 · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) | — | — | — |

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W11 | `Pantheon-Reasoning-31B-1.1` | Plot-architecture writer | Featherless AI (32,768 tokens) |
| W12 | `Goetia-26B-A4B-v1.6` | Broad-knowledge literary workhorse | Featherless AI (32,768 tokens) |
| W16 | `Gemma3-27B-it-vl-Polaris-HI16-Heretic-Uncensored-INSTRUCT` | Literary reasoning writer | Featherless AI (32,768 tokens) |
| W20 | `gemma-3-12b-it-vl-Deepseek-v3.1-Heretic-Uncensored-Thinking` | Investigation writer | Featherless AI (32,768 tokens) |
| W22 | `gemma-3-12b-it-vl-Polaris-GLM-4.7-Flash-VAR-Thinking-Instruct-Heretic-Uncensored` | Hybrid scheme-and-puzzle writer | Featherless AI (32,768 tokens) |
| W23 | `gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking` | Puzzle and timeline reasoner | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W36 | `Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` | 9B direct-delivery workhorse | Featherless AI (32,768 tokens) |
| W37 | `Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` | 9B direct-delivery flagship | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W45 | `Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess` | Book-scale writer-thinker | Featherless AI (32,768 tokens) |
| W49 | `Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` | Warm-and-dark range writer | Featherless AI (32,768 tokens) |
| W50 | `UnslopNemo-12B-v4.1` | Anti-slop workhorse | Featherless AI (32,768 tokens) |
| W51 | `UnslopNemo-12B-v4` | Backup to UnslopNemo v4 | Featherless AI (32,768 tokens) |
| W52 | `UnslopNemo-12B-v3` | Prose stylist with a bad memory | Featherless AI (32,768 tokens) |
| W56 | `Cydonia-24B-v4.1` | The roster's Dungeon Master | Featherless AI (32,768 tokens) |
| W67 | `ERNIE-21B-A3B-Claude-4.5-High-OPUS-Thinking` | Philosopher twin | Featherless AI (32,768 tokens) |
| W68 | `Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1` | Banter and persona engine | Local (GGUF from Hugging Face) |
| W70 | `Rocinante-X-12B-v1-Heretic-Uncensored` | Long-session character engine | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Ria Garcia Reyes

Primary Genre: Literary Fiction, YA, YA (Graphic Novel) · 13 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Science Fiction | Adventure | Speculative Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W74 #3 (General competence: Major Subgenre level, applies across every Minor Subgenre beneath it; whole Major level) · W46 #4 (Black Mirror-style anthology) | — | C05 #1 (Premise generation, Premises and twist shorts) · C09 #4 (Series continuity, Anthology-series planning) · C02 #5 (Premise generation, Premise stress-testing) · W38 #8 (Ethical-dilemma episode structure) | — |
| Contemporary Literary Fiction | Hybrid Drama | Regional Fiction | W40 #8 | — | — | — |
| Contemporary Literary Fiction | Hybrid Drama | Social Drama | W72 #10 (Dark side of realism) | — | — | W40 |
| Contemporary Literary Fiction | Hybrid Drama | Social Realism | — | — | — | W40 |
| Contemporary Literary Fiction | Hybrid Drama | Southern Fiction | W40 #8 | — | — | — |
| Fantasy | Horror | Fable | W45 #5 · W67 #5 | W02 #2 (Short) · W01 #3 (Short) · W04 #3 (Moore and Gaiman; Andersen styles) · W05 #3 · W44 #3 (conditional: Twisted mode) · W06 #5 · W07 #8 (Dark mode; Moore and Gaiman style) · W03 | — | — |

**Rows with no model (7):** Contemporary Literary Fiction > Hybrid Drama > Gender and Sexuality; Contemporary Literary Fiction > Hybrid Drama > Realism; Contemporary Literary Fiction > Hybrid Drama > Social Justice Fiction; Contemporary Literary Fiction > Hybrid Drama > Street Lit; Contemporary Literary Fiction > Hybrid Drama > Urban Fiction; Fantasy > Horror > Supernatural Dread; Fantasy > Horror > Zombies

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C02 | `LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL` | Pocket hybrid planner | Featherless AI (32,768 tokens) |
| C05 | `Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` | Fast premise generator | Featherless AI (8,192 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| W01 | `gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Edge voice sketcher | Local (Unsloth Desktop) |
| W02 | `gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` | Edge comic vignette writer | Local (Unsloth Desktop) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W07 | `gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Manic escalation wildcard | Local (Unsloth Desktop) |
| W38 | `Qwen3.5-9B-Star-Trek-TNG-DS9-Heretic-Uncensored-Thinking` | Star Trek canon voice | Featherless AI (32,768 tokens) |
| W40 | `Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` | Alpha literary realist | Featherless AI (32,768 tokens) |
| W44 | `Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` | Pocket attitude storyteller | Featherless AI (32,768 tokens) |
| W45 | `Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess` | Book-scale writer-thinker | Featherless AI (32,768 tokens) |
| W46 | `MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` | Planned dark scene writer | Featherless AI (32,768 tokens) |
| W67 | `ERNIE-21B-A3B-Claude-4.5-High-OPUS-Thinking` | Philosopher twin | Featherless AI (32,768 tokens) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W72 | `Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` | Literary-dystopian reasoner | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

## Ruth Calloway

Primary Genre: Nonfiction · 7 Genre Matrix rows

No model in the roster is assigned to any of this pen name's Genre Matrix rows.

## Sebastian V. Somerset

Primary Genre: Literary Fiction, Literary Fiction (Adult Comics) · 14 Genre Matrix rows

| Secondary Genre | Major Subgenre | Minor Subgenre | Lead writers | Short-form and conditional writers | Layer and component specialists | Strong adjacent fits |
| --- | --- | --- | --- | --- | --- | --- |
| Historical Fiction | Mystery | Biographical Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W08 #6 (Historical-figure voice) · W32 #6 (Full-length) | W28 #1 (Voice-sketches) · W04 #6 (Voice-sketches) · W05 #6 (Voice-sketches) · W29 #6 (Voice-sketches with more depth than the E4B line) · W06 #8 (Voice-sketches) · W03 (Voice-sketches) | — | W30 (short-form writer, Voice-sketches) |
| Historical Fiction | Mystery | Classic Detective | W18 #1 (Christie and Doyle style) · W23 #1 · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W11 #3 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Mystery | Classic Whodunit | W18 #1 (Christie and Doyle style) · W23 #1 (Christie and Doyle style) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W11 #3 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W09 #5 · W16 #5 (In-voice deduction) | — | W35 #5 (Clue logic; fair-play audit) · C09 #8 (Series continuity, Fair-play clue ledger across books) | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Mystery | Country House-Manor House Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Mystery | Epistolary Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W30 #8 (Literary documents; keeps each voice distinct) · W34 #8 (Document support) | W01 #2 (Short) · W04 #2 (Christie and Doyle style) · W05 #2 · W26 #3 · W06 #4 · W28 #6 (Character documents; OCR reads source documents) · W07 #7 (Unreliable documents) · W03 | C07 #1 (Series continuity, Reads letters, ledgers and depositions and assembles the account) · C08 #1 (Evidence reading, Reads and reasons the contradictions in documents) · C01 #4 (Planning, Structural support) · W60 #8 (Epistolary horror, structured) | W30 (Period prose. Secondary Genre level; whole Secondary level) · W31 (Documents that argue) |
| Historical Fiction | Mystery | Folklore | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | C01 (Planning, Clue chains) · C02 (Planning, Clue chains) · C07 (Planning, Clue chains from artifact images) · C08 (Evidence reading, Clue chains; artifact images and old-script OCR) · W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Mystery | Gothic Romantic Mystery | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W55 #3 · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W47 #5 | W15 #4 | — | W28 (short-form writer, Short, character-driven) · W29 (short-form writer, Short) · W30 (Period prose. Secondary Genre level; whole Secondary level) · W32 (The DECKARD voice in the haunted register) |
| Historical Fiction | Mystery | Historical Crime Fiction | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Mystery | Historical Mystery | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W09 #5 | — | C07 #1 (Evidence reading, Document OCR and triage) · C08 #1 (Evidence reading, OCR and reasoning) · W34 #8 (Document-heavy; reads period letters and ledgers) | C10 (Evidence reading, Document-heavy) · W30 (Period prose. Secondary Genre level; whole Secondary level) · W35 (Document-heavy; OCR) · W41 (Period-document OCR) |
| Historical Fiction | Mystery | Noir Fiction | W31 #1 (Terse default) · W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (Uncensored) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | W66 #4 (Short) | — | W30 (Period prose. Secondary Genre level; whole Secondary level) · W33 |
| Historical Fiction | Mystery | Traditional-Classic Mystery | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Mystery | Victorian Romance Mystery | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | — | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |
| Historical Fiction | Mystery | 1920s Historical Cozy Mystery | W73 #1 (Generalist: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W71 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) · W74 #3 (General competence: Secondary Genre level, applies across every subgenre beneath it; whole Secondary level) | W69 #1 | — | W30 (Period prose. Secondary Genre level; whole Secondary level) |

**Rows with no model (1):** Fantasy > Horror > Supernatural Horror

**Models used for this pen name**

| ID | Model | What it is | Runs on |
| --- | --- | --- | --- |
| C01 | `LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` | Pocket clue and structure planner | Featherless AI (32,768 tokens) |
| C02 | `LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL` | Pocket hybrid planner | Featherless AI (32,768 tokens) |
| C07 | `Qwen3.5-2B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Pocket evidence reader | Featherless AI (32,768 tokens) |
| C08 | `Qwen3.5-4B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` | Complete small pipeline | Featherless AI (32,768 tokens) |
| C09 | `Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` | Series analyst | Featherless AI (32,768 tokens) |
| C10 | `Qwen3.5-27B-Claude-4.6-OS-INSTRUCT` | Clean 27B chief analyst | Featherless AI (32,768 tokens) |
| W01 | `gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Edge voice sketcher | Local (Unsloth Desktop) |
| W03 | `gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Original DECKARD voice build | Local (Unsloth Desktop) |
| W04 | `gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` | Strongest E4B voice build | Local (Unsloth Desktop) |
| W05 | `gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` | Voice-sketch specialist | Local (Unsloth Desktop) |
| W06 | `gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Two-voice banter specialist | Local (Unsloth Desktop) |
| W07 | `gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe-HERETIC-UNCENSORED-Thinking` | Manic escalation wildcard | Local (Unsloth Desktop) |
| W08 | `gemma-4-31B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` | Voice-and-ideas flagship | Featherless AI (32,768 tokens) |
| W09 | `gemma-4-31B-it-Mystery-Fine-Tune-HERETIC-UNCENSORED-Thinking` | Fair-play mystery specialist | Featherless AI (32,768 tokens) |
| W11 | `Pantheon-Reasoning-31B-1.1` | Plot-architecture writer | Featherless AI (32,768 tokens) |
| W15 | `Shadow-Siren-26B-A4B` | Dark-seduction character engine | Featherless AI (32,768 tokens) |
| W16 | `Gemma3-27B-it-vl-Polaris-HI16-Heretic-Uncensored-INSTRUCT` | Literary reasoning writer | Featherless AI (32,768 tokens) |
| W18 | `Gemma-3-27b-it-Gemini-Deep-Reasoning` | Premium fair-play mystery reasoner | Featherless AI (32,768 tokens) |
| W23 | `gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking` | Puzzle and timeline reasoner | Featherless AI (32,768 tokens) |
| W26 | `Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` | Voice-led short-form writer | Featherless AI (16,384 tokens) |
| W28 | `Qwen3.5-4B-Deckard-HERETIC-UNCENSORED-Thinking` | Pocket DECKARD | Featherless AI (32,768 tokens) |
| W29 | `Qwen3.5-9B-Claude-4.6-Opus-Deckard-V4.2-Uncensored-Heretic-Thinking` | 9B DECKARD thinker on a multimodal base | Featherless AI (32,768 tokens) |
| W30 | `Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` | Anti-slop prose specialist | Featherless AI (32,768 tokens) |
| W31 | `Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking` | Dual-mind arguer | Featherless AI (32,768 tokens) |
| W32 | `Qwen3.5-21B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking` | Mid-size DECKARD flagship | Featherless AI (32,768 tokens) |
| W33 | `Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking` | Philip K | Featherless AI (32,768 tokens) |
| W34 | `Qwen3.5-9B-Claude-4.6-OS-Auto-Variable-THINKING` | Adaptive clean analyst | Featherless AI (32,768 tokens) |
| W35 | `Qwen3.5-9B-Claude-4.6-HighIQ-THINKING-HERETIC-UNCENSORED` | 9B precision deducer | Featherless AI (32,768 tokens) |
| W41 | `Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` | Wide-lens visual analyst | Featherless AI (32,768 tokens) |
| W47 | `MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` | Dark seduction and character engine | Featherless AI (32,768 tokens) |
| W55 | `MN-Crimson-Cafe-12B` | Atmospheric ensemble storyteller | Featherless AI (32,768 tokens) |
| W60 | `Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning` | Structured dark planner-writer | Featherless AI (8,192 tokens) |
| W66 | `Llama-3.2-3B-Instruct-uncensored` | 3B abliteration, second build | Featherless AI (32,768 tokens) |
| W69 | `LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF` | Cozy series engine | Local (GGUF from Hugging Face) |
| W71 | `Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` | Flagship generalist | Featherless AI (32,768 tokens) |
| W73 | `Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` | Neutral uncensored flagship | Featherless AI (32,768 tokens) |
| W74 | `Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` | Budget uncensored workhorse | Featherless AI (32,768 tokens) |

# Model reference

One card per model, in ID order. W01–W77 write prose; C01–C10 are component specialists that support a lead writer. "Used for" counts the Genre Matrix rows on which the model is a writer or specialist (strong adjacent fits are not counted).

## Gemma-4 DECKARD line

### W01 · DavidAU/gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking

Edge voice sketcher. Gemma-4 E2B DECKARD, uncensored. Single-voice vignettes on minimal hardware.

**Call:** Local (Unsloth Desktop) · `DavidAU/gemma-4-E2B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` · not served by Featherless AI

**Used for:** Ellis Leigh (4); Naomi McNamara (2); R.S. Raphael (2); R.S. Rhys (2); Avery Lee (1); Callum Reid (1); CeeCee Chestervale (1); Gabby Gabriel (1); Noelle Noir (1); Ria Garcia Reyes (1); Sebastian V. Somerset (1)

**Avoid:** Everything ensemble and long: sagas, epics, multi-POV · Anything style-critical · Fair-play puzzle elegance; Erotica

### W02 · DavidAU/gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking

Edge comic vignette writer. Gemma-4 E2B DECKARD Expresso-ONE Universe, uncensored. Whimsical and comic vignettes on minimal hardware.

**Call:** Local (Unsloth Desktop) · `DavidAU/gemma-4-E2B-it-The-DECKARD-Expresso-ONE-Universe-HERETIC-UNCENSORED-Thinking` · not served by Featherless AI

**Used for:** Ellis Leigh (6); Avery Lee (2); Noelle Noir (2); Cassidy Cavendish (1); CeeCee Chestervale (1); Gabby Gabriel (1); K.K. Kenyatta (1); Marcel Moreau (1); Naomi McNamara (1); R.S. Raphael (1); R.S. Rhys (1); Ria Garcia Reyes (1)

**Avoid:** Everything long-form · Everything style-critical: Gothic Romance, Literary Romance · Fair-play puzzle elegance; Erotica

### W03 · DavidAU/gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking

Original DECKARD voice build. Gemma-4 E4B DECKARD, uncensored. Same voice shelf as the V2-Strong build; its source lists the shelf without a ranking.

**Call:** Local (Unsloth Desktop) · `DavidAU/gemma-4-E4B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` · not served by Featherless AI

**Used for:** Ellis Leigh (3); Sebastian V. Somerset (2); Avery Lee (1); Callum Reid (1); Naomi McNamara (1); Noelle Noir (1); R.S. Raphael (1); R.S. Rhys (1); Ria Garcia Reyes (1)

**Avoid:** Book-scale dystopian, utopian and Social Science Fiction · Philosophical Fiction, AI Science Fiction, Time Travel, Metafiction and Satire: the 31B DECKARD's shelf · Fair-play whodunits; horror registers; Dark Romance and Erotica; epic quests

### W04 · DavidAU/gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking

Strongest E4B voice build. Gemma-4 E4B DECKARD V2-Strong, uncensored. Distinct voices for monologue, fable, epistolary and short philosophical pieces.

**Call:** Local (Unsloth Desktop) · `DavidAU/gemma-4-E4B-it-The-DECKARD-V2-Strong-HERETIC-UNCENSORED-Thinking` · not served by Featherless AI

**Used for:** Ellis Leigh (3); Noelle Noir (3); R.S. Raphael (3); Naomi McNamara (2); R.S. Rhys (2); Sebastian V. Somerset (2); Avery Lee (1); Callum Reid (1); Kai Koan (1); Ria Garcia Reyes (1)

**Avoid:** Book-scale dystopian, utopian and Social Science Fiction · Fair-play whodunits; philosophy at book scale · Horror registers; Dark Romance and Erotica; epic quests and procedurals

### W05 · DavidAU/gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking

Voice-sketch specialist. Gemma-4 E4B DECKARD V3 Expresso, uncensored. Holds a single voice exactly at sketch and short-story length.

**Call:** Local (Unsloth Desktop) · `DavidAU/gemma-4-E4B-it-The-DECKARD-V3-Expresso-HERETIC-UNCENSORED-Thinking` · not served by Featherless AI

**Used for:** Ellis Leigh (3); Naomi McNamara (2); Noelle Noir (2); R.S. Raphael (2); R.S. Rhys (2); Sebastian V. Somerset (2); Avery Lee (1); Callum Reid (1); Ria Garcia Reyes (1)

**Avoid:** Book-scale dystopian, utopian and Social Science Fiction · Fair-play whodunits; idea-weight philosophy; two-voice banter as the engine · Horror registers; Dark Romance and Erotica; epic quests and procedurals

### W06 · DavidAU/gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking

Two-voice banter specialist. Gemma-4 E4B DECKARD Expresso-Universe, uncensored. Sparring dialogue, romantic comedy and comic voice-sketches.

**Call:** Local (Unsloth Desktop) · `DavidAU/gemma-4-E4B-it-The-DECKARD-Expresso-Universe-HERETIC-UNCENSORED-Thinking` · not served by Featherless AI

**Used for:** Ellis Leigh (5); Noelle Noir (3); Avery Lee (2); Gabby Gabriel (2); R.S. Raphael (2); Sebastian V. Somerset (2); August Reinhardt (1); Callum Reid (1); CeeCee Chestervale (1); Kai Koan (1); Naomi McNamara (1); R.S. Rhys (1); Remy Raphael (1); Ria Garcia Reyes (1)

**Avoid:** Book-scale dystopian, utopian and allegory · Fair-play whodunits; full idea-weight philosophy at book scale · Horror registers; Dark Romance, Erotica and dark seduction · Epic quests, wide-lens sweeps and procedurals

### W07 · DavidAU/gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe-HERETIC-UNCENSORED-Thinking

Manic escalation wildcard. A Gemma-4 E4B DECKARD build with Claude Opus thinking, uncensored. Escalates hard on a single keyword; repetition penalty 1.05 to 1.1 acts as a brake.

**Call:** Local (Unsloth Desktop) · `DavidAU/gemma-4-E4B-it-The-DECKARD-Claude-Opus-Expresso-Universe-HERETIC-UNCENSORED-Thinking` · not served by Featherless AI

**Used for:** R.S. Raphael (5); R.S. Rhys (5); Ellis Leigh (4); Naomi McNamara (3); Callum Reid (1); Carys Cassian (1); MJ Montrose (1); Ria Garcia Reyes (1); Sebastian V. Somerset (1)

**Avoid:** Anything needing restraint or precision: Cozy Fiction, Whimsical Mystery, Feel-Good Fiction, Slice-of-Life Fiction, Sweet Romance · Fair-play whodunits; idea-weight philosophy; two-voice banter · Book-scale dystopian or utopian; Dark Romance and Erotica that need control · Procedurals, technothrillers and wide-lens sweeps

### W08 · DavidAU/gemma-4-31B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking

Voice-and-ideas flagship. Gemma-4 31B DECKARD, uncensored. Ideas carried by distinct voices: philosophy, AI fiction, metafiction, satire.

**Call:** Featherless AI · `DavidAU/gemma-4-31B-it-The-DECKARD-HERETIC-UNCENSORED-Thinking` · served context 32,768 tokens · max output 32,768 · class `gemma4-31b` · concurrency cost 2 · image input

**Used for:** R.S. Rhys (4); Ellis Leigh (2); Noelle Noir (2); R.S. Raphael (2); K.K. Kenyatta (1); Kai Koan (1); Naomi McNamara (1); Sebastian V. Somerset (1)

**Avoid:** Cozy Mystery, feel-good and gentle comedy: it over-philosophizes · Atmospheric horror and gothic mood · Erotica; action-forward plotting such as heist and Techno-Thriller

## Gemma-4 31B specialists and 26B merges

### W09 · DavidAU/gemma-4-31B-it-Mystery-Fine-Tune-HERETIC-UNCENSORED-Thinking

Fair-play mystery specialist. Gemma-4 31B fine-tuned for mystery, uncensored. Clue construction, dread and dramatic irony. Keep it away from Cozy Mystery.

**Call:** Featherless AI · `DavidAU/gemma-4-31B-it-Mystery-Fine-Tune-HERETIC-UNCENSORED-Thinking` · served context 32,768 tokens · max output 32,768 · class `gemma4-31b` · concurrency cost 2 · image input

**Used for:** Noelle Noir (7); Sebastian V. Somerset (2); Cassidy Cavendish (1); R.S. Rhys (1)

**Avoid:** Cozy Mystery: the one mystery subgenre to keep away · Feel-good, light romance and banter comedy · Gothic atmosphere; epic-scale worldbuilding

### W10 · DavidAU/gemma-4-31B-it-Grand-Horror-X-INTENSE-HERETIC-UNCENSORED-Thinking

Full-intensity horror. Gemma-4 31B Grand-Horror-X INTENSE, uncensored. Graphic horror at scale.

**Call:** Featherless AI · `DavidAU/gemma-4-31B-it-Grand-Horror-X-INTENSE-HERETIC-UNCENSORED-Thinking` · served context 32,768 tokens · max output 32,768 · class `gemma4-31b` · concurrency cost 2 · image input

**Used for:** R.S. Raphael (9); R.S. Rhys (9); Naomi McNamara (4); Bree Beaumont (1)

**Avoid:** Cozy Mystery, feel-good, Slice-of-Life Fiction, Whimsical Mystery · Light romance and Romantic Comedy; gentle fantasy and Fable · Anything requiring restraint: Legal Thriller, Courtroom Drama

### W11 · Gryphe/Pantheon-Reasoning-31B-1.1

Plot-architecture writer. A Gemma-4 31B trained with thinking on every turn, taught to plan beats like a writer. Strong persona voice, prose-forward interactive fiction and 67.6% fewer clichés than its base. Let the thinking run.

**Call:** Featherless AI · `Gryphe/Pantheon-Reasoning-31B-1.1` · served context 32,768 tokens · max output 32,768 · class `gemma4-31b` · concurrency cost 2 · image input

**Used for:** Noelle Noir (3); Ch'an Lee (2); Remy Raphael (2); Sebastian V. Somerset (2)

**Avoid:** Pure mood pieces: Gothic Romance, Dark Romanticism, Southern Gothic · Erotic Literature and Dark Romance · Banter comedy

### W12 · Naphula/Goetia-26B-A4B-v1.6

Broad-knowledge literary workhorse. A roughly 28-donor Gemma-4 26B MoE (about 4B active) with Gutenberg prose, encyclopedic grounding and Claude and Sonnet reasoning distills. Not uncensored: refusals and jailbreak resistance are intact.

**Call:** Featherless AI · `Naphula/Goetia-26B-A4B-v1.6` · served context 32,768 tokens · max output 32,768 · class `gemma4-25b` · concurrency cost 2 · image input

**Used for:** Christine Leigh (5); Ch'an Lee (3); H.J. Hakimi (3); R.S. Rhys (3); Anais Amaris (1); Bastien Benoit (1); Drew D'Angelo (1); Ellis Leigh (1); Gabriel Varenne (1); K.K. Kenyatta (1); Remy Raphael (1)

**Avoid:** Dark Romance, Grimdark Fantasy at full intensity, Erotic Literature, Transgressional Fiction · Cozy Mystery and feel-good: overkill

### W13 · Naphula/Goetia-26B-A4B-v1.7

Dark-craft and suspense build. An 11-donor, four-stage Gemma-4 26B MoE merge (about 4B active) trading knowledge breadth for tension and layered plotting. Not ablated: refusals are live (use the NoThink template). Run Q5 or higher.

**Call:** Featherless AI · `Naphula/Goetia-26B-A4B-v1.7` · served context 32,768 tokens · max output 32,768 · class `gemma4-25b` · concurrency cost 2 · image input

**Used for:** R.S. Raphael (4); R.S. Rhys (4); Noelle Noir (3); K.K. Kenyatta (2); MJ Montrose (2); Cassidy Cavendish (1); Naomi McNamara (1)

**Avoid:** Cozy Mystery, feel-good and light Romantic Comedy · Erotic Literature and Erotic Romance · Grimdark Fantasy at full brutality; period-accurate historical fiction and Hard Science Fiction

### W14 · Naphula/Goetia-26B-A4B-v1.3-Absolute-Heretic-ARA

Transgressive specialist. A roughly 14-donor dark, RP and style Gemma-4 26B MoE with a reasoning component, ablated to 3/100 refusals at very low damage. Violent and graphic erotic content in long-form prose.

**Call:** Featherless AI · `Naphula/Goetia-26B-A4B-v1.3-Absolute-Heretic-ARA` · served context 32,768 tokens · max output 32,768 · class `gemma4-25b` · concurrency cost 2 · image input

**Used for:** R.S. Raphael (3); R.S. Rhys (3); Naomi McNamara (2); Bree Beaumont (1); Ch'an Lee (1); Christine Leigh (1); Deon D'Arcy (1); Gabriel Varenne (1)

**Avoid:** Cozy Mystery, feel-good and Slice-of-Life Fiction · Fair-play whodunits and Philosophical Mystery · Light Romantic Comedy

### W15 · Vortex5/Shadow-Siren-26B-A4B

Dark-seduction character engine. A six-donor Gemma-4 26B MoE merge (about 4B active) built for morally grey, seductive characters held across multi-turn scenes. 32K native context; a scene performer, not a novelist.

**Call:** Featherless AI · `Vortex5/Shadow-Siren-26B-A4B` · served context 32,768 tokens · max output 32,768 · class `gemma4-25b` · concurrency cost 2 · image input

**Used for:** Deon D'Arcy (5); Bree Beaumont (1); Christine Leigh (1); Naomi McNamara (1); Noelle Noir (1); R.S. Raphael (1); R.S. Rhys (1); Sebastian V. Somerset (1)

**Avoid:** Cozy Mystery, feel-good and Slice-of-Life Fiction · Epic worldbuilding: Epic Fantasy, Space Opera · Fair-play whodunits; pure literary prose registers

## Gemma-3 and Gemma-2

### W16 · DavidAU/Gemma3-27B-it-vl-Polaris-HI16-Heretic-Uncensored-INSTRUCT

Literary reasoning writer. Gemma-3 27B multimodal Polaris HI16 instruct, uncensored. Reasoning absorbed into literary prose.

**Call:** Featherless AI · `DavidAU/Gemma3-27B-it-vl-Polaris-HI16-Heretic-Uncensored-INSTRUCT` · served context 32,768 tokens · class `gemma3-27b` · concurrency cost 2 · image input

**Used for:** H.J. Hakimi (2); Remy Raphael (2); Anais Amaris (1); Deon D'Arcy (1); Ellis Leigh (1); K.K. Kenyatta (1); MJ Montrose (1); Sebastian V. Somerset (1)

**Avoid:** Cozy Mystery, feel-good and banter comedy · Gothic atmosphere; dark seduction and Erotica · Hard procedural planning that needs visible reasoning: clue tables, heist plans

### W17 · DavidAU/Gemma3-27B-it-vl-GLM-4.7-Uncensored-Heretic-Deep-Reasoning

Deep-reasoning mechanism writer. Gemma-3 27B multimodal with GLM 4.7 reasoning, uncensored. Technical systems and schemes.

**Call:** Featherless AI · `DavidAU/Gemma3-27B-it-vl-GLM-4.7-Uncensored-Heretic-Deep-Reasoning` · served context 32,768 tokens · class `gemma3-27b` · concurrency cost 2 · image input

**Used for:** R.S. Rhys (8); MJ Montrose (1); R.S. Raphael (1)

**Avoid:** Cozy Mystery, feel-good and banter comedy · Gothic atmosphere and dark-literary prose; dark seduction and Erotica · Pure puzzle mysteries

### W18 · DavidAU/Gemma-3-27b-it-Gemini-Deep-Reasoning

Premium fair-play mystery reasoner. Gemma-3 27B multimodal with selective Gemini reasoning. Censored: alignment intact.

**Call:** Featherless AI · `DavidAU/Gemma-3-27b-it-Gemini-Deep-Reasoning` · served context 32,768 tokens · class `gemma3-27b` · concurrency cost 2 · image input

**Used for:** Noelle Noir (4); R.S. Rhys (2); Sebastian V. Somerset (2); K.K. Kenyatta (1)

**Avoid:** Cozy Mystery and feel-good · Dark and transgressive content: Grimdark Fantasy, Dark Romance and erotic shelves go elsewhere · Gothic atmosphere; extreme long-arc work (128K, not 1M)

### W19 · DavidAU/gemma-3-12b-it-vl-Gemini-3-Pro-Preview-Heretic-Uncensored-Thinking

Timeline-sweep writer. A 12B multimodal Gemma-3 with Gemini 3 Pro long-horizon reasoning, uncensored (7/100), with vision that reads maps. Best quality per VRAM in the Gemma-3 12B family.

**Call:** Featherless AI · `DavidAU/gemma-3-12b-it-vl-Gemini-3-Pro-Preview-Heretic-Uncensored-Thinking` · served context 32,768 tokens · class `gemma3-12b` · concurrency cost 1 · image input

**Used for:** R.S. Rhys (3); Christine Leigh (2); H.J. Hakimi (2); Anais Amaris (1); Ch'an Lee (1); Eulalie Rowland (1); K.K. Kenyatta (1)

**Cross-genre roles** (forms outside the Genre Matrix): Mystery investigation support

**Avoid:** Cozy Mystery, feel-good and banter comedy · Dark seduction and Erotica; gothic atmosphere and dark-literary prose · Deep technical puzzle-boxes: the GLM 12B twin's shelf

### W20 · DavidAU/gemma-3-12b-it-vl-Deepseek-v3.1-Heretic-Uncensored-Thinking

Investigation writer. A 12B multimodal Gemma-3 with DeepSeek deep-research reasoning, uncensored (7/100), with vision for case material. Evidence-and-procedure stories.

**Call:** Featherless AI · `DavidAU/gemma-3-12b-it-vl-Deepseek-v3.1-Heretic-Uncensored-Thinking` · served context 32,768 tokens · class `gemma3-12b` · concurrency cost 1 · image input

**Used for:** Noelle Noir (5); MJ Montrose (3); Cassidy Cavendish (1); R.S. Rhys (1); Remy Raphael (1)

**Avoid:** Style-critical literary genres: Gothic Romance, Literary Romance · Dark seduction and Erotica; Cozy Mystery and feel-good · Fair-play puzzle elegance

### W21 · DavidAU/gemma-3-12b-it-vl-GPT-5.1-High-Heretic-Uncensored-Thinking

Scheme designer. A 12B multimodal Gemma-3 with GPT-5.1 high reasoning, uncensored. Enumerates designs, options and contingencies; best for corporate, technical and financial schemes.

**Call:** Featherless AI · `DavidAU/gemma-3-12b-it-vl-GPT-5.1-High-Heretic-Uncensored-Thinking` · served context 32,768 tokens · class `gemma3-12b` · concurrency cost 1 · image input

**Used for:** R.S. Rhys (4); MJ Montrose (3)

**Avoid:** Cozy, feel-good and banter comedy · Gothic atmosphere; dark seduction and Erotica · Wide-lens historical (the Gemini-3-Pro twin's shelf); deep mechanism puzzle-boxes (the GLM twin's shelf)

### W22 · DavidAU/gemma-3-12b-it-vl-Polaris-GLM-4.7-Flash-VAR-Thinking-Instruct-Heretic-Uncensored

Hybrid scheme-and-puzzle writer. Gemma-3 12B multimodal blending Polaris and GLM, uncensored. Schemes, puzzles and techno plots.

**Call:** Featherless AI · `DavidAU/gemma-3-12b-it-vl-Polaris-GLM-4.7-Flash-VAR-Thinking-Instruct-Heretic-Uncensored` · served context 32,768 tokens · class `gemma3-12b` · concurrency cost 1 · image input

**Used for:** MJ Montrose (2); R.S. Rhys (2); K.K. Kenyatta (1); Noelle Noir (1); Remy Raphael (1)

**Avoid:** Cozy Mystery, feel-good and banter comedy · Gothic atmosphere and dark-literary prose; dark seduction and Erotica · Single-register work where a dedicated twin is sharper

### W23 · DavidAU/gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking

Puzzle and timeline reasoner. Gemma-3 12B multimodal HighIQ Polaris, uncensored.

**Call:** Featherless AI · `DavidAU/gemma-3-12b-it-vl-HighIQ-Polaris-Heretic-Uncensored-Thinking` · served context 32,768 tokens · class `gemma3-12b` · concurrency cost 1 · image input

**Used for:** Noelle Noir (2); R.S. Rhys (2); Remy Raphael (2); Sebastian V. Somerset (2); Anais Amaris (1); H.J. Hakimi (1); K.K. Kenyatta (1); MJ Montrose (1); Naomi McNamara (1); R.S. Raphael (1)

**Avoid:** Cozy Mystery, feel-good and banter comedy · Gothic atmosphere; dark seduction and Erotica · Pure mechanism depth

### W24 · DavidAU/gemma-3-12b-it-vl-GLM-4.7-Flash-INSTRUCT-Thinking-Hybrid-Heretic-Uncensored

Switchable mechanism writer. Gemma-3 12B multimodal with GLM 4.7 Flash in a hybrid instruct/thinking build, uncensored.

**Call:** Featherless AI · `DavidAU/gemma-3-12b-it-vl-GLM-4.7-Flash-INSTRUCT-Thinking-Hybrid-Heretic-Uncensored` · served context 32,768 tokens · class `gemma3-12b` · concurrency cost 1 · image input

**Used for:** R.S. Rhys (7); MJ Montrose (2); K.K. Kenyatta (1)

**Avoid:** Cozy Mystery, feel-good and banter comedy · Gothic atmosphere; dark seduction and Erotica · Work that needs guaranteed thinking on every response

### W25 · DavidAU/gemma-3-12b-it-vl-GLM-4.7-Flash-Heretic-Uncensored-Thinking

Mechanism-depth thinker. Gemma-3 12B multimodal with GLM 4.7 Flash thinking on every response, uncensored.

**Call:** Featherless AI · `DavidAU/gemma-3-12b-it-vl-GLM-4.7-Flash-Heretic-Uncensored-Thinking` · served context 32,768 tokens · class `gemma3-12b` · concurrency cost 1 · image input

**Used for:** R.S. Rhys (9); MJ Montrose (1); R.S. Raphael (1)

**Avoid:** Cozy Mystery, feel-good and banter comedy · Gothic atmosphere and dark-literary prose; dark seduction and Erotica · Wide-lens historical genres

### W26 · DavidAU/Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated

Voice-led short-form writer. A 9B Gemma-2 writing merge, uncensored and abliterated, at its best on short voice-driven pieces and directed scenes. Not a planner or book-scale drafter.

**Call:** Featherless AI · `DavidAU/Gemma-The-Writer-9B-HERETIC-Uncensored-Abliterated` · served context 16,384 tokens · class `gemma2-9b` · concurrency cost 1

**Used for:** Christine Leigh (6); Deon D'Arcy (6); Carys Cassian (3); Gabby Gabriel (3); Avery Lee (2); Cassidy Cavendish (2); Ellis Leigh (2); Naomi McNamara (2); R.S. Raphael (2); R.S. Rhys (2); AJ Solomon (1); Anya Amara (1); Bree Beaumont (1); Callum Reid (1); CeeCee Chestervale (1); Drew D'Angelo (1); Gia Graceville (1); Gigi Gable (1); H.J. Hakimi (1); Marcel Moreau (1); Mimi Montclair (1); Noelle Noir (1); Remy Raphael (1); Sebastian V. Somerset (1)

**Avoid:** Reasoning and planning work: whodunit clue tables, heist design, outlines · Escalation genres: Slasher, transgression at length · Book-scale work; idea-weight philosophy and metafiction · Dark Romance and seduction; epic quests and procedurals

### W27 · Mantis2024/Dirty-Muse-Writer-v01-Uncensored-Erotica-NSFW

Explicit-literary specialist. A Gemma-2 9B merge combining an uncensored fiction writer with Gutenberg-era prose: frank and lyrical at once, strong with period voice. About 8K native context: keep scenes short.

**Call:** Featherless AI · `Mantis2024/Dirty-Muse-Writer-v01-Uncensored-Erotica-NSFW` · served context 16,384 tokens · class `gemma2-9b` · concurrency cost 1

**Used for:** Deon D'Arcy (5); Christine Leigh (4); D'Annie de Leon (1)

**Avoid:** Anything non-explicit: Cozy Mystery, feel-good, Women's Fiction · Plot-logic genres: whodunits, thrillers, Intellectual Adventure · Epic Fantasy and Space Opera

## Qwen3.5 DECKARD line

### W28 · DavidAU/Qwen3.5-4B-Deckard-HERETIC-UNCENSORED-Thinking

Pocket DECKARD. The flagship DECKARD character layer at 4B: character-forward prose, observation and point of view, vision intact, uncensored (4/100). Trades a little reasoning for narrative competence. Runs on a 4GB card.

**Call:** Featherless AI · `DavidAU/Qwen3.5-4B-Deckard-HERETIC-UNCENSORED-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-4b` · concurrency cost 1 · image input

**Used for:** R.S. Rhys (4); R.S. Raphael (3); Naomi McNamara (2); Noelle Noir (2); Sebastian V. Somerset (2); Callum Reid (1); Ellis Leigh (1); Kai Koan (1)

**Cross-genre roles** (forms outside the Genre Matrix): RP character work

**Avoid:** Pure mechanism and scheme genres · Graphic horror and visceral registers · Voice performance sustained across a book; book-scale drafting · Cozy warmth; fair-play whodunit elegance

### W29 · DavidAU/Qwen3.5-9B-Claude-4.6-Opus-Deckard-V4.2-Uncensored-Heretic-Thinking

9B DECKARD thinker on a multimodal base. Qwen3.5-9B's strong native reasoning trimmed for efficiency, the DECKARD character layer on top, uncensored (6/100 refusals), and vision intact: the only DECKARD build that can read images.

**Call:** Featherless AI · `DavidAU/Qwen3.5-9B-Claude-4.6-Opus-Deckard-V4.2-Uncensored-Heretic-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-9b` · concurrency cost 1 · image input

**Used for:** Noelle Noir (3); R.S. Rhys (3); R.S. Raphael (2); Ellis Leigh (1); Kai Koan (1); Naomi McNamara (1); Sebastian V. Somerset (1)

**Avoid:** Pure mechanism and scheme genres · Graphic horror and visceral registers · Cozy and whimsical warmth; banter duets · Book-scale 1M drafting; video work (untested)

### W30 · DavidAU/Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic

Anti-slop prose specialist. A 9B multimodal Qwen3.5 retrained on the strict PKD/DECKARD dataset to remove recognisable model-prose tics. The cleanest sentence-level prose in the 9B line, uncensored; needs explicit direction for graphic content.

**Call:** Featherless AI · `DavidAU/Qwen3.5-9B-The-Deckard-Pro-Writer-Uncensored-Heretic` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-9b` · concurrency cost 1 · image input

**Used for:** Carys Cassian (3); Cassidy Cavendish (2); Christine Leigh (2); Deon D'Arcy (2); Ellis Leigh (2); Naomi McNamara (2); Noelle Noir (2); R.S. Raphael (2); R.S. Rhys (2); Anya Amara (1); Avery Lee (1); Bree Beaumont (1); Drew D'Angelo (1); Gabby Gabriel (1); Gia Graceville (1); Gigi Gable (1); MJ Montrose (1); Mimi Montclair (1); Remy Raphael (1); Sebastian V. Somerset (1)

**Avoid:** Pulp-pace genres: Thriller-Suspense, Slasher, fast Romantic Adventure · Graphic horror and visceral registers · Cozy warmth; fair-play whodunits; spec-sheet and heist planning · Book-scale drafting; video work (untested)

### W31 · DavidAU/Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking

Dual-mind arguer. Two fused trains of thought in one 9B: a terse Claude analyst that argues with you, and a DECKARD voice that takes over for creative work. Uncensored. State length and detail in every brief or it answers tersely.

**Call:** Featherless AI · `DavidAU/Qwen3.5-9B-Deckard-Claude-DIMOE-Uncensored-Heretic-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-9b` · concurrency cost 1 · image input

**Used for:** Noelle Noir (3); Ellis Leigh (2); MJ Montrose (2); R.S. Rhys (2); Avery Lee (1); Callum Reid (1); Marcel Moreau (1); Naomi McNamara (1); R.S. Raphael (1); Sebastian V. Somerset (1)

**Avoid:** Lush, sustained prose: Romantic Adventure, Sensual Romance, Epic Fantasy · Cozy warmth; graphic horror · Fair-play whodunit elegance; book-scale drafting

### W32 · DavidAU/Qwen3.5-21B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking

Mid-size DECKARD flagship. Qwen3.5-27B contracted to 21B and out-reasoning its own parent: the DECKARD voice-and-ideas register, full uncensoring, 256K native context, and efficiency the 40B lacks.

**Call:** Featherless AI · `DavidAU/Qwen3.5-21B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** R.S. Rhys (6); Noelle Noir (3); Ellis Leigh (2); R.S. Raphael (2); Kai Koan (1); Marcel Moreau (1); Naomi McNamara (1); Sebastian V. Somerset (1)

**Avoid:** Pure mechanism and scheme genres: spec sheets, heist plans, procedurals · Graphic horror and visceral registers · Cozy and whimsical warmth · Book-scale 1M drafting, visual work, manic escalation

### W33 · DavidAU/Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking

Philip K. Dick author-voice model. A 27B multimodal Qwen3.5 trained on five PKD datasets: manufactured realities, unreliable perception, the android question and mystic breakdown. Uncensored; the only roster model built on one writer's obsessions.

**Call:** Featherless AI · `DavidAU/Qwen3.5-27B-Deckard-PKD-Heretic-Uncensored-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** R.S. Rhys (8); R.S. Raphael (4); Noelle Noir (3); Naomi McNamara (2); Christine Leigh (1); Deon D'Arcy (1); Ellis Leigh (1); MJ Montrose (1)

**Avoid:** Hard Science Fiction rigor and derivations · Cozy, whimsical and romance warmth · Epic Fantasy and High Fantasy; procedurals and fair-play whodunits · Graphic horror; book-scale drafting

## Qwen3.5 analyst and instruct line

### W34 · DavidAU/Qwen3.5-9B-Claude-4.6-OS-Auto-Variable-THINKING

Adaptive clean analyst. A 9B multimodal Qwen3.5 whose thinking blocks size themselves to the task; the strongest clean benchmark profile of the 9B line, with vision intact. Censored build; its Heretic twin handles dark content.

**Call:** Featherless AI · `DavidAU/Qwen3.5-9B-Claude-4.6-OS-Auto-Variable-THINKING` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-9b` · concurrency cost 1 · image input

**Used for:** R.S. Rhys (8); MJ Montrose (2); Sebastian V. Somerset (2); K.K. Kenyatta (1)

**Avoid:** Anything needing uncensored delivery; this is the censored build · Voice-driven genres (Dramatic Monologue, Fable, Epistolary Fiction) · Dark registers: Slasher, Transgressional Fiction, Grimdark Fantasy, Dark Romance · Cozy, whimsical and banter; book-scale drafting

### W35 · DavidAU/Qwen3.5-9B-Claude-4.6-HighIQ-THINKING-HERETIC-UNCENSORED

9B precision deducer. Claude 4.6 chain-of-thought fully replaces Qwen's thinking on the multimodal 9B base: short, precise, objective reasoning, uncensored (6/100), with a strong instruct mode when thinking is switched off.

**Call:** Featherless AI · `DavidAU/Qwen3.5-9B-Claude-4.6-HighIQ-THINKING-HERETIC-UNCENSORED` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-9b` · concurrency cost 1 · image input

**Used for:** R.S. Rhys (5); MJ Montrose (4); Noelle Noir (2); K.K. Kenyatta (1); Sebastian V. Somerset (1)

**Avoid:** Voice-and-ideas and voice-driven genres · Graphic horror and visceral registers · Cozy, whimsical and banter · Book-scale drafting; video work (untested)

### W36 · DavidAU/Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED

9B direct-delivery workhorse. The HighIQ model locked to instruct mode: Claude-style prose with no reasoning overhead, the strongest 9B instruct benchmarks in the roster, vision intact, uncensored. Needs explicit direction for graphic content.

**Call:** Featherless AI · `DavidAU/Qwen3.5-9B-Claude-4.6-HighIQ-INSTRUCT-HERETIC-UNCENSORED` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-9b` · concurrency cost 1 · image input

**Used for:** Christine Leigh (4); Deon D'Arcy (4); MJ Montrose (2); Noelle Noir (2); R.S. Rhys (2); Cassidy Cavendish (1); Remy Raphael (1)

**Cross-genre roles** (forms outside the Genre Matrix): Scene continuation and serial work (cross-genre role); RP sessions

**Avoid:** Genres needing shown reasoning: use the HighIQ THINKING twin · Voice-and-ideas genres · Graphic horror and visceral registers · Manic escalation; book-scale drafting; video work (untested)

### W37 · DavidAU/Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT

9B direct-delivery flagship. Locked to instruct mode: Claude-OS-style prose with zero reasoning overhead and the strongest 9B instruct benchmarks in the roster (ARC-C 0.624). Vision intact, uncensored; needs explicit direction for graphic content.

**Call:** Featherless AI · `DavidAU/Qwen3.5-9B-Claude-4.6-OS-HERETIC-UNCENSORED-INSTRUCT` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-9b` · concurrency cost 1 · image input

**Used for:** Christine Leigh (4); Deon D'Arcy (4); MJ Montrose (2); Noelle Noir (2); R.S. Rhys (2); Cassidy Cavendish (1); Remy Raphael (1)

**Cross-genre roles** (forms outside the Genre Matrix): Scene continuation and serial work (cross-genre role)

**Avoid:** Genres needing shown reasoning: use a thinking build · Voice-and-ideas genres · Graphic horror and visceral registers · Manic escalation; book-scale drafting; video work (untested)

### W38 · DavidAU/Qwen3.5-9B-Star-Trek-TNG-DS9-Heretic-Uncensored-Thinking

Star Trek canon voice. A 9B multimodal Qwen3.5 trained on TNG and DS9 material and voice: crew dynamics, ethical dilemmas, first-contact diplomacy. Strong instruct benchmarks and the highest knowledge-application score of any 9B (OBQA 0.454). Uncensored for the setting's dark edges; needs explicit direction.

**Call:** Featherless AI · `DavidAU/Qwen3.5-9B-Star-Trek-TNG-DS9-Heretic-Uncensored-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-9b` · concurrency cost 1 · image input

**Used for:** R.S. Rhys (8); Carys Cassian (1); H.J. Hakimi (1); Hanif J. Hakimi (1); O. O'Sullivan-Oz (1); Ria Garcia Reyes (1)

**Avoid:** Grimdark Fantasy and nihilistic registers; the optimism is baked in · Graphic horror and visceral registers · Hard Science Fiction rigor; technobabble is plot, not physics · Cozy warmth; book-scale philosophy; fair-play whodunits

### W39 · DavidAU/Qwen3.5-27B-Claude-4.6-OS-Auto-Variable-Heretic-Uncensored-Thinking

Uncensored 27B dark analyst. The uncensored twin of the 27B chief analyst: adaptive thinking, full vision, and near-lossless uncensoring. For schemes that must be rigorous and dark at once.

**Call:** Featherless AI · `DavidAU/Qwen3.5-27B-Claude-4.6-OS-Auto-Variable-Heretic-Uncensored-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** MJ Montrose (4); R.S. Rhys (4); R.S. Raphael (1)

**Avoid:** Voice-and-ideas and voice-driven genres · Pure prose-poetry and literary-dark sentence craft · Cozy, whimsical, banter and manic escalation · Book-scale drafting; video work (untested)

### W40 · DavidAU/Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored

Alpha literary realist. The Polaris register (grounded, character-led, morally serious) on the Qwen3.5-27B chassis, uncensored (14/100). The card flags alpha instability: a logic regression (BoolQ 0.694) and think-block looping, worst on MLX and mxfp4. Verify causal logic with the 27B OS INSTRUCT.

**Call:** Featherless AI · `DavidAU/Qwen3.5-27B-HERETIC-Polaris-Advanced-Thinking-Alpha-uncensored` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** R.S. Rhys (3); Hanif J. Hakimi (2); Marcel Moreau (2); Ria Garcia Reyes (2); Anais Amaris (1); Ellis Leigh (1); H.J. Hakimi (1); K.K. Kenyatta (1); Noelle Noir (1); Remy Raphael (1)

**Avoid:** Anything requiring reliable logic: fair-play whodunits, heist plans, paradox audits, procedurals · Mechanism genres: Techno-Thriller specs, Hard Science Fiction derivations · Voice-and-ideas at flagship depth; graphic horror; cozy and banter · MLX and mxfp4 deployments; book-scale drafting

## Qwen3 and Qwen3.6

### W41 · DavidAU/Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking

Wide-lens visual analyst. A 32B multimodal Qwen3-VL that reads images, video, documents and maps, plans in the Gemini scope-and-sweep register, and is uncensored with near-zero damage (3/100 refusals).

**Call:** Featherless AI · `DavidAU/Qwen3-VL-32B-Gemini-Heretic-Uncensored-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3vl-32b` · concurrency cost 2 · image input

**Used for:** R.S. Rhys (7); MJ Montrose (3); Bastien Benoit (1); Drew D'Angelo (1); H.J. Hakimi (1); K.K. Kenyatta (1); Marcel Moreau (1); Noelle Noir (1); R.S. Raphael (1)

**Avoid:** Voice-driven genres and intimate two-voice registers (banter, dark-romance duets) · Pure mechanism tabulation · Cozy and whimsical shelves · Manic escalation and single-scene vividness as the main job

### W42 · DavidAU/Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B

Horror-tainted engine. A 6B Brainstorm 20x build trained on a horror dataset: every genre comes back dark, the thinking block narrates in character, and prose runs long and graphic. Near-abliterated; regenerate on the occasional refusal.

**Call:** Local (Unsloth Desktop) · `DavidAU/Qwen3-Great-Bowels-Of-Horror-FREAKSTORM-6B` · not served by Featherless AI

**Used for:** R.S. Raphael (10); R.S. Rhys (10); Naomi McNamara (3); Bree Beaumont (1); Christine Leigh (1); Deon D'Arcy (1); Gabriel Varenne (1)

**Avoid:** Everything gentle: the taint corrupts Cozy Mystery, Whimsical Mystery, Feel-Good Fiction, Slice-of-Life Fiction, Sweet Romance, Cozy Fiction and Fable · Voice-fidelity work and fair-play whodunits · Idea-weight philosophy and satire · Book-scale drafting and technical work

### W43 · DavidAU/Qwen3-Horror-Instruct-Uncensored-262K-ctx-4B

Pocket horror engine. The horror-tuned sibling of the Short-Story 4B: coherent, escalating graphic horror with a brash narrator voice and 256K native context. Needs explicit direction to reach the graphic level.

**Call:** Featherless AI · `DavidAU/Qwen3-Horror-Instruct-Uncensored-262K-ctx-4B` · served context 32,768 tokens · class `qwen3-4b` · concurrency cost 1

**Used for:** R.S. Raphael (7); R.S. Rhys (7); Naomi McNamara (3); Deon D'Arcy (1); Ellis Leigh (1)

**Avoid:** Everything gentle: the horror tune tints all output · Brief-fidelity genres: whodunits, procedurals, heists · Voice-fidelity performance, book-scale drafting and series continuity · Warm romance and banter

### W44 · DavidAU/Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B

Pocket attitude storyteller. A 4B abliterated Qwen3 with a short-story fine-tune: short, idiosyncratic stories in a brash voice, at high variance. Plan for 2 to 5 regenerations per brief.

**Call:** Featherless AI · `DavidAU/Qwen3-Short-Story-Instruct-Uncensored-262K-ctx-4B` · served context 32,768 tokens · class `qwen3-4b` · concurrency cost 1

**Used for:** Ellis Leigh (6); August Reinhardt (1); Avery Lee (1); Naomi McNamara (1); Noelle Noir (1); R.S. Raphael (1); R.S. Rhys (1); Ria Garcia Reyes (1)

**Cross-genre roles** (forms outside the Genre Matrix): Flash fiction and story seeds

**Avoid:** Anything needing brief fidelity: whodunits, procedurals, heists · Graphic and visceral horror; it drifts under the brief · Voice-fidelity performance, book-scale work and series continuity · Romance that needs control

### W45 · nightmedia/Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess

Book-scale writer-thinker. A seven-stage Qwen3.6 27B merge with genuine long-horizon reasoning, a thinking on/off toggle and 1M native context. The only roster model that plans and drafts whole books.

**Call:** Featherless AI · `nightmedia/Qwen3.6-27B-Architect-Polaris2-Fable-B-F451-Tess` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** R.S. Rhys (4); Ellis Leigh (2); Remy Raphael (2); Anais Amaris (1); H.J. Hakimi (1); K.K. Kenyatta (1); Noelle Noir (1); R.S. Raphael (1); Ria Garcia Reyes (1)

**Avoid:** Cozy Mystery, feel-good and Slice-of-Life Fiction: overkill · Grimdark Fantasy, Dark Romance, Erotic Literature: uncensored weight is diluted · Banter comedy and persona-driven RP

## Mistral Nemo 12B

### W46 · DavidAU/MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored

Planned dark scene writer. The thinking version of the Mistral Nemo 12B Captain Eris Chimera with Claude Opus reasoning, uncensored. Plans each scene before writing; strongest in psychological and gothic horror and dark romance at short to mid length.

**Call:** Featherless AI · `DavidAU/MN-CaptainErisNebula-Chimera-v1.1-THINKING-ClaudeOpus4.5-12B-heretic-uncensored` · served context 32,768 tokens · class `mistral-nemo` · concurrency cost 1

**Used for:** R.S. Rhys (8); R.S. Raphael (6); Naomi McNamara (3); Deon D'Arcy (2); Bastien Benoit (1); Bree Beaumont (1); Carys Cassian (1); H.J. Hakimi (1); Hanif J. Hakimi (1); Noelle Noir (1); O. O'Sullivan-Oz (1); Ria Garcia Reyes (1)

**Avoid:** Book-scale drafting; fair-play whodunits · Idea-weight philosophy; deep technical derivation · Cozy and whimsical registers; voice-sketch monologue; manic escalation

### W47 · DavidAU/MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated

Dark seduction and character engine. The non-thinking Mistral Nemo 12B Captain Eris Chimera, uncensored and abliterated. Character-driven dark romance and gothic registers at short to mid length.

**Call:** Featherless AI · `DavidAU/MN-CaptainErisNebula-12B-Chimera-v1.1-heretic-uncensored-abliterated` · served context 32,768 tokens · class `mistral-nemo` · concurrency cost 1

**Used for:** Deon D'Arcy (5); Naomi McNamara (3); Christine Leigh (2); R.S. Raphael (2); R.S. Rhys (2); Bree Beaumont (1); Ch'an Lee (1); Gabriel Varenne (1); MJ Montrose (1); Noelle Noir (1); Sebastian V. Somerset (1)

**Avoid:** Book-scale drafting; fair-play whodunits; idea-weight philosophy · Cozy and whimsical; voice-sketch monologue · Technical derivation; escalation on a single keyword

### W48 · DavidAU/Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus

Vivid crime and horror scene writer. A Mistral Nemo 12B with Claude Opus thinking, uncensored. Plans, then writes vivid crime, psychological and graphic scenes.

**Call:** Featherless AI · `DavidAU/Mistral-Nemo-Inst-2407-12B-Thinking-Uncensored-HERETIC-HI-Claude-Opus` · served context 32,768 tokens · class `mistral-nemo` · concurrency cost 1

**Used for:** Noelle Noir (5); MJ Montrose (3); R.S. Raphael (3); R.S. Rhys (3); Naomi McNamara (2); Carys Cassian (1); Cassidy Cavendish (1)

**Avoid:** Book-scale drafting; fair-play whodunit elegance · Idea-weight philosophy; manic escalation · Voice-sketch fidelity: monologue, fable, animal fiction; wide-lens planning

### W49 · DavidAU/Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC

Warm-and-dark range writer. A Mistral Nemo 12B with a three-teacher thinking blend (Claude, Gemini, GPT-5.2), uncensored. Covers planned horror and gentle mystery and romance from one model.

**Call:** Featherless AI · `DavidAU/Mistral-Nemo-2407-12B-Thinking-Claude-Gemini-GPT5.2-Uncensored-HERETIC` · served context 32,768 tokens · class `mistral-nemo` · concurrency cost 1

**Used for:** R.S. Raphael (5); R.S. Rhys (5); Deon D'Arcy (4); Naomi McNamara (4); Christine Leigh (3); Noelle Noir (2); Bastien Benoit (1); Ellis Leigh (1); Remy Raphael (1)

**Avoid:** Book-scale drafting; fair-play whodunit elegance · Idea-weight philosophy; manic escalation; deep derivation · Voice-sketch fidelity

### W50 · TheDrummer/UnslopNemo-12B-v4.1

Anti-slop workhorse. A Mistral Nemo 12B adventure and RP model with AI-isms scrubbed from its training data. Clean, witty prose and strong recall; 1M native context suits series continuity.

**Call:** Featherless AI · `TheDrummer/UnslopNemo-12B-v4.1` · served context 32,768 tokens · class `mistral-nemo` · concurrency cost 1 · also on OpenRouter as `thedrummer/unslopnemo-12b`

**Used for:** Noelle Noir (4); Ch'an Lee (2); Deon D'Arcy (1); R.S. Rhys (1); Remy Raphael (1)

**Avoid:** Grimdark Fantasy, Southern Gothic, Weird Fiction · Dense literary modernism: Stream-of-Consciousness, Post-Modern Literature · Fair-play whodunits and Philosophical Mystery; Erotic Literature

### W51 · TheDrummer/UnslopNemo-12B-v4

Backup to UnslopNemo v4.1. The Project Unslop community edition and direct predecessor of v4.1; its source document calls it a backup for v4.1's shelf, not a new niche. 32K native context.

**Call:** Featherless AI · `TheDrummer/UnslopNemo-12B-v4` · served context 32,768 tokens · class `mistral-nemo` · concurrency cost 1

**Used for:** Ch'an Lee (2); Noelle Noir (2); R.S. Rhys (1); Remy Raphael (1)

**Avoid:** Continuity-heavy genres: whodunits, thrillers, sagas · Dark-literary registers; dense modernism; explicit literary erotica

### W52 · TheDrummer/UnslopNemo-12B-v3

Prose stylist with a bad memory. The best prose of the UnslopNemo line, at its best in raw-autocomplete notebook mode, but it loses track of setting and items mid-session. Keep the story bible in the prompt; 1M native context.

**Call:** Featherless AI · `TheDrummer/UnslopNemo-12B-v3` · served context 32,768 tokens · class `mistral-nemo` · concurrency cost 1

**Used for:** Ellis Leigh (3); Remy Raphael (2); Anya Amara (1); Avery Lee (1); CeeCee Chestervale (1); Christine Leigh (1); Deon D'Arcy (1); Gabby Gabriel (1); Gigi Gable (1); Noelle Noir (1)

**Avoid:** Anything continuity-critical: whodunits, thrillers, Epic Sagas, Family Saga · Long RP sessions without external state tracking · Grimdark Fantasy and dark-literary

### W53 · TheDrummer/UnslopNemo-12B-v1

Obedient synopsis executor. Expressive and uncensored, faithful to a detailed outline (heat included), but it brings no personality of its own: supply the character card.

**Call:** Featherless AI · `TheDrummer/UnslopNemo-12B-v1` · served context 32,768 tokens · class `mistral-nemo` · concurrency cost 1

**Used for:** Deon D'Arcy (6); Ellis Leigh (4); Christine Leigh (3); Gabby Gabriel (1); Marcel Moreau (1)

**Avoid:** Anything that needs the model to drive character

### W54 · FallenMerick/MN-Violet-Lotus-12B

Emotional-intelligence specialist. A Mistral Nemo 12B merge of four RP and creative models with a romance-capable lineage. Holds character voice and feeling across long emotional arcs; high prompt adherence.

**Call:** Featherless AI · `FallenMerick/MN-Violet-Lotus-12B` · served context 32,768 tokens · class `mistral-nemo` · concurrency cost 1

**Used for:** Deon D'Arcy (8); Christine Leigh (6)

**Avoid:** Grimdark Fantasy, Transgressional Fiction, Dark Romance at full intensity · Hard Science Fiction, Techno-Thriller, fair-play whodunits · Epic Fantasy and Space Opera

### W55 · EldritchLabs/MN-Crimson-Cafe-12B

Atmospheric ensemble storyteller. A Mistral Nemo 12B fusion of an atmospheric storyteller (Crimson-Constellation) with a long-session multi-character RP model (VelvetCafe-RP-V2). Lush prose, strong cast tracking, 128K native context.

**Call:** Featherless AI · `EldritchLabs/MN-Crimson-Cafe-12B` · served context 32,768 tokens · class `mistral-nemo` · concurrency cost 1

**Used for:** Christine Leigh (8); Gabriel Varenne (3); Deon D'Arcy (2); Naomi McNamara (2); R.S. Raphael (1); R.S. Rhys (1); Sebastian V. Somerset (1)

**Avoid:** Hard Science Fiction and Techno-Thriller · Fair-play whodunits and Police Procedural · Stream-of-Consciousness and Post-Modern Literature; Epic Fantasy and Space Opera

## Mistral Small 24B

### W56 · TheDrummer/Cydonia-24B-v4.1

The roster's Dungeon Master. A Mistral Small 3.2 24B with thick, weighty novel-style prose, strong detail recall over long sessions and 131K native context. Uncensored but not erotica-focused; brief it as a narrator with a running state block.

**Call:** Featherless AI · `TheDrummer/Cydonia-24B-v4.1` · served context 32,768 tokens · class `mistral-24b` · concurrency cost 2 · also on OpenRouter as `thedrummer/cydonia-24b-v4.1`

**Used for:** Ch'an Lee (3); H.J. Hakimi (3); Remy Raphael (2); AJ Solomon (1); Eulalie Rowland (1); R.S. Rhys (1)

**Avoid:** Cozy Mystery and feel-good · Fair-play whodunits and Philosophical Mystery · Dense literary modernism; Erotic Literature

### W57 · dphn/Dolphin-Mistral-24B-Venice-Edition

Utility infielder. A fully steerable general-purpose Mistral Small 24B with no alignment and no fiction training: it obeys the system prompt to the letter. Strong institutional knowledge; 128K native context; image input; temperature 0.15.

**Call:** Featherless AI · `dphn/Dolphin-Mistral-24B-Venice-Edition` · served context 32,768 tokens · class `mistral-24b` · concurrency cost 2 · also on OpenRouter as `cognitivecomputations/dolphin-mistral-24b-venice-edition`

**Used for:** MJ Montrose (4); R.S. Rhys (2); Deon D'Arcy (1); Noelle Noir (1); R.S. Raphael (1)

**Avoid:** Anything where prose style is the product: Gothic Romance, Literary Romance · Character-driven ensemble work: Family Saga, Women's Fiction · Fair-play puzzle plots

### W58 · DavidAU/Dolphin-Mistral-GLM-4.7-Flash-24B-Venice-Edition-Thinking-Uncensored

Dark-operations planner-writer. The Venice generalist with GLM reasoning implanted and no alignment: it deliberates before writing. 32K native context; keep temperature low for procedural passages.

**Call:** Featherless AI · `DavidAU/Dolphin-Mistral-GLM-4.7-Flash-24B-Venice-Edition-Thinking-Uncensored` · served context 32,768 tokens · class `mistral-24b` · concurrency cost 2

**Used for:** MJ Montrose (6); K.K. Kenyatta (1); R.S. Rhys (1)

**Avoid:** Cozy Mystery, feel-good and Slice-of-Life Fiction · Gothic atmosphere and emotional romance · Dense literary modernism; long-arc epics (32K ceiling)

## Llama

### W59 · DavidAU/Llama3.3-8B-Instruct-Thinking-Claude-4.5-Opus-High-Reasoning

Technical spec writer. A Llama-3.3 8B with Claude Opus high reasoning and 128K native context. Deep technical derivation for hard SF and technical thrillers. Censored; its Heretic twin handles dark delivery.

**Call:** Featherless AI · `DavidAU/Llama3.3-8B-Instruct-Thinking-Claude-4.5-Opus-High-Reasoning` · served context 8,192 tokens · class `llama3-8b` · concurrency cost 1

**Used for:** R.S. Rhys (9); MJ Montrose (3); K.K. Kenyatta (1)

**Avoid:** Anything needing uncensored delivery · Voice-driven genres; dark registers · Cozy, whimsical and banter · Book-scale drafting; epic quests and wide-lens sweeps as prose

### W60 · DavidAU/Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning

Structured dark planner-writer. A Llama-3.3 8B with Claude Opus high reasoning, uncensored. Structures gothic, occult and technical dark material before writing it.

**Call:** Featherless AI · `DavidAU/Llama3.3-8B-Instruct-Thinking-Heretic-Uncensored-Claude-4.5-Opus-High-Reasoning` · served context 8,192 tokens · class `llama3-8b` · concurrency cost 1

**Used for:** R.S. Rhys (8); R.S. Raphael (6); Naomi McNamara (3); Bastien Benoit (1); MJ Montrose (1); Sebastian V. Somerset (1)

**Avoid:** Cozy, whimsical and gentle registers · Voice-driven genres; two-voice banter duets · Book-scale drafting; escalation on a single keyword; pure scope planning

### W61 · DavidAU/Llama-3.3-8B-Thinking-Gemini-Flash-11000x-128k

Systems and scope planner. A Llama-3.3 8B with Gemini Flash thinking and 128K native context. Wide-lens planning for climate, corporate and space systems. Not built for uncensored delivery.

**Call:** Featherless AI · `DavidAU/Llama-3.3-8B-Thinking-Gemini-Flash-11000x-128k` · served context 8,192 tokens · class `llama3-8b` · concurrency cost 1

**Used for:** R.S. Rhys (9); MJ Montrose (2)

**Avoid:** Anything needing uncensored delivery · Voice-driven genres: monologue, fable, epistolary · Dark registers; cozy and whimsical · Deep derivation; book-scale drafting

### W62 · DavidAU/L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated

Dark-bias scene writer. A Llama-3 8B merge, uncensored and abliterated, that defaults grim and immersive. Short-form dark fiction.

**Call:** Featherless AI · `DavidAU/L3-Dark-Planet-8B-HERETIC-Uncensored-Abliterated` · served context 8,192 tokens · class `llama3-8b` · concurrency cost 1

**Used for:** R.S. Rhys (5); R.S. Raphael (4); MJ Montrose (2); Naomi McNamara (2); Noelle Noir (2); Anya Amara (1); Carys Cassian (1); Cassidy Cavendish (1); Deon D'Arcy (1); K.K. Kenyatta (1)

**Avoid:** Anything gentle: Cozy Mystery, Whimsical Mystery, Feel-Good Fiction, Slice-of-Life Fiction, Sweet Romance · Fair-play whodunits; idea-weight philosophy, Metafiction, Satire · Book-scale work; epic quests, procedurals, scheme design · Upbeat romance and banter comedy

### W63 · Nitral-AI/Hathor_Tahsin-L3-8B-v0.85

Persona engine. A Llama-3 8B RP model with near-perfect character-card adherence, decent classical-novel cadence and moderate uncensoring. Hard 8K native context: keep scenes under about 1,500 words.

**Call:** Featherless AI · `Nitral-AI/Hathor_Tahsin-L3-8B-v0.85` · served context 8,192 tokens · class `llama3-8b` · concurrency cost 1

**Used for:** Deon D'Arcy (5); Bastien Benoit (2); Christine Leigh (2)

**Avoid:** Epic Fantasy, Space Opera, Grimdark Fantasy · Fair-play whodunits and Philosophical Mystery · Dense literary prose; Literary Romance and Romantic Drama; Erotic Literature

### W64 · e-n-v-y/Legion-V2.1-LLaMa-70B-Elarablated-v0.8

Dark-literary heavyweight. A 20-model Llama-3.3 70B merge with an anti-slop (Elarablated v0.8) pass. Fully uncensored, densely descriptive literary prose, large casts, 128K native context. Multi-GPU class.

**Call:** Featherless AI · `e-n-v-y/Legion-V2.1-LLaMa-70B-Elarablated-v0.8-hf` · served context 32,768 tokens · class `llama33-70b` · concurrency cost 4 · **model ID differs from the Hugging Face repo**

**Used for:** R.S. Raphael (4); R.S. Rhys (4); Naomi McNamara (2); Ch'an Lee (1); Christine Leigh (1)

**Avoid:** Cozy Mystery, Cozy Fantasy and feel-good: overkill · Slice-of-life banter comedy

### W65 · huihui-ai/Llama-3.2-3B-Instruct-abliterated

Clean 3B abliteration. Stock Llama-3.2 3B with refusals removed and benchmarks preserved, but no creative-writing training: the style card carries all the weight. Holds committed tone for about 800 to 1,200 words. A substitute for the chuanli11 build, preferred for noir precision.

**Call:** Featherless AI · `huihui-ai/Llama-3.2-3B-Instruct-abliterated` · served context 32,768 tokens · class `llama32-3b` · concurrency cost 1

**Used for:** Naomi McNamara (3); Noelle Noir (3); R.S. Raphael (3); R.S. Rhys (3); Cassidy Cavendish (1); K.K. Kenyatta (1); MJ Montrose (1)

**Avoid:** Epic Fantasy, Space Opera, Hard Science Fiction · Stream-of-Consciousness, Modernist Fiction, Post-Modern Literature · Fair-play whodunits; Erotic Literature (Llama-3.2 still evades explicit content)

### W66 · chuanli11/Llama-3.2-3B-Instruct-uncensored

3B abliteration, second build. The same profile as the huihui-ai build by a different abliteration: general-purpose, refusals removed, slightly muddier output, still hedges on some topics. Short-form and atmosphere-driven.

**Call:** Featherless AI · `chuanli11/Llama-3.2-3B-Instruct-uncensored` · served context 32,768 tokens · class `llama32-3b` · concurrency cost 1

**Used for:** R.S. Raphael (5); R.S. Rhys (5); Naomi McNamara (3); Noelle Noir (2); Avery Lee (1); Bree Beaumont (1); Deon D'Arcy (1); Sebastian V. Somerset (1)

**Avoid:** Erotic Romance and Erotic Fiction: the base still deflects · Epic Fantasy, Space Opera, Hard Science Fiction · Stream-of-Consciousness, Modernist Fiction, Post-Modern Literature; fair-play whodunits

## ERNIE, Phi and LFM

### W67 · DavidAU/ERNIE-21B-A3B-Claude-4.5-High-OPUS-Thinking

Philosopher twin. A cheap, fast ERNIE MoE (about 3B active) with compact Opus-style ethical reasoning and explicit creative-prose tuning. Mostly uncensored; 128K native context.

**Call:** Featherless AI · `DavidAU/ERNIE-21B-A3B-Claude-4.5-High-OPUS-Thinking` · served context 32,768 tokens · max output 32,768 · class `ernie4_5_moe-21b` · concurrency cost 1

**Used for:** Remy Raphael (4); R.S. Rhys (3); Ellis Leigh (2); Noelle Noir (2); R.S. Raphael (2); Deon D'Arcy (1); Kai Koan (1); Naomi McNamara (1); Ria Garcia Reyes (1)

**Avoid:** Cozy Mystery, feel-good and banter comedy · Dark Romance and seduction character work · Grimdark Fantasy and transgressive; atmospheric gothic

### W68 · ArliAI/Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1

Banter and persona engine. A 3.8B Phi-3.5 roleplay fine-tune trained for persona variety and ensemble banter in light, warm registers. Censored base: it softens or refuses dark material.

**Call:** Local (GGUF from Hugging Face) · `ArliAI/Phi-3.5-mini-3.8B-ArliAI-RPMax-v1.1-GGUF` · not served by Featherless AI

**Used for:** Deon D'Arcy (4); Carys Cassian (3); Christine Leigh (3); Cassidy Cavendish (2); Ellis Leigh (2); Gabby Gabriel (2); Noelle Noir (2); Anya Amara (1); August Reinhardt (1); Avery Lee (1); Bree Beaumont (1); Drew D'Angelo (1); Gia Graceville (1); Gigi Gable (1); Mimi Montclair (1); Remy Raphael (1)

**Avoid:** Dark Romance, Grimdark Fantasy, Erotic Fiction, Mafia Romance: it censors them · Thriller, espionage, heist and conspiracy plot machinery · Epic Fantasy, Space Opera, Hard Science Fiction: worldbuilding drift · Stream-of-Consciousness, Modernist Fiction, Post-Modern Literature

### W69 · DavidAU/LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF

Cozy series engine. A small 2.6B creative-writing merge, reliable on short, formula-shaped, self-contained scenes with a small cast.

**Call:** Local (GGUF from Hugging Face) · `DavidAU/LFM2.5-2.6B-Qwen3.8-Turbo-Brilliance-Power-X12-NEO-MAX-GGUF` · not served by Featherless AI

**Used for:** Noelle Noir (8); Ellis Leigh (4); Avery Lee (1); CeeCee Chestervale (1); Christine Leigh (1); Deon D'Arcy (1); Gabby Gabriel (1); Sebastian V. Somerset (1)

**Avoid:** Epic Fantasy and Epic Quest Fantasy · Hard Science Fiction · Stream-of-Consciousness, Modernist Fiction, Post-Modern Literature · Grimdark Fantasy and Dark/Rogue Epic Fantasy

## Additions of 14 November 2026: Mistral Nemo 12B

### W70 · DavidAU/Rocinante-X-12B-v1-Heretic-Uncensored

Long-session character engine. TheDrummer's Rocinante-X 12B (Mistral Nemo), Heretic-abliterated to 9/100 refusals at near-zero damage. Holds a character and voice across long RP sessions, dialogue-forward, with smooth shifts between tame and explicit scenes. Use the Mistral v3 Tekken or Metharme template; the creator notes some "it's not just X, it's Y" phrasing.

**Call:** Featherless AI · `DavidAU/Rocinante-X-12B-v1-Heretic-Uncensored` · served context 32,768 tokens · class `mistral-nemo` · concurrency cost 1

**Used for:** Deon D'Arcy (7); Christine Leigh (5); Noelle Noir (3); Ch'an Lee (1); Ellis Leigh (1); Gabriel Varenne (1); Naomi McNamara (1); Remy Raphael (1)

**Avoid:** Graphic horror and visceral registers · Fair-play whodunits; idea-weight philosophy and metafiction · Book-scale drafting; deep reasoning and scheme design · Voice-document fidelity: Dramatic Monologue, Epistolary Fiction · Manic escalation; series-scale continuity

## Additions of 14 November 2026: Qwen3.6 27B line and its shrinks

### W71 · DavidAU/Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP

Flagship generalist. A Qwen3.6 27B multi-stage fusion (Fable traces, Claude Opus reasoning, F451, Polaris) with the cleanest Heretic pass in the series (4/100 refusals, KL 0.047). ARC-C 0.711, confirmed by third parties. The strongest reasoner in the roster; specialists still own their niches. Instruct mode temp 0.7 for prose, thinking mode temp 1.0 for planning.

**Call:** Featherless AI · `DavidAU/Qwen3.6-27B-Fable-Fusion-711-Uncensored-Heretic-NM-DAU-MTP` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** Christine Leigh (77); Deon D'Arcy (69); R.S. Rhys (56); Ch'an Lee (51); Remy Raphael (26); H.J. Hakimi (21); Gabriel Varenne (18); Sebastian V. Somerset (14); D'Annie de Leon (11); K.K. Kenyatta (9); Naomi McNamara (8); R.S. Raphael (8); Kai Koan (6); AJ Solomon (5); Anais Amaris (5); Laurent Levesque (5); Bastien Benoit (4); Hanif J. Hakimi (3); MJ Montrose (3); Marcel Moreau (3); Bree Beaumont (2); Ellis Leigh (2); Eulalie Rowland (2); Noelle Noir (2); Anya Amara (1); Avery Lee (1); Carys Cassian (1); O. O'Sullivan-Oz (1); Ria Garcia Reyes (1)

**Cross-genre roles** (forms outside the Genre Matrix): Series-scale continuity (within its context window); Graphic horror on explicit direction

**Avoid:** Manic escalation as a feature · Single-author voice fidelity at book scale · Book-scale 1M drafting; video input (untested)

### W72 · DavidAU/Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic

Literary-dystopian reasoner. A three-stage Qwen3.6 27B: F451 (dystopian and social SF), then Polaris (literary realism), then an intelligence-raising stage; ARC-C 0.665, above its base. Reasons out a society's mechanism, then writes it. Heretic-uncensored, though the card posts no refusal figures.

**Call:** Featherless AI · `DavidAU/Qwen3.6-27B-F451-AND-TRI-Polar-Ultra-Pro-Writer-Uncensored-Heretic` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** R.S. Rhys (4); Hanif J. Hakimi (2); Marcel Moreau (2); Anais Amaris (1); Christine Leigh (1); Ellis Leigh (1); H.J. Hakimi (1); K.K. Kenyatta (1); MJ Montrose (1); Noelle Noir (1); R.S. Raphael (1); Remy Raphael (1); Ria Garcia Reyes (1)

**Avoid:** Pulp-pace genres: Thriller-Suspense, Slasher, fast Romantic Adventure · Graphic horror; cozy and warm registers · Fair-play whodunit elegance; DECKARD-depth Philosophical Fiction and Metafiction · Book-scale 1M drafting; mechanism genres such as Techno-Thriller specs and Hard Science Fiction derivation

### W73 · DavidAU/Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking

Neutral uncensored flagship. Qwen3.6 27B, Heretic'd (4/100 refusals, KL 0.047) and given a light firm-up tune; ARC-C 0.673, above the censored base. No register of its own: it follows the brief's genre. Also the A/B baseline for testing what a flavored build adds.

**Call:** Featherless AI · `DavidAU/Qwen3.6-27B-Heretic2-Uncensored-Finetune-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** R.S. Rhys (98); Christine Leigh (79); Deon D'Arcy (68); Ch'an Lee (51); Remy Raphael (25); H.J. Hakimi (21); Gabriel Varenne (18); R.S. Raphael (14); Sebastian V. Somerset (13); D'Annie de Leon (11); K.K. Kenyatta (9); Naomi McNamara (8); AJ Solomon (5); Kai Koan (5); Laurent Levesque (5); Anais Amaris (4); Bastien Benoit (4); Hanif J. Hakimi (4); MJ Montrose (4); Marcel Moreau (3); Bree Beaumont (2); Carys Cassian (2); Eulalie Rowland (2); O. O'Sullivan-Oz (2); Ria Garcia Reyes (2); Anya Amara (1); Cassidy Cavendish (1); Noelle Noir (1)

**Cross-genre roles** (forms outside the Genre Matrix): Cross-model A/B baseline, prompt development and baseline drafting; Graphic registers on explicit direction

**Avoid:** Genres where a specialist is strictly better: it is strong everywhere and best nowhere · Book-scale drafting; video input (untested)

### W74 · DavidAU/Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking

Budget uncensored workhorse. The Heretic'd Qwen3.6 27B shrunk to 21B (64 to 48 layers) and retuned on four datasets. Keeps about 93% of the 27B's ARC-C (0.602 instruct, 0.445 thinking): coherent, slightly diminished, vision intact. The card suggests 2 to 3 generations per brief.

**Call:** Featherless AI · `DavidAU/Qwen3.6-21B-IQ-Ultra-Heretic-Uncensored-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** Christine Leigh (77); Deon D'Arcy (69); Ch'an Lee (51); R.S. Rhys (51); Remy Raphael (25); H.J. Hakimi (20); Gabriel Varenne (18); Sebastian V. Somerset (13); D'Annie de Leon (11); K.K. Kenyatta (10); Naomi McNamara (10); R.S. Raphael (9); AJ Solomon (5); Kai Koan (5); Laurent Levesque (5); Anais Amaris (4); Bastien Benoit (4); Hanif J. Hakimi (3); Marcel Moreau (3); Bree Beaumont (2); Eulalie Rowland (2); MJ Montrose (2); Anya Amara (1); Carys Cassian (1); Cassidy Cavendish (1); Noelle Noir (1); O. O'Sullivan-Oz (1); Ria Garcia Reyes (1)

**Cross-genre roles** (forms outside the Genre Matrix): Graphic horror and erotica on explicit direction

**Avoid:** Where the 27B tier is meaningfully better: fair-play whodunits, Hard Science Fiction derivation, series audits, flagship-depth voice and ideas · Surreal Literature, Stream-of-Consciousness and Psychotropic Literature: too healthy for the broken-prose shelves · Book-scale drafting; video input (untested)

### W75 · DavidAU/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop

Word-slip instrument. Stage 2 of the 12B shrink (24 of 64 layers). Scene structure and the thinking-block plan hold; the prose carries word-level corruption (ARC-C 0.314). Also usable as a fast planner: take the thinking block's plan and give it to a healthy writer. 2 to 3 generations minimum.

**Call:** Featherless AI · `DavidAU/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** R.S. Raphael (4); R.S. Rhys (4); Naomi McNamara (2)

**Cross-genre roles** (forms outside the Genre Matrix): Creepypasta and uncanny horror (short); Analog-horror and found-document registers; Outline drafting from the thinking block, prose by a healthy model; Experimental fragments and erasure source text; Dream sequences within larger works

**Avoid:** Clean prose: literary fiction, romance, historical, literary mystery · Reliable logic: fair-play whodunits, heist plans, Techno-Thriller specs, procedurals · Coherence-dependent horror (Slasher, Gothic with a sustained reveal); voice-fidelity genres · Cozy and warm registers; book-scale drafting; video input (untested)

### W76 · DavidAU/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking

Logic-drift instrument. The Heretic'd Qwen3.6 27B shrunk to 12B (24 of 64 layers), Stage 1 of a two-stage tune. Sentences stay grammatical but the logic between them breaks (ARC-C 0.314). Draft dream, haunting and breakdown passages here and splice them into a manuscript a healthy model writes. 2 to 3 generations minimum.

**Call:** Featherless AI · `DavidAU/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** R.S. Raphael (5); R.S. Rhys (5); Naomi McNamara (3)

**Cross-genre roles** (forms outside the Genre Matrix): Dream sequences within larger works; Uncanny prose for experimental collage; Madness and possession passages

**Avoid:** Everything that needs narrative logic: mysteries, heists, procedurals, thrillers, romance arcs, war, historical · Clean literary prose; voice-fidelity genres · Graphic horror; cozy and warm registers · Fair-play whodunits, clue tables and planning; book-scale drafting; video input (untested)

### W77 · DavidAU/Qwen3.6-9B-Heretic-Uncensored-Thinking-Sweet-Madness

Surrealist instrument. The Heretic'd Qwen3.6 27B shrunk to 9B (16 of 64 layers). The thinking block still plans; the prose dissolves into dream-logic. The card warns it must not be relied on for anything productive until fully trained. Use it only for passages meant to read as broken, 2 to 3 generations minimum, rep pen 1.1.

**Call:** Featherless AI · `DavidAU/Qwen3.6-9B-Heretic-Uncensored-Thinking-Sweet-Madness` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** R.S. Raphael (3); R.S. Rhys (3); Naomi McNamara (2); Noelle Noir (2)

**Cross-genre roles** (forms outside the Genre Matrix): Madness and fever passages within larger works; Creepypasta and uncanny internet horror (short); Found-document and experimental forms

**Avoid:** Almost everything: any genre that needs narrative coherence · Voice-fidelity genres as controlled performance; fair-play whodunits, clue tables, scheme design · Graphic horror; cozy and warm registers; book-scale drafting · Any productive use: planning, analysis, continuity (the card's own warning); video input (untested)

## Planners

### C01 · DavidAU/LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL

Pocket clue and structure planner. A 1.2B LFM2.5 thinking distill with Claude Opus reasoning, uncensored. Clue tables, outlines, scheme design and continuity audits; does not write primary prose.

**Call:** Featherless AI · `DavidAU/LFM2.5-1.2B-Thinking-Claude-4.6-Opus-Heretic-Uncensored-DISTILL` · served context 32,768 tokens · max output 32,768 · class `lfm2-1b` · concurrency cost 1

**Used for:** MJ Montrose (2); Naomi McNamara (2); R.S. Raphael (2); R.S. Rhys (2); Callum Reid (1); Noelle Noir (1); Sebastian V. Somerset (1)

**Cross-genre roles** (forms outside the Genre Matrix): Outliner and structural passes (any genre); Continuity and consistency audits

**Avoid:** All primary prose; fair-play puzzle prose · Voice-driven genres; book-scale drafting; immersive dark scenes

### C02 · DavidAU/LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL

Pocket hybrid planner. A 1.2B LFM2.5 thinking distill blending several teachers, uncensored. Plans and audits; does not write primary prose.

**Call:** Featherless AI · `DavidAU/LFM2.5-1.2B-Thinking-SuperMinds-7x-Heretic-Uncensored-DISTILL` · served context 32,768 tokens · max output 32,768 · class `lfm2-1b` · concurrency cost 1

**Used for:** MJ Montrose (3); R.S. Rhys (2); Bastien Benoit (1); Carys Cassian (1); H.J. Hakimi (1); Hanif J. Hakimi (1); K.K. Kenyatta (1); O. O'Sullivan-Oz (1); Ria Garcia Reyes (1)

**Cross-genre roles** (forms outside the Genre Matrix): Cross-genre and mashup planning; Continuity audits (any genre)

**Avoid:** All primary prose · Single-register planning where a specialist planner is sharper · Voice-driven, cozy or intimate genres; book-scale drafting

### C03 · DavidAU/LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL

Pocket scope planner. A 1.2B LFM2.5 thinking distill in the Gemini Pro register, uncensored. Timelines, worldbuilding audits and multi-generational structure; does not write primary prose.

**Call:** Featherless AI · `DavidAU/LFM2.5-1.2B-Thinking-Gemini-Pro-1000-Heretic-Uncensored-DISTILL` · served context 32,768 tokens · max output 32,768 · class `lfm2-1b` · concurrency cost 1

**Used for:** R.S. Rhys (7); Anais Amaris (1); Bastien Benoit (1); Ch'an Lee (1); Drew D'Angelo (1); H.J. Hakimi (1); K.K. Kenyatta (1); Laurent Levesque (1); MJ Montrose (1)

**Avoid:** All primary prose · Fair-play clue tables; scheme or mechanism design · Voice-driven, cozy or intimate genres

### C04 · DavidAU/Gemma-3-1B-it-GLM-4.7-Flash-Heretic-Uncensored-Thinking

Pocket planner. A 1B Gemma-3 with GLM 4.7 thinking that runs on a phone or CPU; uncensored but needs explicit direction; 32K native context. The planning half of a pipeline: hand its plans to a prose writer.

**Call:** Featherless AI · `DavidAU/Gemma-3-1B-it-GLM-4.7-Flash-Heretic-Uncensored-Thinking` · served context 32,768 tokens · class `gemma3t-1b` · concurrency cost 1

**Used for:** MJ Montrose (2); Noelle Noir (2); Naomi McNamara (1); R.S. Raphael (1); R.S. Rhys (1)

**Avoid:** Everything style-critical: Gothic Romance, Literary Romance, Weird Fiction · Long-form anything; emotionally complex character work; Erotica

### C05 · DavidAU/Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x

Fast premise generator. A Llama-3.3 8B with Claude Haiku reasoning. Quick premises, twist shorts and short atmospheric pieces. Not built for uncensored delivery.

**Call:** Featherless AI · `DavidAU/Llama-3.3-8B-Instruct-Thinking-Claude-Haiku-4.5-High-Reasoning-1700x` · served context 8,192 tokens · class `llama3-8b` · concurrency cost 1

**Used for:** R.S. Rhys (5); Carys Cassian (2); MJ Montrose (2); H.J. Hakimi (1); Hanif J. Hakimi (1); K.K. Kenyatta (1); O. O'Sullivan-Oz (1); R.S. Raphael (1); Ria Garcia Reyes (1)

**Avoid:** Deep technical exposition · Anything needing uncensored delivery · Voice-driven genres; dark registers · Book-scale drafting; deep mechanism puzzle-boxes

### C06 · DavidAU/Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking

Early-alpha wide-lens planner. Gemini 3 Pro compact reasoning on the Qwen3.5-27B chassis. Censored. The card flags alpha instability: a real logic regression (BoolQ 0.709 against the base's 0.857) and think-block looping, worst on MLX and mxfp4. Scout with it; verify with the 27B OS INSTRUCT before anything enters a manuscript.

**Call:** Featherless AI · `DavidAU/Qwen3.5-27B-Gemini3-Pro-High-Reasoning-Compact-Thinking` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-27b` · concurrency cost 2 · image input

**Used for:** R.S. Rhys (7); Anais Amaris (1); Bastien Benoit (1); Ch'an Lee (1); Drew D'Angelo (1); H.J. Hakimi (1); K.K. Kenyatta (1); Laurent Levesque (1); MJ Montrose (1)

**Avoid:** Anything requiring reliable logic: fair-play whodunits, heist plans, paradox audits, procedurals · Anything needing uncensored delivery; this is the censored build · Voice-and-ideas and voice-driven genres; graphic horror; cozy and banter · MLX and mxfp4 deployments; book-scale drafting

## Analysts and evidence readers

### C07 · DavidAU/Qwen3.5-2B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING

Pocket evidence reader. The smallest roster model that can both reason and see: a 2B multimodal Qwen3.5 with reduced Claude-style thinking and full uncensoring. Support tier: it reads, triages and outlines; it does not headline prose.

**Call:** Featherless AI · `DavidAU/Qwen3.5-2B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-2b` · concurrency cost 1 · image input

**Used for:** R.S. Rhys (3); Sebastian V. Somerset (2); MJ Montrose (1); Naomi McNamara (1); Noelle Noir (1); R.S. Raphael (1)

**Cross-genre roles** (forms outside the Genre Matrix): Outliner and beat-sheets (cross-genre role); Light scene continuation (cross-genre role); Multilingual quick passes

**Avoid:** Primary prose for any genre · Voice-driven genres · Graphic horror and visceral registers · Fair-play whodunit elegance; book-scale drafting; cozy warmth

### C08 · DavidAU/Qwen3.5-4B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING

Complete small pipeline. A 4B multimodal Qwen3.5 that reads documents and images, reasons in adaptive Claude-style blocks and writes the scene, with the cleanest uncensoring of any small model in the roster (4/100). Runs on a 4GB card.

**Call:** Featherless AI · `DavidAU/Qwen3.5-4B-Claude-4.6-OS-Auto-Variable-HERETIC-UNCENSORED-THINKING` · served context 32,768 tokens · max output 32,768 · class `qwen3_5-4b` · concurrency cost 1 · image input

**Used for:** R.S. Rhys (3); MJ Montrose (2); Sebastian V. Somerset (2); Naomi McNamara (1); Noelle Noir (1); R.S. Raphael (1)

**Cross-genre roles** (forms outside the Genre Matrix): Outliner and clue-tables (cross-genre role); Serial scene continuation (cross-genre role)

**Avoid:** Voice-driven genres and voice-and-ideas genres · Graphic horror and visceral registers · Fair-play whodunit elegance; book-scale drafting; cozy warmth

### C09 · DavidAU/Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL

Series analyst. A 7B thinking distill whose 1M-token native context holds a whole multi-book series for continuity audits, series bibles and anthology planning. Censored build: pair it with an uncensored model for dark delivery.

**Call:** Featherless AI · `DavidAU/Qwen2.5-7B-Instruct-1M-Thinking-Claude-Gemini-GPT5.2-DISTILL` · served context 32,768 tokens · class `qwen2-7b` · concurrency cost 1

**Used for:** R.S. Rhys (6); Ch'an Lee (2); Christine Leigh (2); Hanif J. Hakimi (2); Bastien Benoit (1); Carys Cassian (1); Drew D'Angelo (1); H.J. Hakimi (1); Laurent Levesque (1); MJ Montrose (1); Noelle Noir (1); O. O'Sullivan-Oz (1); Ria Garcia Reyes (1); Sebastian V. Somerset (1)

**Avoid:** Voice-driven prose (Dramatic Monologue, Fable, Epistolary Fiction, Animal Fiction) · Dark delivery; this is the censored build · Single-scene vividness and RP character immersion · Deep single-scene derivation

### C10 · DavidAU/Qwen3.5-27B-Claude-4.6-OS-INSTRUCT

Clean 27B chief analyst. The strongest pure reasoner in the roster (ARC-C 0.675), multimodal, with adaptive Gemini/Qwen thinking. Censored build: for maximum-rigor planning and verification where the content stays clean.

**Call:** Featherless AI · `DavidAU/Qwen3.5-27B-Claude-4.6-OS-INSTRUCT` · served context 32,768 tokens · max output 32,768 · class `qwen3.5-27b` · concurrency cost 2 · image input

**Used for:** R.S. Rhys (5); MJ Montrose (3); K.K. Kenyatta (1)

**Cross-genre roles** (forms outside the Genre Matrix): Series-scale continuity audits (cross-genre role)

**Avoid:** Anything needing uncensored delivery; this is the censored build · Voice-and-ideas and voice-driven genres · Dark registers: Slasher, Transgressional Fiction, Grimdark Fantasy, Dark Romance · Cozy, whimsical, banter and manic escalation
