"""Tests for Tavily search/extract: config gating, normalization, safety."""

import asyncio
import sys
import types

import pytest

import claude_research_mcp.tavily_client as tc
from claude_research_mcp.tavily_client import (
    TavilyNotConfigured,
    extract_urls,
    tavily_search,
)

from .conftest import install_fake_tavily

# -- not configured --------------------------------------------------------

async def test_search_requires_tavily(settings_no_key):
    with pytest.raises(TavilyNotConfigured):
        await tavily_search(settings_no_key, query="anything")


# -- normalization ---------------------------------------------------------

async def test_search_normalizes_results(monkeypatch, settings_with_key):
    async def fake_search(query, **kwargs):
        return {
            "answer": "short answer",
            "results": [
                {"url": "https://a.com", "title": "A", "content": "c1",
                 "raw_content": "r1", "score": 0.9, "published_date": "2024"},
                {"url": "https://b.com", "title": "B", "content": "c2"},
            ],
        }

    install_fake_tavily(monkeypatch, search=fake_search)
    out = await tavily_search(settings_with_key, query="q", max_results=2)
    assert out["query"] == "q"
    assert out["result_count"] == 2
    assert out["results"][0]["url"] == "https://a.com"
    assert out["results"][1]["raw_content"] is None
    assert out["answer"] == "short answer"


async def test_search_truncates_long_content(monkeypatch, settings_with_key):
    monkeypatch.setattr(tc, "MAX_CONTENT_CHARS", 10)

    async def fake_search(query, **kwargs):
        return {"results": [{"url": "https://a.com", "title": "A",
                             "content": "x" * 100, "raw_content": "y" * 100}]}

    install_fake_tavily(monkeypatch, search=fake_search)
    out = await tavily_search(settings_with_key, query="q")
    assert len(out["results"][0]["content"]) == 10
    assert len(out["results"][0]["raw_content"]) == 10


# -- key redaction ---------------------------------------------------------

async def test_api_key_is_redacted_in_errors(monkeypatch, settings_with_key):
    monkeypatch.setattr(tc, "TAVILY_MAX_RETRIES", 0)

    async def fake_search(query, **kwargs):
        raise Exception(f"upstream failed for key {settings_with_key.tavily_api_key}")

    install_fake_tavily(monkeypatch, search=fake_search)
    with pytest.raises(RuntimeError) as exc:
        await tavily_search(settings_with_key, query="q")
    msg = str(exc.value)
    assert settings_with_key.tavily_api_key not in msg
    assert "REDACTED" in msg


# -- timeout ---------------------------------------------------------------

async def test_search_times_out(monkeypatch, settings_with_key):
    monkeypatch.setattr(tc, "TAVILY_TIMEOUT_SECONDS", 0.05)
    monkeypatch.setattr(tc, "TAVILY_MAX_RETRIES", 0)

    async def slow_search(query, **kwargs):
        await asyncio.sleep(1.0)
        return {"results": []}

    install_fake_tavily(monkeypatch, search=slow_search)
    with pytest.raises(RuntimeError) as exc:
        await tavily_search(settings_with_key, query="q")
    assert "timed out" in str(exc.value)


# -- rate limit ------------------------------------------------------------

async def test_search_rate_limited(monkeypatch, settings_with_key):
    monkeypatch.setattr(tc, "TAVILY_MAX_RETRIES", 0)

    async def fake_search(query, **kwargs):
        raise Exception("429 Too Many Requests")

    install_fake_tavily(monkeypatch, search=fake_search)
    with pytest.raises(RuntimeError) as exc:
        await tavily_search(settings_with_key, query="q")
    assert "429" in str(exc.value)


async def test_search_retries_then_succeeds(monkeypatch, settings_with_key):
    monkeypatch.setattr(tc, "TAVILY_MAX_RETRIES", 2)
    calls = {"n": 0}

    async def flaky_search(query, **kwargs):
        calls["n"] += 1
        if calls["n"] < 2:
            raise Exception("transient")
        return {"results": [{"url": "https://a.com", "title": "A", "content": "c"}]}

    install_fake_tavily(monkeypatch, search=flaky_search)
    out = await tavily_search(settings_with_key, query="q")
    assert out["result_count"] == 1
    assert calls["n"] == 2


# -- extraction ------------------------------------------------------------

async def test_extract_via_tavily(monkeypatch, settings_with_key):
    async def fake_extract(urls, **kwargs):
        return {"results": [{"url": urls[0], "raw_content": "extracted"}],
                "failed_results": []}

    install_fake_tavily(monkeypatch, search=None, extract=fake_extract)
    out = await extract_urls(settings_with_key, ["https://a.com"])
    assert out["results"][0]["source"] == "tavily"
    assert out["results"][0]["content"] == "extracted"


async def test_extract_empty_list(settings_no_key):
    assert await extract_urls(settings_no_key, []) == {"results": []}


async def test_extract_local_fallback(monkeypatch, settings_no_key):
    # Fake httpx so no real network call happens; bs4 stays real.
    class FakeResp:
        text = "<html><title>Hi</title><body><script>bad()</script><p>Hello world</p></body></html>"

        def raise_for_status(self):
            pass

    class FakeClient:
        def __init__(self, *a, **k):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def get(self, url, headers=None):
            return FakeResp()

    fake_httpx = types.ModuleType("httpx")
    fake_httpx.AsyncClient = FakeClient
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)

    out = await extract_urls(settings_no_key, ["https://a.com"])
    res = out["results"][0]
    assert res["source"] == "local"
    assert "Hello world" in res["content"]
    assert "bad()" not in res["content"]  # script stripped
