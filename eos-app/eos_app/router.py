"""The app's own router (requirements D22, P8, P10; config/routing.yaml).

Every component has a line of experts (a Mixture of Experts, the Author's design, 2026-10-22): its Primary, its
Comparable and, where one is given, a Fallback (the component's own, else the Primary's in the roster). The router
tries them in that order. A model listed in the roster under more than one provider has more than one route: when a
provider is down the router tries the model's next route before it moves to the next expert.

Three lanes. Building Blocks, Sales & Marketing, the editing tools and the evaluation components use the general
lane: the experts above. Prose Writing components that write prose use the prose lane: a model fine-tuned for the
book's genre, via Featherless AI or Unsloth Desktop, then the component's own experts as the safety net (never for
mature text). Media components use the media lane: their experts, each making what the component makes (image,
video, speech, music, sound). Each lane lists its providers in routing.yaml; a model on a provider outside its lane
is never called for that lane.

Checks the router enforces:
- P8: an evaluation component never runs on the same model that wrote what it judges, whatever provider serves it.
- P10: mature text is written only by an Uncensored model on a mature provider; mature media only by an open model on
  Comfy Cloud, the one media provider whose terms allow lawful mature content (fal.ai and OpenRouter don't). An
  evaluation component tries its own experts first; if they refuse mature text, its Mature Fallback (a database
  column) takes over.
- A model with no provider model ID cannot be called, so it is never chosen.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .registry import Registry, RegistryError

ROUTING_PATH = Path(__file__).resolve().parent.parent / "config" / "routing.yaml"


class RoutingError(ValueError):
    """No model may take this call under the routing rules."""


@dataclass(frozen=True)
class Routing:
    providers: dict
    general_providers: list
    prose_providers: list
    media_providers: list
    mature_writer_providers: list
    mature_media_providers: list


def load_routing(path=ROUTING_PATH) -> Routing:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    lanes = raw["lanes"]
    return Routing(raw["providers"], lanes["general"]["providers"], lanes["prose"]["providers"],
                   lanes["media"]["providers"], raw["mature"]["writer_providers"], raw["mature"]["media_providers"])


def route(model, routing: Routing) -> str:
    """Where the call goes: the route for the model's provider."""
    try:
        return routing.providers[model.provider]
    except KeyError:
        raise RoutingError(f"{model.name}: no route for provider {model.provider!r}") from None


def experts(c, reg: Registry) -> list:
    """[(slot, model)] for a component: Primary, Comparable, then its Fallback (the component's own, or the
    Primary's roster Fallback when that is empty) if it is another model."""
    cand = c.candidates or {}
    try:
        line = [(s, m) for s in ("primary", "comparable") if (m := reg.resolve(cand.get(s)))]
        if line:
            fb = reg.resolve(cand.get("fallback") or line[0][1].fallback)   # the component's own, else the roster's
            if fb and fb.ident not in {m.ident for _, m in line}:
                line.append(("fallback", fb))
    except RegistryError as e:
        raise RoutingError(f"{c.name}: {e}") from None
    return line


def with_routes(models, reg: Registry) -> list:
    """Each model followed by the same model on its other providers, so an outage is met by another route first."""
    out, seen = [], set()
    for m in models:
        for r in reg.routes(m):
            if r.key not in seen:
                seen.add(r.key)
                out.append(r)
    return out


def lane_providers(c, routing: Routing, mature: bool = False) -> list:
    """The providers this component's calls may go to (routing.yaml)."""
    if c.makes_media:
        return routing.mature_media_providers if mature else routing.media_providers
    return routing.mature_writer_providers if mature else routing.general_providers


def mature_ok(model, routing: Routing) -> bool:
    return model.uncensored and model.provider in routing.mature_writer_providers


