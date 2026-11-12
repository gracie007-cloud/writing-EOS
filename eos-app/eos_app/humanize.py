"""Humanize: a prose-naturalness rewrite for fiction (requirements v0.8, FR-HU-1 to FR-HU-9, decision D16).

The model does one thing: rewrite a passage so it reads naturally in the pen name's voice. Code does the rest:
it hides what must not change (locked lines and, by default, dialogue) behind placeholders, builds the request
from the settings and the style card, cleans the output, measures rhythm, vocabulary and stock phrasing before
and after, checks length drift and Story Bible names, retries a failed call, and returns a suggestion. The
Author accepts or rejects it paragraph by paragraph (FR-ED-7); nothing is saved here.

The model call is passed in as a function, so the router chooses the model (Edit Actions: Primary, Fallback,
mature tier) and this module never touches the network.
"""

from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "humanize.yaml"
AGENT = "edit_actions.humanize"
TOKEN_RE = re.compile(r"⟦P(\d+)⟧")


class ProtectedSpanError(ValueError):
    """A protected span came back missing, repeated or unknown."""


class HumanizeFailed(RuntimeError):
    """Every attempt failed; the router moves to the Fallback model, then to the Author (P12)."""

    def __init__(self, message, problems):
        super().__init__(message)
        self.problems = problems


# ---------- configuration and settings ----------

@dataclass(frozen=True)
class HumanizeConfig:
    version: str
    limits: dict
    strengths: dict
    english_variants: dict
    em_dash_policies: dict
    stock_phrases: list
    copula_openers: list
    preambles: list
    recommend: dict


def load_config(path=CONFIG_PATH) -> HumanizeConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return HumanizeConfig(**{k: raw[k] for k in HumanizeConfig.__dataclass_fields__})


@dataclass
class HumanizeSettings:
    strength: str = "balanced"           # light | balanced | strong
    passes: int = 1                      # 1 to max_passes
    english_variant: str | None = None   # from the project, e.g. "british"
    protect_dialogue: bool = True
    single_quote_dialogue: bool = False  # for books that use 'single' quotation marks
    em_dash: str = "keep"                # keep | reduce_narration | remove_narration
    voice_notes: str = ""                # from the project style card (FR-DEV-12)
    mature: bool = False                 # passage is in a mature scene: route to the mature tier

    def validate(self, cfg: HumanizeConfig):
        if self.strength not in cfg.strengths:
            raise ValueError(f"unknown strength: {self.strength!r}")
        if not isinstance(self.passes, int) or not 1 <= self.passes <= cfg.limits["max_passes"]:
            raise ValueError(f"passes must be 1 to {cfg.limits['max_passes']}, got {self.passes!r}")
        if self.english_variant is not None and self.english_variant not in cfg.english_variants:
            raise ValueError(f"unknown English variant: {self.english_variant!r}")
        if self.em_dash not in cfg.em_dash_policies:
            raise ValueError(f"unknown em dash policy: {self.em_dash!r}")


# ---------- protected spans (FR-HU-3) ----------

_DOUBLE_DIALOGUE = re.compile(r'"[^"\n]*"|“[^”\n]*”')
_SINGLE_DIALOGUE = re.compile(r"(?<!\w)‘(?:[^’\n]|’(?=\w))*’(?!\w)")


@dataclass
class Protected:
    masked: str
    spans: dict          # token -> original text


def _token(n):
    return f"⟦P{n}⟧"


def protect(text, locked=(), protect_dialogue=True, single_quote_dialogue=False) -> Protected:
    """Replace locked lines, then dialogue, with numbered placeholders the model must keep."""
    if TOKEN_RE.search(text):
        raise ValueError("the text already contains a placeholder mark; remove it before humanizing")
    spans, masked = {}, text

    def take(original):
        tok = _token(len(spans) + 1)
        spans[tok] = original
        return tok

    for lock in locked:
        if lock and lock in masked:
            masked = masked.replace(lock, take(lock), 1)
    if protect_dialogue:
        masked = _DOUBLE_DIALOGUE.sub(lambda m: take(m.group(0)), masked)
        if single_quote_dialogue:
            masked = _SINGLE_DIALOGUE.sub(lambda m: take(m.group(0)), masked)
    return Protected(masked, spans)


