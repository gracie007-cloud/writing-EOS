"""Load models, steps and keys, and refuse any setup that breaks the hard rules."""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
RUNS_DIR = ROOT / "runs"
TEST_PACK = DATA_DIR / "Run01_TestPack.md"
TEST_PACK_RULES = DATA_DIR / "Run01_rules.yaml"   # prose-check rules for this test pack's book only
SLOP_LISTS = CONFIG_DIR / "slop.yaml"             # generic prose-check lists

SECTIONS = ("A", "B", "C", "D", "E")
DEFAULT_CONCURRENCY = 2


class ConfigError(Exception):
    """The configuration breaks a rule; nothing is sent."""


@dataclass(frozen=True)
class Model:
    key: str
    provider: str
    family: str
    weights: str
    mature_ok: bool
    id: str | None = None
    price_in: float | None = None   # USD per million input tokens
    price_out: float | None = None  # USD per million output tokens
    endpoint_url: str | None = None
    price_per_hour: float | None = None

    @property
    def verified(self) -> bool:
        """True once the placeholder ID has been replaced with a real one."""
        return bool(self.id) and not self.id.strip().upper().startswith("VERIFY")


@dataclass(frozen=True)
class Step:
    name: str
    task_type: str
    sections: tuple[str, ...]
    template: Path
    output: str
    temperature: float
    max_tokens: int
    scoring: str
    candidates: tuple[str, ...]
    schema: dict | None = None
    selector_kind: str | None = None
    reasoning_max_tokens: int = 0   # thinking budget on top of max_tokens (the answer budget)
    extra: dict = field(default_factory=dict)

    @property
    def request_max_tokens(self) -> int:
        """What is sent to the provider: answer budget plus thinking budget."""
        return self.max_tokens + self.reasoning_max_tokens


def load_keys() -> dict[str, str]:
    """Read keys from .env in the harness folder, then config/.env.

    Values already set in the environment win. Lines that are not NAME=value
    are ignored silently, and no value is ever printed.
    """
    logging.getLogger("dotenv.main").setLevel(logging.ERROR)
    keys: dict[str, str] = {}
    for path in (ROOT / ".env", CONFIG_DIR / ".env"):
        if not path.is_file():
            continue
        for name, value in dotenv_values(path).items():
            if value and re.fullmatch(r"[A-Z_][A-Z0-9_]*", name or "") and name not in keys:
                keys[name] = value
    for name in list(keys):
        if os.environ.get(name):
            keys[name] = os.environ[name]
    for name in ("OPENROUTER_API_KEY", "HF_TOKEN", "HF_ENDPOINT_CUSTOM", "HF_ENDPOINT_BASELINE"):
        if name not in keys and os.environ.get(name):
            keys[name] = os.environ[name]
    return keys


def _read_yaml(path: Path) -> dict:
    if not path.is_file():
        raise ConfigError(f"Missing config file: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_models(path: Path = CONFIG_DIR / "models.yaml") -> dict[str, Model]:
    raw = _read_yaml(path).get("models") or {}
    models: dict[str, Model] = {}
    for key, spec in raw.items():
        try:
            models[key] = Model(
                key=key,
                provider=spec["provider"],
                family=spec["family"],
                weights=spec.get("weights", ""),
                mature_ok=bool(spec.get("mature_ok", False)),
                id=spec.get("id"),
                price_in=spec.get("price_in"),
                price_out=spec.get("price_out"),
                endpoint_url=spec.get("endpoint_url"),
                price_per_hour=spec.get("price_per_hour"),
            )
        except KeyError as exc:
            raise ConfigError(f"models.yaml: model '{key}' is missing '{exc.args[0]}'") from None
    return models


def load_steps(models: dict[str, Model], path: Path = CONFIG_DIR / "steps.yaml") -> dict[str, Step]:
    doc = _read_yaml(path)
    raw = doc.get("steps") or {}
    default_reasoning = int((doc.get("reasoning") or {}).get("default_max_tokens", 0))
    known = {"task_type", "sections", "template", "output", "temperature", "max_tokens",
             "scoring", "candidates", "schema", "selector_kind", "reasoning_max_tokens"}
    steps: dict[str, Step] = {}
    for name, spec in raw.items():
        try:
            step = Step(
                name=name,
                task_type=spec["task_type"],
                sections=tuple(spec["sections"]),
                template=ROOT / spec["template"],
                output=spec["output"],
                temperature=float(spec["temperature"]),
                max_tokens=int(spec["max_tokens"]),
                scoring=spec["scoring"],
                candidates=tuple(spec.get("candidates") or ()),
                schema=spec.get("schema"),
                selector_kind=spec.get("selector_kind"),
                reasoning_max_tokens=int(spec.get("reasoning_max_tokens", default_reasoning)),
                extra={k: v for k, v in spec.items() if k not in known},
            )
        except KeyError as exc:
            raise ConfigError(f"steps.yaml: step '{name}' is missing '{exc.args[0]}'") from None
        validate_step(step, models)
        steps[name] = step
    return steps


def validate_step(step: Step, models: dict[str, Model]) -> None:
    """Hard rules that can be checked before anything runs."""
    unknown = [s for s in step.sections if s not in SECTIONS]
    if unknown:
        raise ConfigError(f"Step '{step.name}': unknown sections {unknown}")
    if "E" in step.sections and "C" in step.sections:
        raise ConfigError(
            f"Step '{step.name}': Section E (seeded brief) may never be sent with Section C (clean brief)."
        )
    if "ANSWER_KEY" in str(step.template).upper():
        raise ConfigError(f"Step '{step.name}': the template path points at an answer key.")
    if not step.template.is_file():
        raise ConfigError(f"Step '{step.name}': template not found: {step.template.relative_to(ROOT)}")
    for key in step.candidates:
        if key not in models:
            raise ConfigError(f"Step '{step.name}': candidate '{key}' is not in models.yaml")
        if "D" in step.sections and not models[key].mature_ok:
            raise ConfigError(
                f"Step '{step.name}' sends Section D (mature) but candidate '{key}' is not mature_ok."
            )


def load_all() -> tuple[dict[str, Model], dict[str, Step]]:
    models = load_models()
    return models, load_steps(models)


GENERIC_CHECK_LISTS = ("stock_phrases", "injury_vocabulary_limit")
TEST_PACK_CHECK_LISTS = ("pov_character", "auto_fail_terms", "victim_names_in_pov_speech", "pov_emotion_words",
                         "dignity_required")


def load_prose_checks(slop_path: Path = SLOP_LISTS, rules_path: Path = TEST_PACK_RULES) -> dict:
    """Merge the generic slop lists with the test pack's own rules; each file may hold only its own lists."""
    if "ANSWER_KEY" in str(rules_path).upper() or "ANSWER_KEY" in str(slop_path).upper():
        raise ConfigError("Refused: prose checks never read the answer key.")
    generic, book = _read_yaml(slop_path), _read_yaml(rules_path)
    for name, data, allowed, home in ((slop_path.name, generic, GENERIC_CHECK_LISTS, "the test pack's rules file"),
                                      (rules_path.name, book, TEST_PACK_CHECK_LISTS, "config/slop.yaml")):
        stray = [k for k in data if k not in allowed]
        if stray:
            raise ConfigError(f"{name} may not hold {', '.join(stray)}; that belongs in {home}.")
    return {**generic, **book}
