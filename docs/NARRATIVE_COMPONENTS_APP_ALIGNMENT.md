# Narrative Components ↔ Writing EOS app · alignment check

21 October 2026. Compares the restructured Notion database *Narrative Components* (106 rows, corrected Flow Order) with the app as specified (requirements v0.9), drawn (canvas v39) and built (`eos-app`, bake-off harness).

## 1. Verdict

**The order of work now matches the app's workflow.** Every phase of the database has a home in the app, and the per-chapter loop is the same as the app's chapter pipeline step for step.

The gaps are elsewhere, in four areas:
1. **Names:** eight components carry different names in the database and the app.
2. **Missing pieces both ways:** the app's code steps are not rows in the database, and the database has two columns the app does not define (*Swarm Tier*, *Jev Model*).
3. **Model routing:** the app knows only two providers (OpenRouter and Hugging Face endpoints); you will use four. And the database has no column for the mature tier, which the app's router needs.
4. **Out of date:** two canvas screens still show the old order, and the finishing and sales phases have no screens.

## 2. The order, phase by phase

| Database phase | App section | Canvas screen | Built |
|---|---|---|---|
| A · Intake | Develop step 1 (§4.2), FR-FN-2, FR-FN-3 | Story Blueprint | — |
| B · Stage 0 | Develop step 2 | Story Blueprint | Formula engine (`blueprint.py`) |
| C · Naming | Develop step 3, first part (D17) | Story Blueprint · **still shows naming at step 7** | — |
| D · Characters | Develop step 3, Character Development (§4.3) | Story Blueprint, Story Bible | — |
| E · Stage 1 | Develop step 4 | Story Blueprint | Formula engine (Stage 1 checks, antagonist rule) |
| F · Stage 2 | Develop step 5 | Story Blueprint | Formula engine (Outcome Matrix, Oscillation Rule) |
| G · Stage 3 | Develop step 6 | Story Blueprint | Formula engine (Structure Fit, Vacancy Rule) |
| H · World | Develop step 7, FR-FN-4 | Story Blueprint, Story Bible | — |
| I · QA and Bible | Develop step 8, FR-FN-1 | Story Blueprint, Story Bible | — |
| J · Outline | Develop step 9 | Story board | — |
| K · Chapters | Chapter pipeline (§4.5) | Chapters, Generate, Recipes | Harness tests 6 of these steps |
| L · Editor tools | Editor (§4.7, §4.13, FR-HU) | Editor | Humanize (`humanize.py`) |
| M · Finishing | §4.18, FR-EX-2 | Export (assembly only) · **no screens for the rest** | — |
| N · Sales | §4.18 | **no screens** | — |

The chapter loop matches §4.5 in order: Brief Writer → three selectors → plot and world scene briefs → Character State Examiner → Character Scene Brief → Chronology Check (with Scene Brief Rewrite on a fail) → First Draft → the two checks → Rewrite on a fail → Prose Refinement → your edits and the chapter lock → the canon updates.

## 3. Same component, different name

The engine needs one name per component. These eight differ:

