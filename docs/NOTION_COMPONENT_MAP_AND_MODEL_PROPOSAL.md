# Notion narrative components · app coverage and proposed models

Source: Notion database **AI Agentic LLM** (49 rows with Registry Version v2, plus 24 older rows with no version), read 18 Oct 2026. Compared with `WRITING_EOS_REQUIREMENTS_AND_ARCHITECTURE.md` v0.5.

## Part 1 · Is each component in the app?

**Summary:** of the 49 v2 components, **35 are in the app**, **4 are there in a different shape**, **5 are only partly there**, **1 is missing**, and **4 are deferred on both sides**.

| Step | Notion component | In the app? | Where (requirements) |
|---|---|---|---|
| 1 | Braindump Intake (chatbot + uploads) | Yes | §4.2 step 1, Braindump Intake + Narrative Note-Taker. Notion and Drive imports are not specified (FR-EX-4 covers Markdown and DOCX) |
| 2 | Narrative Builder + Manuscript Type | **Partly** | FR-PRJ-2 stores manuscript type as a setting; there is no agent that builds it. Notion notes: MVP is fiction-only, which matches §1.2 |
| 3 | Pen Name ⇄ Genre ⇄ Literary Style (Triad) | Yes | Pen Name Selector (step 1), FR-PRJ-2, genre pack FR-PRJ-5 |
| 3.5 | Premise Adaptation | Yes | §4.2 step 1 |
| 3.6 | Role Extraction | Yes | §4.2 step 3, P3 |
| 4 | Writing Guide Population (Genre Templates) | Yes | Genre packs and Genre Analyst (§4.15, FR-GP) |
| 5 | Story Pitch (Pitch Profile) | Yes | Pitch Profile Builder (step 2) |
| 6 | Conflict Type (Conflict Fit Score) | Yes | Conflict Fit Rater + code (FR-DEV-1) |
| 6.5 | Character Pool Match | Yes | Character Development 01–02, Character Selector (P4) |
| 6.6 | Character Creation (agent team fallback) | Yes | Character Development 03–11, Creation Mode (FR-CD-2) |
| 6.61 | Character Name Generator | Yes | Character Development 06 |
| 7 | Character Seed | Yes | Character Seed Recorder (step 4) |
| 8 | Plot Pitch (Plot Blueprint) | **Partly** | The Plot Blueprint is step 4's output, but no agent is named as its writer (step 4 lists recorder, analyst, spec and audit agents) |
| 9 | Story Dossier | **Partly** | The idea exists (PROVISIONAL work before the Bible lock, P11, FR-SB-1) but there is no named Dossier workspace |
| 10 | Worldbuilding | Yes | Step 7, World and Naming |
| 11 | Synopsis Deep Dive | **Missing** | No synopsis step or agent in the app |
| 12 | Character Development | Yes | §4.3 (13 stages, contracts C0–C13) |
| 13 | Character Arc Architecting (GANT 2.0) | Yes | Step 5, Stage 2 |
| 14 | Cast & Structure Selection | Yes | Step 6, Stage 3 (Vacancy Mapper, Structure Fit) |
| 15 | Literary Style Calibration | **Partly** | The voice profile (FR-VC-2) is measured per pen name; per-project calibration is not specified |
| 16 | Character Name Critique | Yes | Character Development 07 and step 8 |
| 17 | Emotional Critique | Yes | Step 8 |
| 18 | Logic Critique | Yes | Step 8 |
| 18.5 | Originality & Trope Critique | **Partly** | Trope Audit runs at Stage 1 (step 4), but the QA gate (step 8) lists only Emotional, Logic and Name critiques |
| 19 | Story Bible Lock (Consolidation) | Yes | Step 8, Bible Assembler + Bible lock gate |
| 20 | Outline Generator | Yes | Step 9, Narrative Outliner |
| 21 | Outline Emotional & Logic Audit | Yes | Step 9 audits |
| 22 | Plot Sliders | Yes | Step 9, Slider Setter |
| 23 | Plot Selector | Yes | Chapter agent 2 |
| 24 | Character Selector (Chapter) | Yes | Chapter agent 3 |
| 25 | Worldbuilding Selector (Chapter) | Yes | Chapter agent 4 |
| 26 | Wordcount Estimator | Yes | Code (§6.5, word counts and slider maths) |
| 27 | Plot Scene Brief | Different shape | One agent, Chapter Scene Briefs (chapter agent 5), writes the scene plans |
| 28 | Character Scene Brief | Yes | Chapter agent 7 (X2) |
| 29 | Worldbuilding Scene Brief | Different shape | Folded into Chapter Scene Briefs (agent 5); no separate world brief |
| 30 | Chronology Check | Yes | Chapter agent 8 |
| 31 | Scene Brief Rewrite | Different shape | Not a separate agent: a contradiction sends the work back to the Brief Writer (agent 8's gate) |
| 32 | First Draft | Yes | Chapter agents 9 and 10 (mature scenes) |
| 33 | Chronology Check 2 | Yes | Chapter agent 11, Continuity and Knowledge Check |
| 34 | Style Check | Yes | Chapter agent 12, Style, Tone and Arc Check |
| 35 | Rewrite | Yes | Chapter agent 13 |
| 36 | Continuity Ledger Update | Different shape | Split between Character State Delta (16), Summarizer and Canon Update (17) and story time (FR-CH-9) |
| 37 | Prose Refinement (Seven Levels) | Yes | Chapter agent 14 |
| 38 | Edit Actions | Yes | Editor (FR-ED-1) |
| 39 | Chapter Assembly & Obsidian Export | Yes | FR-EX-2; the project folder opens in Obsidian (NFR-7) |
| 40–43 | Blurb, Audiobook Script, Storyboard and Trailer, Marketing | Deferred both sides | Notion: Deferred. App: out of scope for version 1 (§1.3, "Later" on the Blueprint screen) |

**In the app but with no Notion row** (so they have no model in Notion yet): Narrative Note-Taker; Collision Analyst, Antagonist Role Spec; Ghost and Lie Confirmer, Climax Outcome Matrix, Supporting Arcs, Oscillation Planner; Vacancy Mapper, Structure Fit Rater; Reference Audit, Secrets and Knowledge Builder, Rule Extractor, Canon Verifier + Challenger; Arc Beat Planner, Reveal Scheduler, Outline Audit Scorecard, Outline Rewrite; Brief Writer, Character State Examiner (X1), Summarizer; Entity Classifier, Workshop Chat, Character Interview, Chat Extractor, Brainstorm; Genre Analyst, Recipe Builder; Narrative Director. Most sit inside a Notion row (for example Stage 2's four agents inside row 13).

**The 24 older rows:** all but three are covered by a v2 row. **Synopsis Generator** matches the missing row 11. **Themes in Literature Selector** has no agent in the app; theme only enters as a factor in Conflict Fit (FR-DEV-1). **Narrative Research Intelligence Engine** was declined in decision D13 (Q7: no web research step in version 1).

## Part 2 · Proposed model for each component

**How these were chosen, in this order:**
1. A model already named in the v2 row (your current hypothesis), with Gemini 3.1 Pro read as Gemini 4 Argon.
2. Otherwise, the pair you gave the matching older row (Orchestrator: proprietary / open-weight).
3. Otherwise, the pair used for the same task type.

Old fallbacks (Qwen3-235B, Llama 3.3 70B, DeepSeek-V3) are replaced with current models from your roster, as the row notes ask ("retest against current versions"). Every pick is checked against the judge rules: a checker never comes from a family that wrote what it checks (P8), and Claude and Qwen are not judges for the opening chapter test. **All of these are starting assignments for the bake-off to test, not results.** Only the QA critiques have test evidence so far (Gemini 4).

Model IDs: Claude Fable 5.1 `anthropic/claude-fable-5.1` · GPT-6.1 Sol `openai/gpt-6.1-sol` · GPT-5.6 Sol `openai/gpt-5.6-sol` · Gemini 4 Argon `google/gemini-4-argon` · Qwen3.8 Max `qwen/qwen3.8-max-0902` · DeepSeek V4 Pro `deepseek/deepseek-v4-pro` · Kimi K3 `moonshotai/kimi-k3` · GLM 5.3 `z-ai/glm-5.3`.

| Step | Component | Task type | Primary | Fallback (open-weight) | Source |
|---|---|---|---|---|---|
| 1 | Braindump Intake | Synthesis | Claude Fable 5.1 | Qwen3.8 Max | Older row "Braindump Output Architecture" |
| 2 | Narrative Builder + Manuscript Type | Extraction | GPT-6.1 Sol | DeepSeek V4 Pro | Older rows "Narrative Builder", "Manuscript Type Selector" |
| 3 | Pen Name Triad | Ideation | Claude Fable 5.1 | Qwen3.8 Max | Older rows "Pen Name Selector", "Literary Style Selector" |
| 3.5 | Premise Adaptation | Synthesis | Claude Fable 5.1 | Qwen3.8 Max | Same team as the pen name it adapts to |
| 3.6 | Role Extraction | Extraction | GPT-6.1 Sol | DeepSeek V4 Pro | Extraction default |
| 4 | Writing Guide Population | Synthesis | GPT-6.1 Sol | DeepSeek V4 Pro | Older row "Literary Genre Selector" |
| 5 | Story Pitch | Ideation | GPT-6.1 Sol | DeepSeek V4 Pro | Older row "Story Pitch Generator" |
| 6 | Conflict Fit | Extraction | GPT-6.1 Sol | DeepSeek V4 Pro | Extraction default |
| 6.5 | Character Pool Match | Extraction | Claude Fable 5.1 | Qwen3.8 Max | Older row "Character Selector" |
| 6.6 | Character Creation | Ideation | Claude Fable 5.1 | Qwen3.8 Max | Older row "Fictional Character Refiner" |
| 6.61 | Character Name Generator | Ideation | Claude Fable 5.1 | Qwen3.8 Max | Character team; checked by Gemini (row 16) |
| 7 | Character Seed | Extraction | Claude Fable 5.1 | Qwen3.8 Max | Older row "Character Selector" |
| 8 | Plot Pitch (Plot Blueprint) | Ideation | GPT-6.1 Sol | DeepSeek V4 Pro | Older rows "Story Pitch Generator", "Act Structure Recommender" |
| 9 | Story Dossier | Synthesis | Gemini 4 Argon | Kimi K3 | Older row "Story Dossier Scope" |
| 10 | Worldbuilding | Ideation | Gemini 4 Argon | Kimi K3 | Older row "Worldbuilding Selector" |
| 11 | Synopsis Deep Dive | Synthesis | GPT-6.1 Sol | DeepSeek V4 Pro | Older row "Synopsis Generator" |
| 12 | Character Development | Ideation | Claude Fable 5.1 | Qwen3.8 Max | Older row "Fictional Character Refiner"; still to reconcile with the 13 team specs |
| 13 | GANT 2.0 arc | Synthesis | GPT-6.1 Sol | DeepSeek V4 Pro | Older row "Act Structure Recommender" |
| 14 | Cast & Structure | Extraction | GPT-6.1 Sol | DeepSeek V4 Pro | Older row "Act Structure Recommender" |
| 15 | Literary Style Calibration | Extraction | Claude Fable 5.1 | Qwen3.8 Max | Older row "Literary Style Selector" |
| 16–18.5 | Name, Emotional, Logic, Originality critiques | Verdict | **Gemini 4 Argon** (tested) | **Kimi K3** | v2 rows + protocol (Kimi K3 is the panel's first open-weight choice) |
| 19 | Story Bible Lock | Synthesis | Gemini 4 Argon | Kimi K3 | Older row "Story Bible Generator". Its Canon Verifier must then come from another family |
| 20 | Outline Generator | Synthesis | GPT-6.1 Sol | DeepSeek V4 Pro | Older row "Outline Generator" |
| 21 | Outline Audit | Verdict | **Gemini 4 Argon** (tested) | Kimi K3 | v2 row |
| 22 | Plot Sliders | Extraction | GPT-6.1 Sol | DeepSeek V4 Pro | Same team as the outline |
| 23 | Plot Selector | Extraction | GPT-5.6 Sol | DeepSeek V4 Pro | v2 primary; older row's fallback |
| 24 | Character Selector (Chapter) | Extraction | Claude Fable 5.1 | Qwen3.8 Max | v2 primary; older row's fallback |
| 25 | Worldbuilding Selector (Chapter) | Extraction | Gemini 4 Argon | Kimi K3 | v2 row |
| 26 | Wordcount Estimator | Code | — | — | No model |
| 27 | Plot Scene Brief | Synthesis | GPT-5.6 Sol | DeepSeek V4 Pro | v2 primary; current fallback |
| 28 | Character Scene Brief | Synthesis | Claude Fable 5.1 | Qwen3.8 Max | v2 row (Notion spec fallback) |
| 29 | Worldbuilding Scene Brief | Synthesis | Gemini 4 Argon | Kimi K3 | v2 primary; current fallback |
| 30 | Chronology Check | Verdict | **GLM 5.3** | DeepSeek V4 Pro | **Changed.** The three briefs it checks come from OpenAI, Anthropic and Google, so the judge must be another family; GLM is also the cheapest. The router skips DeepSeek if DeepSeek wrote a brief |
| 31 | Scene Brief Rewrite | Synthesis | Claude Fable 5.1 | Qwen3.8 Max | v2 primary; current fallback |
| 32 | First Draft | Prose | Claude Fable 5.1 | Qwen3.8 Max | v2 primary; current fallback. Mature tier: custom abliterated (Hugging Face) |
| 33 | Chronology Check 2 | Verdict | Gemini 4 Argon | Kimi K3 | v2 primary; current fallback. Mature drafts still unresolved (see below) |
| 34 | Style Check | Verdict | **GPT-6.1 Sol** | **GLM 5.3** | **Changed** to fix the judge conflict (Claude can't check Claude's draft), and to keep it a different family from Chronology Check 2 so the two checks don't share a blind spot |
| 35 | Rewrite | Prose | Claude Fable 5.1 | Qwen3.8 Max | v2 primary; current fallback. Mature: custom abliterated |
| 36 | Continuity Ledger Update | Extraction | GPT-6.1 Sol | DeepSeek V4 Pro | Extraction default |
| 37 | Prose Refinement | Prose | Claude Fable 5.1 | Qwen3.8 Max | Prose team. Mature: custom abliterated |
| 38 | Edit Actions | Prose | Claude Fable 5.1 | Qwen3.8 Max | Prose team. Mature: custom abliterated |
| 39 | Chapter Assembly & Export | Code | — | — | No model |
| 40–43 | Deferred steps | — | — | — | Not assigned until they are in scope |

**Three things to weigh before approving:**
1. **Cost.** Claude Fable 5.1 is the most expensive model here ($10 in and $50 out per million tokens) and is Primary on 16 rows, including every prose step. Its bake-off scores will decide whether that's justified.
2. **Mature drafts** (rows 32–38) are still unresolved. Both Hugging Face models share one base model, so a checker reading a mature draft would come from the writer's family.
3. **The missing and partial components** (rows 2, 8, 9, 11, 15, 18.5) get models here, but the app's requirements don't yet have the agents they need.

## Part 3 · Done on 18 Oct 2026

**In the app (requirements v0.6, decision D14):** all six gaps are closed:
- Synopsis Writer (row 11, FR-DEV-10)
- Narrative Builder (row 2, FR-DEV-11)
- Plot Blueprint Writer (row 8, FR-DEV-13)
- Story Dossier and Dossier Keeper (row 9, FR-DEV-9)
- Style Calibrator and the project style card (row 15, FR-DEV-12)
- Originality & Trope Critique in the QA gate (row 18.5, FR-DEV-13)

The Story Blueprint screen on the canvas shows them, with a Story Dossier panel.

**In Notion:**
- **Models written:** the 43 rows above carry their Primary, Fallback and OpenRouter IDs.
- **Linked rows:** the six rows now name the app agent that covers them.
- **New rows:** 32 rows were added for app agents that had none. Each has a step number, task type, starting models (judge-family rules checked), "Untested" status and a note.

| Step | New row | Primary / Fallback |
|---|---|---|
| 0.5 | Narrative Director (advisory) | GPT-6.1 Sol / DeepSeek V4 Pro |
| 1.1 | Narrative Note-Taker | Claude Fable 5.1 / Qwen3.8 Max |
| 4.1 | Genre Analyst | GPT-6.1 Sol / DeepSeek V4 Pro |
| 8.1, 8.2 | Collision Analyst, Antagonist Role Spec | GPT-6.1 Sol / DeepSeek V4 Pro |
| 10.1 | World Naming System Builder | Claude Fable 5.1 / Qwen3.8 Max |
| 10.2 | Element Extractor | GPT-6.1 Sol / DeepSeek V4 Pro |
| 10.3, 10.4 | Location Writer, World Rules Drafter | Gemini 4 Argon / Kimi K3 |
| 10.5 | World Consistency Check | GPT-6.1 Sol / GLM 5.3 |
| 13.1 | Ghost and Lie Confirmer | Gemini 4 Argon / Kimi K3 |
| 13.2–13.4 | Climax Outcome Matrix, Supporting Arcs, Oscillation Planner | GPT-6.1 Sol / DeepSeek V4 Pro |
| 18.6 | Reference Audit | GLM 5.3 / DeepSeek V4 Pro |
| 19.1, 19.2 | Secrets and Knowledge Builder, Rule Extractor | GPT-6.1 Sol / DeepSeek V4 Pro |
| 19.3 | Canon Verifier | GPT-6.1 Sol / GLM 5.3 |
| 19.4 | Canon Challenger | DeepSeek V4 Pro / GLM 5.3 |
| 20.1, 20.2, 21.2 | Arc Beat Planner, Reveal Scheduler, Outline Rewrite | GPT-6.1 Sol / DeepSeek V4 Pro |
| 21.1 | Outline Audit Scorecard | Gemini 4 Argon / Kimi K3 |
| 22.5 | Brief Writer (Chapter) | GPT-5.6 Sol / DeepSeek V4 Pro |
| 22.6 | Recipe Builder | GPT-5.6 Luna / DeepSeek V4 Pro |
| 27.5 | Character State Examiner (X1) | Claude Fable 5.1 / Qwen3.8 Max |
| 36.5 | Summarizer and Canon Update | GPT-6.1 Sol / DeepSeek V4 Pro |
| 38.1, 38.4 | Entity Classifier, Chat Extractor | GPT-5.6 Luna / DeepSeek V4 Pro |
| 38.2 | Workshop Chat | Gemini 4 Argon / Kimi K3 |
| 38.3 | Character Interview | Claude Fable 5.1 / Qwen3.8 Max (mature: custom abliterated) |
| 38.5 | Brainstorm | GPT-6.1 Sol / DeepSeek V4 Pro |

**Not added as rows:** the 13 Character Development stage agents. Row 12 notes that their team specs live elsewhere in Notion, so they still need reconciling. The 32 rows plus the 49 earlier v2 rows make 81 in total; 75 have models, and the other six are code or deferred.
