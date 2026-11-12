class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, tab: 'chars', sel: 'prot', asof: 1, mx: 'presence' };
}
renderVals() {
/*VIEW*/
/*TONES*/
var OUT = '[FROM THE OUTLINE]';
var AFC = { fg: '#A5470B', ring: '#F4B183', bg: '#FDF4EF' };
var CHK = { fg: '#1F4E79', ring: '#9DC3E6', bg: '#F5F7FB' };
var S = function (k, v) { return { k: k, v: v }; };
var RL = function (text, check, af) { return Object.assign({ text: text, check: check }, af ? AFC : CHK); };
var P = function (field, steps) { return { field: field, steps: steps }; };
var X = function (from, v) { return { from: from, v: v }; };
var AP = function (ch, what, tone) { return { ch: ch, what: what, fg: tone === 'no' ? '#A5470B' : (tone === 'on' ? '#1F4E79' : '#5F6E84') }; };
var cast = [
{ id: 'prot', name: '[Protagonist]', tag: 'Hero · Tier 1', role: 'Point-of-view character', full: '[Protagonist’s full name]', sub: 'Name order from the World Naming System · close third person',
body: '[Two or three sentences: who they are when the story opens, the loss they carry, and how they behave under pressure.]',
strategy: [S('Public goal', '[What they say they want]'), S('Hidden goal', '[What they really want]'), S('Pillar first threatened', '[Pillar] · the point of impact'), S('Pillar History', '[The past event that shaped them]'), S('Information', '[What they know, and don’t know, at the start]'), S('Fear', '[Their deepest fear]')],
rules: [RL('Never says [the gated phrase] before Beat 6 (Truth)', 'Auto-fail · beat-gated', true), RL('No named emotions attached to them in narration', 'Auto-fail', true), RL('Acts only on secrets they know by this chapter', 'Knowledge check')],
aliases: ['[First name]', '[Family name]', '[Title + family name]'], aliasNote: 'Their family name is shared with [Ghost figure]. The longer match wins, then this character as the default; anything still unclear is shown, never guessed.',
appears: [AP('Ch 1', 'Point of view · on the page', 'on'), AP('Ch 2 – 24', 'Planned · ' + OUT)],
prog: [P('Refers to others by', [X(1, '[Title or role]'), X(12, '[First names]')]), P('[The gated phrase]', [X(1, 'Never spoken · auto-fail'), X(24, 'Allowed from Beat 6')]), P('Belief Ring', [X(1, 'Beat 1 · Lie, Want declared'), X(2, 'Beats 2 – 5 · ' + OUT), X(24, 'Beat 6 · Truth')]), P('Knows S4 · the planted clue', [X(1, '◐ partly'), X(2, OUT)])] },
{ id: 'mentor', name: '[Mentor]', tag: 'Mentor · Tier 1', role: 'Already holds the Truth', full: '[Mentor’s full name]', sub: 'Naming convention from the World Naming System',
body: '[Who they are to the protagonist, what they have already lived through, and the one human detail that makes them specific.]',
strategy: [S('Arc mode', 'Flat: already holds the Truth'), S('What they have always known', '[Your final call, pitched from the knowledge map]'), S('Resources', '[What they can do that others can’t]'), S('Information', 'Does not know S3 at the start')],
rules: [RL('Gives the minor character in Chapter 1 their full name', 'Required'), RL('Learns S3 only when the outline reveals it', 'Knowledge check')],
aliases: ['[First name]', '[Title]'], aliasNote: 'A title used by several characters needs the context of the scene; unclear matches are shown, never guessed.',
appears: [AP('Ch 1', 'On the page', 'on'), AP('Ch 2 – 24', 'Planned · ' + OUT)],
prog: [P('Arc', [X(1, 'Flat · already holds the Truth')]), P('Knows S3 · the protagonist’s past', [X(1, '✗ not yet'), X(2, OUT)])] },
{ id: 'antag', name: '[Antagonist]', tag: 'Shadow · Tier 1', role: 'Never gives up the Lie', full: '[Antagonist’s full name]', sub: 'Absent from Chapter 1',
body: '[What they want, why it opposes the protagonist, and the belief they will not surrender.]',
strategy: [S('Mirror Map', '[How they reflect the protagonist]'), S('Representation check', '[Pitched to you if their harm is tied to a real group]'), S('Resources', '[What gives them power]'), S('First appearance', OUT)],
rules: [RL('Not named or hinted at in Chapter 1', 'Auto-fail · Ch 1', true), RL('Stays static through the Reckoning', 'Arc check')],
aliases: ['[Name]', '[Code name]'], aliasNote: 'Each alias is also an auto-fail term in Chapter 1.',
appears: [AP('Ch 1', 'Forbidden · any mention is an auto-fail', 'no'), AP('First appearance', OUT)],
prog: [P('Arc', [X(1, 'Static · Lie retained')]), P('On the page', [X(1, 'Absent'), X(2, OUT)])] },
{ id: 'minor', name: '[Minor character]', tag: 'Tier 3', role: 'Appears in Chapter 1', full: '[Minor character’s full name]', sub: 'Tier 3: identity, function, one human detail, a name',
body: '[One sentence on who they are and the single human detail the reader will remember.]',
strategy: [S('One human detail', '[A specific, physical detail]'), S('Function', '[What they do for the story]')],
rules: [RL('Has one specific human detail on the page', 'Required')],
aliases: ['[Name]', '[Role or number]'], aliasNote: 'A role or number can be an alias, so the index finds them even where no one says their name.',
appears: [AP('Ch 1', 'On the page', 'on')],
prog: [P('The protagonist calls them', [X(1, '[Role or number]'), X(12, '[Their name]')])] },
{ id: 'supA', name: '[Supporting character A]', tag: 'Tier 2', role: 'Herald or Shapeshifter', full: '[Supporting character A]', sub: 'Function from the Cast Function Map',
body: '[Their function in the story and what they want.]', strategy: [S('Function', OUT), S('Entry beat', OUT)],
rules: [RL('Not named in Chapter 1', 'Auto-fail · Ch 1', true)], aliases: ['[Name]'], aliasNote: 'Auto-fail term in Chapter 1.',
appears: [AP('Ch 1', 'Forbidden · auto-fail', 'no'), AP('Entry beat', OUT)], prog: [P('Function', [X(1, OUT)])] },
{ id: 'supB', name: '[Supporting character B]', tag: 'Tier 2', role: 'Ally', full: '[Supporting character B]', sub: 'Function from the Cast Function Map',
body: '[Their function in the story and what they want.]', strategy: [S('Function', OUT), S('Entry beat', OUT)],
rules: [RL('Naming convention kept in formal use', 'Name convention')], aliases: ['[Name]', '[Short form]'], aliasNote: 'Matching ignores accents, so a name written without them is still found.',
appears: [AP('Entry beat', OUT)], prog: [P('Function', [X(1, OUT)])] },
{ id: 'ghost', name: '[Ghost figure]', tag: 'Ghost', role: 'The loss behind the protagonist’s Lie', full: '[Ghost figure]', sub: 'Beat 0 of the protagonist’s arc',
body: '[Who or what the protagonist lost, in one sentence.]', strategy: [S('Arc role', 'Beat 0 · Ghost'), S('On the page', OUT)],
rules: [RL('Never explained in Chapter 1', 'Style check')], aliases: ['[Name]'], aliasNote: 'Shares a family name with the protagonist; only the full form counts for them.',
appears: [AP('Ch 1', 'Only through [an object or memory]')], prog: [P('Arc role', [X(1, 'Beat 0 · Ghost')]), P('On the page', [X(1, 'Never explained'), X(2, OUT)])] }
];
var tabDefs = [
{ id: 'chars', name: 'Characters' }, { id: 'arc', name: 'Arc' }, { id: 'secrets', name: 'Secrets' }, { id: 'rel', name: 'Relationships' },
{ id: 'naming', name: 'Naming' }, { id: 'style', name: 'Style rules' }, { id: 'world', name: 'World rules' }, { id: 'matrix', name: 'Matrix' }, { id: 'reserve', name: 'Creative Reserve' }
];
var tabs = tabsOf(tabDefs, st.tab, 'tab');
var show = {};
tabDefs.forEach(function (t) { show[t.id] = st.tab === t.id; });
var voiceRows = [{ k: 'Sentence length', v: '14 words on average · usually 6–22' }, { k: 'Filter verbs (felt, saw, noticed…)', v: 'at most 4 per 1,000 words' }, { k: '-ly adverbs', v: 'at most 6 per 1,000 words' }, { k: 'Dialogue share', v: '25–40% of words' }, { k: 'Paragraphs', v: '2–5 sentences' }];
var DR = function (name, v) { var over = v > 0.35; return { name: name, v: v.toFixed(2), h: Math.round(v / 0.5 * 100) + '%', c: over ? '#ED7D31' : '#2E75B6', fg: over ? '#A5470B' : '#1F4E79' }; };
var drift = [DR('Ch 1 · draft 1', 0.41), DR('Ch 1 · draft 2', 0.28), DR('Ch 1 · draft 3', 0.19)];
var QS = [{ id: 'fear', name: 'What they fear', q: 'What does this character fear losing most, and who knows it?' }, { id: 'past', name: 'Their past', q: 'What happened the last time this character trusted someone?' }, { id: 'contra', name: 'A contradiction', q: 'What does this character do that goes against what they say they believe?' }];
var qCur = QS.filter(function (q) { return q.id === (st.q || 'fear'); })[0];
var questions = QS.map(function (q) { var on = q.id === qCur.id; return { name: q.name, on: on, bg: on ? '#DEEBF7' : '#FFFFFF', fg: on ? '#1F4E79' : '#1B2A41', border: on ? '#2E75B6' : '#D5DCE6', pick: function () { self.setState({ q: q.id }); } }; });
var READ = {
chars: 'Cast Picks · Character State · Character Notes · Continuity Check (as of chapter)',
arc: 'Arc Beats · Voice and Style Check · Character Notes',
secrets: 'Reveal Plan · Continuity Check · Character Interview (as of chapter)',
rel: 'Character Notes · Character Changes Log (pitches changes)',
naming: 'Character Name Generator · Name Critique · naming code checks · Brainstorm',
style: 'Story Rules → auto-fail lists · Voice and Style Check · every Editor suggestion',
world: 'World Picks · Continuity Check',
matrix: 'Code only: mention index, outline, as-of resolver, Character Changes Log',
reserve: 'Character Selector · Name Generator · Brainstorm (search first) · Notion sync'
};
var people = cast.map(function (p) {
var on = p.id === st.sel;
return Object.assign({}, p, { tierShort: p.tag.split(' · ').pop(), on: on, bg: on ? '#F2F7FD' : '#FFFFFF', border: on ? '#2E75B6' : '#E3E8F0', shadow: on ? '0 0 0 3px rgb(46 117 182 / 0.15)' : 'none', pick: function () { self.setState({ sel: p.id }); } });
});
var cur = cast.filter(function (p) { return p.id === st.sel; })[0] || cast[0];
var c = Object.assign({}, cur, {
aliases: cur.aliases.map(function (a) { return { t: a }; }),
progNow: cur.prog.map(function (g) {
var past = g.steps.filter(function (x) { return x.from <= st.asof; });
var later = g.steps.filter(function (x) { return x.from > st.asof; });
return { field: g.field, now: past.length ? past[past.length - 1].v : '—', next: later.length ? 'From Ch ' + later[0].from + ': ' + later[0].v : 'No later change' };
})
});
var asofs = [{ n: 1, name: 'Ch 1' }, { n: 12, name: 'Ch 12' }, { n: 24, name: 'Ch 24' }].map(function (o) {
var on = o.n === st.asof;
return { name: o.name, on: on, bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F3864' : '#4B5B73', pick: function () { self.setState({ asof: o.n }); } };
});
var spine = [
{ k: 'Conflict core', v: '[Conflict core]', note: 'Stage 0 · your final call' },
{ k: 'Structure', v: '[Structure]', note: 'Stage 3 · your final call' },
{ k: 'Outcome', v: '[Outcome]', note: 'Stage 2 · Climax Outcome Matrix' },
{ k: 'Midpoint Pillar shift', v: '[Pillar shift]', note: 'Stakes Ring · in the Arc Blueprint' }
];
var B = function (n, name, when, state) {
var t = state === 'now' ? { bg: '#DEEBF7', ring: '#9DC3E6', numBg: '#2E75B6', numFg: '#FFFFFF', whenFg: '#1F4E79' } : state === 'set' ? { bg: '#FFFFFF', ring: '#E3E8F0', numBg: '#1F3864', numFg: '#FFFFFF', whenFg: '#3B7020' } : { bg: '#FFFFFF', ring: '#E3E8F0', numBg: '#EEF1F5', numFg: '#475569', whenFg: '#5F6E84' };
return Object.assign({ n: n, name: name, when: when }, t);
};
var beats = [B('0', 'Ghost', 'Before the story', 'set'), B('1', 'Lie, Want declared', 'Chapter 1 · now', 'now'), B('2', 'Threat to the Lie', OUT), B('3', 'Want activated', OUT), B('4', 'Need', OUT), B('5', 'Reckoning', OUT), B('6', 'Truth', 'Chapter 24'), B('7', 'New Self', OUT)];
var arcs = [
{ who: '[Protagonist]', mode: 'Hero · Lie → Truth', ghost: '[Ghost figure] · [the loss]', lie: '"[The Lie, in their own words]" · Want declared in Chapter 1', need: '[What they need, but don’t want]', reck: '[The moment the Lie fails]', truth: '[What they come to believe]' },
{ who: '[Mentor]', mode: 'Mentor · flat', ghost: '[Their own past loss]', lie: 'Already holds the Truth', need: '—', reck: '—', truth: 'Shows how to live by it' },
{ who: '[Antagonist]', mode: 'Shadow · static', ghost: OUT, lie: OUT, need: '—', reck: 'Frozen before the story begins', truth: 'Lie retained' }
];
var secrets = [
{ id: 'S1', text: '[A truth about how the world really works]', level: '4 · World', dep: 'S4', reveal: OUT },
{ id: 'S2', text: '[Who the antagonist really is]', level: '3 · Structural', dep: 'S4', reveal: OUT },
{ id: 'S3', text: '[The protagonist’s private past]', level: '1 · Personal', dep: '—', reveal: 'Never explained in Ch 1' },
{ id: 'S4', text: '[A clue planted in Chapter 1]', level: '3 · Structural', dep: '—', reveal: 'Ch 1, in part' }
];
var KN = { '✓': ['Knows', TONE.done], '◐': ['Partly', TONE.you], '✗': ['No', TONE.wait], '?': ['Unknown', TONE.flag] };
var knowRows = [['[Protagonist]', '✗', '✗', '✓', '◐'], ['[Mentor]', '?', '?', '✗', '◐'], ['[Antagonist]', '?', '✓', '?', '✓'], ['Reader', '✗', '✗', '◐', '◐']].map(function (k) {
return { who: k[0], cells: k.slice(1).map(function (s) { var m = KN[s]; return { sym: s, word: m[0], bg: m[1].bg, fg: m[1].fg }; }) };
});
var rels = [
{ pair: '[Protagonist] – [Mentor]', dyn: '[How they talk to each other, in one sentence]', score: '[−5…+5]', trust: '[ ]', gap: '[What one knows that the other doesn’t]' },
{ pair: '[Protagonist] – [Antagonist]', dyn: 'Hero and Shadow; not met in Chapter 1.', score: '[ ]', trust: '[ ]', gap: 'The protagonist doesn’t know they exist.' },
{ pair: '[Mentor] – [Minor character]', dyn: '[Their one exchange in Chapter 1]', score: '—', trust: '—', gap: '—' }
];
var names = [
{ name: '[Protagonist’s full name]', conv: '[Naming culture]', read: '[What the name tells the reader, and how its order works]' },
{ name: '[Mentor’s full name]', conv: '[Naming culture]', read: '[Formal and short forms, and when each is used]' },
{ name: '[Supporting character B]', conv: '[Naming culture]', read: '[Why both parts of the name are kept]' },
{ name: '[Minor character’s full name]', conv: '[Naming culture]', read: '[Shown with its logic, not as texture]' },
{ name: '[In-world term]', conv: 'In-world term', read: '[What it names, and what it replaced]' }
];
var nameRules = [
{ title: 'Collision register', v: 'Main-cast first letters must differ, and no name may sit too close to the pen name on a cover.', check: 'Code · blocks collisions' },
{ title: 'Blocklist', v: 'AI-default and cliché names, e.g. Kael, Elara, Thorne, Seraphina, Nova, Voss, Drake, Lyra, Zara.', check: 'Code · blocks on generate' },
{ title: 'Expectation code · arc channel', v: 'How a character names others can change across the story, as a sign of their arc.', check: 'Style rule · Ch 1–11' }
];
var SR = function (rule, check, gate, tone) { return { rule: rule, check: check, gate: gate, bg: tone.bg, fg: tone.fg, ring: tone.ring }; };
var styleRows = [
SR('[A voice rule from the pen name’s style]', 'Voice and Style Check', 'Always', TONE.run),
SR('Big emotions on the page, never summarized', 'Voice and Style Check', 'Always', TONE.run),
SR('[A naming habit the protagonist keeps until Chapter 12]', 'Auto-fail in Chapters 1–11', 'Ch 1 – 11', TONE.flag),
SR('[The gated phrase]: never said by the protagonist', 'Auto-fail until their Belief Ring reaches Beat 6', 'Until Beat 6', TONE.mature),
SR('No dead air: no name may read as a placeholder', 'Name Critique and naming checks', 'Always', TONE.run)
];
var world = [
{ id: 'Rule 1', name: '[World rule 1]', text: '[What is possible, what it costs, and who controls it, stated precisely enough for a check to enforce.]' },
{ id: 'Rule 2', name: '[World rule 2]', text: '[A rule about how something in the world can be traced or proved.]' },
{ id: 'Rule 3', name: '[World rule 3]', text: '[A rule about who holds power, and what they can’t do.]' },
{ id: 'Rule 4', name: '[World rule 4]', text: '[A rule about how evidence or knowledge can be used.]' }
];
var reserve = [
{ entry: '[Reserved name 1]', type: 'Name', status: 'Reserved', for: 'A minor role', origin: 'From the naming step. Too close to the pen name on a cover, so kept for a supporting part.' },
{ entry: '[Reserved name 2]', type: 'Name', status: 'Reserved', for: 'A minor role', origin: 'From the naming step. Its meaning is heavy-handed for a lead.' },
{ entry: '[Antagonist · option 2]', type: 'Character concept', status: 'Reserved', for: '[ ]', origin: 'From character creation. You proceeded with option 1.' },
{ entry: '[Unused story seed]', type: 'Story seed', status: 'Seed', for: 'Its own storyline', origin: 'From the depth revision.' }
];
var mxModeDefs = [
{ id: 'presence', name: 'Presence', note: 'Where each entry is on the page. Chapter 1 comes from the draft; later chapters show what the outline plans until they are drafted.' },
{ id: 'arc', name: 'Arc beat', note: 'Belief Ring position per chapter, from the outline.' },
{ id: 'know', name: 'Knowledge · protagonist', note: 'What the protagonist knows of each secret, as of each chapter.' },
{ id: 'plan', name: 'Planned vs written', note: 'The outline against the drafts. A mismatch becomes a flag.' }
];
var mxModes = mxModeDefs.map(function (m) {
var on = m.id === st.mx;
return { name: m.name, on: on, bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F3864' : '#4B5B73', pick: function () { self.setState({ mx: m.id }); } };
});
var mxCols = ['Ch 1', 'Ch 2 – 11', 'Ch 12', 'Ch 13 – 23', 'Ch 24'].map(function (t) { return { t: t }; });
var CL = { pov: { bg: '#1F3864', fg: '#FFFFFF' }, on: { bg: '#DEEBF7', fg: '#1F4E79' }, men: { bg: '#F5F7FB', fg: '#1B2A41' }, no: { bg: '#FDE9DC', fg: '#A5470B' }, tbd: { bg: 'transparent', fg: '#5F6E84' }, prov: { bg: '#FFF5D6', fg: '#6B4E00' } };
var cell = function (t, k) { return { t: t, bg: CL[k].bg, fg: CL[k].fg }; };
var plan = function () { return cell('[OUTLINE]', 'tbd'); };
var nd = function () { return cell('Not drafted', 'tbd'); };
var row = function (name, kind, cells) { return { name: name, kind: kind, cells: cells }; };
var mxRows = {
presence: [
row('[Protagonist]', 'Character · Tier 1', [cell('POV', 'pov'), cell('POV', 'pov'), cell('POV', 'pov'), cell('POV', 'pov'), cell('POV', 'pov')]),
row('[Mentor]', 'Character · Tier 1', [cell('On page', 'on'), plan(), plan(), plan(), plan()]),
row('[Antagonist]', 'Character · Tier 1', [cell('Forbidden here', 'no'), plan(), plan(), plan(), plan()]),
row('[Minor character]', 'Character · Tier 3', [cell('On page', 'on'), plan(), plan(), plan(), plan()]),
row('[Supporting character A]', 'Character · Tier 2', [cell('Forbidden here', 'no'), plan(), plan(), plan(), plan()]),
row('[Ghost figure]', 'Character · Ghost', [cell('Mentioned only', 'men'), plan(), plan(), plan(), plan()]),
row('[Main plot thread]', 'Plot thread', [cell('Set up', 'on'), plan(), plan(), plan(), cell('Payoff ' + OUT, 'tbd')]),
row('[The protagonist’s secret]', 'Plot thread · S3', [cell('Shown, not explained', 'men'), plan(), plan(), plan(), plan()])
],
arc: [
row('[Protagonist]', 'Hero · Lie → Truth', [cell('Beat 1 · Lie, Want declared', 'on'), cell('Beats 2 – 5', 'prov'), cell('Beats 2 – 5', 'prov'), cell('Beats 2 – 5', 'prov'), cell('Beat 6 · Truth', 'pov')]),
row('[Mentor]', 'Mentor · flat', [cell('Holds the Truth', 'men'), cell('Holds the Truth', 'men'), cell('Holds the Truth', 'men'), cell('Holds the Truth', 'men'), cell('Holds the Truth', 'men')]),
row('[Antagonist]', 'Shadow · static', [cell('Lie retained', 'no'), cell('Lie retained', 'no'), cell('Lie retained', 'no'), cell('Lie retained', 'no'), cell('Lie retained', 'no')])
],
know: [
row('S1 · how the world works', 'Level 4 · World', [cell('✗ No', 'no'), plan(), plan(), plan(), plan()]),
row('S2 · who the antagonist is', 'Level 3 · Structural', [cell('✗ No', 'no'), plan(), plan(), plan(), plan()]),
row('S3 · their own past', 'Level 1 · Personal', [cell('✓ Knows', 'on'), cell('✓ Knows', 'on'), cell('✓ Knows', 'on'), cell('✓ Knows', 'on'), cell('✓ Knows', 'on')]),
row('S4 · the planted clue', 'Level 3 · Structural', [cell('◐ Partly', 'prov'), plan(), plan(), plan(), plan()])
],
plan: [
row('[Protagonist]', 'Character', [cell('Planned POV · written POV', 'on'), nd(), nd(), nd(), nd()]),
row('[Antagonist]', 'Character', [cell('Planned absent · checked on each draft', 'on'), nd(), nd(), nd(), nd()]),
row('S4 reveal', 'Secret', [cell('Planned in part · checked on each draft', 'on'), nd(), nd(), nd(), nd()])
]
};
var mxDef = mxModeDefs.filter(function (m) { return m.id === st.mx; })[0];
var mx = { note: mxDef.note, rows: mxRows[st.mx] };
var FL = function (text, tag, tone) { return { text: text, tag: tag, bg: tone.bg, fg: tone.fg, ring: tone.ring }; };
var mxFlagRows = [
FL('[Antagonist] and [Supporting character A]: any mention in Chapter 1 is a forbidden appearance', 'Auto-fail · Ch 1', TONE.flag),
FL('A Tier 1 character absent for more than [N] chapters (set in project settings)', 'Gap rule', TONE.run),
FL('S4 clue set up in Chapter 1 · payoff ' + OUT, 'Setup · payoff', TONE.run),
FL('Unregistered names in a draft: sorted by the Name Sorter, then pitched to you', 'Mention index', TONE.run)
];
var ELEMENTS = [{"n": "1", "title": "Title and Logline", "holds": "Working title and the one-sentence logline", "status": "Settled", "t": "done", "note": "", "by": "Story Setup, Story Pitch, Premise Adapter", "byEng": "2 · 5 · 3.5"}, {"n": "2", "title": "Synopsis", "holds": "Plot, key characters, central conflict and the book's themes", "status": "Settled", "t": "done", "note": "", "by": "Synopsis, Story Pitch, Conflict Scoring", "byEng": "11 · 5 · 6"}, {"n": "3", "title": "Characters", "holds": "Main characters in full, supporting characters in brief, their arcs", "status": "Settled · grows with the plot", "t": "done", "note": "", "by": "Cast Roles, Character Pool Match, Role Requirements, New Character and 15 more", "byEng": "3.6 · 6.5 · CD-02 · 6.6 · CD-03a · CD-03b · CD-04 · CD-05 · 6.61 · 16 · CD-08 · CD-08a · CD-09 · CD-10 · CD-11 · 13 · 13.1 · 13.3 · 13.4"}, {"n": "4", "title": "Setting and World-Building", "holds": "Geography, cultures, history, technology and magic", "status": "Approach awaiting you", "t": "you", "note": "Worldbuilding proposes Components for this book.", "by": "Worldbuilding, Naming Rules, World Elements, Locations and 2 more", "byEng": "10 · 10.1 · 10.2 · 10.3 · 10.4 · 10.5"}, {"n": "5", "title": "Plot and Structure", "holds": "Outline, turning points, subplots", "status": "Settled · outline grows", "t": "done", "note": "", "by": "Plot Blueprint, Point of Impact, Antagonist Role, Originality Check and 3 more", "byEng": "8 · 8.1 · 8.2 · 18.5 · 14 · 20 · 20.2"}, {"n": "6", "title": "Themes and Symbolism", "holds": "Canon themes, motifs, symbols and imagery", "status": "Settled", "t": "done", "note": "", "by": "Story Pitch, Character Arc, Supporting Arcs, Style Card", "byEng": "5 · 13 · 13.3 · 15"}, {"n": "7", "title": "Dialogue and Voice", "holds": "How each character speaks; the narrative voice; key lines", "status": "Settled · key lines grow", "t": "done", "note": "", "by": "Character Voice Guide, Style Card, Point of View and Reader, Pen Name and Style", "byEng": "CD-10 · 15 · NEW-02 · 3"}, {"n": "8", "title": "Visual References", "holds": "Mood, palette and character designs", "status": "In progress", "t": "run", "note": "", "by": "Character Profile, Worldbuilding, Style Card", "byEng": "CD-08 · 10 · 15"}, {"n": "9", "title": "Timeline", "holds": "Events in order, and each main character's own timeline", "status": "In progress", "t": "run", "note": "", "by": "Story Timeline, Character Arc, Arc Beats", "byEng": "NEW-04 · 13 · 20.1"}, {"n": "10", "title": "Research and References", "holds": "Notes from your own sources; the book's influences (yours only)", "status": "Settled", "t": "done", "note": "", "by": "Fact Base, Reference Check", "byEng": "NEW-03 · 18.6"}, {"n": "11", "title": "Glossary", "holds": "The book's own terms, names and concepts", "status": "Grows with the drafts", "t": "run", "note": "", "by": "Naming Rules, World Elements, Story Rules", "byEng": "10.1 · 10.2 · 19.2"}, {"n": "12", "title": "Appendices", "holds": "Maps, family trees, important objects", "status": "Grows with the drafts", "t": "run", "note": "", "by": "Story Bible Builder, Creative Reserve", "byEng": "19 · PROP-03"}].map(function (e) { var tn = TONE[e.t]; return Object.assign({}, e, { tBg: tn.bg, tFg: tn.fg, tRing: tn.ring, hasNote: !!e.note }); });
var APPROACHES = [{ n: 'Components', why: 'A world of working parts: technology and magic, mechanics, creatures, travel', on: true }, { n: 'G.R.A.P.E.S.', why: 'A whole civilisation: geography, religion, achievements, politics, economics, society', on: false }, { n: 'M.E.R.P.S.', why: 'Power at the scale of states: military, economy, religion, politics, society', on: false }].map(function (a) { return Object.assign({}, a, { bg: a.on ? '#EAF2FB' : '#F8FAFC', ring: a.on ? '#2E75B6' : '#E3E8F0', tag: a.on ? 'Proposed' : '' }); });
return { voiceRows: voiceRows, drift: drift, driftLabel: 'Voice drift: ' + drift.map(function (b) { return b.name + ' ' + b.v; }).join(', ') + '; rewrite pitched above 0.35', questions: questions, question: qCur.q, 
elements: ELEMENTS, approaches: APPROACHES, viewOpts: viewOpts, isEngine: engine, readBy: READ[st.tab],
tabs: tabs, show: show, people: people, c: c, asofs: asofs, asofLabel: st.asof,
spine: spine, beats: beats, arcs: arcs, secrets: secrets, knowRows: knowRows, rels: rels,
names: names, nameRules: nameRules, styleRows: styleRows, world: world, reserve: reserve,
mxModes: mxModes, mxCols: mxCols, mx: mx, mxFlagRows: mxFlagRows
};
}
}
