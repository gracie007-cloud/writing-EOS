# Media providers, missing components, and the agent-team pattern

*2026-10-22. Proposal for the Author.*

---

## 1 · Which provider for which slot

The deciding test is your premise: media that can follow a mature book. Each provider's own policy, read today:

| Provider | Mature content | Evidence |
|---|---|---|
| **Comfy** (Comfy Cloud, or your own ComfyUI) | **Allowed within the law.** The terms ban only illegal content (CSAM, non-consensual intimate imagery), impersonating real people, and harm. With open-weight models you control the filters. Partner (API) nodes follow their own providers' rules. | [Comfy terms](https://www.comfy.org/terms-of-service) §3–4 |
| **fal.ai** | **Not allowed.** The Acceptable Use Policy bans "sexually explicit content" with no exception for adults or fiction. fal also runs OpenAI's moderation filter across all modalities. | [fal AUP](https://fal.ai/legal/acceptable-use-policy) §1.4; [fal Trust & Safety](https://fal.ai/legal/trust-and-safety) |
| **OpenRouter** | **Not for explicit work.** It defers to each model's own terms, and the image models it carries (GPT Image 2, Gemini) refuse explicit content. It can block anything it judges objectionable. | [OpenRouter terms](https://openrouter.ai/terms) §5, §6.7, §7.8 |

### Recommendation

| Slot | Provider | Covers |
|---|---|---|
| **Primary** | **ComfyUI, on Comfy Cloud** | Every media job, standard and mature: open-weight image (FLUX.2), video (Wan, LTX), speech and music models, character LoRAs, and partner nodes for proprietary models on standard work. |
| **Comparable** | **fal.ai** | Standard-rated media only. Mostly the same open models, hosted and fast. |
| **Fallback** | **OpenRouter** | Standard-rated stills only: GPT Image 2 and Nano Banana Pro, the best for covers and marketing art. |
| **Mature fallback** | **Your own ComfyUI** (the same workflows on your Kaggle GPU) | The only second route that keeps mature work possible when Comfy Cloud is down. Check Kaggle's own terms first; I haven't. |

This mostly matches the line you suggested, with one difference: **for mature work, fal.ai and OpenRouter can't be the comparable or the fallback.** The router will send mature media only to Comfy routes.

Two more points:
- **Covers, thumbnails and store graphics must be retailer-safe whatever the book's rating**, so all three providers can make them.
- **Mature narration has a possible answer.** Open speech models run inside ComfyUI, so they could narrate a mature audiobook. That would replace "left open" with an option for you to try.

---

## 2 · Your Audio-Video Orchestrator design, which the 15 new components only partly follow

Your [Audio-Video Orchestrator](https://app.notion.com/p/3e69e32c513c8080aaa6d71cbfde15fd) page sets out a team: *Sol directs, Fable humanizes, Gemini interprets the visual layer, specialist media models render, the Media Bible keeps continuity, the Author approves canon.* What I added has no Director, and treats media as separate jobs. Missing from it:

| From your page | In the app now | Needed |
|---|---|---|
| **Audio-Visual Production Director** (Sol), team lead | Nothing | A team-lead component over the media pipelines |
| **Media Bible**: visual identity, character appearance, colour, lighting, camera language, typography, voice identity, music identity, sound design | Visual References covers part of the visuals | A Media Bible artifact and its keeper |
| **Media Continuity Ledger**: character → look, voice ID, wardrobe; location → reference; shot → source scene | Nothing | A ledger kept by code, read by every renderer |
| **Voice Performance Specification**: narrator and character voices, pace, pronunciation | Narration reads the script only | A spec step between the script and the speech model |
| **Cover, three stages**: concept (Sol), render, QA (title legibility, thumbnail survival, genre signal) | One Cover Art step | Concept, then render, then Cover QA |
| **Video Voiceover** and **Video Thumbnail** (concept, render, QA) | Not present | Two more components |
| **Trailer Director**: hook, arc, shot list, edit decisions, trailer QA | Trailer Video and Trailer Assembly only | A director step before the shots |
| Rule: **media may interpret canon, may not create it**; GENERATED → REVIEWED → CANON-COMPATIBLE → AUTHOR APPROVED → MEDIA CANON | Not enforced | A status on every asset, checked by code |

---

## 3 · Components in your workspace with no row in the database

From a page-by-page comparison of the ten sections under *Narrative Writing EOS* with the 123 database rows.

**No equivalent row (13):**
- Narrative World Dossier Architect: Themes in Literature Selector
- Story Dossier Engineering: Narrative Function Formulator, Prose Structural Auditor
- Prose Engineering: Prose Variation Style & Technique, Prose Architect, Scene Excerpt Composer, Dialogue Generator
- Media Bible: Audio-Video Orchestrator, Market Researcher, Positioning Moderator, Positioning Bible, Book Influencer Partnership Query Generator, and the Media Bible itself

**A row exists, but the match needs your confirmation:**

| Workspace page | Closest row |
|---|---|
| Book Sales Pitch Generator | Query / Submission Synopsis & Pitch (NEW-09)? |
| Chapter Generator | Brief Writer (22.5) and First Draft (32)? |
| Narrative Brief Generator | Brief Writer (22.5)? |
| Controlled Revision | Rewrite (35)? |
| Prose Realization | First Draft (32) or Prose Refinement (37)? |
| Character State Delta Analyst | Character State Examiner (27.5)? |
| Literary Genre Selector | Genre Analyst (4.1)? |

---

## 4 · The agent-team pattern, which the app doesn't model yet

Your team specs ([Brainstorming Engine](https://app.notion.com/p/3ed9e32c513c81deab0ae24d885ec396), Story Pitch, Target Audience, Fiction Tropes, Plot Selector, Synopsis, Character Refiner and others) define each component as a **team**:
- a Team Lead with its own LLM;
- Co-Leads and sub-agents, each on its own LLM;
- an orchestration pattern: Supervisor, Pipeline, Fan-out/Fan-in or Comparison;
- an input contract, tools and permissions, and memory;
- lifecycle hooks: Session Start, Prompt Submit, Pre-Tool, During-Tool, Post-Agent, Session End;
- deliverables with quality checks, and a `soul.md` personality.

`components.yaml` gives each component only one line of experts and a Swarm Tier. Nothing in the app holds the team.

**What it needs:**
1. A team file per component (`config/teams/<step>.yaml`), copied from its Notion team spec: lead, co-leads and sub-agents with their models, pattern, contract, hooks, deliverables.
2. The router choosing a model per agent, not just per component.
3. Code that runs each pattern and its hooks. For example, the Brainstorming Engine's Pre-Tool hook rejects a run when KNOWN CANON is missing.
4. Team specs written in the same format for every component that has none yet, starting with the 15 new ones and the missing components above.
