class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, levels: { plan: 'auto', mentions: 'del', reserve: 'auto' } };
}
renderVals() {
/*VIEW*/
/*TONES*/
var NAME = { sup: 'Supervised', del: 'Delegated', auto: 'Autonomous' };
var RANK = { sup: 0, del: 1, auto: 2 };
var R = function (id, name, decides, o) {
o = o || {};
return { id: id, name: name, decides: decides, allowAuto: !!o.auto, locked: !!o.locked, earned: o.earned || 'sup', evidence: o.evidence || '' };
};
var groupsDef = [
{ name: 'Story Blueprint', rows: [
R('intake', 'Intake and pen name', 'Agents may settle: premise wording options and repairs to a broken hand-off. The pen name and premise approval stay yours.', { evidence: '6 of 20 decisions recorded' }),
R('pitch', 'Pitch selection', 'Agents may settle: filing the runner-up core and unchosen options to the Reserve. The core pick stays yours.', { evidence: '4 of 20 decisions recorded' }),
R('chars', 'Characters', 'Agents may settle: clarifications and type reflections between stages, Tier 3 names, repairs to a broken hand-off.', { evidence: '14 of 20 decisions recorded' }),
R('world', 'World and naming', 'Agents may settle: minor names that pass every naming check, and duplicate findings.', { evidence: '9 of 20 decisions recorded' }),
R('outline', 'Outline', 'Agents may settle: beat placement options inside a chapter. Approving the outline stays yours.', { evidence: '7 of 20 decisions recorded' })
] },
{ name: 'Chapters', rows: [
R('plan', 'Plan', 'Agents may settle: scene order options, repairs to a broken hand-off. Autonomous applies only to chapters after the next one to be drafted.', { auto: true, earned: 'del', evidence: '23 decisions · 91% agree with you' }),
R('prep', 'Prepare the cast', 'Agents may settle: clarifications between the state and scene-brief steps.', { evidence: '12 of 20 decisions recorded' }),
R('brief', 'Check the brief', 'Agents may settle: whether a flagged sentence is a false alarm, and repeat reports of the same sentence.', { evidence: '11 of 20 decisions recorded' }),
R('draftcheck', 'Check the draft', 'Agents may settle: possible false alarms and duplicate findings. Real problems still go to Rewrite.', { evidence: '0 of 20 decisions recorded' }),
R('lock', 'Lock and record', 'Locking the chapter and every change to canon: always pitched to you.', { locked: true })
] },
{ name: 'Writing tools', rows: [
R('mentions', 'Mentions', 'Agents may settle: adding an unambiguous alias, marking a capitalised word as not a name.', { auto: true, earned: 'del', evidence: '31 decisions · 94% agree with you' }),
R('reserve', 'Creative Reserve filing', 'Agents may settle: filing unchosen options, Brainstorm results and Workshop seeds to the Reserve. Never canon.', { auto: true, earned: 'auto', evidence: '58 decisions · 97% agree · 2% undone' }),
R('workshop', 'Workshop proposals', 'Agents may settle: sending story seeds from a chat to the Reserve. Beats and Bible changes still come to you.', { auto: true, evidence: '5 of 20 decisions recorded' })
] }
];
var counts = { sup: 0, del: 0, auto: 0 };
var yamlLines = ['default: supervised', 'eligibility:', '  confidence: section threshold (calibrated)', '  checker: different family must agree', '  earned: delegated ≥20 · 85% · cal ≤10', '         autonomous ≥50 · 95% · undo <5%', 'breakers: undo 2/10 · contradicted · 25 unseen', 'sections:'];
var groups = groupsDef.map(function (g) {
return { name: g.name, rows: g.rows.map(function (r) {
var lvl = r.locked ? 'sup' : (st.levels[r.id] || 'sup');
counts[lvl] += 1;
yamlLines.push('  ' + r.id + ': ' + (r.locked ? 'always_yours' : NAME[lvl].toLowerCase()));
var opts = ['sup', 'del', 'auto'].map(function (k) {
var on = k === lvl;
var disabled = r.locked ? k !== 'sup' : (k === 'auto' && !r.allowAuto);
return {
name: NAME[k], on: on, disabled: disabled,
tip: disabled ? (r.locked ? 'Your final call' : 'Autonomous is only for work that is not canon') : '',
bg: on ? '#FFFFFF' : 'transparent', fg: disabled ? '#94A3B8' : (on ? '#1F3864' : '#4B5B73'), shadow: on ? '0 1px 3px rgb(16 24 40 / 0.12)' : 'none', cursor: disabled ? 'not-allowed' : 'pointer',
pick: function () { if (disabled) return; var l = Object.assign({}, st.levels); l[r.id] = k; self.setState({ levels: l }); }
};
});
return Object.assign({}, r, { opts: opts, hasWarn: !r.locked && RANK[lvl] > RANK[r.earned], earned: r.locked ? '—' : NAME[r.earned], earnedFg: r.earned === 'sup' ? '#5F6E84' : '#3B7020' });
}) };
});
var levelCards = [
{ name: 'Supervised', count: counts.sup + (counts.sup === 1 ? ' section' : ' sections'), countFg: '#475569', bg: '#FFFFFF', ring: '#E3E8F0', what: 'Agents pitch every decision; you make the final call.', when: 'The default. Every answer you give teaches the Model Lab what you would choose.' },
{ name: 'Delegated', count: counts.del + (counts.del === 1 ? ' section' : ' sections'), countFg: '#1F4E79', bg: '#F2F7FD', ring: '#C9DDF1', what: 'Agents settle the routine calls they are sure of and show you each one; everything else is pitched to you.', when: 'Each one lands in Decided for you on Home, with Undo.' },
{ name: 'Autonomous', count: counts.auto + (counts.auto === 1 ? ' section' : ' sections'), countFg: '#6B4E00', bg: '#FFFBEB', ring: '#FFE699', what: 'Routine calls never wait: unsure ones go ahead as provisional and are pitched to you for review.', when: 'Only for work that is not canon and is cheap to redo.' }
];
return { viewOpts: viewOpts, isEngine: engine, levelCards: levelCards, groups: groups, yaml: yamlLines.join('\n') };
}
}
