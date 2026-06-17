"""Shared fixtures and Tavily fakes for the research MCP tests.

No test makes a real network request: the Tavily client and httpx are replaced
with in-memory fakes.
"""

import sys
import types
from datetime import datetime, timezone

import pytest

from claude_research_mcp.config import Settings
from claude_research_mcp.storage import RunStore


@pytest.fixture
def runs_dir(tmp_path):
    return tmp_path / "runs"


@pytest.fixture
def store(runs_dir):
    return RunStore(str(runs_dir))


@pytest.fixture
def settings_with_key(runs_dir):
    return Settings(
        tavily_api_key="tvly-SECRET-KEY-123",
        tavily_max_results=5,
        tavily_search_depth="advanced",
        runs_dir=str(runs_dir),
    )


@pytest.fixture
def settings_no_key(runs_dir):
    return Settings(
        tavily_api_key=None,
        tavily_max_results=5,
        tavily_search_depth="advanced",
        runs_dir=str(runs_dir),
    )


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def install_fake_tavily(monkeypatch, *, search=None, extract=None):
    """Install a fake `tavily` module exposing AsyncTavilyClient.

    `search` / `extract` are async callables (or raise) used as the client
    methods. Returns nothing; cleaned up automatically by monkeypatch.
    """

    class FakeAsyncTavilyClient:
        def __init__(self, api_key=None):
            self.api_key = api_key

        async def search(self, *args, **kwargs):
            return await search(*args, **kwargs)

        async def extract(self, *args, **kwargs):
            return await extract(*args, **kwargs)

    module = types.ModuleType("tavily")
    module.AsyncTavilyClient = FakeAsyncTavilyClient
    monkeypatch.setitem(sys.modules, "tavily", module)
