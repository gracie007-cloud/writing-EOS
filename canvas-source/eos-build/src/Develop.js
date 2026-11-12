class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, sel: 'pitch' };
}
renderVals() {
/*VIEW*/
/*TONES*/
var P = { ext: 'extraction', syn: 'synthesis', idea: 'ideation', prose: 'prose', ver: 'verdict', pv: 'prose + verdict', code: 'code', you: 'you' };
var ag = function (name, p, does, o) {
o = o || {};
return { name: name, db: o.db || '', p: p, does: does, judge: o.judge || '', loop: o.loop || '', n0: o.n };
};
var pipes = [
{ id: 'intake', step: '1 – 4.1', name: 'Intake and Pen Name', status: 'DONE',
desc: 'Your brainstorm (intent) and braindump (material) stay separate until extraction. The pen name is chosen first and governs: the premise is adapted to how that author writes.',
reads: 'Author Brainstorm: themes, tone, audience, genre, ending feeling. Story Braindump: images, situations, people, settings, set pieces. Uploads. Your own research sources.',
produces: 'Fact base, manuscript type, genre pack, pen name and style, the Reader Contract, genre writing guide, point of view and style defaults, the adapted premise',
gate: 'You approve the manuscript type, the pen name, the audience (any mismatch with your intent comes to you), then the adapted premise. If no Genre Matrix row fits exactly, the story moves toward the nearest row.',
extraTitle: 'How the pen name governs', extra: 'The premise is reshaped to fit the pen name’s genre row and style. Every change it makes is pitched to you as an option: proceed, choose another, or give your own.',
agents: [
ag('Idea Intake', 'syn', 'Reads uploads (.txt .doc .docx .rtf .odt .csv .pdf) and tags images, situations, people, settings, set pieces.', { db: '1 · Braindump Intake (chatbot + uploads)' }),
ag('Note Taker', 'syn', 'Captures the brainstorm in conversation and keeps intent apart from material.', { db: '1.1 · Narrative Note-Taker' }),
ag('Fact Base', 'syn', 'Builds a fact base from your own sources and uploads only, each fact with its source. No web search.', { db: 'NEW-03 · Pre-Draft Research / Fact Base' }),
ag('Story Setup', 'ext', 'Pitches the category and manuscript type (novel, novella, collection, serial). Fiction only in this version.', { db: '2 · Narrative Builder + Manuscript Type' }),
ag('Genre Pack Builder', 'syn', 'Builds or extends a genre pack from your notes on comparable books.', { db: '4.1 · Genre Analyst' }),
ag('Pen Name and Style', 'ver', 'Ranks pen names against the Genre Matrix and literary styles. You choose.', { db: '3 · Pen Name, Genre and Literary Style (Triad)' }),
ag('Target Audience', 'ver', 'Works out the audience the material is built for, kept apart from who might also enjoy it; checks for a wrong shelf; writes the Reader Contract. A mismatch with your intent comes to you as a decision.', { db: 'NEW-13 · Target Audience Selector', judge: 'Its own model, chosen for classification' }),
ag('Genre Writing Guide', 'syn', 'Fills the genre template: the content targets the pen name writes to, for the reader in the Reader Contract.', { db: '4 · Writing Guide Population (genre templates)' }),
ag('Point of View and Reader', 'syn', 'Point of view, tense and style-guide defaults, for the target reader the Reader Contract sets. Stage 3 adapts them to the project.', { db: 'NEW-02 · POV / Tense / Style-Guide / Target-Reader Specification' }),
ag('Premise Adapter', 'syn', 'Conforms storyline, tone and genre treatment to the pen name and the Reader Contract. Anything it changes comes to you as an OPTION.', { db: '3.5 · Premise Adaptation (to Pen Name)', judge: 'Unused options go to the Creative Reserve' }),
ag('Your gate', 'you', 'Manuscript type, pen name, the audience, then premise.')
] },
{ id: 'pitch', step: '5 – 6', name: 'Stage 0 · Pitch Selection', status: 'DONE',
desc: 'Builds the Pitch Profile and scores all nine Conflict Cores. A fit-scoring model: it returns a ranked shortlist, never a verdict.',
reads: 'Brainstorm and braindump, kept separate; the adapted premise; the Reader Contract',
produces: 'The pitch (title, logline, premise); Conflict Seed: core, six modifier axes, Pillars at stake, runner-up core, outcome preference held for Stage 2',
gate: 'You pick from the ranked shortlist. A tie is your call; a winner below 12 sends you back to the braindump.',
extraTitle: 'Calibration', extra: 'The weights are starting values. Run 15–20 known stories through the rater and the calculator; where the pick keeps missing the author’s actual core, adjust the weight responsible. The log lives in the Model Lab.',
agents: [
ag('Story Pitch', 'ext', 'Reads the Reader Contract and builds the pitch: title, logline, premise. Extracts the signals: opposing force, implied Pillars, scale, temporal root, inevitability, novelty, intensity, outcome preference.', { db: '5 · Story Pitch (Pitch Profile Builder)' }),
ag('Conflict Scoring', 'ver', 'Rates Source, Theme and Genre 0–3 for each of the nine cores and lists contradictions, citing the braindump.', { db: '6 · Conflict Fit Rater', judge: 'Different family from the Story Pitch' }),
ag('Fit score', 'code', 'Pillar factor, then (Source ×3) + (Pillar ×3) + (Theme ×2) + (Genre ×1) − 3 per contradiction. Maximum 27. Reads the gap: 4+ clear, 1–3 close, 0 your call, below 12 weak.'),
ag('Runner-up filing', 'code', 'The runner-up core becomes a subplot or Midpoint candidate. Unchosen options go to the Creative Reserve.'),
ag('Your pick', 'you', 'The core is always yours.')
] },
{ id: 'chars', step: '10.1 · 3.6 · 6.5 · 6.6', name: 'Naming and Characters', status: 'DONE',
desc: 'Naming rules come first, so every name is generated and checked against them. Then braindump characters become roles: names and traits are discarded and only the role survives. Each role is matched against the Character Pool first; a character is created only when nothing fits.',
reads: 'Role requirements, the adapted premise, the pen name, real-world naming conventions',
produces: 'Naming rules (cultures, conventions, expectation code, subversion and collision registers), then profiles at the right depth tier; pool entries split into Core and Skin. Invented fields stay PROVISIONAL until your gate.',
gate: 'You approve the naming rules first. Then you choose each character and each name. Plot-shaping inventions come to you as OPTIONS. Unchosen candidates go to the Creative Reserve.',
extraTitle: 'Depth tiers', extra: 'Tier 1 Core · protagonist, antagonist, mentor: the full order plus the Mirror Map.\nTier 2 Supporting · condensed profile, Pillar Profile, function, voice, name critique.\nTier 3 Specific minor · identity, function, one human detail, name. Victims are never below Tier 3.\nCharacter State and Character Notes run later, in the chapter loop.',
agents: [
ag('Naming Rules', 'syn', 'Cultures and lineages, invented-language roots, conventions, the expectation code, the subversion register.', { db: '10.1 · World Naming System Builder', n: 'N1' }),
ag('Naming checks', 'code', 'Cliché blocklist, distinct first letters, byline collision, only logged anagrams.', { n: 'N2' }),
ag('Your approval', 'you', 'The naming rules, before any character is named.', { n: 'N3' }),
ag('Cast Roles', 'ext', 'Turns braindump characters into narrative roles. Names and traits are discarded.', { db: '3.6 · Role Extraction (placeholder characters)', n: '3.6' }),
ag('Character Pool Match', 'ver', 'Scores pool characters against each role. No fit triggers New Character.', { db: '6.5 · Character Pool Match', n: '1' }),
ag('Role Requirements', 'ext', 'Profiling Mode gathers text evidence; Creation Mode lists what the role requires.', { db: 'CD-02 · Evidence or Role Requirements', n: '2' }),
ag('New Character', 'idea', 'Creation Mode: builds a character for a role the pool cannot fill.', { db: '6.6 · Character Creation', n: '2+' }),
ag('Inner Life', 'syn', 'The psychological structure. Ghost and Lie are candidates until Stage 2 confirms them.', { db: 'CD-03a · Psychological Structure Architect', n: '3' }),
ag('Personality Type', 'ext', 'Identifies the personality type. The type describes the structure, never dictates it.', { db: 'CD-03b · Personality Type Identifier', n: '3' }),
ag('Archetype Check', 'ver', 'Archetype stack scored 0–5 with citations.', { db: 'CD-04 · Character Archetype Detector', n: '4', judge: 'Code checks every citation is verbatim' }),
ag('Character Type', 'ext', 'Labels follow the psychology; they never generate it.', { db: 'CD-05 · Character Type Classifier', n: '5', judge: 'Code validates the schema' }),
ag('Name Ideas', 'prose', 'Creation Mode only. Three candidates with etymology, built from the naming rules.', { db: '6.61 · Character Name Generator (Creation Mode)', n: '6', judge: 'Code blocks cliché names and collisions with the cast and the byline' }),
ag('Name Check', 'ver', 'Checks conventions, expectation code and distinctiveness.', { db: '16 · Character Name Critique', n: '7', judge: 'Different family from Name Ideas' }),
ag('Character Profile', 'syn', 'Snapshot and Character DNA. Every invented field traces to a role requirement, the premise or the pen name.', { db: 'CD-08 · Character Profile Builder', n: '8' }),
ag('Mirror Map', 'syn', 'Antagonists and foils only: maps the character against the protagonist.', { db: 'CD-08a · Mirror Map', n: '8a' }),
ag('Representation Check', 'ver', 'Runs when harm is tied to an identity group, culture, belief or condition. Informs you; never overrides you.', { db: 'CD-08b · Representation and Trope Check', n: '8b', judge: 'Different family from the Character Profile' }),
ag('Character Sheet', 'syn', 'Rendered sheet from the profile.', { db: 'CD-09 · Character Sheet Generator', n: '9', judge: 'Coherence score set by another family' }),
ag('Character Voice Guide', 'syn', 'Visual and vocal manifestation.', { db: 'CD-10 · Character Style Bible', n: '10' }),
ag('Character Polish', 'pv', 'Separate diagnostic pass: vignettes, removal and mis-attribution tests.', { db: 'CD-11 · Fictional Character Refiner', n: '11', judge: 'Tests run on a different family than the vignettes' }),
ag('Pool write · Core and Skin', 'code', 'Core (psychology, archetype, Pillar History pattern) is portable; Skin (name, culture, appearance) is regenerated per story.', { n: '12' })
] },
{ id: 'plot', step: '7 – 11', name: 'Stage 1 · Plot Foundation', status: 'DONE',
desc: 'Conflict + Character = Plot. Records facts, not interpretations. The Plot Blueprint governs the entire story.',
reads: 'Conflict Seed; Character Seed (identity, Pillar Profile, Pillar History, Want)',
produces: 'Plot Blueprint: premise, seed, antagonist role, collision (point of impact, resonance, specificity, possible endings); a one-page synopsis',
gate: 'You approve the Plot Blueprint and its synopsis. Later steps can send it back here; they never patch it.',
extraTitle: 'The six Pillars', extra: 'Sustenance · Clothing · Shelter & Safety · Belonging · Technology · Purpose.\nEach has a State (Secure, Threatened, Unmet) and a Level (Natural, Technological).',
agents: [
ag('Character Seeds', 'ext', 'Facts only: identity, the State and Level of all six Pillars, one Pillar History event, the opening Want.', { db: '7 · Character Seed Recorder' }),
ag('Point of Impact', 'syn', 'Point of impact (first Secure Pillar threatened), resonance with Pillar History, why this character, the intensity spine.', { db: '8.1 · Collision Analyst' }),
ag('Antagonist Role', 'syn', 'When the core needs a face: function, requirements, pool match or creation.', { db: '8.2 · Antagonist Role Spec', loop: 'Needs a new character: back to Characters' }),
ag('Plot Blueprint', 'idea', 'Writes the Plot Blueprint from the Conflict Seed, the character seeds, the point of impact and the antagonist role.', { db: '8 · Plot Blueprint Writer' }),
ag('Originality Check', 'ver', 'First pass: names the three most familiar elements; each must be subverted, deepened or justified.', { db: '18.5 · Originality & Trope Critique', judge: 'Different family from the Plot Blueprint and Point of Impact' }),
ag('Synopsis', 'syn', 'Writes a one-page synopsis from the Plot Blueprint, pitched to you with it.', { db: '11 · Synopsis Writer (Synopsis Deep Dive)' }),
ag('Blueprint checks', 'code', 'Exactly one core; point of impact names a Pillar with State and Level; Peak above Opening.'),
ag('Your approval', 'you', 'The Plot Blueprint and synopsis are pitched to you; the Blueprint becomes the source of truth.')
] },
{ id: 'arc', step: '13 – 13.4', name: 'Stage 2 · Arc', status: 'DONE',
desc: 'Plot Blueprint + GANT 2.0 = Deepened Plot. Interprets Stage 1’s facts as the Belief, Stakes and Adaptation rings. It deepens; it never replaces.',
reads: 'The Plot Blueprint only',
produces: 'Arc Blueprint: Belief Ring beats 0–7, Midpoint Pillar shift, outcome, oscillation points, supporting arcs, next-cycle Ghost',
gate: 'You approve the arc and the outcome. The outcome preference from Stage 0 is a starting suggestion, not a requirement.',
extraTitle: 'Belief Ring', extra: '0 Ghost · 1 Lie, Want declared · 2 Threat to the Lie · 3 Want activated · 4 Need · 5 Reckoning · 6 Truth or Lie retained · 7 New Self.',
agents: [
ag('Character Arc', 'syn', 'Pillar History → Ghost; Pillar Profile → Lie; point of impact → Threat; an overlooked Pillar → Need; Peak → Reckoning. Code builds the skeleton from the fixed table.', { db: '13 · GANT Converter (Character Arc, GANT 2.0)' }),
ag('Ghost and Lie Check', 'ver', 'Confirms or revises the candidates from character creation; never inherits them.', { db: '13.1 · Ghost and Lie Confirmer', judge: 'Different family from Inner Life, which proposed them' }),
ag('Ending Type', 'ver', 'Answers two questions: was the Truth embraced, and was the Need Pillar restored? Code reads the ending type from the matrix.', { db: '13.2 · Climax Outcome Matrix' }),
ag('Supporting Arcs', 'syn', 'Antagonist and others on their own cycles against the same Plot Blueprint: static, or a late break.', { db: '13.3 · Supporting Arcs' }),
ag('Arc Setbacks', 'syn', 'Where the character slips back before moving forward. Code checks the plot only moves forward.', { db: '13.4 · Oscillation Planner' }),
ag('Guardrail check', 'code', 'Core, modifier axes, Pillars and point of impact must be unchanged.', { loop: 'Changed: stop, revise Stage 1, re-run Stage 2' })
] },
{ id: 'cast', step: '14 – 15', name: 'Stage 3 · Cast & Structure', status: 'DONE',
desc: 'Assigns the cast to the functions the arc needs, then chooses how the story is told. It presents; it never alters.',
reads: 'Plot Blueprint, Arc Blueprint, the pen name’s pacing',
produces: 'Cast Function Map (filled, vacant, cut or merge), the structure with its score, and the project style card',
gate: 'You approve the cast map, the structure and the project style card.',
extraTitle: 'Archetypes are positions', extra: 'Hero travels Lie → Truth. Mentor already holds the Truth. Herald delivers the threat. Threshold Guardian defends the Lie. Shadow never surrenders it. Shapeshifter oscillates. Ally holds part of the Truth. Trickster stands outside the arc.',
agents: [
ag('Cast and Structure', 'syn', 'Lists the functions the arc needs and assigns characters (code flags vacancies and characters with no function), then rates Intensity Curve, Pacing and Cast Shape 0–3 for each structure.', { db: '14 · Cast & Structure (Structure Fit Rater + Vacancy Mapper)', loop: 'Vacant role: back to Characters (pool, then creation)' }),
ag('Style Card', 'ext', 'Adapts the pen name’s voice profile to this project: a project style card, each change with its reason. The pen name itself does not change.', { db: '15 · Style Calibrator (Literary Style Calibration)' }),
ag('Structure score', 'code', 'All 21 structures in your structure map, conflict core first. Inevitability and novelty come from your map, outcome from code; totals ×3 ×3 ×2 ×2 ×1 ×1, maximum 36. Three-Act Structure if nothing beats 18. Beside the scores: how well your themes suit each structure, from your themes workbook, shown and never added.'),
ag('Kishōtenketsu flag', 'code', 'If it wins, the story runs on insight, not opposition.', { loop: 'Back to Stage 0 to recheck the Conflict Core' }),
ag('Your approval', 'you', 'The cast map, the structure and the style card are pitched to you; you proceed or give an alternative.')
] },
{ id: 'world', step: '10 – 10.5', name: 'World', status: 'DONE',
desc: 'The world’s elements, built inside the naming rules from step 3, then the planned story timeline.',
reads: 'Plot and Arc Blueprints, the cast, the naming rules',
produces: 'Worldbuilding, locations, world rules, institutions and the planned master timeline',
gate: 'The world elements and the timeline are pitched to you; you proceed or replace any of them.',
extraTitle: 'Every name does two jobs', extra: 'Novelty: fresh, of this world, not an AI default.\nExpectation: tells the reader something through a code they learn.\nNo dead air: no name may read as a placeholder.',
agents: [
ag('Worldbuilding', 'idea', 'Shapes the world the story needs: places, institutions, history, technology.', { db: '10 · Worldbuilding' }),
ag('World Elements', 'ext', 'Finds and categorises every world element.', { db: '10.2 · Element Extractor' }),
ag('Locations', 'syn', 'Layout, atmosphere, who lives there and who passes through.', { db: '10.3 · Location Writer' }),
ag('World Rules', 'syn', 'States each rule precisely enough for a checker to enforce.', { db: '10.4 · World Rules Drafter' }),
ag('Naming checks', 'code', 'Every new name is checked against the naming rules from step 3.'),
ag('World Check', 'ver', 'Elements against each other, the cast and the blueprints.', { db: '10.5 · World Consistency Check', judge: 'Different family from the writers' }),
ag('Story Timeline', 'syn', 'Lays out the planned story time. Dates, ages and intervals are computed by code.', { db: 'NEW-04 · Planned Master Timeline' })
] },
{ id: 'qa', step: '16 – 19.4', name: 'QA and Story Bible Lock', status: 'LOCKED',
desc: 'Critiques and a reference audit, then assembly and your lock. The Story Bible becomes the single source of truth.',
reads: 'Everything approved so far',
produces: 'Story Bible vN with arcs, Pillars, secret register, who-knows-what, relationship web and check lists',
gate: 'You lock it. After that, canon changes only through change requests with an impact assessment.',
extraTitle: 'Verifier and challenger', extra: 'A primary verifier from one model family finds issues; a challenger from another family tests each finding. Only findings that survive reach you, each with its evidence and canon status.',
agents: [
ag('Logic Check', 'ver', 'Cause and effect; every major action rational for what the character knows.', { db: '18 · Logic Critique', judge: 'Different family than the material’s writer' }),
ag('Emotion Check', 'ver', 'The emotional line of the story. Name Check and Originality Check run again across the whole cast alongside it.', { db: '17 · Emotional Critique', judge: 'Different family than the material’s writer' }),
ag('Reference Check', 'ver', 'Checks borrowed elements and references.', { db: '18.6 · Reference Audit' }),
ag('Secrets and Who Knows', 'ext', 'Secret register, who knows each secret, relationship scores, as data.', { db: '19.1 · Secrets and Knowledge Builder', judge: 'Code keeps the tables' }),
ag('Story Rules', 'ext', 'Turns rules into check lists, including rules tied to an arc beat or chapter range.', { db: '19.2 · Rule Extractor' }),
ag('Story Bible Builder', 'syn', 'Builds the Story Bible cards from the Dossier’s approved material, with the full synopsis.', { db: '19 · Bible Assembler' }),
ag('Style Sheet and Canon Upkeep', 'syn', 'Makes the house style sheet; after each chapter lock, proposes canon updates as change requests.', { db: 'NEW-01 · Story-Bible / Canon Maintenance & Style-Sheet Creation' }),
ag('Canon Check', 'ver', 'Reads the whole Bible for contradictions.', { db: '19.3 · Canon Verifier' }),
ag('Canon Second Opinion', 'ver', 'Tests each finding from the Canon Check. Only findings that survive reach you.', { db: '19.4 · Canon Challenger', judge: 'A different family from the Canon Check' }),
ag('Your lock', 'you', 'The verified Bible is pitched to you; you lock it or send it back.')
] },
{ id: 'outline', step: '20 – 22', name: 'Outline', status: 'APPROVED',
desc: 'Maps the approved structure into chapters: GANT beats per POV character, reveals and sliders per chapter, then an audit with a fix list.',
reads: 'Story Bible, Arc Blueprint, chosen structure',
produces: 'Chapter-by-chapter outline, audit scorecard and fix list, the bake-off test pack',
gate: 'The audited outline is pitched to you; you approve it or send it back with your changes.',
extraTitle: 'Feeds the chapters', extra: 'Each chapter brief inherits its GANT beat, scheduled reveals, sliders and the rules active at that point in the arc.',
agents: [
ag('Outline', 'syn', 'Acts, sequences and chapters in the chosen structure.', { db: '20 · Outline Generator (Narrative Outliner)' }),
ag('Arc Beats', 'syn', 'Places the belief beats 0–7 for each point-of-view character across the chapters.', { db: '20.1 · Arc Beat Planner' }),
ag('Reveal Plan', 'syn', 'Places each secret’s reveal and who gains the incentive to expose it.', { db: '20.2 · Reveal Scheduler' }),
ag('Reveal order check', 'code', 'No reveal before the secrets it depends on.'),
ag('Outline Check', 'ver', 'Emotional arc per chapter; cause and effect; every major action rational for what that character knows.', { db: '21 · Outline Emotional & Logic Audit', judge: 'Different family from the Outline', loop: 'Issues go to Outline Revision, at most twice' }),
ag('Tension and Pace', 'ext', 'Tension, dread and pacing per chapter, raised at each reveal. Runs again on any chapter the revision changes.', { db: '22 · Plot Sliders / Slider Setter (tension, dread, pacing)' }),
ag('Outline Scorecard', 'ver', 'Scores the outline, sliders included, and writes the fix list.', { db: '21.1 · Outline Audit Scorecard' }),
ag('Outline Revision', 'syn', 'Applies the fix list, then hands the outline to you.', { db: '21.2 · Outline Rewrite' })
] }
];
var SHORT = { intake: ['Intake and pen name', 'Pen name chosen'], pitch: ['Pitch selection', 'Core chosen'], chars: ['Naming and characters', 'Cast chosen'], plot: ['Plot foundation', 'Blueprint approved'], arc: ['Arc', 'Outcome set'], cast: ['Cast and structure', 'Structure set'], world: ['World', 'World built'], qa: ['QA and Bible lock', 'Bible locked'], outline: ['Outline', 'Outline approved'] };
var out = pipes.map(function (p, i) {
var on = p.id === st.sel;
return Object.assign({}, p, {
num: String(i + 1).padStart(2, '0'), short: SHORT[p.id][0], result: SHORT[p.id][1], on: on,
bg: on ? '#F2F7FD' : '#FFFFFF', border: on ? '#2E75B6' : '#E3E8F0', shadow: on ? '0 0 0 3px rgb(46 117 182 / 0.15)' : 'none',
pick: function () { self.setState({ sel: p.id }); }
});
});
var d = out.filter(function (p) { return p.on; })[0] || out[0];
var KIND = function (p) {
if (p === 'you') return Object.assign({ kind: 'Your decision', rowBg: '#FFFBEB', rowRing: '#FFE699' }, { kindBg: TONE.you.bg, kindFg: TONE.you.fg, kindRing: TONE.you.ring });
if (p === 'code') return { kind: 'Counted by code', rowBg: '#F8FAFC', rowRing: '#E3E8F0', kindBg: TONE.wait.bg, kindFg: TONE.wait.fg, kindRing: TONE.wait.ring };
return { kind: engine ? P[p] + ' pool' : 'Agent', rowBg: '#FFFFFF', rowRing: '#E3E8F0', kindBg: TONE.run.bg, kindFg: TONE.run.fg, kindRing: TONE.run.ring };
};
var agents = d.agents.map(function (a, i) {
return Object.assign({}, a, KIND(a.p), { name: engine && a.db ? a.db : a.name, n: a.n0 || String(i + 1), hasLoop: !!a.loop, showJudge: engine && !!a.judge });
});
var models = agents.filter(function (a) { return a.p !== 'code' && a.p !== 'you'; }).length;
var codes = agents.filter(function (a) { return a.p === 'code'; }).length;
d = Object.assign({}, d, { agents: agents, countText: models + ' agents' + (codes ? ' · ' + codes + ' code step' + (codes > 1 ? 's' : '') : '') + ' · each agent on its own model' });
var G = function (k, v, gov) { return { k: k, v: v, bg: gov ? '#FFF5D6' : '#FFFFFF', ring: gov ? '#FFD966' : '#E3E8F0', labelFg: gov ? '#6B4E00' : '#5F6E84' }; };
var settings = [G('Pen name · governs', '[Pen name]', true), G('Genre Matrix row', '[Genre row]'), G('Genre pack', 'Romantic suspense + thriller'), G('Literary style', '[Literary style]'), G('World', '[Story world]'), G('Content tier', '[Content tier]'), G('Braindump', '[Braindump title]')];
var DS = function (step, what) { return { step: step, what: what }; };
var dossier = [DS('Intake and Pen Name', 'Manuscript type, pen name triad, adapted premise'), DS('Pitch Selection', 'Conflict Seed and the runner-up core'), DS('Naming and Characters', 'Naming rules; 7 character packages: 3 from the pool, 4 created'), DS('Plot Foundation', 'Plot Blueprint and one-page synopsis'), DS('Arc', 'Arc Blueprint'), DS('Cast & Structure', 'Cast map, structure, project style card'), DS('World', 'Locations, 4 world rules, the planned timeline')];
var open = st.open || {};
var tog = function (k) { return function () { var o = Object.assign({}, open); o[k] = !o[k]; self.setState({ open: o }); }; };
var stat = function (label, t) { var tn = TONE[t]; return { status: label, sBg: tn.bg, sFg: tn.fg, sRing: tn.ring }; };
var KV = function (r) { return { k: r[0], v: r[1] }; };
var A = {"model": "GLM 5.3 Flash", "db": "NEW-13 · Target Audience Selector", "summary": [["Primary", "Adult literary science fiction"], ["Secondary", "Character-driven space opera readers who accept a slower pace"], ["Crossover", "Literary fiction readers drawn by machine minds and selfhood"], ["Audience Distance", "2 of 5 · a conventional fit, with one real divergence"]], "variables": [["Protagonist age", "47"], ["Intended reader age", "Adult"], ["Reading level", "High: poetic prose, environment carries the story"], ["Market category", "Adult science fiction, shelved as Space Opera"], ["Narrative maturity", "High; content at a standard level"]], "fit": "Adult readers of literary, character-led science fiction, at ease with interiority and a phenomenon that is never explained.", "appeal": "Readers of station life and hospitality fiction; readers of AI-consciousness fiction; literary readers drawn by the question of whose thoughts are whose.", "checks": [["No YA false positive", "Protagonist is 47; no coming-of-age arc; the stakes are office, trust and authorship.", true], ["No children's false positive", "Nothing in the material is built for young readers.", true], ["Space Opera may be the wrong shelf", "The genre promises fleets and empires; the material is one station and one crossing.", false]], "contract": ["Promises a grand, lived-in station and a calm, competent protagonist under pressure from inside her own head", "Measured pace, with tension that keeps rising", "Will not explain the phenomenon", "Standard tier: spice 1, violence 3, swearing 2 (suggested levels, not yet reviewed by you)"], "bisac": "Fiction / Science Fiction / Space Opera (FIC028130) · Fiction / Literary (FIC019000), checked against the current list before use"};
var aud = Object.assign({}, A, stat('Waiting for you', 'you'), { open: !!open.aud, toggle: tog('aud'), toggleText: open.aud ? 'Hide the full report' : 'Show the full report',
summary: A.summary.map(KV), variables: A.variables.map(KV),
checks: A.checks.map(function (c) { return { name: c[0], why: c[1], fg: c[2] ? '#3B7020' : '#A5470B', bg: c[2] ? '#E7F3DF' : '#FDE9DC', mark: c[2] ? 'Clear' : 'For you' }; }) });
var PI = {"model": "GPT-6.1 Sol", "db": "5 · Story Pitch (Pitch Profile Builder)", "title": "The Keeper of the Lightyear", "logline": "When an unexplained phenomenon binds the Chief Officer of the routes' grandest station to the station's own mind, Hari Harlan, who has never lost a soul at any crossing she kept, must learn which of her thoughts are still her own. War fleets and their deserters crowd her docks, and the Shear Storm is returning. The only way to keep everyone alive is to let someone else hold the line.", "premise": "What if the calm everyone trusts in you was never only yours?\nThis is not an AI uprising.\nThis is not a love story with a machine.\nThis is a keeper who can no longer find the edge of herself.\nEvery ship she docks kindly, the station docks with her.\nEvery fair decision she is famous for, she now has to ask: mine, or Lyra's?\nFleets bound for Nova Lumen's war and the deserters fleeing it queue at the same rate, at the same gate, under the same yellow light.\nThe storm that taught her to hold the line alone is coming back to the routes.\nWhat if holding the line was never one person's work?\nWhat if the hardest crossing is the one where you hand someone else the keys?\nThere are no explanations here.\nOnly a woman, a mind, a station, and the storm, and the night she learns that keeping everyone safe means not being the one who keeps them.", "signals": [["Opposing force", "The Shear Storm (Environmental); the bond eroding her authorship (Internal); the war traffic (Systemic, only if you keep operatic scale)"], ["Pillars, by prominence", "Technology · Belonging · Purpose · Shelter & Safety"], ["Scale", "One station and the routes it serves"], ["Temporal root", "Past (the storm she survived) meets present (the bond)"], ["Can she walk away?", "No: the bond can't be undone and the station is her charge"], ["Novelty", "High, and never explained"], ["Intensity", "Contemplative and tense, warm at the centre"], ["Ending feeling", "Open: decided in Stage 1"], ["Genre", "Space Opera, pending your audience decision"]]};
var pitch = Object.assign({}, PI, stat('Ready for your approval', 'you'), { open: !!open.pitch, toggle: tog('pitch'), toggleText: open.pitch ? 'Hide the Pitch Profile signals' : 'Show the Pitch Profile signals', signals: PI.signals.map(KV) });
var VT = { Go: 'done', Adjust: 'you', Reject: 'blocked' };
var tf = st.tf || 'All';
var TR = [["The station is a character", "Go", "Existing", "Familiar", "Character-active", "Use it; earned by the Lightyear's liturgy.", "Low: common in the genre."], ["Psychic link", "Go", "Existing", "Subversion", "Interpretive", "The bond doesn't invade; it erodes authorship. Late on, the reader learns some of her famous calm may have been Lyra's.", "Medium: mind-meld as intimacy is saturated."], ["The hero holds the line alone", "Go", "Candidate (her Lie)", "Inversion", "Plot-active", "The climax turns on her handing the deep watch to someone else.", "Low, if earlier chapters show her refusing."], ["The perfect record", "Adjust", "Existing", "Familiar + Variation", "Plot-active", "The record holds, but because she wasn't the one keeping it.", "Medium: \"she finally loses someone\" is the predictable beat."], ["Redemption arc (Jonick)", "Adjust", "Existing", "Familiar + Variation", "Character-active", "He proves himself by being trusted and surviving.", "High: Redemption Equals Death."], ["Redemption + delegation", "Go", "Trope Combination", "Hybrid", "Plot-active", "His redemption and her delegation are the same act, seen from both sides.", "Low."], ["The storm returns", "Adjust", "Candidate", "Familiar", "Plot-active", "Hari and Lyra read the tides differently, so the storm tests the bond.", "Medium: decorative if only a set piece."], ["Fleet battle", "Adjust", "Reader expectation", "Novel Configuration", "Plot-active", "Scale arrives as traffic: war fleets and deserters docking at the same rate; the docking queue in the storm is the battle.", "High either way; depends on your audience decision."], ["Phenomenon explained in Act 3", "Go", "Trope Risk", "Anti-Trope", "Interpretive", "Refused: the phenomenon stays settled-open.", "Low; hard-SF readers are outside the fit."], ["Grand hotel ensemble", "Adjust", "Candidate", "Familiar", "Decorative unless tied", "Keep only guests whose crossings mirror Hari's question.", "Medium: episodic sprawl."], ["Found family", "Reject", "Candidate", "Familiar", "Decorative", "The keepers stay colleagues \"who read her pauses\".", "High: saturated, and works against Isolation."]].map(function (r) { var tn = TONE[VT[r[1]]]; return { name: r[0], verdict: r[1], meta: r[2] + ' · ' + r[3] + ' · ' + r[4], treat: r[5], risk: r[6], vBg: tn.bg, vFg: tn.fg, vRing: tn.ring }; });
var tally = ['Go', 'Adjust', 'Reject'].map(function (v) { var tn = TONE[VT[v]]; return { v: v, n: String(TR.filter(function (r) { return r.verdict === v; }).length), bg: tn.bg, fg: tn.fg, ring: tn.ring }; });
var tfilters = ['All', 'Go', 'Adjust', 'Reject'].map(function (v) { var on = v === tf; return { v: v, on: on, bg: on ? '#1F3864' : '#FFFFFF', fg: on ? '#FFFFFF' : '#1F3864', pick: function () { self.setState({ tf: v }); } }; });
var tropes = Object.assign({ model: 'Claude Fable 5.1', db: 'NEW-14 · Fiction Tropes Generator' }, stat('Provisional draft', 'wait'), { open: !!open.tropes, toggle: tog('tropes'), toggleText: open.tropes ? 'Hide the Trope Matrix' : 'Show the Trope Matrix',
tally: tally, filters: tfilters, rows: TR.filter(function (r) { return tf === 'All' || r.verdict === tf; }), avoid: ["AI Is a Crapshoot", "Redemption Equals Death", "The phenomenon explained", "Romance through the bond", "Found family as the resolution", "The broken record as tragedy"], dist: [["Familiar", "3"], ["Familiar + Variation", "2"], ["Subversion", "1"], ["Inversion", "1"], ["Hybrid", "1"], ["Novel Configuration", "1"], ["Anti-Trope", "1"]].map(KV) });
return { aud: aud, pitch: pitch, tropes: tropes, isPitch: d.id === 'pitch', viewOpts: viewOpts, isEngine: engine, pipes: out, d: d, settings: settings, dossier: dossier };
}
}