def missing_or_extra(masked, p: Protected) -> list:
    found = TOKEN_RE.findall(masked)
    problems = []
    for tok in p.spans:
        n = found.count(TOKEN_RE.match(tok).group(1))
        if n == 0:
            problems.append(f"A protected passage was dropped: {p.spans[tok][:40]!r}")
        elif n > 1:
            problems.append(f"A protected passage was repeated: {p.spans[tok][:40]!r}")
    for num in set(found):
        if _token(int(num)) not in p.spans:
            problems.append(f"The output invented a placeholder ({_token(int(num))}).")
    return problems


def restore(masked, p: Protected) -> str:
    problems = missing_or_extra(masked, p)
    if problems:
        raise ProtectedSpanError("; ".join(problems))
    return TOKEN_RE.sub(lambda m: p.spans[m.group(0)], masked)


# ---------- the request (FR-HU-2, FR-HU-4) ----------

@dataclass
class ModelRequest:
    agent: str
    task_type: str
    tier: str            # standard | mature
    temperature: float
    messages: list


USER_LEAD = "Rewrite this passage:"


def build_request(masked_text, settings: HumanizeSettings, cfg: HumanizeConfig, target_words) -> ModelRequest:
    settings.validate(cfg)
    lo, hi = round(target_words * 0.9), round(target_words * 1.1)
    parts = [
        "You are a fiction line editor. Rewrite the passage so it reads as natural, living prose in the "
        "author's voice. It is part of a novel: keep the point of view, tense, events, facts, names and order "
        "of beats exactly as they are, and add nothing new.",
        f"Depth: {cfg.strengths[settings.strength]['instruction']}",
    ]
    if settings.voice_notes:
        parts.append(f"Voice (from the project style card): {settings.voice_notes}")
    if settings.english_variant:
        parts.append(cfg.english_variants[settings.english_variant])
    parts += [
        "What to change: runs of sentences with the same length or shape; stock or abstract phrasing where a "
        "concrete detail already in the passage would serve; sentences that sum up a feeling instead of showing "
        "it; stiff connectors. Do not add hedges, rhetorical questions or asides the voice would not use.",
        "Avoid these phrases: " + "; ".join(cfg.stock_phrases) + ".",
        cfg.em_dash_policies[settings.em_dash],
        "Marks like ⟦P1⟧ stand for dialogue or lines the author has locked. Keep every mark exactly "
        "once, unchanged, where it belongs in the sentence; you may change the narration around it.",
        f"Length: about {target_words} words; stay between {lo} and {hi}.",
        "Output plain prose paragraphs only, with the same paragraph breaks where they still work. Italics "
        "with *asterisks* may stay. No headings, lists, bold, notes or explanation.",
    ]
    return ModelRequest(AGENT, "prose", "mature" if settings.mature else "standard",
                        cfg.strengths[settings.strength]["temperature"],
                        [{"role": "system", "content": "\n\n".join(parts)},
                         {"role": "user", "content": f"{USER_LEAD}\n\n{masked_text}"}])


# ---------- clean-up (FR-HU-5) ----------

