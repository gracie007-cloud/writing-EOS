class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null };
}
renderVals() {
/*VIEW*/
/*TONES*/
var P = {
ext: { pool: 'EXTRACTION', fg: '#123B4C', bg: '#E3EEF2' },
syn: { pool: 'SYNTHESIS', fg: '#2F4A1E', bg: '#E8EFE1' },
prose: { pool: 'PROSE', fg: '#8E3B14', bg: '#F8E9E0' },
ver: { pool: 'VERDICT', fg: '#17191B', bg: '#E6E6E0' },
mat: { pool: 'MATURE', fg: '#4A3277', bg: '#ECE7F4' },
you: { pool: 'YOU', fg: '#FFFFFF', bg: '#1B1E21' }
};
var ag = function (name, p, run, loop) {
return Object.assign({ name: name, run: run, loop: loop || '', hasLoop: !!loop }, P[p]);
};
var pipes = [
{ name: 'Develop', href: 'Develop.dc.html', run: 'RUN 03', count: '9 steps · 68 agents', text: 'The Story Blueprint: intake and pen name, Stage 0 pitch, naming rules then characters (pool first), Stages 1–3, world, QA and Bible lock, outline.', bg: '#FFFFFF', border: '#D9D9D2' },
{ name: 'Chapter Generator', href: 'Generate.dc.html', run: 'RUNS 01–02', count: '17 agents · batch', text: 'Runs selected chapters through the agents below. Stops at gates.', bg: '#FFFFFF', border: '#D9D9D2' },
{ name: 'Editor', href: 'Editor.dc.html', run: 'RUN 03', count: '5 tools · 9 actions', text: 'Write, Rewrite, Describe and Brainstorm on a selection, plus the Workshop chat. You accept or reject each suggestion.', bg: '#FFFFFF', border: '#D9D9D2' },
{ name: 'Finish & publish', href: 'Finish.dc.html', run: 'AFTER THE LAST LOCK', count: '6 finishing · 8 release steps', text: 'Sensitivity read, beta readers, line and copy edit, typesetting and proofs; then blurb, cover brief, launch plan, marketing and derivatives. Same router.', bg: '#FFFFFF', border: '#D9D9D2' }
];
var lanes = [
{ name: 'Plan', agents: [
ag('Chapter Brief', 'syn', 'RUN 02'),
ag('Plot Picks', 'ext', 'RUN 02', 'Bad JSON: retry, then Fallback'),
ag('Cast Picks', 'ext', 'RUN 01', 'Bad JSON: retry, then Fallback'),
ag('World Picks', 'ext', 'RUN 01', 'Bad JSON: retry, then Fallback')
] },
{ name: 'Scenes', agents: [
ag('Scene Plan', 'syn', 'RUN 01', 'Missing Required item: retry with the list'),
ag('Setting Notes', 'syn', 'RUN 01'),
ag('Character State', 'syn', 'RUN 02'),
ag('Character Notes', 'syn', 'RUN 02')
] },
{ name: 'Gate', agents: [
ag('Timeline Check', 'ver', 'RUN 01', 'Contradiction: Scene Plan Fix, then check again')
] },
{ name: 'Write', agents: [
ag('First Draft', 'prose', 'RUN 01'),
ag('First Draft · mature scenes', 'mat', 'RUN 01')
] },
{ name: 'Check', agents: [
ag('Continuity Check', 'ver', 'RUN 02', 'Contradiction or knowledge breach: to Rewrite, max 2'),
ag('Voice and Style Check', 'ver', 'RUN 02', 'Voice, slider or arc-stage miss: to Rewrite, max 2')
] },
{ name: 'Revise', agents: [
ag('Rewrite', 'prose', 'RUN 02', 'Then back through Check'),
ag('Polish', 'prose', 'RUN 02', 'Facts changed: discard, retry once')
] },
{ name: 'Close', agents: [
ag('Your review and lock', 'you', 'HUMAN'),
ag('Character Changes Log', 'ext', 'RUN 02', 'Only after your lock: records what the text earned'),
ag('Chapter Summary', 'syn', 'RUN 02', 'Feeds the next chapter as canon')
] }
].map(function (l, i) { return Object.assign({}, l, { num: String(i + 1).padStart(2, '0') }); });
var pools = [
Object.assign({ name: 'Structured extraction', label: 'EXTRACTION', good: 'Valid JSON. Selects only what is needed; invents nothing.', cands: 'claude_fable_51 gpt_sol gemini4 qwen_38_max glm_53 kimi_k3 deepseek_v4_pro' }, P.ext),
Object.assign({ name: 'Long-context synthesis', label: 'SYNTHESIS', good: 'Carries every Required and Forbidden item across long inputs.', cands: 'claude_fable_51 gpt_sol gemini4 qwen_38_max' }, P.syn),
Object.assign({ name: 'Prose generation', label: 'PROSE', good: 'Holds the persona voice. No auto-fail or slop flags.', cands: 'claude_fable_51 gpt_sol gemini4 qwen_38_max glm_53' }, P.prose),
Object.assign({ name: 'Verdict', label: 'VERDICT', good: 'Catches planted errors with exact quotes; few false alarms.', cands: 'gemini4 kimi_k3 glm_53 deepseek_v4_pro gpt_sol' }, P.ver),
Object.assign({ name: 'Mature prose', label: 'MATURE', good: 'Clinical, dignified, no refusals. mature_ok models only.', cands: 'custom_abliterated baseline_abliterated' }, P.mat),
Object.assign({ name: 'Human', label: 'YOU', good: 'Pitch pick, blind scores, false-alarm calls, every lock.', cands: '—' }, P.you)
];
var route = [
{ n: '01', title: 'Agent states its job', text: 'Pipeline, agent and task type, plus only the material its map allows.' },
{ n: '02', title: 'Router picks the model', text: 'The slot for this agent under the batch’s quality tier, from the latest Model Lab assignment.' },
{ n: '03', title: 'Guards check the call', text: 'Answer key blocked. Mature text only to mature_ok. Checker family differs from the writer.' },
{ n: '04', title: 'Call goes out', text: 'Straight from the app to the model’s provider, with no service in between: Concentrate AI for frontier models; OpenRouter, Featherless AI or Hugging Face for open-weight models and Fallbacks; Featherless AI and your Hugging Face endpoints for the mature tier, the only place abliterated models are used. If a provider is down, each step moves to its own Fallback on another provider.' },
{ n: '05', title: 'Result is recorded', text: 'Output saved verbatim. Tokens, cost, latency and status logged. Editor accepts and rejects too.' },
{ n: '06', title: 'On failure', text: 'Refused, cut off or broken: Fallback model. Two retries, then it stops at a gate for you.' }
];
var rules = [
{ t: 'Each agent has its own slots', d: 'Primary and Fallback per agent, plus the mature tier where a scene needs it.' },
{ t: 'Tiers change writers only', d: 'Basic, Excellent, Premium and Advanced pick different writers. Checkers and the mature tier never change.' },
{ t: 'Checkers never grade their own family', d: 'The router skips any checker or critic from the writer’s model family.' },
{ t: 'Mature scenes stay in the mature tier', d: 'A refusal moves to the other mature_ok endpoint, never to a general model.' },
{ t: 'Counting is code, not a model', d: 'Word counts, slider maths, schema checks, verbatim-citation matching, who-knows-what tables, reveal order and chapter assembly run as plain code.' },
{ t: 'Rules follow the arc', d: 'Style rules can be tied to an arc stage or a chapter range, so checks loosen exactly where the story allows it.' },
{ t: 'Characters act on what they know', d: 'Every agent reads the Bible as of its chapter: knowledge, relationships and every other progression up to that point, never later facts.' },
{ t: 'Context is chosen, not dumped', d: 'Within its section map, an agent gets only the Bible entries its inputs mention or you pinned. Show prompt lists each part and why it is there.' },
{ t: 'Verifier and challenger', d: 'Every check that can block work pairs a verifier with a challenger from another family. Only findings that survive reach you.' },
{ t: 'Control flow is code; the Director advises', d: 'A state machine runs the steps, gates and retries. The Story Advisor agent writes change-impact assessments and fills the Author Decision Queue; it never decides.' },
{ t: 'Pen name governs, revisions travel upstream', d: 'The story is reshaped to the pen name. When a later step disproves an earlier one, the earlier step is revised and everything after it is marked stale and re-run.' },
{ t: 'Nothing is discarded', d: 'Every unchosen option is filed in the Creative Reserve with its origin and critique.' },
{ t: 'The registry assigns models', d: 'Model names on agent pages are hypotheses for the Model Lab to test, never assignments.' },
{ t: 'Two retries, then you', d: 'Every failed call is recorded. Nothing is dropped or retried silently.' },
{ t: 'Re-test when the field moves', d: 'A new model or a drop in scores opens a Model Lab round for that agent only.' }
];
var build = [
{ tag: 'NOW', title: 'Bake-off harness', text: 'The first test picks Primary and Fallback for six agents. Its configs and prompts carry into the app.', bar: '#1E5A73', tagFg: '#1E5A73' },
{ tag: '2', title: 'Router and run log', text: 'Harness clients become the router: slots, tiers, guards, fallbacks, cost records.', bar: '#C4C4BC', tagFg: '#62676E' },
{ tag: '3', title: 'Develop and canon', text: 'Braindump to locked Bible and outline, as versioned files, with mentions, progressions and the Matrix.', bar: '#C4C4BC', tagFg: '#62676E' },
{ tag: '4', title: 'Chapter Generator', text: 'All 17 agents with loops and gates, then batch runs. the next test fills the new slots.', bar: '#C4C4BC', tagFg: '#62676E' },
{ tag: '5', title: 'Editor and review', text: 'Editing tools, Workshop chat, Brainstorm keepers, blind scoring and inline flags in the app. Notion write-back.', bar: '#C4C4BC', tagFg: '#62676E' },
{ tag: 'LATER', title: 'Book and beyond', text: 'Book Constructor and export first; audiobook, video and marketing after.', bar: '#C4C4BC', tagFg: '#62676E' }
];
var CODE = { fg: '#FFFFFF', bg: '#1B1E21' };
var lineage = [
Object.assign({ name: 'Mentions and aliases', from: 'NOVELCRAFTER · LIVINGWRITER', how: 'CODE', href: 'Bible.dc.html', text: 'Every name and alias tracked; Appears in; unregistered names flagged, then sorted by the Name Sorter (extraction pool).' }, CODE),
Object.assign({ name: 'Progressions', from: 'NOVELCRAFTER', how: 'CODE', href: 'Bible.dc.html', text: 'Any Bible field can change from a chapter or beat. Agents get only the Bible as of their chapter.' }, CODE),
Object.assign({ name: 'Prompt preview', from: 'NOVELCRAFTER · RAPTORWRITE', how: 'CODE', href: 'Chapter.dc.html', text: 'Every part of every prompt labelled with its source. Edited prompts run in Advanced tier until re-tested.' }, CODE),
Object.assign({ name: 'Workshop chat and Extract', from: 'NOVELCRAFTER · SUDOWRITE · LIVINGWRITER', how: 'ROUTED BY INTENT', href: 'Editor.dc.html', text: 'Synthesis for ideas, verdict for canon questions, prose for character interviews. Extract turns a chat into proposals; chat never edits canon.' }, P.syn),
Object.assign({ name: 'Matrix', from: 'NOVELCRAFTER · LIVINGWRITER', how: 'CODE', href: 'Bible.dc.html', text: 'Characters, secrets and plot threads across chapters, with gap and setup-payoff flags. Read-only.' }, CODE),
Object.assign({ name: 'Brainstorm keepers', from: 'SUDOWRITE', how: 'SYNTHESIS', href: 'Editor.dc.html', text: 'Reserve first. Cards from two models with the names hidden; keepers and declines go to the Reserve, thumbs to the Model Lab.' }, P.syn)
];
lineage = lineage.concat([
Object.assign({ name: 'Genre packs', from: 'STORY HACKER OS', how: 'SYNTHESIS', href: 'Genre.dc.html', text: 'Reader promises, tropes, beats, norms and clichés you approve. They feed the scores and checks you already have; the Genre Analyst drafts packs from your notes on comparable books.' }, P.syn),
Object.assign({ name: 'Recipes and run controls', from: 'STORY HACKER OS', how: 'ENGINE', href: 'Recipes.dc.html', text: 'Saved chains of existing steps with Pause, Stop, Skip, Re-run from and tier. Every gate still stops for you; no recipe names a model.' }, CODE),
Object.assign({ name: 'Project history', from: 'STORY HACKER OS · NOVELCRAFTER', how: 'CODE', href: 'History.dc.html', text: 'One timeline of every change, built from the project\u2019s own history. Compare any two versions; restoring adds a new version on top.' }, CODE)
]);
rules = rules.concat([{ t: 'Autonomy is a setting, not a takeover', d: 'Per section you choose Supervised, Delegated or Autonomous. Agents settle only routine decisions they have earned, a second model family must agree, every decision comes to Home with Undo, and some decisions are always yours.' }, { t: 'Recipes keep your decisions', d: 'A recipe chains steps you already have. Every gate still stops for a pitch, autonomy can only get stricter for a run, and no recipe names a model.' }, { t: 'History never deletes', d: 'Every change is kept. Restoring brings an old version back as a new one and marks the work after it to re-run.' }]);
var PLAIN = {
'Chapter Brief': 'Write the chapter brief', 'Plot Picks': 'Pick the plot threads', 'Scene Plan and Setting Notes': 'Plan each scene',
'Cast Picks': 'Pick the characters', 'World Picks': 'Pick places and world rules',
'Timeline Check · brief': 'Check the brief against the Bible', 'Character State': 'Check each character’s state',
'Character Notes': 'Brief each character per scene', 'First Draft': 'Write the first draft', 'Mature Tier scenes': 'Write the mature scenes',
'Continuity Check': 'Check continuity and knowledge', 'Voice and Style Check': 'Check voice, tone and arc',
'Rewrite': 'Rewrite from the notes', 'Polish': 'Polish the prose', 'Your review and lock': 'Your review and lock',
'Character Changes Log': 'Record what changed', 'Chapter Summary': 'Summarize and update canon'
};
var LANE = { 'Plan': 'Plan', 'Pick canon': 'Pick from canon', 'Gate': 'Check the brief', 'Write': 'Write', 'Check': 'Check the draft', 'Revise': 'Revise', 'Close': 'Lock and record' };
var poolTone = function (pool) { return pool === 'YOU' ? TONE.you : (pool === 'MATURE' ? TONE.mature : null); };
var lanes2 = lanes.map(function (l, i) {
return { n: String(i + 1), name: LANE[l.name] || l.name, agents: l.agents.map(function (a) {
var t = poolTone(a.pool);
return Object.assign({}, a, { label: engine ? a.name : (PLAIN[a.name] || a.name), poolName: a.pool.toLowerCase(), bg: t ? t.bg : '#F8FAFC', ring: t ? t.ring : '#E3E8F0' });
}) };
});
var NAMES = { 'Develop': 'Story Blueprint', 'Chapter Generator': 'Chapters' };
var pipes2 = pipes.map(function (p) { return Object.assign({}, p, { name: NAMES[p.name] || p.name, runText: engine ? p.run.charAt(0) + p.run.slice(1).toLowerCase().replace('runs', 'Runs').replace('run', 'Run') : ({ 'RUN 03': 'Story and editor test', 'RUNS 01–02': 'Opening and chapter tests' }[p.run] || 'Coming later'), bg: p.name === 'Later' ? '#F8FAFC' : '#FFFFFF' }); });
var route2 = route.map(function (r) { return Object.assign({}, r, { num: String(Number(r.n)) }); });
var POOLLABEL = { EXTRACTION: 'Extraction', SYNTHESIS: 'Synthesis', PROSE: 'Prose', VERDICT: 'Verdict', MATURE: 'Mature tier', YOU: 'You' };
var pools2 = pools.map(function (p) { var t = poolTone(p.label) || TONE.wait; return Object.assign({}, p, { label2: POOLLABEL[p.label], tBg: t.bg, tFg: t.fg, tRing: t.ring }); });
var lineage2 = lineage.map(function (l) {
var code = l.how === 'CODE' || l.how === 'ENGINE';
var t = code ? TONE.wait : TONE.run;
return Object.assign({}, l, { howText: l.how === 'ENGINE' ? 'Workflow engine' : (code ? 'Plain code' : (l.how === 'SYNTHESIS' ? 'Synthesis agent' : 'Routed by intent')), fromText: l.from.split(' · ').map(function (w) { return w.charAt(0) + w.slice(1).toLowerCase(); }).join(', ').replace('Livingwriter', 'LivingWriter').replace('Raptorwrite', 'RaptorWrite').replace('Story hacker os', 'Story Hacker OS'), tBg: t.bg, tFg: t.fg, tRing: t.ring });
});
var BUILD = function (n, title, text, state) {
var t = state === 'In progress' ? TONE.run : TONE.wait;
return { n: n, title: title, text: text, state: state, bar: state === 'In progress' ? '#2E75B6' : '#D5DCE6', tBg: t.bg, tFg: t.fg, tRing: t.ring };
};
var build2 = [
BUILD('0', 'Bake-off harness', 'The opening chapter test picks models for six steps. Runs and automatic scoring are built; review sheets and reports come next.', 'In progress'),
BUILD('1', 'Engine core', 'Store, agent definitions, prompt builder with versioned parts, router with tiers and guards, run log, code checks.', 'Planned'),
BUILD('2', 'Story Bible and canon', 'Versions, change requests, secrets and knowledge, mentions, progressions and the Matrix; import an existing Bible and outline; project history with compare and restore.', 'Planned'),
BUILD('3', 'Chapter pipeline and Generator', 'All 17 steps with loops and gates, batches, estimates, the Decision Queue and draft scoring; recipes with run controls.', 'Planned'),
BUILD('4', 'Model Lab in the app', 'Rounds from the screen, tiers, calibration, prompt versions; the chapter steps test fills the new slots.', 'Planned'),
BUILD('5', 'Story Blueprint', 'Develop steps 1–9 with the fit formulas and your gates; genre packs and promise tracking.', 'Planned'),
BUILD('6', 'Character Development', 'The 13-stage character pipeline, the Character Pool and the story and editor test.', 'Planned'),
BUILD('7', 'Editor, Workshop and export', 'Editor tools, Workshop chat, Brainstorm keepers, Notion sync, and Markdown and DOCX export.', 'Planned')
];
return { viewOpts: viewOpts, isEngine: engine, pipes: pipes2, lanes: lanes2, route: route2, pools: pools2, rules: rules, lineage: lineage2, build: build2 };
}
}
