"""Model access. Phase 1: OpenRouter only (Hugging Face endpoints arrive in Phase 4)."""

from __future__ import annotations

import time
from dataclasses import dataclass

import httpx

OPENROUTER_URL = "https://openrouter.ai/api/v1"
MAX_RETRIES = 2            # never more than two retries (CLAUDE.md rule 8)
RETRYABLE = {408, 409, 425, 429, 500, 502, 503, 504}


@dataclass
class CallResult:
    text: str | None
    input_tokens: int | None
    output_tokens: int | None
    cost_usd: float | None
    cost_source: str | None   # "openrouter" | "generation_lookup" | None
    finish_reason: str | None
    latency_s: float
    attempts: int
    generation_id: str | None = None
    error: str | None = None
    reasoning: str | None = None
    reasoning_tokens: int | None = None


def build_body(model_id: str, prompt: str, temperature: float, max_tokens: int,
               reasoning_max_tokens: int = 0) -> dict:
    """Request body. `max_tokens` is the answer budget; thinking gets its own budget on top."""
    body = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens + reasoning_max_tokens,
        "usage": {"include": True},
    }
    if reasoning_max_tokens:
        body["reasoning"] = {"max_tokens": reasoning_max_tokens, "exclude": False}
    return body


class OpenRouterClient:
    def __init__(self, api_key: str, timeout: float = 600.0, sleep=time.sleep):
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is not set. Add it to .env in the harness folder.")
        self._sleep = sleep
        self._http = httpx.Client(
            base_url=OPENROUTER_URL,
            timeout=httpx.Timeout(timeout, connect=30.0),
            headers={
                "Authorization": f"Bearer {api_key}",
                "X-Title": "Writing EOS bake-off",
            },
        )

    def close(self) -> None:
        self._http.close()

    def chat(self, model_id: str, prompt: str, temperature: float, max_tokens: int,
             reasoning_max_tokens: int = 0) -> CallResult:
        body = build_body(model_id, prompt, temperature, max_tokens, reasoning_max_tokens)
        attempts = 0
        last_error = None
        while attempts <= MAX_RETRIES:
            attempts += 1
            started = time.perf_counter()
            try:
                response = self._http.post("/chat/completions", json=body)
            except httpx.HTTPError as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                if attempts <= MAX_RETRIES:
                    self._sleep(2 ** attempts)
                    continue
                break
            latency = time.perf_counter() - started

            if response.status_code in RETRYABLE and attempts <= MAX_RETRIES:
                last_error = f"HTTP {response.status_code}: {_error_text(response)}"
                self._sleep(_retry_after(response, 2 ** attempts))
                continue
            if response.status_code >= 400:
                return CallResult(None, None, None, None, None, None, latency, attempts,
                                  error=f"HTTP {response.status_code}: {_error_text(response)}")

            data = response.json()
            if data.get("error"):
                last_error = f"Provider error: {_error_text(response)}"
                code = (data["error"] or {}).get("code")
                if code in RETRYABLE and attempts <= MAX_RETRIES:
                    self._sleep(2 ** attempts)
                    continue
                return CallResult(None, None, None, None, None, None, latency, attempts, error=last_error)

            choice = (data.get("choices") or [{}])[0]
            message = choice.get("message") or {}
            usage = data.get("usage") or {}
            cost = usage.get("cost")
            cost_source = "openrouter" if cost is not None else None
            generation_id = data.get("id")
            if cost is None and generation_id:
                cost = self._lookup_cost(generation_id)
                cost_source = "generation_lookup" if cost is not None else None
            details = usage.get("completion_tokens_details") or {}
            return CallResult(
                text=message.get("content"),
                input_tokens=usage.get("prompt_tokens"),
                output_tokens=usage.get("completion_tokens"),
                cost_usd=cost,
                cost_source=cost_source,
                finish_reason=choice.get("finish_reason") or choice.get("native_finish_reason"),
                latency_s=latency,
                attempts=attempts,
                generation_id=generation_id,
                reasoning=_reasoning_text(message),
                reasoning_tokens=details.get("reasoning_tokens"),
            )
        return CallResult(None, None, None, None, None, None, 0.0, attempts, error=last_error or "Unknown error")

    def _lookup_cost(self, generation_id: str) -> float | None:
        """OpenRouter publishes the final cost a moment after the call finishes."""
        for _ in range(3):
            self._sleep(1.5)
            try:
                response = self._http.get("/generation", params={"id": generation_id})
            except httpx.HTTPError:
                continue
            if response.status_code == 200:
                cost = (response.json().get("data") or {}).get("total_cost")
                if cost is not None:
                    return float(cost)
        return None


def _reasoning_text(message: dict) -> str | None:
    """Thinking text, if the provider returned it (plain field, or reasoning_details blocks)."""
    if message.get("reasoning"):
        return message["reasoning"]
    parts = [d.get("text") or d.get("summary") or "" for d in message.get("reasoning_details") or []
             if isinstance(d, dict)]
    joined = "\n\n".join(p for p in parts if p)
    return joined or None


def _retry_after(response: httpx.Response, default: float) -> float:
    try:
        return min(float(response.headers.get("retry-after", default)), 60.0)
    except ValueError:
        return default


def _error_text(response: httpx.Response) -> str:
    """A short error message from the response. Never includes request headers."""
    try:
        err = response.json().get("error")
        if isinstance(err, dict):
            return str(err.get("message") or err)[:300]
        if err:
            return str(err)[:300]
    except ValueError:
        pass
    return response.text[:300]
