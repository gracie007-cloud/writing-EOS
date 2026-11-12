class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, tab: 'lines', moves: {} };
}
renderVals() {
/*VIEW*/
/*TONES*/
var LINES = [{ id: 'main', name: 'Main plot' }, { id: 'b', name: 'B-story' }, { id: 'sub', name: 'Subplot · [Ghost figure]' }, { id: 'none', name: 'Unassigned' }];
var K = function (id, ch, sc, title, line, when, place, state) { return { id: id, ch: ch, sc: sc, title: title, line: line, when: when, place: place, state: state }; };
var CARDS = [
K('c1s1', 1, 1, '[Scene 1 · Opening]', 'main', 'Day 1 · 05:40', '[Location A]', 'brief'),
K('c1s2', 1, 2, '[Scene 2] · mature tier', 'main', 'Day 1 · 07:15', '[Location A]', 'brief'),
K('c1s3', 1, 3, '[Scene 3]', 'b', 'Day 1 · 08:00', '[Location B]', 'brief'),
K('c1s4', 1, 4, '[Scene 4 · Coda]', 'none', 'Day 1 · 19:30', '[Location A]', 'brief'),
K('c2s1', 2, 1, '[Ch 2 · Scene 1]', 'main', 'Day 2 · 09:00', '[Location C]', 'outline'),
K('c2s2', 2, 2, '[Ch 2 · Scene 2]', 'sub', 'Day 2 · 22:10', '[Location A]', 'outline'),
K('c3s1', 3, 1, '[Ch 3 · Scene 1]', 'b', 'Day 4 · 18:30', '[Location B]', 'outline'),
K('c3s2', 3, 2, '[Ch 3 · Scene 2]', 'main', 'Day 4 · 21:00', '[Location C]', 'outline'),
K('c4s1', 4, 1, '[Ch 4 · Scene 1]', 'sub', 'Day 5 · 07:30', '[Location A]', 'outline')
];
var STATE = { brief: ['Brief ready', TONE.done], outline: ['Outline only', TONE.wait] };
var lineOf = function (c) { return st.moves[c.id] || c.line; };
var cardVals = function (c) {
var s2 = STATE[c.state];
var moved = !!st.moves[c.id] && st.moves[c.id] !== c.line;
return { title: c.title, where: 'Ch ' + c.ch + ' · Scene ' + c.sc, when: c.when, state: s2[0], tBg: s2[1].bg, tFg: s2[1].fg, tRing: s2[1].ring, moved: moved,
shadow: moved ? '0 0 0 2px #FFC000' : 'inset 0 0 0 1px #E3E8F0',
opts: LINES.map(function (l) { return { id: l.id, name: l.name, on: l.id === lineOf(c) }; }),
move: function (e) { var m = Object.assign({}, st.moves); m[c.id] = e.target.value; self.setState({ moves: m }); } };
};
var columns = LINES.map(function (l) {
var cs = CARDS.filter(function (c) { return lineOf(c) === l.id; });
var none = l.id === 'none';
return { name: l.name, count: cs.length + (cs.length === 1 ? ' scene' : ' scenes'), cards: cs.map(cardVals),
bg: none ? '#FFF8F3' : '#F8FAFC', ring: none ? '#F4B183' : '#E3E8F0', fg: none ? '#A5470B' : '#1B2A41',
hasNote: none && cs.length > 0, note: 'Every scene should serve a plot line; loose scenes are how a middle sags.' };
});
var movedIds = Object.keys(st.moves).filter(function (id) { return CARDS.some(function (c) { return c.id === id && c.line !== st.moves[id]; }); });
var first = CARDS.filter(function (c) { return c.id === movedIds[0]; })[0];
var lineName = function (id) { return LINES.filter(function (l) { return l.id === id; })[0].name; };
var pendingTitle = !first ? '' : (movedIds.length === 1 ? 'Drafted change: move Ch ' + first.ch + ' · Scene ' + first.sc + ' to ' + lineName(st.moves[first.id]) : 'Drafted change: ' + movedIds.length + ' scenes moved between plot lines');
var flags = [
{ kind: 'Act length', text: 'Act 2 is planned 18% over its share of the book', where: 'Beats', tab: 'beats' },
{ kind: 'No plot line', text: (function (n) { return n + (n === 1 ? ' scene has' : ' scenes have') + ' no plot line'; })(CARDS.filter(function (c) { return lineOf(c) === 'none'; }).length), where: 'Plot lines', tab: 'lines' },
{ kind: 'Beat with no scene', text: 'Midpoint: trust or betrayal has no scene yet', where: 'Beats', tab: 'beats' },
{ kind: 'Story time', text: 'Ch 1 · Scene 3: [Location B] cannot be reached by 08:00', where: 'Timeline', tab: 'time' }
].filter(function (f) { return f.text.indexOf('0 scenes') !== 0; }).map(function (f) { return Object.assign({}, f, { go: function () { self.setState({ tab: f.tab }); } }); });
var tabs = tabsOf([{ id: 'lines', name: 'Plot lines' }, { id: 'beats', name: 'Beats and word targets' }, { id: 'time', name: 'Story timeline' }], st.tab, 'tab');
var TOTAL = 90000, CH = 24;
var fmt = function (n) { return n.toLocaleString('en-GB'); };
var actDefs = [{ name: 'Act 1', share: 25, planned: 21800 }, { name: 'Act 2', share: 50, planned: 53100 }, { name: 'Act 3', share: 25, planned: 19600 }];
var acts = actDefs.map(function (a) {
var target = TOTAL * a.share / 100;
var d = Math.round((a.planned - target) / target * 100);
var over = d > 15;
return { name: a.name, planned: fmt(a.planned) + ' words', target: fmt(target), delta: (d > 0 ? '+' : '') + d + '%', fg: over ? '#A5470B' : '#3B7020',
pct: Math.min(100, Math.round(a.planned / target * 100)) + '%', bar: over ? '#ED7D31' : '#70AD47', bg: over ? '#FFF8F3' : '#FFFFFF', ring: over ? '#F4B183' : '#E3E8F0' };
});
var B = function (pct, name, scenes) { return { pct: pct, name: name, scenes: scenes }; };
var beats = [B(3, 'Meet under threat', 2), B(12, 'The danger escalates', 1), B(25, 'Forced together', 1), B(38, 'Closeness interrupted by danger', 2), B(50, 'Midpoint: trust or betrayal', 0), B(75, 'The relationship breaks', 1), B(85, 'The threat revealed', 1), B(92, 'Joint climax', 2), B(98, 'Together', 1)].map(function (b) {
var none = b.scenes === 0;
var t = none ? TONE.flag : TONE.done;
return { pct: b.pct + '%', name: b.name, target: 'about word ' + fmt(Math.round(TOTAL * b.pct / 100 / 100) * 100) + ' · Ch ' + Math.max(1, Math.round(b.pct * CH / 100)),
scenes: none ? 'No scene yet' : b.scenes + (b.scenes === 1 ? ' scene' : ' scenes'), tBg: t.bg, tFg: t.fg, tRing: t.ring, bg: none ? '#FFF8F3' : '#F8FAFC', ring: none ? '#F4B183' : '#E3E8F0' };
});
var dayNames = [];
CARDS.forEach(function (c) { var d = c.when.split(' · ')[0]; if (dayNames.indexOf(d) < 0) dayNames.push(d); });
var days = dayNames.map(function (d) {
return { name: d, items: CARDS.filter(function (c) { return c.when.indexOf(d + ' ·') === 0; }).map(function (c) {
var clash = c.id === 'c1s3';
return { time: c.when.split(' · ')[1], where: 'Ch ' + c.ch + ' · Scene ' + c.sc, title: c.title, place: c.place, hasFlag: clash,
flag: 'Scene 2 ends at [Location A] at 07:15 and the trip takes 90 minutes, so 08:00 is too early.', bg: clash ? '#FFF8F3' : '#F8FAFC', ring: clash ? '#F4B183' : '#E3E8F0' };
}) };
});
return {
viewOpts: viewOpts, isEngine: engine, flags: flags, tabs: tabs, isLines: st.tab === 'lines', isBeats: st.tab === 'beats', isTime: st.tab === 'time',
columns: columns, acts: acts, beats: beats, days: days, targetWords: fmt(TOTAL), chapterCount: String(CH),
hasPending: movedIds.length > 0, pendingTitle: pendingTitle, pendingStale: 'the briefs and checks of the chapters involved, and the Matrix', discard: function () { self.setState({ moves: {} }); }
};
}
}