def clean_output(text, settings: HumanizeSettings, cfg: HumanizeConfig) -> str:
    """Strip markup and lead-ins; apply the em dash policy. Run on masked text, so dialogue is untouched."""
    out = text.strip()
    for pat in cfg.preambles:
        out = re.sub(pat, "", out, count=1, flags=re.I)
    out = re.sub(r"```.*?```", "", out, flags=re.S)
    out = re.sub(r"^#{1,6}\s+", "", out, flags=re.M)
    out = re.sub(r"\*\*(.+?)\*\*", r"\1", out)
    out = re.sub(r"__(.+?)__", r"\1", out)
    out = re.sub(r"^\s*(?:[-+•]|\d+\.)\s+", "", out, flags=re.M)
    out = re.sub(r"^>\s?", "", out, flags=re.M)
    out = re.sub(r"`([^`]*)`", r"\1", out)
    out = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", out)
    if settings.em_dash != "keep":
        paras = out.split("\n")
        for i, para in enumerate(paras):
            seen = [0]

            def swap(m):
                seen[0] += 1
                if settings.em_dash == "reduce_narration" and seen[0] == 1:
                    return m.group(0)
                return ", "
            paras[i] = re.sub(r"\s*—\s*", swap, para)
        out = "\n".join(paras)
        out = re.sub(r",\s*([.,;:!?])", r"\1", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


# ---------- measures (FR-HU-6) ----------

_SENT_SPLIT = re.compile(r"(?<=[.!?])[\"'”’)]*\s+")
_WORD = re.compile(r"[A-Za-zÀ-ɏ]+(?:['’][A-Za-z]+)*")


@dataclass
class Measures:
    words: int
    sentences: int
    sentence_mean: float
    sentence_spread: float        # standard deviation of sentence length, in words
    lexical_variety: float        # moving-average type-token ratio, 0-100
    stock_phrases: int
    phrases_found: list
    copula_openers: int
    em_dashes: int
    reading_ease: float           # Flesch Reading Ease
    grade_level: float            # Flesch-Kincaid grade


def _sentences(text):
    return [s for s in (x.strip() for x in _SENT_SPLIT.split(text.strip())) if _WORD.search(s)]


def _syllables(word):
    w = word.lower()
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]+", w)))


def _mattr(words, window=50):
    if not words:
        return 0.0
    if len(words) <= window:
        return 100 * len(set(words)) / len(words)
    ratios = [len(set(words[i:i + window])) / window for i in range(len(words) - window + 1)]
    return 100 * sum(ratios) / len(ratios)


def measure(text, cfg: HumanizeConfig) -> Measures:
    sents = _sentences(text)
    words = _WORD.findall(text)
    lows = [w.lower() for w in words]
    lens = [len(_WORD.findall(s)) for s in sents] or [0]
    mean = sum(lens) / len(lens)
    spread = math.sqrt(sum((n - mean) ** 2 for n in lens) / len(lens))
    low_text = text.lower().replace("’", "'")
    found = []
    count = 0
    for ph in cfg.stock_phrases:
        n = len(re.findall(r"(?<!\w)" + re.escape(ph.lower()) + r"(?!\w)", low_text))
        if n:
            found.append(ph)
            count += n
    copula = sum(1 for s in sents for pat in cfg.copula_openers
                 if re.search(pat, s.lstrip("\"'“‘").lower()))
    nw, ns = max(len(words), 1), max(len(sents), 1)
    syl = sum(_syllables(w) for w in words)
    ease = 206.835 - 1.015 * (nw / ns) - 84.6 * (syl / nw)
    grade = 0.39 * (nw / ns) + 11.8 * (syl / nw) - 15.59
    return Measures(len(words), len(sents), round(mean, 1), round(spread, 1), round(_mattr(lows), 1), count,
                    found, copula, text.count("—"), round(ease, 1), round(grade, 1))


# ---------- recommendation by code (FR-HU-7) ----------

def recommend(text, cfg: HumanizeConfig, base: HumanizeSettings | None = None):
    """Suggest strength and passes from the text itself. Returns (settings, plain-English reason)."""
    m = measure(text, cfg)
    r = cfg.recommend
    count = m.stock_phrases + m.copula_openers
    tells = count * 1000 / max(m.words, 1)
    s = HumanizeSettings(**asdict(base)) if base else HumanizeSettings()
    if (count >= r["strong_min_tells"] and tells >= r["strong_if_tells_per_1000"]) or             (m.sentences >= 4 and m.sentence_spread < r["strong_if_spread_below"]):
        s.strength = "strong"
    elif (count >= 1 and tells >= r["balanced_if_tells_per_1000"]) or             (m.sentences >= 4 and m.sentence_spread < r["balanced_if_spread_below"]):
        s.strength = "balanced"
    else:
        s.strength = "light"
    s.passes = 2 if s.strength == "strong" and m.words > r["two_passes_if_strong_and_words_over"] else 1
    noun = "stock phrase or summary opener" if count == 1 else "stock phrases or summary openers"
    reason = (f"{count} {noun} in {m.words} words "
              f"({tells:.0f} per 1,000), and sentence lengths vary by about {m.sentence_spread} words, "
              f"so {s.strength} with {s.passes} pass{'es' if s.passes > 1 else ''}.")
    return s, reason


