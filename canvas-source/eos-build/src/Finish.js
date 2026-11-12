class Component extends DCLogic {
constructor(props) {
super(props);
this.state = { view: null, stage: 'writing', route: 'self' };
}
renderVals() {
/*VIEW*/
/*TONES*/
var FIN = [{"step": "NEW-12", "name": "Sensitivity Read", "does": "A careful read of the locked book for harm tied to identity, culture, belief or condition. Findings come to you with the passage and a suggestion; you decide.", "who": "Agent", "runs": "sequence", "gate": "", "engine": "NEW-12 · Sensitivity / Authenticity Reading · verdict · swarm full · Jev settles · candidates Muse Wonder / None genuinely comparable — least-gap: MiMo-V2.6-Pro (not parity)"}, {"step": "NEW-06", "name": "Beta Readers", "does": "Tracks your human readers: who has which version, their notes, and which notes became changes. No model writes in a reader’s name.", "who": "You and readers", "runs": "sequence", "gate": "", "engine": "NEW-06 · Beta / Alpha Reader Management · synthesis · swarm light · Jev advises · candidates Gemini 4 Argon / None genuinely comparable — least-gap: MiMo-V2.6-Pro (not parity)"}, {"step": "NEW-05a", "name": "Line and Copy Edit", "does": "Line and copy edits on the locked book, shown paragraph by paragraph. Your locked lines never change.", "who": "Agent", "runs": "sequence", "gate": "", "engine": "NEW-05a · Line & Copy Correction Pass (execution) · prose · swarm light · Jev advises · candidates Claude Fable 5.1 / Kimi K3"}, {"step": "PROP-01", "name": "Assemble and Export", "does": "Puts the locked chapters together and exports EPUB, Word or Markdown, including to Obsidian.", "who": "Code", "runs": "sequence", "gate": "", "engine": "PROP-01 · Chapter Assembly & Obsidian Export · code · swarm none · Jev none"}, {"step": "NEW-07", "name": "Typesetting", "does": "Formats the book for retail: trim size, fonts, front and back matter, and the ISBN you supply.", "who": "Code", "runs": "sequence", "gate": "", "engine": "NEW-07 · Retail Formatting / Typesetting / ISBN / Front-&-Back Matter · code · swarm none · Jev none"}, {"step": "NEW-05b", "name": "Proofread", "does": "Proofreading on the typeset pages. You sign off the proof before anything is published.", "who": "Agent", "runs": "sequence", "gate": "Author signs off the proof", "engine": "NEW-05b · Proof Correction Pass (on typeset pages) · prose · swarm light · Jev advises · candidates Claude Fable 5.1 / Kimi K3"}];
var REL = [{"step": "40", "name": "Blurb", "does": "The back-cover and retailer description, in the pen name’s voice.", "who": "Agent", "runs": "sequence", "gate": "", "engine": "40 · Book Blurb · ideation · swarm light · Jev advises · candidates Claude Fable 5.1 / Kimi K3"}, {"step": "NEW-08", "name": "Cover Brief", "does": "A brief for your cover designer: genre signals, mood, what the cover must promise.", "who": "Agent", "runs": "sequence", "gate": "", "engine": "NEW-08 · Cover Brief · ideation · swarm light · Jev advises · candidates Claude Fable 5.1 / Kimi K3"}, {"step": "NEW-10", "name": "Launch Plan", "does": "Author bio, platform, advance copies, pricing and distribution, from your own data and notes.", "who": "Agent", "runs": "sequence", "gate": "", "engine": "NEW-10 · Author Bio / Platform / ARC / Pricing / Distribution · synthesis · swarm light · Jev advises · candidates GPT-6.1 Sol / MiMo-V2.6-Pro (least-gap — not parity)"}, {"step": "43", "name": "Marketing Copy", "does": "Ads, posts and promotion copy from the locked book.", "who": "Agent", "runs": "sequence", "gate": "", "engine": "43 · Marketing, Promotion & Sales Copy · ideation · swarm light · Jev advises · candidates Claude Fable 5.1 / Kimi K3"}];
var EXT = [{"step": "NEW-09", "name": "Agent Submission", "does": "A submission synopsis and query letter for agents and publishers.", "who": "Agent", "runs": "on_demand", "gate": "", "engine": "NEW-09 · Query / Submission Synopsis & Pitch · ideation · swarm light · Jev advises · candidates Claude Fable 5.1 / Kimi K3"}, {"step": "41", "name": "Audiobook Script", "does": "A script for narration, from the locked book.", "who": "Agent", "runs": "on_demand", "gate": "", "engine": "41 · Audiobook Script · prose · swarm light · Jev advises · candidates Claude Fable 5.1 / Kimi K3"}, {"step": "42", "name": "Book Trailer", "does": "Storyboard and trailer script for a book video.", "who": "Agent", "runs": "on_demand", "gate": "", "engine": "42 · Cinematic Storyboard & Trailer Script · ideation · swarm light · Jev advises · candidates Claude Fable 5.1 / Kimi K3"}, {"step": "NEW-11", "name": "Translations", "does": "Translations and other versions of the locked book.", "who": "Agent", "runs": "on_demand", "gate": "", "engine": "NEW-11 · Translation & Other Derivatives · ideation · swarm light · Jev advises · candidates Claude Fable 5.1 / Kimi K3"}];
var stage = st.stage;
var STATUS = {
writing: { fin: ['wait', 'wait', 'wait', 'wait', 'wait', 'wait'], rel: ['wait', 'wait', 'wait', 'wait'] },
finishing: { fin: ['done', 'run', 'wait', 'wait', 'wait', 'wait'], rel: ['run', 'done', 'wait', 'wait'] }
};
var LABEL = { wait: 'Waiting', run: 'In progress', done: 'Done' };
var mark = function (list, states, offset) {
return list.map(function (r, i) {
var s = states[i]; var t = TONE[s];
return Object.assign({}, r, { num: String(i + 1 + (offset || 0)).padStart(2, '0'), state: LABEL[s], tBg: t.bg, tFg: t.fg, tRing: t.ring,
hasGate: !!r.gate, whoBg: r.who === 'Code' ? TONE.wait.bg : (r.who === 'Agent' ? TONE.run.bg : TONE.you.bg),
whoFg: r.who === 'Code' ? TONE.wait.fg : (r.who === 'Agent' ? TONE.run.fg : TONE.you.fg) });
});
};
var stages = [{ id: 'writing', name: 'While writing' }, { id: 'finishing', name: 'After the last lock' }].map(function (o) {
var on = o.id === stage;
return { name: o.name, on: on, bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F3864' : '#4B5B73', shadow: on ? '0 1px 3px rgb(16 24 40 / 0.12)' : 'none', pick: function () { self.setState({ stage: o.id }); } };
});
var routes = [{ id: 'self', name: 'Self-publishing' }, { id: 'trad', name: 'Agent or publisher' }].map(function (o) {
var on = o.id === st.route;
return { name: o.name, on: on, bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F3864' : '#4B5B73', shadow: on ? '0 1px 3px rgb(16 24 40 / 0.12)' : 'none', pick: function () { self.setState({ route: o.id }); } };
});
var extras = EXT.filter(function (r) { return st.route === 'trad' || r.step !== 'NEW-09'; }).map(function (r) {
return Object.assign({}, r, { tool: r.step === 'NEW-09' ? 'For the submission route' : 'When you ask' });
});
var writing = stage === 'writing';
return {
viewOpts: viewOpts, isEngine: engine, stages: stages, routes: routes,
banner: writing ? 'These steps start when every chapter is locked: 0 of 24 so far. You can plan them now; nothing runs until then.' : 'Every chapter is locked. Finishing runs in this order, and nothing is published until you sign off the proof.',
bannerBg: writing ? TONE.wait.bg : TONE.done.bg, bannerRing: writing ? TONE.wait.ring : TONE.done.ring,
fin: mark(FIN, STATUS[stage].fin), rel: mark(REL, STATUS[stage].rel), extras: extras,
routeNote: st.route === 'trad' ? 'Agent Submission is added below. The release steps wait for your publisher’s schedule.' : 'Release steps run once your proof is signed off.'
};
}
}
