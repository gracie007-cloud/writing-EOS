class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, level: 5, fid: 0, overturned: false };
}
renderVals() {
/*VIEW*/
/*TONES*/
var slop = 1;
var fid = st.overturned ? st.fid : 0;
var LV = [
{ n: 1, name: 'Basic grammatical competence', d: 'Grammar, spelling and punctuation are sound.' },
{ n: 2, name: 'Avoiding adverbs', d: 'Strong verbs carry the weight; adverbs are rare.' },
{ n: 3, name: 'Variation', d: 'Sentence lengths and shapes vary with purpose.' },
{ n: 4, name: 'Originality in accuracy', d: 'Familiar ideas are put in fresh, exact ways.' },
{ n: 5, name: 'Truthful to the narrator', d: 'Every line serves the story and the point of view. The target for this chapter.' },
{ n: 6, name: 'Emotional infusion', d: 'Word choice and image carry feeling without naming it.' },
{ n: 7, name: 'Sublime prose', d: 'Rare: the prose itself becomes the experience.' }
];
var paint = function (on, locked) {
return on ? { bg: '#2E75B6', fg: '#FFFFFF', border: '#1F4E79', cursor: 'pointer' } : { bg: locked ? '#F5F7FB' : '#FFFFFF', fg: locked ? '#94A3B8' : '#1B2A41', border: locked ? '#E3E8F0' : '#CBD5E1', cursor: locked ? 'not-allowed' : 'pointer' };
};
var levels = LV.map(function (l) { return Object.assign({ n: l.n, name: l.name, on: st.level === l.n, pick: function () { self.setState({ level: l.n }); } }, paint(st.level === l.n, false)); });
var level = LV.filter(function (l) { return l.n === st.level; })[0];
var fids = [0, 1, 2, 3].map(function (n) {
var locked = !st.overturned && n !== 0;
return Object.assign({ n: n, on: fid === n, disabled: locked, pick: function () { self.setState({ fid: n }); } }, paint(fid === n, locked));
});
var score = Math.max(0, (st.level / 7) * 5 + (fid / 3) * 4 + 1 - 0.5 * slop);
var OK = 'M20 6 9 17l-5-5', BAD = 'M12 8v5 M12 17h.01';
var C = function (t, v, ok) { var tone = ok ? TONE.done : TONE.flag; return { t: t, v: v, icon: ok ? OK : BAD, bg: tone.bg, fg: tone.fg }; };
var checks = [C('Stock phrases', '1 · "the weight of"', false), C('Repeated openings, 3 or more in a row', 'None', true), C('Forbidden names and terms', 'None', true), C('Characters named before their first appearance', 'None', true), C('Complete, not cut off', 'Yes', true)];
var af = st.overturned ? { title: 'Auto-fail overturned by you', bg: '#F5F7FB', ring: '#E3E8F0', fg: '#475569' } : { title: 'Auto-fail · 1', bg: '#FDF4EF', ring: '#F4B183', fg: '#A5470B' };
var CM = function (k, v, ok) { return { k: k, v: v, fg: ok ? '#3B7020' : '#A5470B' }; };
var craft = [CM('Sentence length', '17 words on average · yours 6–22', true), CM('Filter verbs', '7 per 1,000 words · yours at most 4', false), CM('-ly adverbs', '3 per 1,000 words · yours at most 6', true), CM('Dialogue share', '18% · yours 25–40%', false), CM('Voice drift', '0.31 · rewrite pitched above 0.35', true)];
return { craft: craft, 
viewOpts: viewOpts, isEngine: engine, levels: levels, level: level, fids: fids, checks: checks, af: af,
overturnLabel: st.overturned ? 'Restore the flag' : 'Overturn the flag',
fidNote: st.overturned ? '' : 'Locked at 0 by the auto-fail',
toggleOverturn: function () { self.setState({ overturned: !st.overturned, fid: st.overturned ? 0 : st.fid }); },
scoreText: score.toFixed(2)
};
}
}
