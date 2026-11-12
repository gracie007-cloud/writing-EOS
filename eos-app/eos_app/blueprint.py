"""Story Blueprint formula engine (requirements v0.7, FR-DEV-14 to FR-DEV-23, Appendix C).

Code computes what the Notion Story Blueprint Pipeline defines as a formula or a table: the Pillar
factor, Conflict Fit totals and the decision table, the Structure Fit categorical factors and totals,
the Climax Outcome Matrix, the Vacancy Rule, the Oscillation Rule, stage gates and the Stage 2
Guardrail. Models supply only the judgement scores (the raters). Every result says which parts came
from a model and which from code, and the table version used.

The Conflict Core pick, the outcome and the structure are always the Author's calls (FR-AU-4):
results carry a recommendation and decided_by="author", never a decision.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

TABLES_PATH = Path(__file__).resolve().parent.parent / "config" / "blueprint_tables.yaml"

RATER, CODE, MAP = "rater", "code", "map"   # map: scored from the Author's Conflict and Structure Map
AUTHOR, AGENT = "author", "agent_may_settle"


class TableError(ValueError):
    """The formula tables are inconsistent."""


class StageGateError(RuntimeError):
    """A stage was started before its inputs were approved."""


# ---------- tables ----------

@dataclass(frozen=True)
class Tables:
    version: str
    weights: dict
    cores: list
    pillars: list
    core_pillars: dict
    antagonist_face_cores: list
    scales: dict
    outcomes: dict
    structures: dict
    kishotenketsu: str
    three_act: str
    archetypes: list
    gant_conversion: list
    adaptation_states: list
    guardrail_fields: list
    stage_prerequisites: dict
    author_final_calls: list
    agent_may_settle: list

    @property
    def outcome_names(self):
        m = self.outcomes["matrix"]
        return [v for row in m.values() for v in row.values()] + [self.outcomes["flat"]]


def load_tables(path=TABLES_PATH) -> Tables:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    try:
        t = Tables(**{k: raw[k] for k in Tables.__dataclass_fields__})
    except KeyError as e:
        raise TableError(f"blueprint tables are missing {e}") from None
    _validate(t)
    return t


def _validate(t: Tables):
    cf = t.weights["conflict_fit"]
    expect = 3 * (cf["source"] + cf["pillar"] + cf["theme"] + cf["genre"])
    if cf["maximum"] != expect:
        raise TableError(f"conflict_fit maximum is {cf['maximum']} but the weights give {expect}")
    sf = t.weights["structure_fit"]
    expect = 3 * sum(sf[k] for k in ("outcome", "intensity_curve", "pen_name_pacing", "inevitability", "novelty", "cast_shape"))
    if sf["maximum"] != expect:
        raise TableError(f"structure_fit maximum is {sf['maximum']} but the weights give {expect}")
    if set(t.core_pillars) != set(t.cores):
        raise TableError("core_pillars must list every core exactly once")
    for core, ps in t.core_pillars.items():
        for p in ps:
            if p not in t.pillars:
                raise TableError(f"core {core} names an unknown Pillar: {p}")
    for c in t.antagonist_face_cores:
        if c not in t.cores:
            raise TableError(f"antagonist_face_cores names an unknown core: {c}")
    for special in (t.kishotenketsu, t.three_act):
        if special not in t.structures:
            raise TableError(f"the {special} structure is missing")
    for name, s in t.structures.items():
        vals = s["outcome"]
        if vals != "Any" and any(v not in t.outcome_names for v in vals):
            raise TableError(f"structure {name} has an unknown outcome: {vals}")
    if set(t.author_final_calls) & set(t.agent_may_settle):
        raise TableError("a decision cannot be both the Author's and an agent's")


def _check_0_3(name, v):
    if not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 3:
        raise ValueError(f"{name} must be a whole number from 0 to 3, got {v!r}")


def _known(kind, value, allowed):
    if value not in allowed:
        raise ValueError(f"unknown {kind}: {value!r}")


# ---------- Stage 0: Conflict Fit (FR-DEV-1, FR-DEV-15, FR-DEV-16) ----------

def pillar_factor(core, implied, tables: Tables) -> int:
    """3 if the first and (when present) second implied Pillars are typical of the core; 2 if the first is;
    1 if any other is; 0 otherwise. `implied` is ordered most prominent first."""
    _known("core", core, tables.cores)
    for p in implied:
        _known("Pillar", p, tables.pillars)
    typical = set(tables.core_pillars[core])
    if not implied:
        return 0
    if implied[0] in typical:
        return 3 if len(implied) < 2 or implied[1] in typical else 2
    return 1 if any(p in typical for p in implied[1:]) else 0


def conflict_fit(source, pillar, theme, genre, contradictions, tables: Tables) -> int:
    for name, v in (("source", source), ("pillar", pillar), ("theme", theme), ("genre", genre)):
        _check_0_3(name, v)
    if not isinstance(contradictions, int) or contradictions < 0:
        raise ValueError(f"contradictions must be a whole number of 0 or more, got {contradictions!r}")
    w = tables.weights["conflict_fit"]
    return (source * w["source"] + pillar * w["pillar"] + theme * w["theme"] + genre * w["genre"]
            - contradictions * w["contradiction_penalty"])


@dataclass(frozen=True)
class CoreRating:
    """The Conflict Fit Rater's scores for one core (each 0-3), with the number of contradictions found."""
    source: int
    theme: int
    genre: int
    contradictions: int = 0


