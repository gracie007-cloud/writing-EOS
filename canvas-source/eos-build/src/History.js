class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, area: 'all', who: 'all', sel: 'd3' };
}
renderVals() {
/*VIEW*/
/*TONES*/
var E = function (id, day, time, who, area, text, kind, o) { o = o || {}; return { id: id, day: day, time: time, who: who, area: area, text: text, kind: kind, cmp: o.cmp || 'none', engine: o.engine || '' }; };
var DEF = [
E('a1', 'Today', '10:42', 'you', 'chapters', 'Kept the flagged sentence in the Chapter 4 brief: a false alarm', 'answer', { engine: 'decision dq-0412 · proceed · chronology_check_brief · commit 7c1e2a9' }),
E('r1', 'Today', '10:15', 'recipe', 'chapters', 'Plan ahead started on Chapters 4–6', 'recipe', { cmp: 'recipe', engine: 'recipes/plan.yaml v3 · run rcp-0007 · 24 jobs queued' }),
E('d3', 'Today', '09:58', 'agent', 'chapters', 'Chapter 1 · Draft 3 written from your notes', 'version', { cmp: 'draft', engine: 'rewrite · primary · [Primary model] · run 2026-10-18/0139 · commit 4b9d0f1' }),
E('p1', 'Today', '09:30', 'you', 'chapters', 'Restore point: Before the revision pass', 'point', { cmp: 'point', engine: 'history/restore-points.yaml · tag rp-before-revision · commit 2e77c40' }),
E('x1', 'Today', '09:12', 'agent', 'bible', 'Decided for you: six unchosen scene openings filed to the Creative Reserve', 'decided', { engine: 'decision record dr-0388 · reserve filing · checker agreed (other family)' }),
E('br1', 'Yesterday', '20:05', 'recipe', 'chapters', 'Polish a chapter finished on its own branch: Chapter 1 is waiting for you to merge', 'recipe', { cmp: 'branch', engine: 'branch run/polish-0002 · 1 chapter · unmerged · lock check passed' }),
E('b1', 'Yesterday', '18:20', 'you', 'bible', 'Locked the Story Bible', 'version', { cmp: 'lock', engine: 'bible lock · automatic restore point rp-before-lock · commit 91af3c2' }),
E('b2', 'Yesterday', '16:05', 'you', 'bible', 'Approved a change: [Mentor]’s rank changes from Chapter 9', 'version', { cmp: 'bible', engine: 'change request cr-0031 · progression · commit 5d02be8' }),
E('s1', 'Yesterday', '14:40', 'you', 'settings', 'Autonomy for Mentions set to Delegated', 'setting', { cmp: 'setting', engine: 'autonomy.yaml · mentions: supervised → delegated · commit c3e19aa' }),
E('m1', 'Yesterday', '11:02', 'you', 'lab', 'Opening chapter test: all 15 drafts scored', 'answer', { engine: 'Run 01 · scores_first_draft.json · blind map opened after scoring' }),
E('g1', '16 Oct 2026', '17:30', 'you', 'story', 'Genre pack approved: Romantic suspense, with Psychological thriller blended in', 'version', { cmp: 'pack', engine: 'project.yaml genre_pack: romsus@2 + psych@1 · commit 0aa4e57' }),
E('o1', '16 Oct 2026', '12:10', 'you', 'story', 'Outline approved: 24 chapters', 'version', { engine: 'outline approved · automatic restore point · commit e8b1d33' })
];
var AREAS = [{ id: 'all', name: 'Everything' }, { id: 'story', name: 'Story' }, { id: 'bible', name: 'Bible' }, { id: 'chapters', name: 'Chapters' }, { id: 'settings', name: 'Settings' }, { id: 'lab', name: 'Model Lab' }];
var WHOS = [{ id: 'all', name: 'Everyone' }, { id: 'you', name: 'You' }, { id: 'agent', name: 'Agents' }, { id: 'recipe', name: 'Recipes' }];
var pills = function (defs, cur, key) {
return defs.map(function (f) { var on = f.id === cur; var o = {}; o[key] = f.id; return { name: f.name, on: on, bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F3864' : '#4B5B73', shadow: on ? '0 1px 3px rgb(16 24 40 / 0.12)' : 'none', pick: function () { self.setState(o); } }; });
};
var WHO = { you: 'By you', agent: 'By an agent', recipe: 'By a recipe' };
var AREA = { story: 'Story', bible: 'Bible', chapters: 'Chapters', settings: 'Settings', lab: 'Model Lab' };
var KIND = { version: ['V', TONE.run], answer: ['✓', TONE.done], recipe: ['R', TONE.navy], point: ['★', TONE.you], decided: ['A', TONE.wait], setting: ['S', TONE.wait] };
var shown = DEF.filter(function (e) { return (st.area === 'all' || e.area === st.area) && (st.who === 'all' || e.who === st.who); });
var dayNames = [];
shown.forEach(function (e) { if (dayNames.indexOf(e.day) < 0) dayNames.push(e.day); });
var days = dayNames.map(function (d) {
return { name: d, items: shown.filter(function (e) { return e.day === d; }).map(function (e) {
var k = KIND[e.kind];
var on = e.id === st.sel;
var point = e.kind === 'point';
return { text: e.text, time: e.time, who: WHO[e.who], area: AREA[e.area], engine: e.engine, mark: k[0], tBg: k[1].bg, tFg: k[1].fg, tRing: k[1].ring, on: on,
bg: point ? '#FFFBEB' : (on ? '#F2F7FD' : '#FFFFFF'), shadow: on ? 'inset 0 0 0 2px #2E75B6' : (point ? 'inset 0 0 0 1px #FFE699' : 'inset 0 0 0 1px #E3E8F0'),
canOpen: e.cmp !== 'none', openLabel: on ? 'Showing' : (point ? 'Compare' : 'Open'), open: function () { self.setState({ sel: e.id }); } };
}) };
});
var seg = function (t, k) {
return { t: t, bg: k === 'del' ? '#FDECEB' : (k === 'ins' ? '#E7F3DF' : 'transparent'), fg: k === 'del' ? '#A8321F' : (k === 'ins' ? '#2F5A1A' : '#1B2A41'), deco: k === 'del' ? 'line-through' : 'none' };
};
var CMP = {
draft: { label: 'Compare · Chapter 1', title: 'Draft 3 against Draft 2', sub: 'Opening of scene 1. Word-level changes; everything else is unchanged.', kind: 'prose',
paras: [[seg('The ferry was late again. She waited at the end of the pier '), seg('with her collar up', 'del'), seg(' '), seg('collar up against the wind', 'ins'), seg(', counting '), seg('the', 'del'), seg(' gulls because counting '), seg('was easier than thinking', 'del'), seg(' '), seg('kept the letter in her pocket quiet', 'ins'), seg('.')],
[seg('Across the water the town '), seg('looked small', 'del'), seg(' '), seg('had shrunk to a row of lit windows', 'ins'), seg(', and somewhere behind one of them [Supporting character A] was '), seg('probably', 'del'), seg(' already '), seg('waiting', 'del'), seg(' '), seg('rehearsing', 'ins'), seg(' the same apology.')]],
stats: '13 words removed · 14 added',
restore: true, restoreTitle: 'Restore Draft 2?', restoreLabel: 'Restore as Draft 4',
restoreWhy: 'Draft 2 comes back as Draft 4, so Draft 3 is kept. Draft 3 fixed both notes you left; restoring undoes those fixes. This work would be marked to re-run:',
stale: ['The checks on this chapter', 'What changed in Chapter 1, and its summary', 'Plans for Chapter 2 that read the summary · [$ estimate] to re-run'],
git: 'git diff 4b9d0f1~1 4b9d0f1 -- chapters/ch01/draft.v3.md\n 1 file changed, 17 insertions(+), 9 deletions(-)\nrun 2026-10-18/0139 · rewrite · [Primary model]' },
bible: { label: 'Compare · Story Bible', title: '[Mentor] · rank', sub: 'A progression: the new value applies from Chapter 9 on. Earlier chapters still read the old one.', kind: 'fields',
fields: [{ k: 'Rank · Chapters 1–8', before: '[Rank A]', after: '[Rank A] (unchanged)' }, { k: 'Rank · from Chapter 9', before: '[Rank A]', after: '[Rank B]' }, { k: 'Appears in', before: '11 chapters', after: '11 chapters' }],
restore: true, restoreTitle: 'Undo this change', restoreLabel: 'Restore the earlier entry',
restoreWhy: 'Canon changes go through a change request. Restoring the earlier entry opens one for you to approve, and marks:', stale: ['Chapters 9–24 plans that read the new rank', 'The Matrix column for [Mentor]'],
git: 'git show 5d02be8 -- bible/characters/mentor.md\ncr-0031 · progression from: ch09' },
setting: { label: 'Compare · Settings', title: 'Autonomy for Mentions', sub: 'Changed by you. Agents now settle routine name sorting and show each one in Decided for you.', kind: 'fields',
fields: [{ k: 'Level', before: 'Supervised', after: 'Delegated' }],
restore: true, restoreTitle: 'Change it back', restoreLabel: 'Set Mentions to Supervised', restoreWhy: 'Nothing needs to re-run. Decisions already settled stay in Decided for you, each with Undo:', stale: ['4 settled since the change'],
git: 'git show c3e19aa -- autonomy/autonomy.yaml' },
point: { label: 'Restore point', title: 'Before the revision pass', sub: 'Named by you today at 09:30. Compare the whole project now with this point, or restore it.', kind: 'note',
lines: ['Since this point: 1 chapter draft, 1 brief answer, 1 recipe run, 6 Reserve filings.', 'The Story Bible and outline have not changed since.'],
restore: true, restoreTitle: 'Restore the whole project to this point?', restoreLabel: 'Restore to this point', restoreWhy: 'Everything since comes back as new versions on top, so nothing is lost. These would be marked to re-run:', stale: ['Chapter 1 checks, summary and record', 'Plans for Chapters 4–6 from the running recipe'],
git: 'git tag rp-before-revision 2e77c40\ngit diff rp-before-revision HEAD --stat' },
recipe: { label: 'Recipe run', title: 'Plan ahead · Chapters 4–6', sub: 'Started by you. Still running: open Recipes for its controls.', kind: 'note',
lines: ['10:15 · Started · estimate [$ estimate]', '10:31 · Chapter 4 brief flagged, pitched to you; Chapters 5 and 6 kept planning', '10:42 · You kept the sentence; Chapter 4 finished planning'],
restore: false, git: 'recipes/runs/rcp-0007.json · controls: [] · 11 of 24 jobs done' },
branch: { label: 'Run branch', title: 'Polish a chapter · Chapter 1', sub: 'Finished yesterday at 20:05 on its own branch. Your manuscript has not changed.', kind: 'note',
lines: ['3 paragraphs changed, 1 locked paragraph untouched.', 'Merge it in the Editor, paragraph by paragraph, or discard it; a discarded branch stays in History.'],
restore: false, git: 'git log main..run/polish-0002 --oneline' },
lock: { label: 'Story Bible', title: 'Locked yesterday at 18:20', sub: 'An automatic restore point was made just before the lock.', kind: 'note',
lines: ['47 entries locked as canon.', 'Changes from now on go through change requests.'],
restore: false, git: 'git tag rp-before-lock 91af3c2' },
pack: { label: 'Compare · Genre pack', title: 'Genre pack for this project', sub: 'Approved by you on 16 Oct 2026.', kind: 'fields',
fields: [{ k: 'Main pack', before: 'None', after: 'Romantic suspense' }, { k: 'Blended in', before: 'None', after: 'Psychological thriller' }],
restore: false, git: 'git show 0aa4e57 -- project.yaml' }
};
var selEntry = DEF.filter(function (e) { return e.id === st.sel; })[0] || DEF[2];
var c = CMP[selEntry.cmp] || CMP.draft;
var cmp = { label: c.label, title: c.title, sub: c.sub, isProse: c.kind === 'prose', isFields: c.kind === 'fields', isNote: c.kind === 'note',
paras: (c.paras || []).map(function (p) { return { segs: p }; }), stats: c.stats || '', fields: c.fields || [], lines: c.lines || [],
canRestore: !!c.restore, restoreTitle: c.restoreTitle || '', restoreLabel: c.restoreLabel || '', restoreWhy: c.restoreWhy || '', stale: c.stale || [], git: c.git };
return { viewOpts: viewOpts, isEngine: engine, areas: pills(AREAS, st.area, 'area'), whos: pills(WHOS, st.who, 'who'), days: days, isEmpty: !shown.length,
shownCount: shown.length + (shown.length === 1 ? ' entry' : ' entries'), cmp: cmp };
}
}