| Database | App (requirements) |
|---|---|
| Story Pitch (Pitch Profile Builder) | Pitch Profile Builder |
| Pen Name, Genre and Literary Style (Triad) | Pen Name Selector |
| Chronology Check 2 | Continuity and Knowledge Check (§4.5 #11) |
| Style Check | Style, Tone and Arc Check (§4.5 #12) |
| Continuity Ledger Update | Character State Delta (§4.5 #16) |
| Plot Sliders / Slider Setter | Slider Setter |
| Outline Generator (Narrative Outliner) | Narrative Outliner |
| Cast & Structure (Structure Fit Rater + Vacancy Mapper) | two agents: Vacancy Mapper and Structure Fit Rater |

The **Step** number is the safest key between the two. Each agent's definition file in the app should carry the database Step.

## 4. In the app, not in the database

**Code steps.** The database already holds three code rows (Chapter Assembly, Wordcount Estimator, Retail Formatting) to map the complete pipeline. These app code steps are missing:
- Conflict Fit Calculator and Runner-up Filing (Stage 0)
- Blueprint Checks (Stage 1)
- Guardrail Check (Stage 2)
- Structure Fit Calculator and Kishōtenketsu Flag (Stage 3)
- Naming Checks (naming and world)
- Reveal Order Check (outline)
- Auto-fail checks and craft measures (every draft, FR-CH-2, FR-VC-1)
- Pool Write (Character Development stage 12), and stage 00/13 (Fictional Characters Development: you plus code)

**Two parts of the chapter pipeline:**
- **Mature tier scenes** (§4.5 #10): a routing rule rather than a component. But the database has no column for which model writes mature scenes.
- **The challenger:** the Continuity and Knowledge Check has a second checker from another model family (FR-CH-3). The database shows one model.

## 5. In the database, not defined in the app

| Column | What the app needs to know |
|---|---|
| **Swarm Tier** (Full · Light · None) | Not defined anywhere in the requirements. Does it mean several models working on a step versus one, or a depth of checking? |
| **Jev Model** (jev-1.14.0; "decision support only" on 65 rows) | Not defined in the requirements, and not a model on OpenRouter (the closest listing is a router, *TypeSafe: Jev Router*). If Jev chooses models or decides workflow, that conflicts with the rule that **control flow is code** (§6.6, D9). If it only advises, the app can treat it like the Narrative Director: it pitches, and never decides. |
| **Category** (Building Blocks · Prose Writing · Evaluation · Sales & Marketing) | Fine as a label. The app runs by Phase and Flow Order, not by Category. |

## 6. Model routing

**Providers.** The app's spec and the harness know two providers:
- OpenRouter (`OpenRouterClient` in the harness)
- your Hugging Face endpoints (configured, but not yet called by any code)

You will route through four: **Concentrate AI** (primary, frontier models), **OpenRouter** (some frontier models, open-weight fallbacks), **Featherless AI** (inference provider) and **Hugging Face** (some open-weight models).

These parts of the app change with that:
- **Registry (FR-ML-1):** every model gets a provider field and that provider's own model ID. The same model can have different IDs on different providers.
- **Privacy and security (NFR-1, §6.9):** the outbound allowlist adds Concentrate AI and Featherless AI.
- **Keys:** one key per provider in `.env`, never printed or logged.
- **Cost logging (NFR-3):** today it reads OpenRouter's cost lookup. Each provider needs its own way to report cost, or registry prices as a fallback.
- **Router (§6.4):** the Fallback can be on another provider, so a provider outage triggers the Fallback the same way a refusal does.
- **Harness:** a client per provider, so bake-off rounds can test models where they will actually run.

**What the router needs per component** (§6.4, §6.7) compared with the database:

| Router needs | Database has |
|---|---|
| Primary model and its provider | Frontier Model (no provider) |
| Fallback model and its provider | Comparable Open-Weight (no provider); 23 rows say "None genuinely comparable" |
| Mature-tier model (`mature_ok`) for mature scenes | — |
| Task type | Task Type ✓ |
| For checkers: which components' work it judges, so the router can block a same-family judge | — (the dependency list behind the Flow Order covers this; it should travel with the roster) |

## 7. Three Notion places hold model information

1. **AI Agentic LLM** registry: 81 v2 rows with Primary, Fallback and OpenRouter IDs. The requirements name it the source of truth (FR-ML-1).
2. **Model Assignment Sheet**: 90 rows, made for your picks.
3. **Narrative Components**: 106 rows with Frontier, Open-Weight and Jev columns.

They already disagree. For example, Claude Fable's fallback is Qwen3.8 Max in the registry and Kimi K3 in Narrative Components.

**Recommendation:**
- *Narrative Components* is the source of truth for **what runs and in what order**.
- Your coming **roster** is the source of truth for **which model and which provider**.
- The two are joined by Step.
- Once the roster arrives, the other two retire.

## 8. Out of date or missing on the app side

- **Story Blueprint screen:** still shows naming at step 7 and characters without it.
- **Ecosystem screen:** says "9 steps · 55 agents" and "OpenRouter for general models, Hugging Face endpoints".
- **Model Lab screen:** OpenRouter only.
- **Finishing and Sales (phases M, N):** no screens, apart from Export for assembly.
- **Formula engine:** its stage gates don't yet require the naming system before characters (D17).
- **Order check (FR-FLOW-6):** not built. A working prototype of the dependency check exists from today's audit.

## 9. Decisions for you

1. **Swarm Tier:** what does it mean, so the app can act on it?
2. **Jev Model:** what does Jev do? Advisory only (fits the app as it stands), or does it choose models or steps (needs a design decision)?
3. **Code steps:** add them to the database as rows (Runs: "Code"), so it maps the whole pipeline? Recommended.
4. **Source of truth:** adopt the split in §7?
5. **Providers:** record the four-provider routing as a decision when the roster arrives, and update the registry, router, security list, cost logging and harness to match? Recommended.