@dataclass
class CoreRow:
    core: str
    source: int
    pillar: int
    theme: int
    genre: int
    contradictions: int
    total: int
    sources: dict


@dataclass
class CoreResult:
    sheet: list
    reading: str                 # weak | tie | close_contest | clear_fit
    recommended: str | None
    runner_up: str | None
    gap: int
    tied: list
    actions: list                # routing an agent may settle (FR-AU-3)
    question: str | None
    table_version: str
    inputs: dict
    decided_by: str = AUTHOR     # the core pick is always the Author's


TIE_QUESTION = "Which opposing force would the story be lost without?"


def score_cores(ratings: dict, implied_pillars, tables: Tables) -> CoreResult:
    """Rank all nine cores and read the result with the decision table (checked in order: weak, tie, close, clear)."""
    missing = [c for c in tables.cores if c not in ratings]
    if missing:
        raise ValueError(f"every core must be rated; missing: {', '.join(missing)}")
    extra = [c for c in ratings if c not in tables.cores]
    if extra:
        raise ValueError(f"unknown core: {', '.join(extra)}")
    rows = []
    for core in tables.cores:
        r = ratings[core]
        p = pillar_factor(core, implied_pillars, tables)
        rows.append(CoreRow(core, r.source, p, r.theme, r.genre, r.contradictions,
                            conflict_fit(r.source, p, r.theme, r.genre, r.contradictions, tables),
                            {"source": RATER, "pillar": CODE, "theme": RATER, "genre": RATER, "contradictions": RATER}))
    rows.sort(key=lambda r: -r.total)   # stable: equal totals keep the table's core order
    first, second = rows[0], rows[1]
    gap = first.total - second.total
    d = tables.weights["decision"]
    tied, runner, question, actions = [], None, None, []
    if first.total < d["weak_below"]:
        reading, recommended = "weak", None
        actions.append(("return_to_braindump", None))
    elif gap == 0:
        reading, recommended = "tie", None
        tied = [r.core for r in rows if r.total == first.total]
        question = TIE_QUESTION
    elif gap < d["clear_gap"]:
        reading, recommended, runner = "close_contest", first.core, second.core
        actions.append(("file_runner_up", second.core))
    else:
        reading, recommended = "clear_fit", first.core
    return CoreResult(rows, reading, recommended, runner, gap, tied, actions, question, tables.version,
                      {"ratings": {c: vars(r) for c, r in ratings.items()}, "implied_pillars": list(implied_pillars)})


def needs_antagonist(core, tables: Tables) -> bool:
    _known("core", core, tables.cores)
    return core in tables.antagonist_face_cores


# ---------- Stage 2: Climax Outcome Matrix (FR-DEV-19) ----------

def outcome_type(truth_embraced: bool, need_pillar_restored: bool, tables: Tables, flat_arc=False) -> str:
    """Derive the outcome type from the agent's two answers. The outcome itself is pitched; the Author decides."""
    if flat_arc:
        return tables.outcomes["flat"]
    row = tables.outcomes["matrix"]["truth_embraced" if truth_embraced else "lie_retained"]
    return row["restored" if need_pillar_restored else "lost"]


def _matrix_axes(outcome, tables: Tables):
    """The (row, column) of an outcome in the matrix, or None for Flat."""
    for row, cols in tables.outcomes["matrix"].items():
        for col, name in cols.items():
            if name == outcome:
                return row, col
    return None


# ---------- Stage 3: Structure Fit (FR-DEV-20) ----------

@dataclass(frozen=True)
class StoryProfile:
    outcome: str
    inevitability: str
    novelty: str
    temporal_root: str
    residual_unmet: bool = False     # a Pillar still Unmet at the Denouement
    core: str = ""                   # the Conflict Core the Author picked: the map ranks structures by it first


