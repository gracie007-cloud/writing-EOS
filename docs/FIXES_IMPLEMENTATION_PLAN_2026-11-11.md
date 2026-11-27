# Writing EOS · Fixes implementation plan

| | |
|---|---|
| **Date** | 2026-11-11 |
| **Basis** | An audit of the project as it stands today: every check below was run against the real files, not recalled |
| **Scope** | `eos-app/` (engine, config, tests), the model roster export, the bake-off harness, the requirements document, the design canvas, the package |
| **Status** | Stages 0 and 1 carried out on 2026-11-12; B3 closed and the canvas copy brought up to date on 2026-11-25 (section 0). The rest waits on decisions 4, 5 and 6 in section 4 and on your roster pass. |

---

## 0. Status on 2026-11-25

| Finding | Status |
|---|---|
| **B3** mature books | **Done** (requirements v0.30, D33), by another route than decision 2 proposed. Your rule (2026-11-25): the mature tier is the uncensored models an inference provider or an aggregator serves, Featherless AI or OpenRouter. It is built from the roster, the Notion catalog *Abliterated & Uncensored Models* and the 2026-11-14 register, which supply the genre tags the roster never had. Prose writers are chosen by the book's pen name and subgenre; any other text component with no mature expert hands the passage to the tier. **All 17 model-routed components of the chapter loop now have a mature route.** The tier holds 62 models on 64 routes. Hugging Face GGUFs are fine-tune bases and are never called. |
| **C2** canvas | **Repository copy brought up to date.** The 12 files that had changed on the live canvas since 22 October are in `canvas-source/eos-design/project/`, each matching the live file's SHA-256. `canvas-source/eos-build/src/` is still the October input: do not run `build.py` until it is brought up to date from the boards. |
| **D1** first real run | **Dry run done.** `python -m eos_app.dryrun` builds the seven prompts of the slice from each agent's allowed inputs (one definition per agent in `config/agents/`, refused if it asks for more), picks every model through the router, stops at all three gates, and prices the run, sending nothing. Endpoints for Concentrate AI, OpenRouter and Featherless AI were checked against each provider's documentation; the five models' IDs match Concentrate's catalog. Result: 7 prompts, 11 planned calls (Target Audience now has its cross-check), 3 gate stops, about $0.44. Before the live run: Target Audience (decision 5), and decision 6, the spending cap. It ran here on the test vault; run it on your library from your computer. |
| **B1, B2** IDs and second routes | **Partly closed by the Proprietary & Open/Near Frontier Models catalog** (exported to `llm-identifier-creative-writing-proprietary/`). It adds eight Concentrate AI routes (Claude Fable 5 and 5.2; Gemini 4 Carbon, Hydrogen and Neon; Kimi K3.1 Pro and Pro Highspeed; Qwen3.8 Omni Flash beside its OpenRouter route) and fills Fish Audio S2 Pro's ID. Visual Consistency Check and Narration Check no longer stop when OpenRouter is down. Its 14 media rows (Comfy Cloud, and Gemini 3.1 Flash TTS Preview) use newer names than the roster's ID-less rows (e.g. FLUX.2 Pro vs FLUX.2, Seedance 2.5 vs 2.0), so they are reported, not matched. **Yours:** say which roster row each one replaces. |
| **C3** the 14 November register | **Superseded (2026-11-25).** The Author found `registry.json`, `routing.json`, `REGISTER.md` and `VERIFICATION.md` incorrect. The registry is now built only from the Notion roster and the three catalogs; prose writers are chosen by the catalogs' genre tags, not by pen name; W69 lives only in *Base Models for Fine-Tuning*. The four files were deleted on 2026-11-27 (the Author). |
| **B10** look-alike names | One more found and handled: a roster row named for `Qwen3-VL-12B…NEO-MAX-GGUF` carries the ID of `Qwen3-VL-32B-Gemini-Heretic` (register W41). **Corrected in Notion on 2026-11-25**, with the Llama-3.2-8X3B Horror and Hathor_Tahsin v0.9 rows, which held another model's ID; the build now reports no mismatched names. The duplicate Qwen3.5-9B-Deckard-Claude-DIMOE row on Featherless was moved to Notion's Trash (the Author, 2026-11-25). |
| **C1** roster copy | **Refreshed from live Notion (2026-11-25).** The repository's roster export was a 12 November copy (293 rows); it now matches the live *LLM Identifier - Master List* (418 rows). Sonar Deep Research is not uncensored there; ElevenLabs is no longer in the roster. Media models come from the Proprietary catalog. In *Narrative Components* the 11 media components now name the current models (Fish Audio S2 Pro leads narration; Stable Audio 2.5 leads sound effects; MiMo V2.6 Flash replaces MiMo-V2-Omni). |

