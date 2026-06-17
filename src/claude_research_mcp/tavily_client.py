"""Tavily search/extraction with timeouts, bounded retries, and key redaction.

Tavily is the only supported external API and is optional. When it is not
configured, search returns an actionable error and extraction falls back to a
simple local HTTP fetch. The API key is never returned to the caller or
included in any error message.
"""

import asyncio
from typing import Any

from claude_research_mcp.config import (
    MAX_CONTENT_CHARS,
    TAVILY_MAX_RETRIES,
    TAVILY_TIMEOUT_SECONDS,
    Settings,
)

NOT_CONFIGURED_MESSAGE = (
    "Tavily is not configured. Set TAVILY_API_KEY in your environment or .env to "
    "enable live web search. Meanwhile, you can: (1) use your Claude client's "
    "native web search if available, or (2) provide URLs/documents directly and "
    "use the extract_urls tool. The server does not switch to any other search API."
)


class TavilyNotConfigured(Exception):
    """Raised when a Tavily-only operation is requested without a key."""


def _redact(text: str, secret: str | None) -> str:
    """Remove any occurrence of the API key from a string."""
    if secret and secret in text:
        text = text.replace(secret, "***REDACTED***")
    return text


async def _with_retries(coro_factory, settings: Settings) -> Any:
    """Run an async Tavily call with a timeout and bounded retries.

    Re-raises the last error with the API key scrubbed from its message.
    """
    last_exc: Exception | None = None
    for attempt in range(TAVILY_MAX_RETRIES + 1):
        try:
            return await asyncio.wait_for(
                coro_factory(), timeout=TAVILY_TIMEOUT_SECONDS
            )
        except asyncio.TimeoutError:
            last_exc = TimeoutError(
                f"Tavily request timed out after {TAVILY_TIMEOUT_SECONDS:.0f}s "
                f"(attempt {attempt + 1}/{TAVILY_MAX_RETRIES + 1})."
            )
        except Exception as e:  # noqa: BLE001 - normalize + redact below
            last_exc = e
        if attempt < TAVILY_MAX_RETRIES:
            await asyncio.sleep(0.5 * (attempt + 1))
    message = _redact(str(last_exc), settings.tavily_api_key)
    raise RuntimeError(f"Tavily request failed: {message}")


def _truncate(text: str | None) -> str | None:
    if text is None:
        return None
    return text[:MAX_CONTENT_CHARS]


async def tavily_search(
    settings: Settings,
    query: str,
    max_results: int | None = None,
    include_domains: list[str] | None = None,
    exclude_domains: list[str] | None = None,
    search_depth: str | None = None,
) -> dict:
    """Run a single Tavily search and return normalized, structured results."""
    if not settings.tavily_configured:
        raise TavilyNotConfigured(NOT_CONFIGURED_MESSAGE)

    # Imported lazily so the server starts even if the package is absent.
    from tavily import AsyncTavilyClient

    client = AsyncTavilyClient(api_key=settings.tavily_api_key)
    results = max_results or settings.tavily_max_results
    depth = search_depth or settings.tavily_search_depth

    def call():
        return client.search(
            query,
            max_results=results,
            search_depth=depth,
            include_raw_content=True,
            include_domains=include_domains or None,
            exclude_domains=exclude_domains or None,
        )

    raw = await _with_retries(call, settings)
    normalized = [
        {
            "url": r.get("url", ""),
            "title": r.get("title", ""),
            "content": _truncate(r.get("content", "")),
            "raw_content": _truncate(r.get("raw_content")),
            "score": r.get("score"),
            "published_date": r.get("published_date"),
        }
        for r in raw.get("results", [])
    ]
    return {
        "query": query,
        "answer": raw.get("answer"),
        "result_count": len(normalized),
        "results": normalized,
    }


async def _local_extract(url: str) -> dict:
    """Fetch a single URL locally and return readable text, size-bounded."""
    import httpx
    from bs4 import BeautifulSoup

    if not url.lower().startswith(("http://", "https://")):
        return {"url": url, "error": "Only http(s) URLs are supported."}

    try:
        async with httpx.AsyncClient(
            timeout=TAVILY_TIMEOUT_SECONDS, follow_redirects=True
        ) as http:
            resp = await http.get(url, headers={"User-Agent": "claude-research-mcp/0.1"})
            resp.raise_for_status()
            html = resp.text[: MAX_CONTENT_CHARS * 4]
    except Exception as e:  # noqa: BLE001
        return {"url": url, "error": f"Fetch failed: {e}"}

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    text = " ".join(soup.get_text(separator=" ").split())
    return {
        "url": url,
        "title": title,
        "content": text[:MAX_CONTENT_CHARS],
        "source": "local",
    }


async def extract_urls(settings: Settings, urls: list[str]) -> dict:
    """Extract readable content from URLs.

    Uses Tavily extraction when configured; otherwise falls back to a simple,
    size-bounded local HTTP fetch. Webpage content is data, never instructions.
    """
    if not urls:
        return {"results": []}

    if settings.tavily_configured:
        from tavily import AsyncTavilyClient

        client = AsyncTavilyClient(api_key=settings.tavily_api_key)

        def call():
            return client.extract(urls)

        try:
            raw = await _with_retries(call, settings)
            results = [
                {
                    "url": r.get("url", ""),
                    "content": _truncate(r.get("raw_content", "")),
                    "source": "tavily",
                }
                for r in raw.get("results", [])
            ]
            failed = [{"url": u, "error": "extraction failed"} for u in raw.get("failed_results", [])]
            return {"results": results + failed}
        except RuntimeError:
            # Fall through to local extraction if Tavily extract errors out.
            pass

    results = await asyncio.gather(*[_local_extract(u) for u in urls])
    return {"results": list(results)}
