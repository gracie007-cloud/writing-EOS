class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, run: 'running', recipe: 'plan' };
}
renderVals() {
/*VIEW*/
/*TONES*/
var S = function (name, note, o) { o = o || {}; return { name: name, note: note, stop: !!o.stop, optional: !!o.optional, code: !!o.code, agent: o.agent || '' }; };
var DEF = [
{ id: 'plan', name: 'Plan ahead', kind: 'Starter recipe', badge: 'Running', what: 'Plans the next chapters so drafting never waits. Planning only: no prose is written.', meta: 'Last run today · Chapters 4–6',
facts: [['Steps', '8 per chapter'], ['Stops for you', 'When a brief is flagged'], ['Runs on', 'The next 3 chapters'], ['Estimate', '[$ estimate]']],
steps: [S('Write the chapter brief', 'From the outline entry and the summaries so far', { agent: 'brief_writer' }), S('Pick the plot threads', 'Only threads the outline puts in this chapter', { agent: 'chapter_plot_selector' }), S('Pick the characters', 'From canon, as of this chapter', { agent: 'chapter_character_selector' }), S('Pick places and world rules', 'From canon, as of this chapter', { agent: 'chapter_worldbuilding_selector' }), S('Plan each scene', 'Must-haves and must-nots carried into every scene', { agent: 'chapter_scene_briefs' }), S('Check each character’s state', 'What each character knows and wants here', { agent: 'character_state_examiner' }), S('Brief each character per scene', 'Voice, goal and secret per scene', { agent: 'character_scene_brief' }), S('Check the brief against the Bible', 'A flagged sentence stops this chapter and is pitched to you', { stop: true, agent: 'chronology_check_brief' })],
estimate: 'About 24 agent runs for 3 chapters · [$ estimate] · stops only if a brief is flagged' },
{ id: 'draft', name: 'Draft chapters', kind: 'Built in · the Generate batch', badge: 'Built in', what: 'Takes chapters from plan to a draft ready for your review. The same batch you start on Generate.', meta: 'Last run 16 Oct 2026 · Chapter 1',
facts: [['Steps', '17 per chapter'], ['Stops for you', 'Merge, review and lock'], ['Runs on', 'Chapters you pick'], ['Estimate', '[$ estimate]']],
steps: [S('Plan', '5 steps: brief, threads, characters, places, scenes'), S('Prepare the cast', '2 steps: state and per-scene briefs'), S('Check the brief', 'Stops if a sentence contradicts the Bible', { stop: true }), S('Write', 'First draft; mature scenes in the mature tier'), S('Check the draft', 'Continuity and knowledge; voice, tone and arc'), S('Revise', 'Rewrite from the notes; polish the prose'), S('Merge into the manuscript', 'The batch writes on its own branch; you take its changes paragraph by paragraph', { stop: true }), S('Your review and lock', 'Always yours: nothing is locked without you', { stop: true }), S('Lock and record', 'What changed; summary and canon update')],
estimate: 'About 17 agent runs per chapter · [$ estimate] each · drafting waits for the previous chapter’s lock' },
{ id: 'polish', name: 'Polish a chapter', kind: 'Starter recipe', badge: 'Starter', what: 'A revision pass on a chapter you have read: rewrite from notes, polish, then both checkers again.', meta: 'Not run yet',
facts: [['Steps', '6'], ['Stops for you', 'Your review'], ['Runs on', 'One chapter'], ['Estimate', '[$ estimate]']],
steps: [S('Rewrite from the notes', 'Your notes and the checkers’ findings', { agent: 'rewrite' }), S('Polish the prose', 'Sentence-level only; can be skipped', { optional: true, agent: 'prose_refinement' }), S('Automatic checks', 'Clichés, gated phrases, repeated openings', { code: true }), S('Check continuity and knowledge', 'A different model family from the writer', { agent: 'continuity_knowledge_check' }), S('Check voice, tone and arc', 'Reads your genre pack’s promises for this chapter', { agent: 'style_tone_arc_check' }), S('Merge, paragraph by paragraph', 'Runs on its own branch; lines you locked come back untouched', { stop: true })],
estimate: 'About 5 agent runs · [$ estimate] · stops once, for your review' },
{ id: 'summaries', name: 'Refresh summaries', kind: 'Starter recipe', badge: 'Starter', what: 'After a change upstream, re-summarises only the chapters whose inputs changed.', meta: 'Last run 14 Oct 2026',
facts: [['Steps', '4'], ['Stops for you', 'Any change to canon'], ['Runs on', 'Stale chapters only'], ['Estimate', '[$ estimate]']],
steps: [S('Find chapters with changed inputs', 'From the stale marks', { code: true }), S('Summarise each chapter', 'One summary per stale chapter', { agent: 'summarizer_canon_update' }), S('Compare with the old summary', 'Field by field', { code: true }), S('Your review of canon changes', 'Canon never changes without you', { stop: true })],
estimate: 'One agent run per stale chapter · [$ estimate] · stops if canon would change' },
{ id: 'promise', name: 'Promise check', kind: 'Starter recipe', badge: 'Starter', what: 'Checks every reader promise in your genre pack against the outline and the locked chapters.', meta: 'Last run today',
facts: [['Steps', '4'], ['Stops for you', 'A missing promise'], ['Runs on', 'Outline and locked chapters'], ['Estimate', 'Free: plain code']],
steps: [S('Read your genre pack', 'Main pack and blend', { code: true }), S('Match promises to the outline', 'Planned chapter for each promise', { code: true }), S('Match promises to locked chapters', 'Delivered, with the quote', { code: true }), S('Pitch each missing promise', 'With where it could be paid off', { stop: true })],
estimate: 'No model calls · free · stops for each missing promise' },
{ id: 'bible', name: 'Bible from braindump', kind: 'Starter recipe', badge: 'Starter', what: 'Runs the Story Blueprint from your notes to an approved outline, stopping at every decision that is yours.', meta: 'Last run 12 Oct 2026',
facts: [['Steps', '9'], ['Stops for you', 'Every gate'], ['Runs on', 'A new braindump'], ['Estimate', '[$ estimate]']],
steps: [S('Intake and pen name', 'Pen name and genre pack, then the adapted premise', { stop: true }), S('Pitch selection', 'You pick the conflict from a ranked shortlist', { stop: true }), S('Characters', 'Pool first, then create; every tier 1–2 choice is yours', { stop: true }), S('Plot foundation', 'Trope audit reads your pack', { stop: true }), S('Arc', 'Outcome and arc approval', { stop: true }), S('Cast and structure', 'Structure Fit, with your pack’s preferred structures', { stop: true }), S('World and naming', 'Naming system and elements', { stop: true }), S('Quality check and Bible lock', 'Lock is always yours', { stop: true }), S('Outline', 'Every reader promise placed, or flagged', { stop: true })],
estimate: 'About 60 agent runs · [$ estimate] · stops at all 9 gates' }
];
var byId = {};
DEF.forEach(function (r) { byId[r.id] = r; });
var cur = byId[st.recipe] || DEF[0];
var recipes = DEF.map(function (r) {
var on = r.id === cur.id;
var t = r.badge === 'Running' ? (st.run === 'running' ? TONE.run : (st.run === 'paused' ? TONE.you : TONE.wait)) : (r.badge === 'Built in' ? TONE.navy : TONE.wait);
var badge = r.badge === 'Running' ? ({ running: 'Running', paused: 'Paused', stopped: 'Stopped' }[st.run]) : r.badge;
return { name: r.name, what: r.what, meta: r.meta, badge: badge, tBg: t.bg, tFg: t.fg, tRing: t.ring, on: on,
bg: on ? '#F2F7FD' : '#FFFFFF', border: on ? '#2E75B6' : '#E3E8F0', shadow: on ? '0 0 0 3px rgb(46 117 182 / 0.15)' : '0 1px 2px rgb(16 24 40 / 0.05)',
pick: function () { self.setState({ recipe: r.id }); } };
});
var tag = function (name, t) { return { name: name, bg: t.bg, fg: t.fg, ring: t.ring }; };
var steps = cur.steps.map(function (s, i) {
var tags = [];
if (s.stop) tags.push(tag('Stops for you', TONE.you));
if (s.optional) tags.push(tag('Can be skipped', TONE.wait));
if (s.code) tags.push(tag('Plain code', TONE.wait));
if (engine && s.agent) tags.push(tag(s.agent, TONE.navy));
return { num: String(i + 1), name: s.name, note: s.note, tags: tags,
bg: s.stop ? '#FFFBEB' : '#FFFFFF', ring: s.stop ? '#FFE699' : '#E3E8F0', numBg: s.stop ? '#FFC000' : '#DEEBF7', numFg: s.stop ? '#12244A' : '#1F4E79' };
});
var RS = { running: ['Running', TONE.run, '#2E75B6'], paused: ['Paused', TONE.you, '#FFC000'], stopped: ['Stopped', TONE.wait, '#94A3B8'] }[st.run];
var run = {
state: RS[0], tBg: RS[1].bg, tFg: RS[1].fg, tRing: RS[1].ring, bar: RS[2], done: '11', total: '24', pct: '46%', agentRuns: '11 agent runs, 1 retried',
spent: '[$ spent]', estimate: '[$ estimate]', cap: '[$ cap]',
nowLabel: st.run === 'running' ? 'Now' : (st.run === 'paused' ? 'Paused before' : 'Stopped before'),
now: 'Pick places and world rules · Chapter 5',
canPause: st.run === 'running', canResume: st.run !== 'running', canStop: st.run !== 'stopped', resumeLabel: st.run === 'stopped' ? 'Run the rest' : 'Resume',
footer: st.run === 'stopped' ? 'Stopped. The 11 finished steps are kept; the other 13 are cancelled and can run again later.' : (st.run === 'paused' ? 'Paused after the current call finished. Nothing is lost while it waits.' : 'Pause waits for the current call to finish. Stop keeps everything already done. Every control you use is recorded in History.')
};
var yaml = ['id: ' + cur.id, 'name: ' + cur.name, 'version: 3', 'inputs: { chapters: next_3 }', 'autonomy: { override: stricter_only }', 'cost_cap: project_default', 'steps:'].concat(cur.steps.map(function (s) { return '  - ' + (s.agent || (s.code ? 'code_check' : 'gate')) + (s.stop ? '   # stop point' : '') + (s.optional ? '   # optional' : ''); })).concat(['validated: [steps_exist, inputs_exist,', '  gates_are_stops, no_model_named]']);
return {
viewOpts: viewOpts, isEngine: engine, run: run, recipes: recipes,
sel: { name: cur.name, kind: cur.kind, what: cur.what, facts: cur.facts.map(function (f) { return { k: f[0], v: f[1] }; }), steps: steps, estimate: cur.estimate },
pause: function () { self.setState({ run: 'paused' }); }, resume: function () { self.setState({ run: 'running' }); }, stop: function () { self.setState({ run: 'stopped' }); },
startSel: function () { self.setState({ run: 'running', recipe: 'plan' }); },
yaml: yaml.join('\n'), yamlName: 'recipes/' + cur.id + '.yaml'
};
}
}