Today: 287 tests pass. Readiness: 117 ready, 0 degraded, 0 blocked, 6 code only. Every component has a route for
mature material (90 had none before D33). Mature tier: 62 models on 64 routes, fitted to 212 subgenres; 40 fine-tune bases. Media is called on Comfy Cloud first, then Concentrate AI,
then OpenRouter (the Author, 2026-11-25), so an outage of Comfy Cloud would stop 6 components (the four image
components, Sound Effects, Trailer Video).

**Still yours:** the 18 model IDs (B1), second-provider rows (B2), the Jev row (B8), the roster rows (B10), and decisions
4 and 6. The Kimi K3.1 and Nemotron pairings were corrected in Notion
(2026-11-25): every pairing now names a model. **New, yours:** the push gate (D10) will flag the uploaded register and catalog files on a machine where
your library is present; whether to allow those paths is your call.

## Status on 2026-11-12

The corrections that did not need a decision from you are done, tested and published to
https://github.com/gracie007-cloud/writing-EOS. 260 tests pass (228 before).

| Finding | Status |
|---|---|
| **A1** version history | **Done.** The project is a git repository on GitHub, private since 2026-11-12, and now includes the bake-off harness, the worked examples and the canvas source. |
| **A2** lost build scripts | **Done, differently.** The old generator could not be recovered whole: the transcript held only its 21 October version. It is replaced by `python -m eos_app.sync`, which builds `components.yaml` from a Notion export joined with the new tracked file `config/component_inputs.yaml`. A test proves it rebuilds today's file byte for byte. |
| **A3** package | **Replaced.** The GitHub repository is now the downloadable copy. The old folder and zip are left untouched on disk and are not published. |
| **B1** models with no ID | **Code done.** The router never chooses one. **Yours:** the 18 IDs. |
| **B2** one provider | **Code done.** A second roster row with the same Model Name is a second route. **Yours:** the rows. |
| **B3** mature books | **Waits on decision 2** and a fresh roster export with your Genre column. |
| **B4** prose safety net | **Done.** |
| **B5** gates | **Done.** The queue stops at every gate; chapters keep their own progress. |
| **B6** slot names | **Done.** `primary`, `comparable`, `fallback`. |
| **B7** Target Audience | **Closed (2026-11-25)** by the catalogs' pairings: each model now carries its Comparable and Fallback from the three Notion catalogs, and GLM 5.3 Flash's Fallback, MiMo V2.6 Flash, gives Target Audience its second expert from another family. Decision 5 is no longer needed. |
| **B8** Jev | **Reported.** **Yours:** the roster row. |
| **B9** lane lists, media kinds | **Done.** |
| **B10** look-alike names | **Code done.** **Yours:** the six roster rows. |
| **B11** unchecked writers | **Reported.** **Waits on decision 4.** |
| **C1** requirements | **Done** in v0.28: one statement of each routing rule; §6.4 rewritten; Appendix A generated from the app's own component list. **Decision 3 answered (retire):** the quality tiers were removed in v0.29 (D32). |
| **C2** canvas | **Done for routing and for what was approved but never drawn.** *Blueprint:* experts, routes, lanes, gates, hosting, the mature rules and the build status. *Model Lab:* how a step gets its experts, the roster's real models, judging by model. *Library:* a Reference lists tab for the five lists under development. *Finish and publish:* interior art, cover art, marketing visuals, narration, music, sound, trailer video and assembly. *Home, Story Blueprint, Chapters, Recipes, Autonomy:* every "model family" phrase replaced. **Not drawn yet:** the editing suite as its own panel in the Editor, and Visual References and Map Maker in the World step. The usability pass on each board is still to do. The quality tiers were taken off the canvas after decision 3. |
| **D1** first real run | Not started. **Waits on decision 6.** |