# ---------- checks (FR-HU-8) ----------

@dataclass
class CheckResult:
    errors: list
    warnings: list
    word_drift: float


def check(original, result, cfg: HumanizeConfig, terms=()) -> CheckResult:
    errors, warnings = [], []
    a, b = measure(original, cfg), measure(result, cfg)
    if not result.strip():
        errors.append("The output is empty.")
    drift = 100 * (b.words - a.words) / max(a.words, 1)
    if abs(drift) > cfg.limits["word_drift_fail"]:
        errors.append(f"Length changed too much: {a.words} words became {b.words} ({drift:+.0f}%).")
    elif abs(drift) > cfg.limits["word_drift_warn"]:
        warnings.append(f"Length changed by {drift:+.0f}% ({a.words} to {b.words} words).")
    for t in terms:
        pat = r"(?<!\w)" + re.escape(t) + r"(?!\w)"
        if re.search(pat, original) and not re.search(pat, result):
            errors.append(f"A Story Bible name was dropped: {t}.")
    if b.stock_phrases > a.stock_phrases:
        new = [p for p in b.phrases_found if p not in a.phrases_found]
        warnings.append(f"Stock phrases rose from {a.stock_phrases} to {b.stock_phrases}"
                        + (f": {', '.join(new)}." if new else "."))
    if b.copula_openers > a.copula_openers:
        warnings.append(f"Summary openers rose from {a.copula_openers} to {b.copula_openers}.")
    return CheckResult(errors, warnings, round(drift, 1))


# ---------- the whole action (FR-HU-1, FR-HU-9) ----------

@dataclass
class HumanizeResult:
    text: str
    before: Measures
    after: Measures
    warnings: list
    errors: list
    word_drift: float
    passes_run: int
    retries: int
    requests: list = field(repr=False)
    inputs: dict = field(default_factory=dict)
    config_version: str = ""
    status: str = "suggestion"       # shown through the paragraph gate; never saved here
    decided_by: str = "author"


def humanize(text, settings: HumanizeSettings, call_model, cfg: HumanizeConfig, locked=(), terms=()) -> HumanizeResult:
    """Run the passes. call_model(ModelRequest) -> str is supplied by the router."""
    settings.validate(cfg)
    if not text.strip():
        raise ValueError("nothing to humanize")
    if len(text) > cfg.limits["max_chars"]:
        raise ValueError(f"the passage is over {cfg.limits['max_chars']:,} characters; humanize it scene by scene")
    p = protect(text, locked, settings.protect_dialogue, settings.single_quote_dialogue)
    target = measure(text, cfg).words
    current, requests, retries = p.masked, [], 0
    for _ in range(settings.passes):
        problems = []
        for attempt in range(1 + cfg.limits["retries"]):
            req = build_request(current, settings, cfg, target)
            requests.append(req)
            out = clean_output(call_model(req) or "", settings, cfg)
            problems = missing_or_extra(out, p)
            if not problems:
                problems = check(text, restore(out, p), cfg, terms).errors
            if not problems:
                current = out
                break
            retries += 1
        else:
            raise HumanizeFailed("Humanize failed after retries; try the Fallback model.", problems)
    final = restore(current, p)
    res = check(text, final, cfg, terms)
    return HumanizeResult(final, measure(text, cfg), measure(final, cfg), res.warnings, res.errors, res.word_drift,
                          settings.passes, retries, requests,
                          {"settings": asdict(settings), "locked": list(locked), "terms": list(terms),
                           "protected_spans": len(p.spans)}, cfg.version)
