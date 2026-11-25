# Writing EOS app engine

The first working parts of the app itself:
- the **Story Blueprint formula engine** (`eos_app/blueprint.py`; requirements v0.7, FR-DEV-14 to FR-DEV-23, Appendix C)
- **Humanize** (`eos_app/humanize.py`; requirements v0.8, FR-HU-1 to FR-HU-9), described at the end of this file.
- the **workflow engine** (`eos_app/workflow.py`; requirements v0.10, FR-FLOW, FR-NM, FR-SW), described below.
- the **shared library** (`eos_app/library.py`; requirements v0.20, FR-LIB): your eight pools, from characters and pen names to content levels and the conflict-to-structure map, described below.

## Story Blueprint formula engine

The Story Blueprint Pipeline gives formulas and tables for planning a story. This engine computes everything those formulas and tables decide, so a model never does arithmetic or looks up a table. A model only supplies the judgement scores, such as how strongly the material supports a source of conflict. Code then works out the totals, the rankings and the routing.

## What it computes

| Step | Function | Who supplies what |
|---|---|---|
| Pillar factor | `pillar_factor` | Code, from the implied Pillars and the core's typical Pillars |
| Conflict Fit for all nine cores, ranked, read with the decision table | `score_cores` | The rater gives Source, Theme, Genre and contradictions. Code does the rest. |
| Does the conflict need a face? | `needs_antagonist` | Code |
| Climax outcome type | `outcome_type` | The agent answers two questions with reasons. Code finds the type. |
| Structure Fit for the six structures, the baseline of 18, the Kishōtenketsu flag | `score_structures` | Code scores Outcome, Inevitability and Novelty. The rater scores Intensity Curve, Pacing and Cast Shape. |
| Cast Function Map (Vacancy Rule) | `cast_function_map` | The agent assigns characters to functions. Code checks the assignments and lists the gaps. |
| Arc checks (Oscillation Rule, Collapse warning, next Ghost) | `arc_checks` | Code |
| Arc Blueprint skeleton from the Plot Blueprint | `gant_skeleton` | Code |
| Stage gates and the Stage 2 Guardrail | `stage_gate`, `guardrail_diff` | Code |
| Pillar notation and the Technology fallback check | `pillar_notation`, `parse_pillar`, `technology_fallback_flag` | Code |
| Stage 1 quality checks | `plot_blueprint_checks` | Code |
| Who decides | `who_decides` | Code, from the tables |

## Who decides

Every result carries a recommendation, never a decision. The Conflict Core pick, the outcome, the structure, the cast map and any cut or merge are the Author's calls (`decided_by = "author"`).

Agents may settle only the routing the formulas determine:
- returning weak material to the braindump
- filing a runner-up core
- sending work back after a Guardrail or Kishōtenketsu flag
- sending a vacant function to the Character Pool
- starting the Antagonist Role Spec
- recording the next Ghost

These are listed under `agent_may_settle` in the tables. Anything not on that list goes to the Author.

Every result records its inputs, the table version, and which factor came from the rater and which from code.

## Tables

All weights and tables live in `config/blueprint_tables.yaml`. To calibrate (FR-DEV-8), change a weight, update `maximum` to match, change `version`, and log the change. The engine refuses to load the file if a maximum doesn't match its weights or a name is unknown.

## Humanize

Humanize rewrites a passage so it reads as natural prose in the pen name's voice. It is the Editor's Humanize action and an optional Prose Refinement pass. The model only rewrites; code does the rest:

1. **Protects** locked lines and dialogue behind placeholders like `⟦P1⟧`, so they come back exactly as written.
2. **Builds the request** from the settings and the project style card: strength, passes, English variant, em dash policy and a word range of ±10%.
3. **Cleans** the output: lead-ins, headings, lists and bold are removed; *italics* stay; the em dash policy touches narration only.
4. **Measures** before and after: sentence length and spread, vocabulary variety, stock phrases, summary openers, em dashes and reading ease.
5. **Checks** length drift (warning above 10%, failure above 25%) and that every Story Bible name survives. A failed call is retried twice, then the router moves to the Fallback.
6. **Returns a suggestion** for the paragraph gate. Nothing is saved until you accept it.

