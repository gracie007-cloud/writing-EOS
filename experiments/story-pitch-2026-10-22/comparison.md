# Story Pitch experiment · comparison and recommendation

**A** = Story Pitch decides the audience and the tropes itself (`A-integrated.md`).
**B** = Target Audience Selector → Fiction Tropes Generator → Story Pitch (`B-standalone.md`).
Both start from the same inputs (`00-inputs.md`). No model was called.

## What this test can and cannot show

- **Same writer.** Claude wrote both versions and knew both specs. To limit that, A was written first, saved, and not edited afterwards.
- **It tests what each set-up asks for, not how good a model is.** Your concern was that the model that writes a good pitch may be poor at choosing an audience or tropes. Only real calls to the assigned models can answer that, and you asked me not to spend credit on them.
- What the test does show: what each set-up *asks for*, and so what it catches.

## Side by side

| | A · Integrated | B · Standalone |
|---|---|---|
| **Audience** | One paragraph: "adult readers of character-driven SF", with comparison authors | Five variables kept apart; fit kept apart from appeal; primary, secondary and crossover readers; Audience Distance 2; YA and children's checks; Reader Contract; BISAC candidates |
| **The biggest catch** | Not seen | **The genre label and the material disagree.** Space Opera promises fleets and empires; the material is a single station. B put this to you as a decision with two options |
| **Tropes** | Six tropes, picked to sell the hook | Ten tropes, each with a type, interaction test, risk, treatment and verdict |
| **Trope risk** | No checks beyond "not an AI uprising" | Avoidance List of six. It catches *Redemption Equals Death* for Jonick, and *Found Family*, which works against the Isolation theme |
| **Tropes A chose that B rejected or changed** | Found Family; Storm Returns (decorative as A used it) | Found Family rejected. The storm changed so that Hari and Lyra read the tides differently |
| **Pitch** | "Partner or replacement?" This leans toward the AI-threat reading B lists to avoid | Carries the inversion (hand someone else the keys), fleets arriving as traffic, and the never-explained promise |
| **Profile signals** | Nearly the same. One slip: A named "Man vs. Nature" as a core; the app's core is Environmental | Correct core names |
| **Cost and time** | One pass | Three passes; the TAS team has four agents and the FTG team three. Several times A's cost at Stage 0. Not measured |
| **Fit with the specs** | Breaks the TAS rule against choosing the audience to suit the pitch. Breaks one job per component (D25) | Matches both specs, with one exception: FTG at Stage 0 lacks its inputs (below) |

The "Man vs. Nature" slip was mine, not a result of the integrated set-up. A check on core names would catch it in either version.

## Why A missed what B caught

A's brief never asked for a misclassification check, a risk assessment or an avoidance list, so the pass did not produce them. A capable writer still left them out.

You could add those checklists to the Story Pitch brief. Then one pass holds three jobs, and the writer checks its own pitch. That is exactly what the TAS spec rules out when it separates the selector from Marketing: "must not reverse-engineer the audience."

## A timing finding

- **FTG at Stage 0 is provisional.** Its spec needs a worldbuilding brief, full character bios and your familiarity→novelty dial. None of them exist at Stage 0.
- **The Notion database already has this right.** It places FTG at flow 76, after characters and world.
- **TAS at flow 13** (just before Story Pitch at 14) is right for an early diagnostic. Its spec says to re-run it after the manuscript exists.

## Decision (the Author, 2026-10-22): the three stay separate

**The main reason is the model.** Each component is a slot for its own best-fit model:
- **Fiction Tropes Generator:** an expensive creative model such as Claude Fable 5.1.
- **Target Audience Selector:** a cheap one such as GLM-5.3 Flash, which is enough for classification.
- **Story Pitch:** GPT-6.1 Sol, which is strong at pitch writing.

Rolling components into one another removes those slots. It also hides each model's merit at its own job, which a hand-written test like this one cannot show. The structural findings above are a second reason on top of that.

**Positions:**
- **TAS at flow 13**, before Story Pitch. Story Pitch reads the Reader Contract and does not choose the audience. TAS re-runs after the manuscript.
- **Story Pitch at flow 14.**
- **FTG at flow 76**, after characters and world, where its inputs exist. Its Matrix and Avoidance List govern the Scene Briefs.

**Note:** the Notion team specs still name GPT-6.1 Sol / DeepSeek-V4 Pro as lead for both TAS and FTG. Those leads need to change to the models above.

## Still open

- Your answer to B1's misalignment: keep Space Opera and bring in operatic scale through Nova Lumen's war (a), or shelve the book as literary SF (b).
- **Model columns.** NEW-13 and NEW-14 still carry Story Pitch's models (GPT-6.1 Sol / MiMo-V2.6-Pro). Both models you named are in the LLM Identifier roster: *GLM 5.3 Flash* and *Claude Fable 5.1*.
- **Not yet in the app.** NEW-13 and NEW-14 are missing from `components.yaml`. Rechecked in Notion: each Flow Order (13, 14, 76) has a single row, so there is no collision.