def writer_models(c, reg: Registry, routing: Routing, genre: str | None = None, mature: bool = False) -> list:
    """The models that may write for this component, in the order the router tries them."""
    if c.is_evaluation:
        raise RoutingError(f"{c.name} is an evaluation component; use choose_checker")
    line = [m for _, m in experts(c, reg)]
    if c.makes_media:
        wrong = [f"{m.name} makes {(m.modality or 'text').lower()}" for m in line if m.modality != c.modality]
        if wrong:
            raise RoutingError(f"{c.name} makes {c.modality.lower()}, but {'; '.join(wrong)}")
        allowed = lane_providers(c, routing, mature)
        models = [m for m in with_routes(line, reg) if m.provider in allowed and (m.open_weights or not mature)]
        if not models:          # mature: only open models on a provider whose terms allow lawful mature media
            raise RoutingError(f"{c.name}: no {'open ' if mature else ''}model on {', '.join(allowed)} among its "
                               f"experts{' for mature media' if mature else ''}")
        return models
    if c.writes_prose:
        tuned = [m for m in (reg.for_genre(genre) if genre else []) if m.provider in routing.prose_providers]
        if mature:
            tuned = [m for m in tuned if mature_ok(m, routing)]
            if not tuned:
                raise RoutingError(f"{c.name}: no mature-tier model is tagged for {genre or 'this genre'} "
                                   f"(Uncensored, on {', '.join(routing.mature_writer_providers)})")
            return tuned
        stand_ins = [m for m in with_routes(line, reg) if m.provider in routing.general_providers]
        return tuned + [m for m in stand_ins if m.key not in {t.key for t in tuned}]   # the safety net stays
    models = with_routes(line, reg)
    if mature:
        models = [m for m in models if mature_ok(m, routing)]
        if not models:
            raise RoutingError(f"{c.name}: mature text needs a mature-tier model, and none is assigned")
        return models
    models = [m for m in models if m.provider in routing.general_providers]
    if not models:
        raise RoutingError(f"{c.name}: none of its experts is on a general-lane provider "
                           f"({', '.join(routing.general_providers)})")
    return models


def unusable(m, down=(), down_providers=()) -> str:
    """Why this model cannot be called right now; '' when it can."""
    if not m.model_id:
        return f"{m.name} has no provider model ID yet"
    if m.provider in down_providers:
        return f"{m.name} is on {m.provider}, which is down"
    return f"{m.name} is down" if m.key in down else ""


def choose_writer(c, reg: Registry, routing: Routing, genre: str | None = None, mature: bool = False, down=(),
                  down_providers=()):
    reasons = []
    for m in writer_models(c, reg, routing, genre, mature):
        why = unusable(m, down, down_providers)
        if not why:
            return m
        reasons.append(why)
    raise RoutingError(f"{c.name}: no model that may write this can be called: " + "; ".join(reasons))


def checker_models(judge, reg: Registry, routing: Routing) -> list:
    """An evaluation component's experts, with their routes, on the general lane."""
    if not judge.is_evaluation:
        raise RoutingError(f"{judge.name} judges nothing; it is not an evaluation component")
    return [m for m in with_routes([m for _, m in experts(judge, reg)], reg) if m.provider in routing.general_providers]


def choose_checker(judge, writer, reg: Registry, routing: Routing, mature: bool = False, refused=(), down=(),
                   down_providers=()):
    """The model an evaluation component runs on to judge work made by `writer`: its experts in order, then, for
    mature work they all refused, its Mature Fallback. A model is skipped if it is the writer's own model on any
    provider (P8), has refused, cannot be called, or is down."""
    tried = checker_models(judge, reg, routing)
    said_no = {reg.by_key[k].ident for k in refused if k in reg.by_key}       # a refusal is the model's, not a route's

    def why_not(m):
        if m.ident == writer.ident:
            return f"{m.name} wrote the text"
        return f"{m.name} is refusing" if m.ident in said_no else unusable(m, down, down_providers)

    if mature and all(why_not(m) for m in tried):
        if not judge.mature_fallback:
            raise RoutingError(f"{judge.name}: its Mature Fallback is still open, so mature work can't be judged yet")
        tried = tried + [reg.resolve(judge.mature_fallback)]
    reasons = []
    for m in tried:
        why = why_not(m)
        if not why:
            return m
        reasons.append(why)
    raise RoutingError(f"{judge.name} has no model to judge {writer.name}: " + "; ".join(reasons))


def same_model_report(w, reg: Registry) -> list:
    """Each checker whose Primary is the very model that is the Primary of a component it judges: the pairing that
    happens on every normal run. The router steps past it to the next expert at each call; this list shows where a
    checker would rarely run on its own Primary. Prose writers are shown with their stand-in experts; genre
    fine-tunes are checked at each call."""
    out = []
    for judge in w.ordered():
        if not judge.is_evaluation:
            continue
        line = experts(judge, reg)
        if not line:
            continue
        jm = line[0][1]
        for step in judge.judges:
            writer = w.by_step[step]
            wl = experts(writer, reg) if writer.task_type != "code" else []
            if wl and wl[0][1].ident == jm.ident:
                out.append(f"{judge.name} and {writer.name} both have {jm.name} as Primary")
    return out