`recommend()` suggests the strength and passes from the text itself, with a one-line reason and no model call. All settings, phrase lists and limits are in `config/humanize.yaml`.

The model call is passed in as a function: the router picks the Edit Actions model (Primary, Fallback, mature tier), so this module never touches the network.

The approach comes from the open-source *ai-humanizer-app* on GitHub. That repository has no licence, so none of its code or prompt text is used here: this is a fresh version written for fiction. It aims at the pen name's voice, not at passing AI detectors.

## Workflow engine

The app follows the Notion database *Narrative Components*. `config/components.yaml` is the app's copy of it: one entry per component, 123 in all. Each entry holds:
- the Step and the database name, shown in the Engine view
- a plain name, shown in the Writer view
- its place in the Flow Order and its phase
- how it runs: in sequence, per chapter, only on a failed check, on demand, or throughout
- the inputs it needs and the gate after it
- its code parts
- its line of experts: `primary` (the database's Frontier Model column), `comparable` (Comparable Open-Weight) and `fallback` (Fallback Model). The slot says the model's place in the line, not what kind of model it is: a cheaper comparable model can be the Primary
- for a media component, what it makes (`modality`)
- the Swarm Tier and the Jev role

`workflow.py` reads that file and:
- refuses a copy with a gap in the order, a repeated name or an input that isn't in the list
- `check_order()` lists, in plain words, every component that would run before an input it needs
- `next_to_run()` gives the components that can start now: their inputs are done **and every gate before them is approved**. Nothing past a gate is offered until you approve it; `waiting_on()` names the gate holding a component back
- chapters keep their own progress: `next_to_run(..., chapter=2)` gives chapter 2's work. Planning may run ahead; drafting waits for the previous chapter's lock
- the recipe gate applies only when a recipe was built (`gate_when_run`)
- `chapter_loop()` gives the 17 steps of every chapter, and `gates()` your decision points
- `run_plan()` says how many models work on a component: Full = the Primary plus a second, different expert from its own line, Light = one, None = code
- `jev_role()` says what Jev (`typesafe/jev-1.14`) may do with a decision: it settles only what agents may settle, and otherwise its pick is a recommendation

### When the database changes

Export *Narrative Components* from Notion as CSV (… → Export → Markdown & CSV), then:

    python -m eos_app.sync check "<the export.csv>"    # lists what would change; writes nothing
    python -m eos_app.sync build "<the export.csv>"    # rebuilds components.yaml and checks its order

The database does not record what a component takes in, its code parts, what a checker judges or what a media component makes. Those live in `config/component_inputs.yaml`, which this app owns. A new database row needs an entry there first; the build stops and names it otherwise. `python -m eos_app.sync export out.csv` writes the app's copy in the database's own columns, for comparing by eye.

**Rule:** everything the app depends on is built by a command in this repository. Nothing lives in a temporary folder.

## Models and routing

`config/models.yaml` is the app's copy of three sources, joined (decision D33):
- your roster *LLM Identifier*: every model with a provider, its ID, its boxes (Frontier, Open-Weights, Uncensored,
  Can Run Locally) and its Comparable and Fallback models;
- the **mature catalog** *LLM Identifier for Creative Writing: Abliterated & Uncensored Models*
  (`..\llm-identifier-creative-writing-abliterated\abliterated_models.csv`): every model in it is marked uncensored,
  a model the roster lacks is added, and its Genres and Genre Category become the model's genre tags. A Hugging Face
  row not served through Inference Providers is a GGUF kept to fine-tune later: recorded as `fine_tune_base` and
  never called;
- the **open-weight catalog** *Open-Weight & Fine-Tuned Models*
  (`..\llm-identifier-creative-writing-open-weight\open_weight_models.csv`): folded in the same way without the
  uncensored mark: its routes, genre tags and missing IDs reach the prose lane; its Hugging Face GGUFs are fine-tune
  bases; a media row that matches no roster row is reported, not added;
- the **register** `..\registry.json` (verified against the providers on 2026-11-14): the context each provider
  actually serves (`served_context`: size every request to it), the register ID (W01 to W77, C01 to C10), the
  Genre Matrix subgenres each model serves, and a model's second route on OpenRouter.

Export the roster and the mature catalog from Notion as CSV and rebuild:

    python -m eos_app.registry "..\roster\LLM Identifier export.csv" --mature "..\llm-identifier-creative-writing-abliterated\abliterated_models.csv" --open "..\llm-identifier-creative-writing-open-weight\open_weight_models.csv" --register ..\registry.json

The build lists rows that look mistyped (an ID copied from another row, a model listed twice) and the models the
register verified that neither Notion source lists yet. Where a newer source names a mistyped roster row, the row
takes that name and the build says so; correct the roster to match.

The register's routing table, `..\routing.json` (which models write for each pen name in each Genre Matrix path, by
role), is read from the repository root when the app loads, like the library pools. It names pen names, so it is
never copied into the app (D10).

