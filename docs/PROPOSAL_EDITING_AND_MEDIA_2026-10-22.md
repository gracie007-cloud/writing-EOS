# Proposal · Self-editing and proofreading, and generative media

*2026-10-22. For the Author's approval before anything is written to Notion or the app. One job per component (D25); each component gets its own line of experts (D27); every checker runs on a different model from what it judges (P8).*

---

## 1 · What the app has today, and what is missing

| Already in the app | What it does | Gap |
|---|---|---|
| Editor rewrite actions (FR-ED-1), one of them "Fix grammar" | Rewrites a selection on request | No continuous proofreading of the Author's own writing, and no issue-by-issue review |
| Craft measures (FR-VC-1), counted by code | Sentence lengths, filter verbs, -ly adverbs, dialogue share, POV slips, repeated openings | Counts only; no reports the Author can work through, no explanations, no fixes |
| Humanize (FR-HU) | Removes machine-sounding prose | Not an editing coach |
| Line & Copy Edit (NEW-05a), Proofread (NEW-05b) | End-of-book passes on the locked manuscript and typeset pages | Nothing while the Author is writing |
| Cover Brief, Audiobook Script, Storyboard & Trailer Script | Text briefs and scripts | **Nothing generates images, audio or video.** Requirements §1.3 still lists media as out of scope |

---

## 2 · Self-editing and proofreading (the Grammarly / ProWritingAid / AutoCrit layer)

Three components, on demand, in the Editor phase (L). Each works on any text: the Author's own writing, or an agent's draft before the Author accepts it.

| New component | The job (one each) | Like | Code or model |
|---|---|---|---|
| **Proofreader** | Correctness and consistency as the Author writes. Spelling, grammar and punctuation. House-style consistency against the Story Bible: names and glossary terms, the project's English variant, capitals, hyphens, numbers. One issue at a time, each with Accept or Ignore. | Grammarly (correctness) | Consistency by **code**. Grammar by **two models**: an edit is offered only when both make it, the 2026 fix for over-correction. |
| **Self-Edit Reports** | Reports the Author works through: overused and repeated words, echoes, sentence starts, sentence variety, sticky sentences and glue words, passive voice, adverbs, filter words, dialogue tags and adverbs in tags, clichés and stock phrases, pacing (scene vs summary, dialogue share), readability, sensory balance, commonly confused words. Each is measured against the pen name's voice profile (FR-VC-2) and the genre pack, never against other authors' books (D13). | ProWritingAid and AutoCrit reports | **Code** (P9), no model cost. Builds on the craft measures. |
| **Edit Coach** | For an issue the Author picks (from a report, or "show, don't tell", clarity, tone, wordiness): explains it in the book's own terms and proposes a fix through the paragraph gate. Locked lines and dialogue are protected. Never applied without the Author. | AutoCrit guidance, Grammarly clarity and tone | **Model**, story-aware (reads the Story Bible) |

**Proposed experts (from the roster):**

| Component | Primary | Comparable | Why |
|---|---|---|---|
| Proofreader | GPT-6 Luna | GLM 5.3 Flash | Proofreading is minimal edits. Models correct alike, so two cheap, fast ones that must agree beat one expensive one. Both are on Concentrate AI. |
| Edit Coach | Claude Fable 5.1 | Kimi K3 | Literary judgement, the creative lane in your team specs. When Fable wrote the draft, the router moves to Kimi K3 (P8). |

The end-of-book passes (NEW-05a, NEW-05b) stay as they are; the Proofreader gives them a cleaner manuscript to start from.

---

## 3 · Generative media: visuals, audio, audio-visual

### 3.1 Components

