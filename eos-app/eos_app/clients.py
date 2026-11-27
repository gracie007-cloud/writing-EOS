"""Requests to the providers that serve chat completions: Concentrate AI, OpenRouter and Featherless AI, all
OpenAI-compatible (requirements §6.9; endpoints in routing.yaml, checked against each provider's docs 2026-11-25).

`build_request` gives the exact request one call would send: the URL, the headers and the body. The key is never
read into it: the header names the .env variable that holds the key (`Bearer ${OPENROUTER_API_KEY}`), so a request
preview, a run record or a log can show the request whole. Nothing here opens a connection; sending is the live
run's job, which waits on the Author's word and a spending cap (fixes plan, decision 6).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

ROUTING_PATH = Path(__file__).resolve().parent.parent / "config" / "routing.yaml"


@dataclass(frozen=True)
class Endpoint:
    route: str
    url: str | None
    key_env: str


def load_endpoints(path=ROUTING_PATH) -> dict:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")).get("endpoints") or {}
    return {r: Endpoint(r, e.get("url"), e["key_env"]) for r, e in raw.items()}


def build_request(endpoint: Endpoint | None, route: str, model_id: str, prompt: str, temperature: float,
                  max_tokens: int) -> dict:
    """The request for one call. `problem` says why it could not be sent as it stands, or is None."""
    problem = None
    if endpoint is None:
        problem = f"no endpoint is configured for the route {route!r} (routing.yaml, endpoints)"
    elif not endpoint.url:
        problem = f"the {route} endpoint has no URL yet (routing.yaml, endpoints)"
    key_env = endpoint.key_env if endpoint else f"{route.upper()}_API_KEY"
    return {"url": endpoint.url if endpoint else None,
            "headers": {"Authorization": f"Bearer ${{{key_env}}}", "Content-Type": "application/json"},
            "body": {"model": model_id, "messages": [{"role": "user", "content": prompt}],
                     "temperature": temperature, "max_tokens": max_tokens},
            "problem": problem}