**Run `python -m eos_app.readiness` from `eos-app/` at any time** to see the current state. Today: 117 ready,
0 degraded, 0 blocked, 6 code only. An outage of Concentrate AI would stop 106 components, 17 of them inside every
chapter.

**What changed in the numbers.** The audit counted components whose experts all sit on one provider (111). The
readiness report counts what could actually be *called*, which is stricter and more useful, so some figures below
differ slightly from its output.

**Three things found while doing the work.**
1. **The repository was public at first**, so your own material was kept out of the first three commits. You made
   it private on 2026-11-12, and the harness with its test pack, the story-pitch experiment, the import report,
   the screenshot and the canvas source were added then. Keys, the real answer key and the library pools are
   still never stored. Two lines in the documents that named a ship and two pen names were made generic, as
   decision D10 already requires. `tools/check_public.py` runs before every push: it refuses keys, and it keeps
   `eos-app/` and the requirements free of names from your library or from your list in `.private-words.txt`.
2. **Notion's query index is stale.** A direct query of *Narrative Components* returned duplicate Flow Order numbers
   and models you replaced on 22 October. I did not use it. The sync tool takes a CSV export, which is always live.
3. **The canvas source on disk is three weeks old.** It is stored in `canvas-source/` as a record; the live canvas
   is the source.

---

## 1. Where the app really stands

Three sentences before any fix:

1. **The parts that exist are sound in isolation.** 228 tests pass. All 13 library pools load from your real library with no problems (the 19 notes on Character Flaws are scaffolding gaps, as agreed). The Flow Order has no component running before an input it needs.
2. **The app does not run yet.** There is no code that sends a prompt to a model, saves the result, or shows a screen. What exists is the rule-keeping machinery (order of work, router, registry, formulas, Humanize, library, Story Bible layout) and a design canvas. No component has ever gone through the router to a model.
3. **The safety net under the work is missing.** There is no version history anywhere, and the scripts that build two of the app's own files have been lost.

So the fixes fall into four groups, in the order they should be done:

| Group | What it is | Why this order |
|---|---|---|
| **A · Safety net** | Version history; rebuild the lost build scripts | Until this is done, any other fix can be lost the same way |
| **B · Defects** | Things the router, registry and order-of-work get wrong today | Cheap to fix now, expensive once real calls depend on them |
| **C · Drift** | The requirements and the canvas still state rules you overturned | A wrong document is how a wrong rule gets rebuilt |
| **D · The missing spine** | One real end-to-end run | The next class of defects only shows up when a call goes out |

---

## 2. Findings and fixes

Each finding says what is wrong, how I know, the fix, and what "done" looks like. **You** marks what only you can do or decide.

### Group A · Safety net

#### A1 · There is no version history
- **Evidence.** `Projects-Writing EOS` and `eos-app` are not git repositories. The harness folder had `git init` run once and has zero commits. Decision D2 says projects live in git.
- **Risk.** One bad edit, a OneDrive-style rollback or a deleted folder, and there is nothing to return to.
- **Fix.** One repository at the project root. Kept out of it: `.env`, `library/` (your real characters; never packaged), any `*ANSWER_KEY*` file (ignored by pattern, never opened), `Writing-EOS-App/`, the zip, harness `runs/`, caches. The harness's empty inner repository is folded into the one repository.
- **Done when.** A first commit holds today's state, and `git status` is clean after the test run.
- **You.** Say "commit" (I never commit without being asked), and confirm the harness's empty inner repository can be removed.

