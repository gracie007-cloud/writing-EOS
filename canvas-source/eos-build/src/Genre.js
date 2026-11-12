class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, pack: 'romsus', filter: 'all', tab: 'promises' };
}
renderVals() {
/*VIEW*/
/*TONES*/
var CH = 24;
var B = function (pct, name) { return { pct: pct, name: name }; };
var T = function (name, kind, note) { return { name: name, kind: kind, note: note }; };
var PR = function (text, when, status) { return { text: text, when: when, status: status || '' }; };
var DEF = [
{ id: 'romsus', name: 'Romantic suspense', kind: 'Main pack · in this project', use: 'main', group: 'starter', status: 'Approved · 12 Oct 2026',
blurb: 'Two leads fall in love while a real threat closes in. The romance and the danger rise and resolve together.',
norms: [['Chapter length', '2,500–4,000 words'], ['Scene length', '1,000–2,000 words'], ['Point of view', 'Both leads, close third'], ['Tense', 'Past'], ['Intimate scenes', 'On the page, mature tier'], ['Rhythm', 'Danger and closeness alternate']],
promises: [PR('Real danger early, and it keeps escalating', 'first tenth', 'Planned · Ch 2'), PR('The danger forces the leads together', 'first quarter', 'Planned · Ch 4'), PR('The leads earn trust through what they do, not what they say', 'throughout', 'Planned · Ch 9, 14'), PR('The mystery and the romance resolve in the same climax', 'final tenth', 'Missing'), PR('A happy ending, or one clearly on its way', 'last chapter', 'Planned · Ch 24')],
tropes: [T('Forced proximity', 'Expected', 'Tie it to the threat, never to coincidence.'), T('Protector hero', 'Expected', 'Let the protected lead save the day at least once.'), T('Enemies to lovers', 'Optional', 'Works when the distrust has a reason the reader shares.'), T('Walking into danger alone', 'Worn out', 'Give every risky choice a reason readers accept.'), T('The ex is the villain', 'Worn out', 'Readers guess it early; needs a twist you approve.')],
beats: [B(3, 'Meet under threat'), B(12, 'The danger escalates'), B(25, 'Forced together'), B(38, 'Closeness interrupted by danger'), B(50, 'Midpoint: trust or betrayal'), B(75, 'The relationship breaks'), B(85, 'The threat revealed'), B(92, 'Joint climax'), B(98, 'Together')],
cliches: ['her heart skipped a beat', 'a shiver of awareness', 'danger was his middle name', 'released a breath she didn’t know she was holding', 'every nerve ending'] },
{ id: 'psych', name: 'Psychological thriller', kind: 'Blended in · for the threat', use: 'blend', group: 'starter', status: 'Approved · 12 Oct 2026',
blurb: 'Dread from the inside: a mind the reader can’t fully trust, and a turn that is fair when you look back.',
norms: [['Chapter length', '1,500–3,000 words'], ['Scene length', '600–1,500 words'], ['Point of view', 'One narrator, close'], ['Tense', 'Past or present'], ['Intimate scenes', 'Brief, off the page'], ['Rhythm', 'Short chapters, a hook at every end']],
promises: [PR('A twist that is fair when you reread', 'last fifth', 'Planned · Ch 21'), PR('Dread that rises chapter by chapter', 'throughout', 'Planned · Ch 3–20'), PR('The narrator’s view is not the whole truth', 'from the first act', 'Delivered · Ch 1')],
tropes: [T('Unreliable narrator', 'Expected', 'Plant the tells on the page, not in the reveal.'), T('Memory loss', 'Worn out', 'Only with a cause the story has earned.'), T('The perfect neighbour', 'Optional', 'Strong if the warmth is real at first.')],
beats: [B(5, 'Something is wrong'), B(25, 'Point of no return'), B(50, 'The first turn'), B(80, 'Everything collapses'), B(90, 'The real turn'), B(100, 'Aftershock')],
cliches: ['something felt off', 'I should have known', 'the silence was deafening'] },
{ id: 'cozy', name: 'Cozy mystery', kind: 'Starter pack', use: '', group: 'starter', status: 'Starter · ready to use',
blurb: 'An amateur sleuth, a close community and a fair puzzle. Violence stays off the page.',
norms: [['Chapter length', '2,000–3,500 words'], ['Scene length', '800–1,500 words'], ['Point of view', 'The sleuth, first or close third'], ['Tense', 'Past'], ['Intimate scenes', 'Off the page'], ['Rhythm', 'A clue or a setback every chapter']],
promises: [PR('Every key clue appears before the reveal', 'final sixth'), PR('A community readers want to return to', 'throughout'), PR('The body arrives early', 'first tenth'), PR('Order restored at the end', 'last chapter')],
tropes: [T('Sleuth with a day job', 'Expected', 'Give the job a skill that cracks the case.'), T('Bumbling police officer', 'Worn out', 'Make them competent and at odds for a reason.'), T('Confession at a gathering', 'Optional', 'Common; vary the setting.')],
beats: [B(8, 'The body is found'), B(15, 'The sleuth commits'), B(30, 'A false lead'), B(50, 'Midpoint twist'), B(65, 'A second threat'), B(80, 'Sleuth in danger'), B(90, 'The reveal'), B(97, 'Order restored')],
cliches: ['the plot thickens', 'little did she know', 'a chill ran down her spine'] },
{ id: 'epic', name: 'Epic fantasy', kind: 'Starter pack', use: '', group: 'starter', status: 'Starter · ready to use',
blurb: 'A world with rules that cost something, a threat that grows to world scale, and companions who become family.',
norms: [['Chapter length', '3,000–6,000 words'], ['Scene length', '1,500–3,000 words'], ['Point of view', 'Several, close third'], ['Tense', 'Past'], ['Intimate scenes', 'Varies by pen name'], ['Rhythm', 'Slow build, rising set pieces']],
promises: [PR('Magic with a price, used cleverly at the climax', 'final tenth'), PR('The threat grows from local to world-scale', 'by the midpoint'), PR('Companions who become family', 'throughout')],
tropes: [T('Chosen one', 'Worn out', 'Fresh only if the choosing is questioned.'), T('Magic system with a cost', 'Expected', 'Show the cost before it matters.'), T('Mentor’s fall', 'Optional', 'Earn it; don’t use it to clear the stage.')],
beats: [B(5, 'The ordinary world cracks'), B(20, 'Leaving home'), B(50, 'The truth about the threat'), B(75, 'All is lost'), B(90, 'The final stand'), B(100, 'The new world')],
cliches: ['ancient evil stirred', 'the prophecy foretold', 'a shadow fell across the land'] },
{ id: 'space', name: 'Space opera', kind: 'Starter pack', use: '', group: 'starter', status: 'Starter · ready to use',
blurb: 'Big stakes across worlds, a crew with loyalties under strain, and technology that shapes society.',
norms: [['Chapter length', '3,000–5,000 words'], ['Scene length', '1,200–2,500 words'], ['Point of view', 'Two to four, close third'], ['Tense', 'Past'], ['Intimate scenes', 'Varies by pen name'], ['Rhythm', 'Action set pieces between politics']],
promises: [PR('Scale: the fate of more than one world', 'by the midpoint'), PR('A crew whose loyalty is tested', 'throughout'), PR('Technology with social consequences', 'first act')],
tropes: [T('Ragtag crew', 'Expected', 'Give each member a reason to leave.'), T('Evil empire', 'Worn out', 'Show why ordinary people support it.'), T('Ancient alien tech', 'Optional', 'Tie it to the theme, not just the plot.')],
beats: [B(5, 'The call'), B(25, 'Jump to the wider war'), B(50, 'The cost of winning'), B(75, 'Betrayal'), B(92, 'Fleet battle'), B(100, 'A changed galaxy')],
cliches: ['space, the final frontier', 'the stars stretched into lines', 'the ship groaned'] },
{ id: 'mine', name: '[Your pack]', kind: 'Yours · draft from the Genre Analyst', use: '', group: 'yours', status: 'Draft · pitched to you',
blurb: 'Built from your notes on comparable books. Nothing in it is used until you approve it.',
norms: [['Chapter length', '[from your notes]'], ['Scene length', '[from your notes]'], ['Point of view', '[from your notes]'], ['Tense', '[from your notes]'], ['Intimate scenes', '[from your notes]'], ['Rhythm', '[from your notes]']],
promises: [PR('[Promise drafted from your notes]', '[where]'), PR('[Promise drafted from your notes]', '[where]')],
tropes: [T('[Trope]', 'Optional', '[Freshness note, citing the note it came from]')],
beats: [B(10, '[Beat]'), B(50, '[Beat]'), B(90, '[Beat]')],
cliches: ['[phrase from your notes]'] }
];
var byId = {};
DEF.forEach(function (p) { byId[p.id] = p; });
var cur = byId[st.pack] || DEF[0];
var FIL = [{ id: 'all', name: 'All' }, { id: 'project', name: 'In this project' }, { id: 'starter', name: 'Starter' }, { id: 'yours', name: 'Yours' }];
var keep = function (p) { return st.filter === 'all' || (st.filter === 'project' ? !!p.use : p.group === st.filter); };
var shown = DEF.filter(keep);
var filters = FIL.map(function (f) {
var on = f.id === st.filter;
return { name: f.name, on: on, bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F3864' : '#4B5B73', shadow: on ? '0 1px 3px rgb(16 24 40 / 0.12)' : 'none', pick: function () { self.setState({ filter: f.id }); } };
});
var badgeOf = function (p) {
if (p.use === 'main') return ['Main pack', TONE.done];
if (p.use === 'blend') return ['Blended in', TONE.run];
if (p.group === 'yours') return ['Draft', TONE.you];
return ['Starter', TONE.wait];
};
var packs = shown.map(function (p) {
var on = p.id === cur.id;
var b = badgeOf(p);
return { name: p.name, blurb: p.blurb, status: p.status, badge: b[0], tBg: b[1].bg, tFg: b[1].fg, tRing: b[1].ring, on: on,
bg: on ? '#F2F7FD' : '#FFFFFF', border: on ? '#2E75B6' : '#E3E8F0', shadow: on ? '0 0 0 3px rgb(46 117 182 / 0.15)' : '0 1px 2px rgb(16 24 40 / 0.05)',
pick: function () { self.setState({ pack: p.id }); } };
});
var tabs = tabsOf([{ id: 'promises', name: 'Reader promises' }, { id: 'tropes', name: 'Tropes' }, { id: 'beats', name: 'Structure' }, { id: 'cliches', name: 'Clichés' }], st.tab, 'tab');
var inProject = !!cur.use;
var promises = cur.promises.map(function (r) {
var s = r.status;
var t = !s ? TONE.wait : (s.indexOf('Missing') === 0 ? TONE.flag : (s.indexOf('Delivered') === 0 ? TONE.done : TONE.run));
var miss = s.indexOf('Missing') === 0;
return { text: r.text, when: r.when, status: s, hasStatus: inProject && !!s, tBg: t.bg, tFg: t.fg, tRing: t.ring, rowBg: miss ? '#FFF8F3' : '#FFFFFF', rowRing: miss ? '#F4B183' : '#E3E8F0' };
});
var KIND = { Expected: TONE.done, Optional: TONE.wait, 'Worn out': TONE.flag };
var tropes = cur.tropes.map(function (r) { var t = KIND[r.kind]; return Object.assign({}, r, { tBg: t.bg, tFg: t.fg, tRing: t.ring }); });
var WORDS = 90000;
var beats = cur.beats.map(function (b) { return { pct: b.pct + '%', name: b.name, chapter: 'Ch ' + Math.max(1, Math.round(b.pct * CH / 100)) + ' · about word ' + (Math.round(WORDS * b.pct / 10000) * 100).toLocaleString('en-GB') }; });
var uses = [
{ where: 'Story Blueprint · step 2', name: engine ? 'Conflict Fit Rater' : 'Choosing the conflict', what: 'The Genre factor is scored against the pack.', href: 'Develop.dc.html' },
{ where: 'Story Blueprint · step 4', name: engine ? 'Trope Audit' : 'Checking tropes', what: 'Reads the trope list; worn-out tropes need a twist.', href: 'Develop.dc.html' },
{ where: 'Story Blueprint · step 6', name: engine ? 'Structure Fit Rater' : 'Choosing the structure', what: 'Shows the pack’s structures beside the scores.', href: 'Develop.dc.html' },
{ where: 'Story Blueprint · step 9', name: engine ? 'Outline Audit Scorecard' : 'Checking the outline', what: 'Lists each reader promise with its chapter, or missing.', href: 'Develop.dc.html' },
{ where: 'Chapters · Check the draft', name: engine ? 'Style, Tone and Arc Check' : 'Checking voice, tone and arc', what: 'Gets the promises and voice cues due in that chapter.', href: 'Chapter.dc.html' },
{ where: 'Every draft', name: engine ? 'Auto-fail checks (code)' : 'Automatic checks', what: 'Adds the pack’s clichés to the phrases flagged.', href: 'Chapter.dc.html' }
];
var yaml = ['id: ' + cur.id, 'name: ' + cur.name, 'status: ' + (cur.group === 'yours' ? 'draft' : 'approved'), 'scaled_to_chapters: ' + CH, 'promises:'].concat(cur.promises.map(function (r) { return '  - ' + r.text.toLowerCase().slice(0, 42) + '…'; })).concat(['tropes: ' + cur.tropes.length + ' (expected / optional / worn_out)', 'beats: [' + cur.beats.map(function (b) { return b.pct; }).join(', ') + ']', 'cliches: ' + cur.cliches.length + ' → auto_fail.genre', 'used_by: [conflict_fit_rater, trope_audit,', '  structure_fit_rater, outline_audit_scorecard,', '  style_tone_arc_check, auto_fail]']);
var missing = cur.promises.filter(function (r) { return r.status.indexOf('Missing') === 0; }).length;
return {
viewOpts: viewOpts, isEngine: engine, filters: filters, packs: packs, shownCount: shown.length + (shown.length === 1 ? ' pack' : ' packs'),
sel: { name: cur.name, kind: cur.kind, blurb: cur.blurb, norms: cur.norms.map(function (n) { return { k: n[0], v: n[1] }; }), canUse: !cur.use && cur.group !== 'yours' },
tabs: tabs, isPromises: st.tab === 'promises', isTropes: st.tab === 'tropes', isBeats: st.tab === 'beats', isCliches: st.tab === 'cliches',
promises: promises, tropes: tropes, beats: beats, cliches: cur.cliches, chapterCount: String(CH),
promiseNote: inProject ? (missing ? 'Tracked against your outline and locked chapters. A missing promise is pitched to you on Home before the last third is planned.' : 'Tracked against your outline and locked chapters.') : 'Not in this project. Blend it in to track these promises against your outline.',
uses: uses, yaml: yaml.join('\n'), yamlName: 'library/genres/' + cur.id + '.yaml'
};
}
}
