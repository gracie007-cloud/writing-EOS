class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, format: 'epub', scope: 'all' };
}
renderVals() {
/*VIEW*/
/*TONES*/
var pills = function (defs, cur, key) {
return defs.map(function (f) { var on = f.id === cur; var o = {}; o[key] = f.id; return { name: f.name, on: on, bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F3864' : '#4B5B73', shadow: on ? '0 1px 3px rgb(16 24 40 / 0.12)' : 'none', pick: function () { self.setState(o); } }; });
};
var FORMATS = [{ id: 'epub', name: 'EPUB', note: 'An e-book file for readers and retailers. Built by the app itself.' }, { id: 'docx', name: 'Word (DOCX)', note: 'For an editor, an agent or a print designer. Styles follow your chapter headings.' }, { id: 'md', name: 'Markdown', note: 'Plain text files, one per chapter. Opens anywhere, including Obsidian.' }];
var SCOPES = [{ id: 'locked', name: 'Locked chapters', note: 'No chapter is locked yet, so this would be empty. Choose the whole book to share drafts.' }, { id: 'all', name: 'Whole book, drafts marked', note: 'Unlocked chapters are included with a “Draft” heading so nobody mistakes them for final text.' }];
var fmt = FORMATS.filter(function (f) { return f.id === st.format; })[0];
var scope = SCOPES.filter(function (f) { return f.id === st.scope; })[0];
var I = function (name, note, ready) { var t = ready ? TONE.done : TONE.wait; return { name: name, note: note, state: ready ? 'Ready' : 'Later', tBg: t.bg, tFg: t.fg, tRing: t.ring }; };
var importers = [I('Markdown folder', 'One file per chapter, or one file split at headings', true), I('Word (DOCX)', 'Split at Heading 1', true), I('Scrivener', 'Planned, one tool at a time', false), I('Novelcrafter', 'Planned', false), I('Sudowrite', 'Planned', false)];
var C = { yours: '#FFC000', draft: '#2E75B6', polish: '#9DC3E6', edited: '#B98A00' };
var key = [{ t: 'Yours', c: C.yours }, { t: 'Agent draft', c: C.draft }, { t: 'Agent polish', c: C.polish }, { t: 'Your edit of agent text', c: C.edited }];
var R = function (name, note, y, d, p, e, engineText, bg) {
return { name: name, note: note, bg: bg || '#FFFFFF', engine: engineText,
parts: [{ w: y + '%', c: C.yours }, { w: d + '%', c: C.draft }, { w: p + '%', c: C.polish }, { w: e + '%', c: C.edited }],
label: y + d + p + e === 0 ? 'No text yet' : 'Yours ' + y + '% · agent draft ' + d + '% · agent polish ' + p + '% · your edit of agent text ' + e + '%' };
};
var rows = [
R('Chapter 1', 'Not locked yet · figures will change', 22, 51, 9, 18, 'provenance/ch01.v3.json · 61 model calls · first_draft, rewrite, prose_refinement'),
R('Chapter 2', 'Outline only', 0, 0, 0, 0, 'no text yet'),
R('Story Bible', 'Locked · brainstorms and workshop ideas you kept', 64, 21, 0, 15, 'bible/ · reserve keepers · workshop extracts'),
R('Whole book so far', 'Drafts so far · nothing locked yet', 22, 51, 9, 18, 'locked chapters: 0 of 24 · figures from working drafts', '#F8FAFC')
];
return {
viewOpts: viewOpts, isEngine: engine, formats: pills(FORMATS, st.format, 'format'), scopes: pills(SCOPES, st.scope, 'scope'),
formatName: fmt.name, formatNote: fmt.note, scopeNote: scope.note, importers: importers, key: key, rows: rows
};
}
}
