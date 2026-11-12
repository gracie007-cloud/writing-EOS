class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, tier: 'excellent', picked: { 1: true, 2: true, 3: true }, run: 'idle' };
}
renderVals() {
/*VIEW*/
/*TONES*/
var tierDefs = [
{ id: 'basic', name: 'Basic', tag: 'Good quality, economical', writers: 'the cheapest tested model within 15% of the best score for each step.' },
{ id: 'excellent', name: 'Excellent', tag: 'The best choice for most chapters', writers: 'the best average score, or a cheaper model within 5% of it.', rec: true },
{ id: 'premium', name: 'Premium', tag: 'Best quality, whatever it costs', writers: 'the best average score for each step, cost ignored.' },
{ id: 'advanced', name: 'Advanced', tag: 'Experimental', writers: 'new or untested models, for pitches and drafts only. Results are marked experimental.' }
];
var tiers = tierDefs.map(function (t) {
var on = t.id === st.tier;
return Object.assign({}, t, { rec: !!t.rec, on: on, bg: on ? '#F2F7FD' : '#FFFFFF', border: on ? '#2E75B6' : '#E3E8F0', dot: on ? '#2E75B6' : '#94A3B8', dotFill: on ? '#2E75B6' : 'transparent', pick: function () { self.setState({ tier: t.id }); } });
});
var tier = tierDefs.filter(function (t) { return t.id === st.tier; })[0];
var chs = [
{ n: 1, title: '[Chapter 1 title]', state: '7 of 17 · needs you', t: TONE.you, done: 7 },
{ n: 2, title: '[Chapter 2 title]', state: 'Outline only', t: TONE.wait },
{ n: 3, title: '[Chapter 3 title]', state: 'Outline only', t: TONE.wait },
{ n: 4, title: '[Chapter 4 title]', state: 'Outline only', t: TONE.wait },
{ n: 5, title: '[Chapter 5 title]', state: 'Outline only', t: TONE.wait },
{ n: 6, title: '[Chapter 6 title]', state: 'Outline only', t: TONE.wait }
];
var chapters = chs.map(function (c) {
var on = !!st.picked[c.n];
return Object.assign({}, c, {
num: String(c.n).padStart(2, '0'), on: on, bg: on ? '#F2F7FD' : '#FFFFFF', ring: on ? '#9DC3E6' : '#E3E8F0',
tBg: c.t.bg, tFg: c.t.fg, tRing: c.t.ring,
toggle: function () { var p = Object.assign({}, st.picked); p[c.n] = !on; self.setState({ picked: p }); }
});
});
var sel = chs.filter(function (c) { return st.picked[c.n]; });
var total = sel.length * 16;
var already = sel.reduce(function (n, c) { return n + (c.done || 0); }, 0);   // Chapter 1 has 7 steps done, as on Chapters and Home
var done = st.run === 'idle' ? already : Math.min(total, already + 5);
var Q = function (title, state, note, t, gate) { return Object.assign({ title: title, state: state, note: note, isGate: !!gate, rowBg: gate ? '#FFFBEB' : '#FFFFFF' }, t); };
var queue = sel.map(function (c, i) {
var title = 'Chapter ' + c.n + ' · ' + c.title;
if (st.run === 'idle') return Q(title, 'Queued', 'Starts with the brief and the picks.', TONE.wait);
if (i === 0) return Q(title, 'Needs you', 'Stopped at the brief check: 1 possible false alarm to confirm.', TONE.you, true);
if (i === 1) return Q(title, 'Planning', 'Writing the brief. Drafting waits for the chapter before to be locked.', TONE.run);
return Q(title, 'Queued', 'Planning starts when a slot frees up.', TONE.wait);
});
var RUN = { idle: ['Ready', TONE.wait], running: ['Running', TONE.run], paused: ['Paused', TONE.you] };
return {
viewOpts: viewOpts, isEngine: engine,
tiers: tiers, tier: tier, chapters: chapters, queue: queue, empty: sel.length === 0,
selCount: String(sel.length), totalRuns: String(total), doneRuns: String(done),
pct: total ? Math.round(done / total * 100) + '%' : '0%',
runLabel: RUN[st.run][0], runTone: RUN[st.run][1],
showStart: st.run !== 'running', showPause: st.run === 'running',
startLabel: st.run === 'paused' ? 'Resume' : 'Generate ' + sel.length + ' chapter' + (sel.length === 1 ? '' : 's'),
start: function () { self.setState({ run: 'running' }); },
pause: function () { self.setState({ run: 'paused' }); },
reset: function () { self.setState({ run: 'idle' }); },
selectAll: function () { self.setState({ picked: { 1: true, 2: true, 3: true, 4: true, 5: true, 6: true } }); },
selectNone: function () { self.setState({ picked: {} }); }
};
}
}