@dataclass(frozen=True)
class StructureRating:
    """The Structure Fit Rater's scores for one structure (each 0-3)."""
    intensity_curve: int
    pen_name_pacing: int
    cast_shape: int


@dataclass
class StructureRow:
    structure: str
    core_fit: str                    # the map's fit for the Conflict Core: best | situational | none
    outcome: int
    inevitability: int
    novelty: int
    intensity_curve: int
    pen_name_pacing: int
    cast_shape: int
    total: int
    sources: dict


@dataclass
class StructureResult:
    sheet: list
    recommended: str | None
    tied: list
    three_act: bool
    kishotenketsu_flag: bool
    actions: list
    table_version: str
    inputs: dict
    decided_by: str = AUTHOR         # the structure is always the Author's


_CORE_RANK = {"best": 2, "situational": 1, "none": 0}


def _map_score(axis, value, fits, s):
    """A categorical factor scored from the Author's map: best fit 3, situational 2, a structure the map lists under
    no value of this axis 1 (no view), a structure listed only under other values 0."""
    how = fits.get((axis, value))
    if how == "best":
        return s["exact"]
    if how == "situational":
        return s["adjacent"]
    return s["mismatch"] if any(a == axis for a, _ in fits) else s["any"]


def _outcome_score(value, allowed, tables, s):
    if allowed == "Any":
        return s["any"]
    if value in allowed:
        return s["exact"]
    mine = _matrix_axes(value, tables)
    if mine:
        for a in allowed:
            theirs = _matrix_axes(a, tables)
            if theirs and (theirs[0] == mine[0] or theirs[1] == mine[1]):
                return s["adjacent"]
    return s["mismatch"]


def score_structures(story: StoryProfile, ratings: dict, tables: Tables, fits: dict) -> StructureResult:
    """Structure Fit over the 21 structures of the Author's Conflict and Structure Map (the standing order).
    fits is the map: {structure: {(axis, value): 'best' | 'situational'}}. The core decides first (best, then
    situational, then none); within that, the formula total decides. Inevitability and novelty are scored from the
    map, outcome from the table, and intensity curve, pen-name pacing and cast shape by the rater."""
    _known("outcome", story.outcome, tables.outcome_names)
    _known("inevitability", story.inevitability, tables.scales["inevitability"])
    _known("novelty", story.novelty, tables.scales["novelty"])
    _known("temporal root", story.temporal_root, tables.scales["temporal_root"])
    if story.core:
        _known("conflict core", story.core, tables.cores)
    unknown = sorted(set(fits) - set(tables.structures))
    if unknown:
        raise TableError(f"the map names structures the table has no outcome ideal for: {', '.join(unknown)}")
    missing = [n for n in tables.structures if n not in ratings]
    if missing:
        raise ValueError(f"every structure must be rated; missing: {', '.join(missing)}")
    w, s = tables.weights["structure_fit"], tables.weights["structure_scoring"]
    rows = []
    for name, ideal in tables.structures.items():
        r, fit = ratings[name], fits.get(name, {})
        for k in ("intensity_curve", "pen_name_pacing", "cast_shape"):
            _check_0_3(f"{name} {k}", getattr(r, k))
        core_fit = fit.get(("Conflict Core", story.core), "none") if story.core else "none"
        out = _outcome_score(story.outcome, ideal["outcome"], tables, s)
        if out == s["exact"] and story.outcome == "Triumph" and ideal.get("triumph_needs_residual_unmet") \
                and not story.residual_unmet:
            out = s["adjacent"]
        inev = _map_score("Inevitability", story.inevitability, fit, s)
        root = ideal.get("inevitability_exact_with_temporal_root")
        if root and story.temporal_root == root:
            inev = s["exact"]
        nov = _map_score("Novelty", story.novelty, fit, s)
        total = (out * w["outcome"] + r.intensity_curve * w["intensity_curve"] + r.pen_name_pacing * w["pen_name_pacing"]
                 + inev * w["inevitability"] + nov * w["novelty"] + r.cast_shape * w["cast_shape"])
        rows.append(StructureRow(name, core_fit, out, inev, nov, r.intensity_curve, r.pen_name_pacing, r.cast_shape, total,
                                 {"core_fit": MAP, "outcome": CODE, "inevitability": MAP, "novelty": MAP,
                                  "intensity_curve": RATER, "pen_name_pacing": RATER, "cast_shape": RATER}))
    rows.sort(key=lambda r: (-_CORE_RANK[r.core_fit], -r.total, r.structure))
    top = rows[0]
    leaders = [r.structure for r in rows if r.core_fit == top.core_fit and r.total == top.total]
    kisho = tables.kishotenketsu in leaders
    actions = [("kishotenketsu_send_back", None)] if kisho else []
    tied = []
    if top.total <= w["three_act_baseline"]:
        three_act, recommended = True, tables.three_act
    elif len(leaders) > 1:
        three_act, recommended, tied = False, None, leaders
    else:
        three_act, recommended = False, leaders[0]
    return StructureResult(rows, recommended, tied, three_act, kisho, actions, tables.version,
                           {"story": vars(story), "ratings": {n: vars(r) for n, r in ratings.items()}})


