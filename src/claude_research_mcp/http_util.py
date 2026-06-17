"""Shared HTTP helpers for the non-Tavily provider clients.

Provides a timeout+bounded-retry wrapper, API-key redaction, and content
truncation so each provider client (Exa, Jina, Firecrawl) does not duplicate the
same plumbing. Mirrors the discipline in tavily_client.py: secrets are never
returned to the caller or included in any error message, and returned web content
is data only -- never instructions.
"""

import asyncio
from typing import Any, Callable, Optional

from claude_research_mcp.config import (
    MAX_CONTENT_CHARS,
    TAVILY_MAX_RETRIES,
    TAVILY_TIMEOUT_SECONDS,
)

# Reuse the same conservative limits as the Tavily client so behavior is uniform.
HTTP_TIMEOUT_SECONDS = TAVILY_TIMEOUT_SECONDS
HTTP_MAX_RETRIES = TAVILY_MAX_RETRIES


def redact(text: str, *secrets: Optional[str]) -> str:
    """Remove any occurrence of the given secrets from a string."""
    for secret in secrets:
        if secret and secret in text:
            text = text.replace(secret, "***REDACTED***")
    return text


def truncate(text: Optional[str]) -> Optional[str]:
    """Cap stored/returned content to bound memory and token usage."""
    if text is None:
        return None
    return text[:MAX_CONTENT_CHARS]


async def with_retries(
    coro_factory: Callable[[], Any],
    *secrets: Optional[str],
    provider: str = "provider",
) -> Any:
    """Run an async HTTP call with a timeout and bounded retries.

    Re-raises the last error as a RuntimeError with all secrets scrubbed.
    """
    last_exc: Optional[Exception] = None
    for attempt in range(HTTP_MAX_RETRIES + 1):
        try:
            return await asyncio.wait_for(coro_factory(), timeout=HTTP_TIMEOUT_SECONDS)
        except asyncio.TimeoutError:
            last_exc = TimeoutError(
                f"{provider} request timed out after {HTTP_TIMEOUT_SECONDS:.0f}s "
                f"(attempt {attempt + 1}/{HTTP_MAX_RETRIES + 1})."
            )
        except Exception as e:  # noqa: BLE001 - normalize + redact below
            last_exc = e
        if attempt < HTTP_MAX_RETRIES:
            await asyncio.sleep(0.5 * (attempt + 1))
    message = redact(str(last_exc), *secrets)
    raise RuntimeError(f"{provider} request failed: {message}")