`eos_app/router.py` picks the model for each call (`config/routing.yaml`):
- **Experts:** each component's Primary, then its Comparable, then its Fallback (the database's Fallback Model, or the Primary's roster Fallback when that is empty). A cheaper comparable model goes first.
- **Routes:** a model listed in the roster under two providers has two routes. When a provider is down, the router tries the same model's other route before it moves to the next expert. To give a model a second route, add a roster row with the same Model Name and the other provider.
- **No ID, no call:** a model with no provider model ID is never chosen.
- **Lanes:** each lane's providers are listed in `routing.yaml` and enforced.
- **Prose:** writers in Prose Writing use the register's writers for the book's pen name and subgenre (lead
  writers, then strong adjacent fits, in the register's order), then every model tagged for the subgenre, with the
  component's own experts behind them as the safety net. Pass `pen_name=` and `genre=` (the minor subgenre, or the
  major where the path has none) to `writer_models()` or `choose_writer()`.
- **Mature tier (P10, D33):** mature text goes only to an uncensored model served by an inference provider or an
  aggregator: Featherless AI or OpenRouter. Local models and fine-tune bases are not in it. A prose writer uses the
  tier's models fitted to the book and never its general experts; any other text component with no mature expert
  hands the passage to the tier for the book's pen name and subgenre. A model's own row leads and its OpenRouter
  route follows, as a second route on an outage.
- **Fine-tune bases** (Hugging Face GGUFs) are never chosen on any lane.
- **Checkers:** the 21 evaluation components (each lists what it `judges` in components.yaml) never run on the
  model that wrote the text, whichever provider serves it; for mature text their experts refuse, their
  `mature_fallback` takes over. Two routes to one set of weights count as one model: Venice Uncensored on OpenRouter
  is `dphn/Dolphin-Mistral-24B-Venice-Edition`, so it never judges text that model wrote on Featherless AI.
- **Editing tools:** Proofreader and Edit Coach run on their own experts, not the genre fine-tunes; Self-Edit
  Reports is code.
- **Media:** image, video, speech, music and sound components use only models that make what they make (the
  roster's Modality), routed
  to OpenRouter, Hugging Face, ElevenLabs, Comfy Cloud or Featherless AI. Comparables and Fallbacks run on Comfy Cloud; mature media goes only to open models there.
- `same_model_report()` lists where a checker and something it judges share a Primary.

### What could run today

    python -m eos_app.readiness          # the summary and everything that needs attention
    python -m eos_app.readiness --all    # every component

It asks the router which models each component could actually call and sends nothing to any model. A component is **ready**, **degraded** (it would run, but on a later expert or with no second expert to cross-check) or **blocked** (nothing it could call). The report also counts what an outage of each provider would stop, and lists what is still open: no route for mature material, a Mature Fallback left open, writers nothing checks, and Jev's missing roster row. It sizes the mature tier: its models and routes per provider, the subgenres they cover, and the fine-tune bases recorded but never called.

## Dry run of the first slice (fixes plan D1)

The first stretch of the Flow Order, Story Pitch and the six components it needs, built end to end **without
sending anything**:

    python -m eos_app.dryrun --project "..\projects\dry-run" --library "..\library" ^
        --braindump braindump.md --brainstorm brainstorm.md --manuscript-type Novel ^
        --genre-path "Primary > Secondary > Major > Minor" --pen-name "<pen name>"

- **Agent definitions** (`config/agents/*.yaml`, one per agent, requirements §6.7) list each agent's inputs: the
  Author's material, the outputs of the steps it needs, the gate decisions before it, and library slices. Loading
  refuses an input its component may not have (its `needs` in components.yaml, its `read_by` in library_map.yaml).
- **The prompt builder** (`eos_app/prompts.py`) builds each prompt from those inputs only, from a versioned
  template in `prompts/`, labels every part for Show prompt, keeps it inside the agent's context budget (optional
  blocks are left out lowest priority first, and recorded), and refuses answer-key paths and anything shaped like a
  key. Library slices go through `prompt_view`, chosen for the book: only the pen name taken at the gate, only the
  content levels for the book's genre path.