# ---------- Stage 3: Vacancy Rule (FR-DEV-21) ----------

@dataclass
class CastMap:
    statuses: dict
    holders: dict
    cut_or_merge: list
    actions: list
    warnings: list
    decided_by: str = AUTHOR         # the cast map and any cut or merge are the Author's


def cast_function_map(required, assignments, characters, tables: Tables, split_reasons=None) -> CastMap:
    split_reasons = split_reasons or {}
    for fn in list(required) + list(assignments):
        _known("archetype", fn, tables.archetypes)
    for holders in assignments.values():
        for ch in holders:
            _known("character", ch, characters)
    statuses, actions, warnings, held = {}, [], [], {c: [] for c in characters}
    for fn in tables.archetypes:
        holders = [h for h in assignments.get(fn, []) if h]
        for h in holders:
            held[h].append(fn)
        if fn not in required:
            statuses[fn] = "Not required"
            if holders:
                warnings.append(f"{fn} is assigned but the arc does not need it.")
        elif holders:
            statuses[fn] = "Filled"
            if len(holders) > 1 and not split_reasons.get(fn):
                warnings.append(f"{fn} is split across {len(holders)} characters without a stated reason.")
        else:
            statuses[fn] = "Vacant (create)"
            actions.append(("send_to_pool", fn))      # Character Pool first, then Character Creation
    for ch, fns in held.items():
        if len(fns) > 2:
            warnings.append(f"{ch} holds {len(fns)} functions ({', '.join(fns)}); one character may hold two.")
    cut = [c for c in characters if not held[c]]
    return CastMap(statuses, {fn: list(assignments.get(fn, [])) for fn in tables.archetypes}, cut, actions, warnings)


# ---------- stage gates and the Stage 2 Guardrail (FR-DEV-22, FR-DEV-5) ----------

def stage_gate(stage, approved, tables: Tables):
    """Refuse a stage until everything it and the stages before it need has been approved."""
    order = list(tables.stage_prerequisites)
    _known("stage", stage, order)
    needed = [x for s in order[:order.index(stage) + 1] for x in tables.stage_prerequisites[s]]
    missing = [x for x in needed if x not in approved]
    if missing:
        raise StageGateError(f"{stage} cannot start; not yet approved: {', '.join(missing)}")


def guardrail_diff(before: dict, after: dict, tables: Tables) -> list:
    """The protected fields Stage 2 changed. Any change means a send-back to Stage 1 (agent may settle)."""
    return [f for f in tables.guardrail_fields if before.get(f) != after.get(f)]


# ---------- Stage 2: Oscillation Rule and the GANT skeleton (FR-DEV-19) ----------

@dataclass
class ArcCheck:
    oscillations: int
    warnings: list
    errors: list
    next_ghost: list
    actions: list


def arc_checks(plot_beats, adaptation_path, outcome, tables: Tables, denouement_unmet=()) -> ArcCheck:
    """The Plot Ring only moves forward; the Adaptation Ring may loop back (loops are counted)."""
    _known("outcome", outcome, tables.outcome_names)
    states = tables.adaptation_states
    for st in adaptation_path:
        _known("adaptation state", st, states)
    errors, warnings, actions = [], [], []
    for a, b in zip(plot_beats, plot_beats[1:]):
        if b < a:
            errors.append(f"The Plot Ring moves backward (beat {a} to beat {b}); it may only move forward.")
    idx = [states.index(st) for st in adaptation_path]
    loops = sum(1 for a, b in zip(idx, idx[1:]) if b < a)
    if outcome in ("Triumph", "Bittersweet") and "Collapse" not in adaptation_path:
        warnings.append(f"A {outcome} arc never passes Collapse.")
    next_ghost = list(denouement_unmet)
    if next_ghost:
        actions.append(("record_next_ghost", next_ghost))
    return ArcCheck(loops, warnings, errors, next_ghost, actions)


