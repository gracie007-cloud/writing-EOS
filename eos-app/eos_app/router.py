"""The app's own router (requirements D22, P8, P10; config/routing.yaml).

Every component has a line of experts (a Mixture of Experts, the Author's design, 2026-10-22): its Primary (the
database's Frontier Model), its Comparable (the Comparable Open-Weight model) and, where the roster gives one, the
Primary's Fallback Model. The router tries them in that order.

Three lanes. Building Blocks, Sales & Marketing, the editing tools and the evaluation components use the general
lane: the experts above. Prose Writing components that write prose use the prose lane: a model fine-tuned for the
book's genre, via Featherless AI or Unsloth Desktop; until one is tagged for the genre, the component's own experts
stand in (never for mature text). Media components use the media lane: their experts, each of the right modality
(image, video, speech, music, sound), via OpenRouter, Hugging Face, ElevenLabs, Comfy Cloud or Featherless AI.

Checks the router enforces:
- P8: an evaluation component never runs on the same model that wrote what it judges.
- P10: mature text is written only by an Uncensored model on a mature provider; mature media only by an open model on
  Comfy Cloud, the one media provider whose terms allow lawful mature content (fal.ai and OpenRouter don't). An evaluation component tries its own
  experts first; if they refuse mature text, its Mature Fallback (a database column) takes over.
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
    mature_writer_providers: list
    mature_media_providers: list


def load_routing(path=ROUTING_PATH) -> Routing:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return Routing(raw["providers"], raw["lanes"]["general"]["providers"], raw["lanes"]["prose"]["providers"],
                   raw["mature"]["writer_providers"], raw["mature"]["media_providers"])


def route(model, routing: Routing) -> str:
    """Where the call goes: the route for the model's provider."""
    try:
        return routing.providers[model.provider]
    except KeyError:
        raise RoutingError(f"{model.name}: no route for provider {model.provider!r}") from None


def experts(c, reg: Registry) -> list:
    """[(slot, model)] for a component: Primary, Comparable, then its Fallback (the database's Fallback Model, or
    the Primary's roster Fallback when that is empty) if it is another model. A component whose Author-chosen primary
    is open-weight starts with its Comparable as Primary."""
    cand = c.candidates or {}
    try:
        frontier, comparable = reg.resolve(cand.get("frontier")), reg.resolve(cand.get("open_weight"))
        line = [("primary", comparable)] if cand.get("primary") == "open_weight" else \
            [(s, m) for s, m in (("primary", frontier), ("comparable", comparable)) if m]
        if line:
            fb = reg.resolve(cand.get("fallback") or line[0][1].fallback)   # the component's own, else the roster's
            if fb and fb.key not in {m.key for _, m in line}:
                line.append(("fallback", fb))
    except RegistryError as e:
        raise RoutingError(f"{c.name}: {e}") from None
    return line


def mature_ok(model, routing: Routing) -> bool:
    return model.uncensored and model.provider in routing.mature_writer_providers


def writer_models(c, reg: Registry, routing: Routing, genre: str | None = None, mature: bool = False) -> list:
    """The models that may write for this component, in the order the router tries them."""
    if c.is_evaluation:
        raise RoutingError(f"{c.name} is an evaluation component; use choose_checker")
    if c.makes_media:
        models = [m for _, m in experts(c, reg)]
        wrong = [m.name for m in models if not m.modality]
        if wrong:
            raise RoutingError(f"{c.name}: {', '.join(wrong)} makes text, not media")
        if mature:          # only open models on a provider whose terms allow lawful mature media (Comfy)
            models = [m for m in models if m.open_weights and m.provider in routing.mature_media_providers]
            if not models:
                raise RoutingError(f"{c.name}: no open model on {', '.join(routing.mature_media_providers)} "
                                   f"among its experts for mature media")
        return models
    if c.writes_prose:
        tuned = [m for m in (reg.for_genre(genre) if genre else []) if m.provider in routing.prose_providers]
        if mature:
            tuned = [m for m in tuned if mature_ok(m, routing)]
            if not tuned:
                raise RoutingError(f"{c.name}: no mature-tier model is tagged for {genre or 'this genre'} "
                                   f"(Uncensored, on {', '.join(routing.mature_writer_providers)})")
            return tuned
        return tuned or [m for _, m in experts(c, reg)]
    models = [m for _, m in experts(c, reg)]
    if mature:
        models = [m for m in models if mature_ok(m, routing)]
        if not models:
            raise RoutingError(f"{c.name}: mature text needs a mature-tier model, and none is assigned")
    return models


def choose_writer(c, reg: Registry, routing: Routing, genre: str | None = None, mature: bool = False, down=()):
    for m in writer_models(c, reg, routing, genre, mature):
        if m.key not in down:
            return m
    raise RoutingError(f"{c.name}: every model that may write this is unavailable")


def choose_checker(judge, writer, reg: Registry, routing: Routing, mature: bool = False, refused=(), down=()):
    """The model an evaluation component runs on to judge text written by `writer`: its experts in order, then,
    for mature text they all refused, its Mature Fallback. A model is skipped if it is the writer
    itself (P8), is down, or has refused."""
    if not judge.is_evaluation:
        raise RoutingError(f"{judge.name} judges nothing; it is not an evaluation component")
    tried = [m for _, m in experts(judge, reg)]
    if mature and all(m.key in refused or m.key in down or m.key == writer.key for m in tried):
        if not judge.mature_fallback:
            raise RoutingError(f"{judge.name}: its Mature Fallback is still open, so mature work can't be judged yet")
        tried.append(reg.resolve(judge.mature_fallback))
    reasons = []
    for m in tried:
        if m.key in down or m.key in refused:
            reasons.append(f"{m.name} is {'down' if m.key in down else 'refusing'}")
        elif m.key == writer.key:
            reasons.append(f"{m.name} wrote the text")
        else:
            return m
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
            if wl and wl[0][1].key == jm.key:
                out.append(f"{judge.name} and {writer.name} both have {jm.name} as Primary")
    return out
