"""Exa semantic (neural) web search, normalized to the Tavily result shape.

Exa is an optional retrieval backend. It is strong on semantic / multi-hop
queries and returns query-dependent "highlights" plus full text, which makes it a
good complement to Tavily's keyword search. When no EXA_API_KEY is set this
returns an actionable error -- it never silently switches providers.

Results are returned in the SAME shape as tavily_search so Claude can treat all
search backends uniformly: {query, answer, result_count, results:[{url, title,
content, raw_content, score, published_date}]}. Returned content is data only.
"""

from typing import Optional

from claude_research_mcp.config import Settings
from claude_research_mcp.http_util import truncate, with_retries

EXA_SEARCH_URL = "https://api.exa.ai/search"

NOT_CONFIGURED_MESSAGE = (
    "Exa is not configured. Set EXA_API_KEY in your environment or .env to enable "
    "semantic web search. The server does not switch to any other search API."
)


class ExaNotConfigured(Exception):
    """Raised when an Exa operation is requested without a key."""


async def exa_search(
    settings: Settings,
    query: str,
    max_results: Optional[int] = None,
    include_domains: Optional[list[str]] = None,
    exclude_domains: Optional[list[str]] = None,
) -> dict:
    """Run a single Exa search and return normalized, Tavily-shaped results."""
    if not settings.exa_configured:
        raise ExaNotConfigured(NOT_CONFIGURED_MESSAGE)

    import httpx

    num_results = max_results or settings.tavily_max_results
    payload: dict = {
        "query": query,
        "numResults": num_results,
        "type": "auto",  # let Exa pick neural vs keyword per query
        "contents": {
            "text": {"maxCharacters": 8000},
            "highlights": {"numSentences": 3, "highlightsPerUrl": 3},
        },
    }
    if include_domains:
        payload["includeDomains"] = include_domains
    if exclude_domains:
        payload["excludeDomains"] = exclude_domains

    async def call():
        async with httpx.AsyncClient(timeout=30.0) as http:
            resp = await http.post(
                EXA_SEARCH_URL,
                headers={
                    "x-api-key": settings.exa_api_key or "",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            resp.raise_for_status()
            return resp.json()

    raw = await with_retries(call, settings.exa_api_key, provider="Exa")

    normalized = []
    for r in raw.get("results", []):
        highlights = r.get("highlights") or []
        # The highlights are the clean, query-relevant passages; prefer them as the
        # short "content" snippet and keep full text as raw_content.
        snippet = " […] ".join(highlights) if highlights else (r.get("text") or "")
        normalized.append(
            {
                "url": r.get("url", ""),
                "title": r.get("title", ""),
                "content": truncate(snippet),
                "raw_content": truncate(r.get("text")),
                "score": r.get("score"),
                "published_date": r.get("publishedDate"),
            }
        )
    return {
        "query": query,
        "answer": None,  # Exa search returns no synthesized answer in this mode
        "result_count": len(normalized),
        "results": normalized,
        "provider": "exa",
    }