def gant_skeleton(plot_blueprint: dict, tables: Tables) -> dict:
    """Beat number -> [(component, field, value)], built from the fixed conversion table (Appendix C9)."""
    beats = {n: [] for n in range(8)}
    for row in tables.gant_conversion:
        fields = row["field"] if isinstance(row["field"], list) else [row["field"]]
        values = [plot_blueprint.get(f) for f in fields]
        value = " / ".join(str(v) for v in values if v) or None
        beats[row["beat"]].append((row["component"], " + ".join(fields), value))
    return beats


# ---------- Pillar notation and the Technology fallback (FR-DEV-18) ----------

_PILLAR_RE = re.compile(r"^(?P<holder>.+?) · (?P<pillar>.+?): (?P<state>\w+) \((?P<level>\w+)\)$")


def pillar_notation(holder, pillar, state, level, tables: Tables) -> str:
    _known("Pillar", pillar, tables.pillars)
    _known("Pillar state", state, tables.scales["pillar_state"])
    _known("Pillar level", level, tables.scales["pillar_level"])
    if not holder:
        raise ValueError("a Pillar needs a holder")
    return f"{holder} · {pillar}: {state} ({level})"


def parse_pillar(text, tables: Tables):
    m = _PILLAR_RE.match(text.strip())
    if not m:
        raise ValueError(f"not in the form 'Holder · Pillar: State (Level)': {text!r}")
    parts = m.group("holder", "pillar", "state", "level")
    pillar_notation(*parts, tables)
    return parts


def technology_fallback_flag(states, natural_fallback: bool):
    """states: [(holder, pillar, state, level)]. When Technology is threatened and there is no natural
    fallback, the threat cascades to the underlying Pillar and Intensity should rise."""
    if natural_fallback:
        return None
    hit = [h for h, p, st, _ in states if p == "Technology" and st in ("Threatened", "Unmet")]
    if not hit:
        return None
    return (f"Technology is threatened for {', '.join(hit)} with no natural fallback: the threat cascades to the "
            "underlying Pillar, so Intensity should rise.")


# ---------- Stage 1 quality checks (FR-DEV-6, FR-DEV-17) ----------

TROPE_TREATMENTS = ("subverted", "deepened", "justified")
_SENTENCE_END = re.compile(r"[.!?]+(?=\s|$)")


def plot_blueprint_checks(bp: dict, tables: Tables) -> list:
    """Return the failures; an empty list means the Plot Blueprint passes."""
    fails = []
    core = bp.get("core")
    if not isinstance(core, str) or core not in tables.cores:
        fails.append("The Plot Blueprint must name exactly one Conflict Core.")
        core = None
    poi = bp.get("point_of_impact") or {}
    if not (poi.get("pillar") in tables.pillars and poi.get("state") in tables.scales["pillar_state"]
            and poi.get("level") in tables.scales["pillar_level"]):
        fails.append("The point of impact must name a Pillar with its State and Level.")
    spec = (bp.get("specificity") or "").strip()
    if not spec or len([p for p in _SENTENCE_END.split(spec) if p.strip()]) != 1:
        fails.append("Specificity must be answered in one sentence.")
    if not (bp.get("resonance") or "").strip():
        fails.append("Resonance must be checked and stated.")
    scale = tables.scales["intensity"]
    inten = bp.get("intensity") or {}
    opening, peak, shape = inten.get("opening"), inten.get("peak"), bp.get("shape", "standard")
    if opening not in scale or peak not in scale:
        fails.append("Peak and Opening Intensity must both be on the intensity scale.")
    elif shape == "siege":
        if scale.index(peak) < scale.index(opening):
            fails.append("Peak Intensity may not fall below Opening in a siege shape.")
    elif shape != "aftermath" and scale.index(peak) <= scale.index(opening):
        fails.append("Peak Intensity must be above Opening unless the shape is a deliberate siege or aftermath.")
    if core and needs_antagonist(core, tables):
        role = bp.get("antagonist_role") or {}
        if not all(role.get(k) for k in ("function", "requirements", "source")):
            fails.append(f"A {core} conflict needs a face: the Antagonist Role (function, requirements, pool match "
                         "or creation) is missing.")
    audit = bp.get("trope_audit") or []
    if len(audit) != 3 or any(a.get("treatment") not in TROPE_TREATMENTS or not a.get("element") for a in audit):
        fails.append("The trope audit needs the three most familiar elements, each subverted, deepened or justified.")
    return fails


# ---------- who decides (FR-AU-3, FR-AU-4) ----------

def who_decides(kind, tables: Tables) -> str:
    """'agent_may_settle' only for routing the formulas determine; everything else is the Author's."""
    return AGENT if kind in tables.agent_may_settle else AUTHOR