| New component | Phase | Reads | Produces | Kind |
|---|---|---|---|---|
| **Visual References** | H · World, then Story Bible element 8 | Character cards, setting cards, world element, palette (pen name, themes workbook) | Character designs, mood boards, location art; the reference sheets every later image must match | Image model |
| **Map Maker** | H · World | Locations, world rules | Maps for the Bible's Appendices and the book's front matter | Image model |
| **Cover Art** | N · Sales, after Cover Brief | Cover Brief, pen name's cover style and palette, Visual References | Cover options with title and byline set | Image model, strong at type |
| **Interior Art** | M · Finishing, before Typesetting | Visual References, chapter list | Chapter heads, ornaments, scene-break marks | Image model |
| **Audiobook Narration** | N · Sales, after Audiobook Script | Audiobook Script, character voices from Dialogue and Voice (Bible element 7), name pronunciations | Narrated chapters, with a separate voice for each main character | Speech model |
| **Music and Sound** | N · Sales | Trailer storyboard, pen name's tone | Trailer score, audiobook intro and outro, sound effects | Music and sound models |
| **Trailer Video** | N · Sales, after Storyboard & Trailer Script | Storyboard, Cover Art, Visual References | Video shots, started from the approved art so characters stay consistent | Video model (image-to-video) |
| **Trailer Assembly** | N · Sales | Shots, narration, music, captions | The finished trailer | **Code** (ffmpeg) |
| **Marketing Visuals** | N · Sales, after Marketing Copy | Cover Art, Marketing Copy | Social posts, banners, ad sizes | Image model |

### 3.2 Checkers (evaluation components, each with a Mature Fallback per D27)

| New checker | Judges | How |
|---|---|---|
| **Visual Consistency Check** | Visual References, Map Maker, Cover Art, Interior Art, Marketing Visuals, Trailer Video | A vision model compares each image or frame with the Story Bible and the reference sheets: eye colour, scars, uniforms, the shape of a named ship. Never the model that made the image. |
| **Narration Check** | Audiobook Narration | Speech-to-text transcribes the audio, and code compares it with the script: dropped lines, mispronounced Bible names, the wrong voice on a line. |

### 3.3 Proposed experts (October 2026 leaderboards; to be confirmed in the Model Lab)

| Job | Primary | Comparable | Notes |
|---|---|---|---|
| Cover Art (type on the image) | GPT Image 2 | Ideogram (v3/v4) | GPT Image 2 leads most text-to-image arenas. Ideogram is the usual pick for precise title layout. |
| Visual References, Interior Art, Marketing Visuals | FLUX.2 (multi-reference) | Nano Banana Pro (Gemini image) | The two strongest for keeping a character the same across many images. A trained character LoRA (in Unsloth Desktop or Comfy) is the long-run option for recurring leads. |
| Map Maker | Nano Banana Pro | GPT Image 2 | Layout and labels |
| Audiobook Narration | ElevenLabs v3 | Gemini 3.1 Flash TTS | Both recur as the narration leaders. Open-weight option: VibeVoice or Fish Audio S2 Pro. |
| Music | ElevenLabs Music | Lyria 3 Pro | Both licensed for commercial use. Suno has no official API and its terms vary by plan. |
| Sound effects | ElevenLabs Sound Effects | MMAudio (open) | |
| Trailer Video | Seedance 2.0 or Gemini Omni (Veo line) | Wan 3.0 (open) | The top of the video arenas is close to a statistical tie. Image-to-video from the approved art keeps characters consistent. |
| Visual Consistency Check | Gemini 4 Argon (vision) | GPT-6.1 Sol | Text-and-vision judges from the existing roster |
| Narration Check | A speech-to-text model (ElevenLabs Scribe or Whisper-class) | | Transcription only; code does the comparing |

### 3.4 Routes

Concentrate AI offers no image, audio or video generation. Media needs:
- **OpenRouter:** GPT Image 2 and Gemini images. Already allowed.
- **Hugging Face Inference Providers:** FLUX.2, Wan and the other open-weight image and video models. Already allowed.
- **ElevenLabs:** narration, music, sound effects, speech-to-text. **A new outbound destination.**
- **Comfy Cloud and your Kaggle GPU (ComfyUI):** open-weight image and video workflows and LoRA training. **New.**
- **Google AI:** Veo, Gemini Omni, Lyria and Gemini TTS, if those are chosen. **New.**