#### A2 · The scripts that build the app's own files are gone
- **Evidence.** `config/components.yaml` begins "Regenerate this file when the database changes". The script that regenerates it (`make_components.py`), the dependency checker (`nc_depcheck.py`), the Notion read-back files and the packager with its proper-noun gate (`package_app.py`) all lived in a temporary session folder. That folder has been emptied. I searched your user folder and found none of them.
- **Risk.** The Narrative Components database is edited live. Today the app cannot follow it (D18: the database leads), and the package cannot be rebuilt with its safety gate.
- **Fix.**
  1. Recover the originals from this session's saved transcript, where they were recorded as written.
  2. Move them into the repository as real tools: `tools/sync_components.py`, `tools/package_app.py`.
  3. Move component inputs into a tracked file, `config/component_inputs.yaml`. (Inputs exist nowhere in Notion; see C3.)
  4. Prove the recovery: regenerating from the recovered inputs must reproduce today's `components.yaml` exactly before the tool is trusted.
- **Done when.** `python tools/sync_components.py` rebuilds `components.yaml` byte for byte, and the rule "nothing the app depends on lives in a temporary folder" is written into the README.
- **Note.** A fresh read of the database is part of this step. It has had three weeks to change; I have not checked what moved.

#### A3 · The downloadable package is out of date
- **Evidence.** `Writing-EOS-App.zip` is from 22 October. It is already behind the app: `library_map.yaml` and `test_library.py` (changed when the scaffolding pools got their readers), the test vault's folder layout, and the requirements document all differ.
- **Fix.** Rebuild with the recovered packager after A2 and Group B.
- **Done when.** Every file in the package matches the app, and the gate passes.

---

### Group B · Defects in what is built

All of these were confirmed by running the router across all 123 components.

#### B1 · The router can choose a model that cannot be called
- **Evidence.** 18 roster models have no provider model ID. They fill 24 expert slots, all in media. **Six media components have no callable model at all:** Visual References, Map Maker, Interior Art, Marketing Visuals, Sound Effects, Trailer Video. The router returns them anyway.
- **Fix (mine).** The router skips a model with no ID and says why. A new readiness report gives each component one of three states: *ready*, *degraded* (running on a later expert), *blocked* (nothing callable), with the reason.
- **Fix (you).** Fill the 18 IDs in the roster: FLUX.2, Qwen-Image, Z-Image Turbo, Ideogram, Seedance 2.0, Wan 2.2, LTX-2, MiniMax Music 3, ACE-Step, Stable Audio Open, Stability Text To Audio (Comfy Cloud); Nano Banana Pro, Gemini 3.1 Flash TTS, Fish Audio S2 Pro (OpenRouter); ElevenLabs Sound Effects, ElevenLabs Scribe (ElevenLabs); Chatterbox (Featherless AI); Wan 3.0 (Hugging Face).
- **Done when.** The readiness report shows no *blocked* media component.

#### B2 · One provider going down stops almost everything
- **Evidence.** For 111 of the 117 model-routed components, every expert is on a single provider; for 105 of them that provider is Concentrate AI. D22 promises a Fallback on a different provider.
- **Cause.** The roster lists each model under one provider, and the registry keeps one route per model. Only 21 components have a third expert at all.
- **Fix (mine).** A model may have more than one route. Roster rows for the same model on different providers are grouped as one model with an ordered list of routes. On an outage the router tries the model's next route before moving to the next expert. Run records name the route used.
- **Fix (you).** Add a second-provider row for the workhorse models. Six were found on OpenRouter's model list on 18 October (Claude Fable 5.1, GPT-6.1 Sol, Gemini 4 Argon, Kimi K3, DeepSeek V4 Pro, Qwen 3.8 Max); GLM 5.3, GLM 5.3 Flash and MiMo 2.6 Pro need checking.
- **Done when.** The readiness report shows how many components survive the loss of each provider, and Concentrate AI going down leaves none of the per-chapter components stopped.