- **Requests** (`eos_app/clients.py`): the exact request for each call, built for Concentrate AI, OpenRouter and
  Featherless AI (endpoints in `routing.yaml`, checked against each provider's documentation). The header names the
  .env variable that holds the key; the key itself is never read.
- **Cost**: `config/prices.yaml`, per million tokens, each line with its source and date. Featherless AI is a flat
  subscription. The estimate is a worst case: every step at its full answer budget.

It walks the slice in Flow Order, picks each component's models through the router (the Primary, and for the Full
tier a second expert that cross-checks), and stops at each of the three gates: manuscript type, pen name, adapted
premise. A dry run cannot take your decisions, so the genre path and pen name the later prompts read are stand-ins
you name on the command line, marked as such everywhere; earlier steps' outputs are placeholders.

It writes into the project folder, which lives outside the app and is never committed (it names your library, D10):
`runs/<date>/runs.jsonl` (one record per planned call, status "not sent"), `prompts/dry-run/NN-<agent>.md` (Show
prompt with the requests) and `dry-run.html` (a card per step with Proceed and My alternative, and the gate stops).

Today: 7 prompts, 10 planned calls on Concentrate AI, 3 gate stops, at most $0.44. One item before a live run:
Target Audience is on the Full tier with one expert (decision 5).

## Shared library

