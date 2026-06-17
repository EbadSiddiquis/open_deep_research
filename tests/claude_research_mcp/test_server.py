"""Server-level tests: starts without Tavily; tools return safe errors."""

import pytest

import claude_research_mcp.server as server
from claude_research_mcp.config import Settings
from claude_research_mcp.storage import RunStore


@pytest.fixture(autouse=True)
def isolated_server(monkeypatch, tmp_path):
    """Point the server at a temp store and a no-Tavily settings object."""
    store = RunStore(str(tmp_path / "runs"))
    settings = Settings(
        tavily_api_key=None,
        tavily_max_results=5,
        tavily_search_depth="advanced",
        runs_dir=str(tmp_path / "runs"),
    )
    monkeypatch.setattr(server, "store", store)
    monkeypatch.setattr(server, "settings", settings)
    return server


def test_server_imports_without_tavily():
    # The module imported at top without raising, even with no Tavily key.
    assert server.mcp is not None
    assert hasattr(server, "main")


async def test_search_tool_safe_error_when_unconfigured():
    out = await server.tavily_search(query="anything")
    assert out["tavily_configured"] is False
    assert "not configured" in out["error"].lower()


async def test_search_tool_rejects_empty_query():
    out = await server.tavily_search(query="   ")
    assert "error" in out


def test_full_run_lifecycle_via_tools():
    run = server.start_research_run("Best telehealth PM systems?", "standard", "telehealth")
    run_id = run["run_id"]

    server.update_plan(run_id, brief="Compare systems",
                       subquestions=[{"id": "sq1", "question": "pricing", "status": "pending"}])

    server.add_sources(run_id, [{
        "id": "s1", "url": "https://vendor.com/pricing", "normalized_url": "",
        "title": "Pricing", "retrieved_at": "2026-06-16T00:00:00Z", "excerpt": "",
    }])
    assert len(server.list_sources(run_id)["sources"]) == 1

    server.record_claims(run_id, [{
        "id": "c1", "claim": "Vendor X costs $99/mo", "classification": "fact",
        "supporting_source_ids": ["s1"], "contradicting_source_ids": [],
        "confidence": "high",
    }])

    status = server.research_status(run_id)
    assert status["source_count"] == 1
    assert status["research_brief"] == "Compare systems"
    assert len(status["pending_subquestions"]) == 1

    saved = server.save_report(run_id, "# Report\n", "report.md")
    assert saved["ok"]


def test_start_run_rejects_bad_depth():
    out = server.start_research_run("Q", "ultra")
    assert "error" in out


def test_tools_return_error_for_bad_run_id():
    assert "error" in server.list_sources("../escape")
    assert "error" in server.research_status("../escape")
    assert "error" in server.save_report("../escape", "x", "report.md")