#### B3 · A mature book cannot be planned or written
- **Evidence.** For mature material, 87 of the 96 writing components have no model they are allowed to use. Only the 9 media components pass.
- **Two separate causes.**
  1. *Prose.* Mature prose needs a genre fine-tune that is Uncensored and on Featherless AI. The registry holds **zero** models with a genre: the roster export the app was built from has no Genre column.
  2. *Everything else.* Building Blocks and Sales & Marketing components have no mature route of any kind. The Mature Fallback column exists only for the checkers. Yet a mature scene must still be planned, briefed and summarised by components that read it.
- **Fix (mine).** Re-export the roster so the Genre tags arrive; then build whichever rule you choose below.
- **You (decision 2).** Recommended: extend the **Mature Fallback** column to writing components that handle scene content, and let it also be the interim for mature prose when no genre fine-tune is tagged yet. The roster already has 37 Uncensored models on Featherless AI to choose from. Components that never see scene text need none. The alternative is to leave mature books blocked until fine-tunes exist.
- **Done when.** For a mature scene, every component in the chapter loop has a model it may use, or is named as deliberately excluded.

#### B4 · A tagged fine-tune removes the prose safety net
- **Evidence.** In the router, once any fine-tune is tagged for the book's genre, the component's own experts are dropped from the line. If that fine-tune is unreachable (the Unsloth machine is off), First Draft, Rewrite and Polish stop.
- **Fix.** For non-mature prose: fine-tunes first, then the component's own experts. Mature prose keeps its strict rule.
- **Done when.** A test takes the fine-tune down and the component still writes.

#### B5 · Work is offered past a gate you have not approved
- **Evidence.** The order-of-work code checks inputs only. Walking the queue runs all 96 queued components with no approval given, although 20 Author gates are defined.
- **Fix.** `next_to_run` takes the set of approved gates; anything after an unapproved gate waits. Progress is also tracked per chapter (today "done" is one flag per book, so chapter 2 cannot be told from chapter 1).
- **Done when.** A test shows the queue stopping at each of the 20 gates until it is approved.

#### B6 · The slot names say the opposite of what they hold
- **Evidence.** In `components.yaml` the slots are still called `frontier` and `open_weight`. After the cheaper-first changes, 25 slots hold the other kind (for example Conflict Scoring: MiMo 2.6 Pro in `frontier`, GPT-6.1 Sol in `open_weight`). A one-off `primary: open_weight` switch exists for a single component.
- **Fix.** Rename the slots to what they are: `primary`, `comparable`, `fallback`. Remove the one-off switch. The Notion column names stay as they are; the sync tool maps them.
- **Done when.** No file in the app uses the old slot names.

#### B7 · Target Audience is asked for a cross-check it cannot have
- **Evidence.** Its Swarm Tier is Full (two models), and it has one expert (GLM 5.3 Flash).
- **Fix (mine).** Loading the components refuses a Full tier with fewer than two different experts.
- **You (decision 5).** Give it a Comparable, or set its tier to Light.

#### B8 · Jev cannot be routed
- **Evidence.** `components.yaml` names `typesafe/jev-1.14`; the roster has no such row.
- **You.** Add the roster row (OpenRouter).

#### B9 · Two guards are written down but not enforced
- **Evidence.** `routing.yaml` lists which providers each lane may use. The router loads the general list and never checks it; it does not read the media list at all. Separately, a media component only checks that a model *has* a modality, not that it is the right one: a Music step would accept an Image model. There are no violations today.
- **Fix.** Enforce the lane lists; give each media component its modality and check it.
- **Done when.** A test with a wrong-lane provider and a wrong-modality model is refused.