New destinations are your decision (§6.9).

---

## 4 · Decisions this needs from you

1. **Approve the 12 components:** 3 editing, 9 media. Or tell me which to drop or merge.
2. **Media models in your roster.** The LLM Identifier holds text models. I propose adding the media models to it with a **Modality** column (text, image, video, speech, music, sound, speech-to-text, vision) so the registry and router treat them like every other expert.
3. **New outbound destinations:** ElevenLabs, Comfy Cloud, Google AI.
4. **Mature books.** Image, video and speech providers refuse explicit content. Covers and trailers can stay within a standard rating, but narrating a mature audiobook needs an uncensored-capable speech route. The likely route is an open speech model fine-tuned in Unsloth Desktop. **This is open.**
5. **Scope.** Requirements §1.3 lists media as out of scope for version 1. Approving section 3 moves it in.

## Sources (model research, 2026-10-22)

- Image: [Artificial Analysis text-to-image](https://artificialanalysis.ai/image/leaderboard/text-to-image?open-weights=true), [Lumenfall arena](https://lumenfall.ai/arena/text-to-image), [LLM Stats](https://llm-stats.com/leaderboards/best-ai-for-image-generation), [BudgetPixel](https://budgetpixel.com/arena/leaderboard)
- Type on images: [GPT Image 2 vs Ideogram](https://crepal.ai/blog/aiimage/image-gpt-image-2-vs-ideogram/), [ropewalk text-in-image tests](https://ropewalk.ai/blog/best-ai-text-in-image-models-2026), [invideo](https://invideo.io/blog/best-ai-model-text-in-images/)
- Character consistency: [Gemini vs OpenAI vs Flux vs Runway (May 2026)](https://techstackups.com/comparisons/gemini-vs-openai-vs-flux-vs-runway-character-consistency-may-2026/), [FLUX.2 multi-ref guide](https://selfielabstudio.com/blog/flux-2-multi-ref-character-consistency-guide-20260329)
- Video: [Arena text-to-video](https://arena.ai/leaderboard/video/text-to-video), [Artificial Analysis text-to-video](https://artificialanalysis.ai/embed/text-to-video-leaderboard/leaderboard/text-to-video), [OrcaRouter, Oct 2026](https://www.orcarouter.ai/blog/hidream-o1-video-1-0-leaderboard-debut-api-gap), [invideo](https://invideo.io/blog/best-ai-video-model/)
- Speech: [codesota audiobooks](https://www.codesota.com/speech/best-for-audiobooks), [MarkTechPost TTS benchmark](https://www.marktechpost.com/2026/05/30/best-text-to-speech-tts-models-in-2026-a-benchmark-based-comparison/), [eachlabs](https://www.eachlabs.ai/blog/best-ai-text-to-speech-models-2026)
- Music: [ElevenLabs Magazine](https://elevenlabsmagazine.com/best-ai-music-generators-2026/), [modelhunter](https://modelhunter.ai/blog/best-ai-music-generation-models-2026), [rework](https://resources.rework.com/tools/ai-tools/best-ai-music-generators-2026)
- Proofreading: [Multi-dimensional evaluation of LLMs for GEC (AIED 2026)](https://arxiv.org/html/2605.07635), [Edit-level majority voting (BEA 2026)](https://aclanthology.org/2026.bea-1.60/)
- Routes: [Concentrate AI supported models](https://concentrate.ai/docs/api-reference/endpoint/supported-models), [Concentrate multi-modal](https://concentrate.ai/docs/api-reference/endpoint/multi-modal), [OpenRouter image models](https://openrouter.ai/blog/tutorials/image-generation-models/)
