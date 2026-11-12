"""Split the test pack into sections and build prompts from templates.

The step's `sections` list in steps.yaml is the only source of what a step receives.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .config import SECTIONS, Model, Step

SECTION_HEADING = re.compile(r"^## ([A-E]) ·")
PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")


class AnswerKeyError(Exception):
    """An answer key was about to be read for a prompt."""


class PromptError(Exception):
    """A prompt would break a rule; nothing is sent."""


def guard_path(path: Path | str) -> None:
    if "ANSWER_KEY" in str(path).upper():
        raise AnswerKeyError(f"Refused: '{Path(path).name}' is an answer key and may only be read by the scorer.")


def read_test_pack(path: Path) -> str:
    guard_path(path)
    return path.read_text(encoding="utf-8")


def split_sections(text: str) -> dict[str, str]:
    """Return {letter: body} for each '## X ·' section, without its heading."""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        match = SECTION_HEADING.match(line)
        if match:
            current = match.group(1)
            sections[current] = []
            continue
        if line.startswith("## "):
            current = None
            continue
        if current:
            sections[current].append(line)

    cleaned: dict[str, str] = {}
    for letter, lines in sections.items():
        while lines and (not lines[-1].strip() or lines[-1].strip() == "---"
                         or lines[-1].strip().startswith("*End of test pack")):
            lines.pop()
        while lines and not lines[0].strip():
            lines.pop(0)
        cleaned[letter] = "\n".join(lines)
    return cleaned


def check_mature(step: Step, model: Model) -> None:
    if "D" in step.sections and not model.mature_ok:
        raise PromptError(f"Refused: '{model.key}' is not mature_ok, so it may not receive Section D.")


def build_prompt(step: Step, sections: dict[str, str]) -> str:
    """Fill the step's template with only the sections the step is allowed."""
    if "E" in step.sections and "C" in step.sections:
        raise PromptError(f"Refused: step '{step.name}' would send Section E with Section C.")
    guard_path(step.template)
    template = step.template.read_text(encoding="utf-8")

    values: dict[str, str] = {}
    for letter in step.sections:
        if letter not in sections:
            raise PromptError(f"The test pack has no Section {letter}, which step '{step.name}' needs.")
        values[f"SECTION_{letter}"] = sections[letter]
    if step.schema is not None:
        values["SCHEMA"] = json.dumps(step.schema)
    if step.selector_kind:
        values["SELECTOR_KIND"] = step.selector_kind.replace("_", " ")

    def fill(match: re.Match) -> str:
        name = match.group(1)
        if name in values:
            return values[name]
        if name.startswith("SECTION_") and name[-1] in SECTIONS:
            raise PromptError(
                f"Refused: template for '{step.name}' asks for {name}, which this step may not receive."
            )
        raise PromptError(f"Template for '{step.name}' has an unknown placeholder {{{{{name}}}}}.")

    return PLACEHOLDER.sub(fill, template)


def input_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def estimate_tokens(text: str) -> int:
    """Rough token count (about four characters per token); used only for estimates."""
    return max(1, -(-len(text) // 4))