#### B10 · Roster rows that look mistyped
- **Evidence.** Six roster rows look mistyped: five carry a provider ID that belongs to a different model (for example, `KoboldAI/LLaMA2-13B-Tiefighter` carries the ID of an EVA-Yi model), and one is an exact duplicate. *Qwen3.8 Omni Flash* has neither Frontier nor Open-Weights ticked. *Command A* and *Command A+* reduce to the same name, and the registry silently takes the first.
- **Fix (mine).** A name that matches two different models becomes an error, not a silent pick. The build stamps the real date instead of a fixed one.
- **You.** Correct the six rows and the tick boxes in Notion. The full list comes with the registry report.

#### B11 · Writers nobody checks
- **Evidence.** No evaluation component judges Character Interview, Proofread, Music or Sound Effects. Visual Consistency Check and Narration Check still have no Mature Fallback (already known).
- **You (decision 4).** Name a checker for each, or accept them unchecked. Proofread is the last pass, so unchecked may be right there.

---

### Group C · Sources of truth that have drifted

#### C1 · The requirements still state the family rules you overturned
- **Evidence.** D27 replaced model families with your line of experts, and P8 was rewritten. But at least twelve places still say "another family": FR-CD-7, FR-CH-3, FR-ML-6, FR-WS-2, FR-AU-5, FR-AU-6, FR-FN-5, FR-SW-1, FR-SW-3, the §6.4 diagram and guards, the §6.7 example, Appendix B. §6.4 still describes "abliterated" models and Hugging Face endpoints as the mature lane, and "all four providers" (there are seven). Appendix A counts 57 agents; there are 123 components. Two code comments and the app's README carry the same wording.
- **Fix.** One consolidation pass to v0.27: a single statement of each rule, the older wording removed, not layered over.
- **You (decision 3).** Do the four **quality tiers** (Basic, Excellent, Premium, Advanced) survive now that each component has Primary, Comparable and Fallback chosen cheaper-first? My recommendation: retire them. They choose between writers, which your expert line already does.

#### C2 · The canvas shows a design the project has moved past
- **Evidence.** I read the live Blueprint board. It still says: checkers "never grade their own family" (four separate rules), a "Mature prose" pool of abliterated models on Hugging Face endpoints, task-type pools as the way models are chosen, "9 steps · 68 agents", and the harness as the build "in progress". Nothing on it shows the prose lane, the media lane, Unsloth Desktop, Comfy Cloud, ElevenLabs or Tailscale. The other boards I checked against the 22 October source copy, not the live canvas: the editing suite and media components appear only in fragments, and the Library board has no "under development" pools.
- **Fix.** A canvas pass in two parts: (a) correct the Blueprint and Model Lab boards to the current routing; (b) add what was approved and never drawn (editing suite, media, scaffolding pools).
- **Standing note.** Your earlier judgement that the canvas reads like a specification still applies. I would do the usability pass on each board as it is corrected, not as a separate project.

#### C3 · Component inputs live nowhere you can see
- **Evidence.** Open question Q13: the database records order, phase, gates and models, but not what each component takes in. That table existed only in the lost script; it survives because it was copied into `components.yaml`.
- **Fix.** Covered by A2 (a tracked inputs file). An Inputs column in Notion remains your call.

#### C4 · Tracked, not fixed (yours)
- The 13 components awaiting your team specs.
- The five scaffolding pools awaiting research; Epithet Words still has no reader.
- Open question Q9 (the mature level; default 4).

---

### Group D · The missing spine