Your eight pools live once, beside your projects, in `Projects-Writing EOS\library\`:
- `characters\`: the Character Pool (455 cards)
- `pen-names\`: the Pen Names Pool (32 pen names across 606 subgenre rows)
- `narrative-genres\`: the Narrative Genres Pool (566 genres)
- `story-pitches\`: the Story Pitch Pool (37 writing topics)
- `content-levels\`: Content Levels (spice, violence and swearing for 529 subgenre paths)
- `conflict-structure-map\`: the Conflict and Structure Map (36 mappings, 21 plot structures)
- `arc-and-theme\`: Character Arc and Theme (your template; the app adds entries)
- `themes\`: Themes in Literature (eleven sheets of your workbook, from the vault folder *Theme in Literature*: genre fit, definitions, complementary themes, the three worldbuilding approaches and the Bible's world layout, structure fit, dialogue and voice, colours, timeline)
- `character-traits\`, `character-flaws\`, `animal-natures\`, `epithet-words\`, `clothing\`: your *Fictional Character Development* knowledge base (Character Traits and Personal Strengths, Character Flaws, Animal Traits, Character Building, Types of Clothing), read straight from the .xlsx and .docx files. These are **scaffolding**: brainstorming material with incomplete information, for ideas only, never canon (`is_scaffolding()`). `words()`, `synonyms()`, `animal_traits()`, `epithet_slots()` and `sections_about()` give the Character Development components what they need.

They stay Obsidian notes, so you can open `library\` as a vault. Your vault in `OneDrive\Documents\Obsidian Vault\Writing EOS` stays the master: edit there and re-import.

**Importing**
- `import_folder()` copies a vault folder in exactly as it is. Your vault is never changed.
- Archive folders, zip folders and Obsidian's settings are skipped.
- Re-importing copies only the notes that changed in your vault. The library remembers each note as it was last copied (`.import-baseline.json` in each pool folder), so a note you also edited in the library is left for you, never overwritten.
- A note gone from your vault, removed or renamed, is reported and never deleted. If you rename a card, delete its old copy from the library so the two don't share an id.
- `docs/LIBRARY_IMPORT_REPORT_2026-10-21.md` lists what came in and what needs your attention.

**Field names**
- The app uses your vault's own field names and Controlled Vocabulary.
- On a character card, the `**field:** value` lines count as fields; the frontmatter wins where both give one.
- `config/library_map.yaml` holds the aliases for other spellings and the words that place a role (Protagonist, Mentor, anti-hero) in an archetype position. If your notes use a word the map doesn't know, add one line there; no note needs editing.

**Rules the code enforces**
- **Pool first:** `may_create_character()` refuses to create a character until Character Pool Match has searched the pool and found no fit.
- **Only usable characters are offered:** `candidates_for_role()` offers *Ready to Pull* and *Reimagined* characters, and *Assigned to Project* ones only to the book they're assigned to. Incomplete cards and statuses outside your vocabulary are never offered. `unclassified()` lists characters whose role the map can't place.
- **Your approval to add:** `write_character()` adds a character only with your G5 approval, as *Ready to Pull*, in `characters\new\` for you to copy into the vault.
- **Pen names and bylines:** `pen_names_for()` finds the pen names with a row in a genre, and `byline_collisions()` flags character names that share a word with the byline.
- **Named influences stay with you:** `prompt_view()` never sends a card's private fields, and turns styles that name real authors, directors or works into their description alone.
- **Pitches and doctrine:** `pitches()` offers writing topics as story pitches; `doctrine()` sends the framework topics to the Story Bible instead.
- **Content levels:** `content_levels_for()` finds a subgenre's suggested ceiling and asks for the genre path when a subgenre sits under several. `check_scene_levels()` sends a scene at the mature level (4 by default, set in the map) to the mature tier and flags any level above the book's ceiling.
- **Structures:** `rank_structures()` shortlists every plot structure your map fits to the story, the core first; `table_disagreements()` lists where your map and the formula's structure table disagree. Neither is changed for you.
- **Arc entries:** `write_arc_entry()` writes one entry in your template's shape, only after you approve arc and outcome, in `arc-and-theme\new\<book>\`.
- **Characters are completed for the book:** a pool card is a launchpad. `profile_gaps()` lists what a developed character still lacks and which Character Development stage owes it; `may_promote()` keeps gate G5 shut until the profile is complete; `settled_open()` finds what you marked settled-open on a card, which is never filled. `skin_carried_over()` lists Skin fields still word for word as on the card; `may_promote(..., card=..., kept=...)` keeps G5 shut until they are regenerated for the book or you keep them.
- **Every relationship is cast:** `uncast_roles()` finds relationships naming no character in the pool (return channel R6: back to Cast Roles and Character Pool Match); `write_arc_entry()` refuses them as a backstop.
- **Places go to the world:** `settings()` lists the pool's setting cards for Worldbuilding and Locations; they are never offered as cast and don't count as roles to place.
- **Themes:** each theme is Canon or Motif (your list's Theme Type column). `book_theme()` accepts only a Canon theme as the book's; a lead character's arc entry (`lead=True`) must carry a Canon theme. `themes_for()` rates every theme for a book's genre path (good, situational, open, not an ideal fit; the most specific listing decides, and equal ones that disagree show as mixed). Each suggestion carries the theme's definition; `theme_pair()` gives its complementary theme, how they intersect and the partner's own fit; `theme_brief()` is what a model is told (definitions and pairings only). `write_arc_entry(..., themes=...)` accepts only a theme from your list. The list's shorthand (Contemporary, Nonfiction) is set out in the map.
- **Story Bible elements:** `world_brief()` gives Worldbuilding its starting directions under the approach you approve (Components, G.R.A.P.E.S. or M.E.R.P.S.); `theme_structure_fit()` shows how your themes suit each structure, beside the scores; `theme_aspects()` reads a theme's dialogue and voice, colours or timeline row.
- **Private:** the library never goes into the code package.

## Run the tests

You need Python 3.11 or newer.

```bash
cd eos-app
pip install -r requirements.txt
python -m pytest
```

The tests use no network and no model. If pytest crashes on start-up with an error about another package's plugin (for example `langsmith`), set `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and run it again. That error comes from other software installed on the computer, not from this engine.

## Story Bible

`config/story_bible.yaml` sets out the Bible's twelve elements: what each holds, which components fill it, which pools feed it, and which registers (characters, arc, secrets, naming, world rules and the rest) it contains. `eos_app/story_bible.py` loads it and `check_bible()` checks it against the components and the library map. The Story Bible Builder assembles the elements; Canon Check and its second opinion check them; you lock the Bible.
