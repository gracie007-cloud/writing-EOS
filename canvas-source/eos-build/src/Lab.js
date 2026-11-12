class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, tab: 'run1' };
}
renderVals() {
/*VIEW*/
/*TONES*/
var T = {
done: { fg: '#123B4C', chip: '#E3EEF2' },
you: { fg: '#8E3B14', chip: '#F8E9E0' },
blocked: { fg: '#4A3277', chip: '#ECE7F4' }
};
var rows = [
{ step: 'Cast Picks', scoring: 'Extraction · automatic', cands: 'claude_fable_51 gpt_sol gemini4 qwen_38_max glm_53', runs: '15', primary: '[after report]', fallback: '[after report]', state: 'SCORED', t: 'done' },
{ step: 'World Picks', scoring: 'Extraction · automatic', cands: 'gemini4 kimi_k3 deepseek_v4_pro gpt_sol', runs: '12', primary: '[after report]', fallback: '[after report]', state: 'SCORED', t: 'done' },
{ step: 'Scene Plan and Setting Notes', scoring: 'Synthesis · you', cands: 'claude_fable_51 gpt_sol gemini4 qwen_38_max', runs: '12', primary: '—', fallback: '—', state: '12 TO REVIEW', t: 'you' },
{ step: 'Timeline Check', scoring: 'Verdict · auto + confirm', cands: 'gemini4 kimi_k3 glm_53 deepseek_v4_pro gpt_sol', runs: '15', primary: '—', fallback: '—', state: '1 TO CONFIRM', t: 'you' },
{ step: 'First Draft', scoring: 'Prose · checks + you', cands: 'claude_fable_51 gpt_sol gemini4 qwen_38_max glm_53', runs: '15', primary: '—', fallback: '—', state: '15 TO SCORE', t: 'you' },
{ step: 'First Draft · Mature', scoring: 'Prose · dignity + you', cands: 'custom_abliterated baseline_abliterated', runs: '6', primary: '—', fallback: 'n/a', state: 'NO ENDPOINT', t: 'blocked' }
].map(function (r) { return Object.assign({}, r, T[r.t]); });
var dash = '— · —';
var models = [
{ key: 'claude_fable_51', family: 'anthropic', weights: 'proprietary', route: 'Concentrate AI', mature: 'no', price: dash },
{ key: 'gpt_sol', family: 'openai', weights: 'proprietary', route: 'Concentrate AI', mature: 'no', price: dash },
{ key: 'gemini4', family: 'google', weights: 'proprietary', route: 'Concentrate AI', mature: 'no', price: dash },
{ key: 'qwen_38_max', family: 'qwen', weights: 'open', route: 'OpenRouter', mature: 'no', price: dash },
{ key: 'glm_53', family: 'zhipu', weights: 'open', route: 'OpenRouter', mature: 'no', price: dash },
{ key: 'deepseek_v4_pro', family: 'deepseek', weights: 'open', route: 'OpenRouter', mature: 'no', price: dash },
{ key: 'kimi_k3', family: 'moonshot', weights: 'open', route: 'OpenRouter', mature: 'no', price: dash },
{ key: 'custom_abliterated', family: '[base family], abliterated', weights: 'open', route: 'HF endpoint', mature: 'mature_ok', price: '— / hour' },
{ key: 'baseline_abliterated', family: '[base family], abliterated', weights: 'open', route: 'HF endpoint', mature: 'mature_ok', price: '— / hour' }
].map(function (m) { return Object.assign({}, m, { matureFg: m.mature === 'no' ? '#62676E' : '#4A3277' }); });
var PL = {
ext: { pool: 'EXTRACTION', fg: '#123B4C', bg: '#E3EEF2' },
syn: { pool: 'SYNTHESIS', fg: '#2F4A1E', bg: '#E8EFE1' },
prose: { pool: 'PROSE', fg: '#8E3B14', bg: '#F8E9E0' },
ver: { pool: 'VERDICT', fg: '#17191B', bg: '#E6E6E0' }
};
var run2 = [
{ agent: 'Chapter Brief', p: 'syn', scoring: 'You compare its brief with the Ch 1 brief: scenes, lengths, Required and Forbidden carried.', needs: 'An outline extract for Chapter 1' },
{ agent: 'Plot Picks', p: 'ext', scoring: 'Automatic against the answer key: stage, beat and threads.', needs: 'Plot entries in the answer key' },
{ agent: 'Continuity Check', p: 'ver', scoring: 'Automatic: planted contradictions and knowledge breaches caught, minus confirmed false alarms. Drafter family excluded.', needs: 'A seeded draft where a character acts on a secret they don’t know yet' },
{ agent: 'Voice and Style Check', p: 'ver', scoring: 'Automatic: planted voice violations, slider misses and wrong-stage behaviour caught.', needs: 'A seeded draft with planted voice breaks and an arc-stage slip' },
{ agent: 'Rewrite', p: 'prose', scoring: 'Auto checks on the result, then your prose level and fidelity.', needs: 'A flawed draft plus reviewer notes' },
{ agent: 'Polish', p: 'prose', scoring: 'Auto checks, a fact-change scan against the input, then you.', needs: 'A passing draft to refine' },
{ agent: 'Character State', p: 'syn', scoring: 'You compare predicted states with the profile; code flags any trait change.', needs: 'Profiles plus a scene brief under pressure' },
{ agent: 'Character Notes', p: 'syn', scoring: 'You score briefs for precision; code checks knowledge limits and gated rules.', needs: 'Canon packages plus a scene with a planted knowledge trap' },
{ agent: 'Character Changes Log', p: 'ext', scoring: 'Automatic against a key of planted changes, including one planned beat the text did not earn.', needs: 'A locked sample chapter and its change key' },
{ agent: 'Name Sorter', p: 'ext', scoring: 'Automatic: unregistered names sorted against a key (person, place, object, term, not a name).', needs: 'A draft with planted unregistered names and look-alikes' },
{ agent: 'Chapter Summary', p: 'syn', scoring: 'Automatic: new facts listed against the answer key; invented facts cost points.', needs: 'A locked sample chapter and its fact list' }
].map(function (r) { return Object.assign({}, r, PL[r.p]); });
var TESTED = { fg: '#123B4C', bg: '#E3EEF2' }, UNTESTED = { fg: '#8E3B14', bg: '#F8E9E0' }, LATER = { fg: '#4A4F55', bg: '#EEEEE8' };
var pversions = [
Object.assign({ agent: 'First Draft', prompt: 'First draft prompt · original', status: 'TESTED · RUN 01', settings: '0.85 · 6,000 + 4,000' }, TESTED),
Object.assign({ agent: 'Timeline Check · brief', prompt: 'Brief check prompt · original', status: 'TESTED · RUN 01', settings: '0.1 · 1,200 + 4,000' }, TESTED),
Object.assign({ agent: 'Cast Picks', prompt: 'Selector prompt · original', status: 'TESTED · RUN 01', settings: '0.2 · 800 + 4,000' }, TESTED),
Object.assign({ agent: 'Rewrite', prompt: 'Rewrite prompt · edited by you', status: 'UNTESTED · ADVANCED TIER', settings: '[ ] · [ ] + [ ]' }, UNTESTED),
Object.assign({ agent: 'Workshop Chat', prompt: 'Workshop prompt · original', status: 'RUN 03', settings: '[ ] · [ ] + [ ]' }, LATER),
Object.assign({ agent: 'Brainstorm', prompt: 'Brainstorm prompt · original', status: 'RUN 03 · THUMBS AS EVIDENCE', settings: '[ ] · [ ] + [ ]' }, LATER)
];
var tabDefs = [{ id: 'run1', name: engine ? 'Run 01' : 'Opening chapter' }, { id: 'tiers', name: 'Quality tiers' }, { id: 'next', name: 'Next rounds' }, { id: 'prompts', name: 'Prompts' }, { id: 'models', name: 'Models' }, { id: 'decisions', name: 'Decisions' }, { id: 'calib', name: 'Calibration' }];
var tabs2 = tabsOf(tabDefs, st.tab, 'tab');
var show = {};
tabDefs.forEach(function (t) { show[t.id] = st.tab === t.id; });
var STATE = { done: TONE.done, you: TONE.you, blocked: TONE.blocked };
var cap = function (t) { return t.charAt(0) + t.slice(1).toLowerCase(); };
var rows2 = rows.map(function (r) {
var t = STATE[r.t];
return Object.assign({}, r, { stateText: cap(r.state), bg: t.bg, fg: t.fg, ring: t.ring, candList: r.cands.split(' ').map(function (c) { return { t: c }; }) });
});
var models2 = models.map(function (m) {
var verified = m.key === 'glm_53';
var hf = m.route === 'HF endpoint';
return Object.assign({}, m, {
price: verified ? '$0.079 · $4.80 per M' : m.price,
verified: verified ? 'Verified' : (hf ? 'Not connected' : 'Verify ID'),
vBg: verified ? TONE.done.bg : (hf ? TONE.blocked.bg : TONE.wait.bg), vFg: verified ? TONE.done.fg : (hf ? TONE.blocked.fg : TONE.wait.fg), vRing: verified ? TONE.done.ring : (hf ? TONE.blocked.ring : TONE.wait.ring),
matureText: m.mature === 'no' ? 'General tier' : 'Mature tier', matureFg: m.mature === 'no' ? '#5F6E84' : '#5B3A8C'
});
});
var POOLN = { EXTRACTION: 'extraction pool', SYNTHESIS: 'synthesis pool', PROSE: 'prose pool', VERDICT: 'verdict pool' };
var run2b = run2.map(function (r) { return Object.assign({}, r, { poolName: POOLN[r.pool] }); });
var PV = function (v) { var s = v.status; var t = s.indexOf('UNTESTED') === 0 ? TONE.flag : (s.indexOf('TESTED') === 0 ? TONE.done : TONE.wait); return Object.assign({}, v, { statusText: engine ? cap(s).replace('run 01', 'Run 01').replace('run 03', 'Run 03').replace('advanced tier', 'Advanced tier') : cap(s).replace(/^Run 03/, 'Story and editor test').replace(/run 03/, 'story and editor test').replace(/run 01/, 'opening chapter test').replace('advanced tier', 'Advanced tier'), bg: t.bg, fg: t.fg, ring: t.ring }); };
var tierCards = [
{ name: 'Basic', tag: 'Good quality, economical', writers: 'Writers: the cheapest tested model within 15% of the best score.' },
{ name: 'Excellent', tag: 'The best choice for most', writers: 'Writers: the best average, or a cheaper model within 5% of it.', def: true },
{ name: 'Premium', tag: 'Best quality, whatever it costs', writers: 'Writers: the best average score, cost ignored.' },
{ name: 'Advanced', tag: 'Experimental', writers: 'Writers: new or untested models, for pitches and drafts only. Results are marked experimental.' }
].map(function (t) { return Object.assign({ def: false }, t); });
var DS = function (agent, what, section, n, agree, cal, undo, earned) {
var tone = earned === 'Autonomous' ? TONE.you : (earned === 'Delegated' ? TONE.run : TONE.wait);
return { agent: agent, what: what, section: section, count: n ? n + ' of your decisions' : 'No decisions yet', agree: agree || 0, agreeText: agree ? agree + '% agree' : '—', width: (agree || 0) + '%', bar: agree >= 85 ? '#70AD47' : '#94A3B8', cal: cal, undo: undo, earned: 'Earned: ' + earned, bg: tone.bg, fg: tone.fg, ring: tone.ring };
};
var decisions = [
DS('Reserve filing', 'Files unchosen options and seeds', 'Creative Reserve', 58, 97, '3 pts', '2%', 'Autonomous'),
DS('Name Sorter', 'Sorts unregistered names', 'Mentions', 31, 94, '4 pts', '—', 'Delegated'),
DS('Scene Plan and Setting Notes', 'Scene order options, hand-off repairs', 'Plan', 23, 91, '6 pts', '—', 'Delegated'),
DS('Character Name Generator', 'Tier 3 names', 'Characters', 14, 79, '9 pts', '—', 'Supervised'),
DS('Timeline Check', 'Possible false alarms', 'Check the brief', 11, 82, '12 pts', '—', 'Supervised'),
DS('Continuity Check', 'Possible false alarms', 'Check the draft', 0, 0, '—', '—', 'Supervised')
];
return { decisions: decisions, viewOpts: viewOpts, isEngine: engine, tabs: tabs2, show: show, rows: rows2, models: models2, run2: run2b, pversions: pversions.map(PV), tierCards: tierCards };
}
}