#### D1 · Nothing has ever run end to end
- **Evidence.** `eos-app` has no provider client, prompt builder, agent runner, project store, run log or web server. The harness can call OpenRouter only, and is two of its four phases.
- **Why it belongs in a fixes plan.** Every defect above was found by reading and simulating. The defects that matter most (a provider's real response format, a refusal, a timeout, a cost that surprises you) cannot be found that way.
- **Fix: one thin slice, not the whole of build phase 1.** The first stretch of your Flow Order: the Story Pitch and the six components it depends on, each on the model its own row names, stopping at each of your gates on the way.

  **Idea Intake** → **Story Setup** *(gate: manuscript type)* → **Genre Pack Builder** → **Pen Name and Style** *(gate: pen name)* → **Target Audience** → **Premise Adapter** *(gate: adapted premise)* → **Story Pitch**

  Seven components, three gates, and four of your library pools read for real (pen names, genres, content levels, story pitches). Fiction Tropes is not in it: your Flow Order places it at position 79, after the Story Bible.

  The slice needs only: a prompt builder that gives each component its allowed inputs and nothing else; the corrected router; one client for the OpenAI-style providers (Concentrate AI, OpenRouter); a run record per call (model, route, tokens, cost, time, status); a project folder; and one plain page that shows each result as a card with *Proceed* and *My alternative*.
- **Safeguards.** A **dry run** comes first: it builds every prompt and picks every model without sending anything, so the whole slice is testable at no cost. The first live run happens only on your word, with a spending cap you set (decision 6). The answer-key rule and the keys-in-`.env` rule are enforced in code from the first line.
- **Done when.** The dry run shows seven prompts, the model chosen for each and a stop at all three gates; then one live run produces seven saved outputs, a run record for every call and pitches you can accept or replace.

---

## 3. Order of work

| Stage | Contains | Size | Waits on you |
|---|---|---|---|
| **0 · Safety net** | A1, A2 | Small | "Commit"; the inner repository |
| **1 · Corrections** | B1, B2, B4, B5, B6, B7, B9, B10 (my parts), each with a test written first | Medium | Nothing |
| **2 · Your roster pass** | B1 IDs, B2 second routes, B3, B8, B10 rows, B11 | Yours | Decisions 2, 4, 5 |
| **3 · Rebuild and report** | Re-export the roster, rebuild registry and components, readiness report, A3 package | Small | Stage 2 |
| **4 · Truth alignment** | C1 requirements v0.27, C2 canvas | Medium | Decision 3 |
| **5 · First real run** | D1 dry run, then live | Medium | Decision 6 |

Stages 1 and 2 run side by side: I correct the code while you correct the roster. Stage 4 can also overlap with stage 5. After stage 5 the build returns to the requirements' own build plan (§8), from a base that is versioned, reproducible and proven by one real run.

---

## 4. What I need from you

1. **Version history.** May I put the project under git and make the first commit, leaving out `.env`, `library/` and any answer key?
2. **Mature route.** ~~Extend Mature Fallback to the writing components that handle scene content (recommended), or keep mature books blocked until genre fine-tunes exist?~~ **Answered 2026-11-25 (D33):** the mature tier is the uncensored models on Featherless AI and OpenRouter, fitted by pen name and subgenre.
3. **Quality tiers.** ~~Retire them (recommended) or keep them?~~ **Answered 2026-11-12: retired** (D32).
4. **Unchecked writers.** A checker for Character Interview, Proofread, Music, Sound Effects, or leave them unchecked?
5. **Target Audience.** A Comparable model, or Light tier?
6. **First live run.** A spending cap for the seven-component run.

---

## 5. What this audit did not cover

- **Line-by-line review** of `library.py`, `blueprint.py` and `humanize.py`. Their tests pass and the real library loads clean; I did not hunt for defects inside them as I did in the router.
- **The live Notion database and roster.** I audited the app's copies from 22 October. Changes you made in Notion since then are not reflected here.
- **The canvas boards other than Blueprint**, which I checked against the 22 October source copy only.
- **The vault's contents.** I confirmed that no note in the vault has changed since 22 October and the scaffolding folder holds the same three sets, so the library is not behind it. I did not re-read the notes themselves.
- **Anything needing a live call.** No model was called and no credit was spent.
