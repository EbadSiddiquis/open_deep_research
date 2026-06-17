"""Tests for run creation, source/claim storage, dedup, and path safety."""

import json

import pytest

from claude_research_mcp.storage import StorageError, normalize_url

from .conftest import now_iso


def _source(id_, url, **kw):
    base = {
        "id": id_,
        "url": url,
        "normalized_url": "",
        "title": kw.get("title", "T"),
        "retrieved_at": now_iso(),
        "excerpt": kw.get("excerpt", ""),
    }
    base.update({k: v for k, v in kw.items() if k not in base})
    return base


# -- run creation ----------------------------------------------------------

def test_create_run_scaffolds_files(store, runs_dir):
    meta = store.create_run("What is X?", "standard", name="x test")
    run_dir = runs_dir / meta.id
    assert run_dir.is_dir()
    for f in ("run.json", "request.md", "plan.json", "sources.json",
              "claims.json", "conflicts.json", "notes.md"):
        assert (run_dir / f).exists()
    assert json.loads((run_dir / "sources.json").read_text()) == []
    assert meta.depth == "standard"


def test_get_metadata_roundtrip(store):
    meta = store.create_run("Q", "deep")
    again = store.get_metadata(meta.id)
    assert again.id == meta.id
    assert again.question == "Q"


# -- invalid run ids / path traversal -------------------------------------

@pytest.mark.parametrize("bad", ["../escape", "a/b", "..", "foo/../bar", "x" * 65, "", "with space"])
def test_invalid_run_ids_rejected(store, bad):
    with pytest.raises(StorageError):
        store.list_sources(bad)


def test_path_traversal_cannot_escape_base(store, runs_dir, tmp_path):
    # Even a crafted id must not resolve outside the runs directory.
    with pytest.raises(StorageError):
        store._run_dir("../../etc")  # noqa: SLF001 - testing the guard directly


def test_unknown_run_id(store):
    with pytest.raises(StorageError):
        store.status("20200101-000000-abc-123456")


# -- sources ---------------------------------------------------------------

def test_add_sources_and_list(store):
    meta = store.create_run("Q", "quick")
    res = store.add_sources(meta.id, [_source("s1", "https://Example.com/a/")])
    assert res["added"] == ["s1"]
    sources = store.list_sources(meta.id)
    assert len(sources) == 1
    # normalized_url is auto-filled when blank.
    assert sources[0]["normalized_url"] == "https://example.com/a"


def test_add_sources_validation_error(store):
    meta = store.create_run("Q", "quick")
    res = store.add_sources(meta.id, [{"id": "bad", "url": "https://x.com"}])
    assert res["added"] == []
    assert res["errors"] and res["errors"][0]["index"] == 0


def test_add_sources_skips_duplicate_ids(store):
    meta = store.create_run("Q", "quick")
    store.add_sources(meta.id, [_source("s1", "https://a.com", title="first")])
    store.add_sources(meta.id, [_source("s1", "https://a.com", title="second")])
    sources = store.list_sources(meta.id)
    assert len(sources) == 1
    assert sources[0]["title"] == "first"


def test_deduplicate_sources(store):
    meta = store.create_run("Q", "quick")
    store.add_sources(meta.id, [
        _source("s1", "https://example.com/page"),
        _source("s2", "https://www.example.com/page/?utm_source=x"),
        _source("s3", "https://other.com/"),
    ])
    res = store.deduplicate_sources(meta.id)
    assert res["kept"] == 2
    assert len(res["removed"]) == 1
    assert res["removed"][0]["duplicate_of"] == "s1"


# -- claims ----------------------------------------------------------------

def test_record_claims_and_conflicts(store):
    meta = store.create_run("Q", "standard")
    res = store.record_claims(meta.id, [
        {"id": "c1", "claim": "A", "classification": "fact",
         "supporting_source_ids": ["s1"], "contradicting_source_ids": [],
         "confidence": "high"},
        {"id": "c2", "claim": "B", "classification": "estimate",
         "supporting_source_ids": ["s1"], "contradicting_source_ids": ["s2"],
         "confidence": "low"},
    ])
    assert set(res["upserted"]) == {"c1", "c2"}
    assert res["conflicts"] == 1
    status = store.status(meta.id)
    assert len(status["conflicts"]) == 1


def test_record_claims_bad_classification(store):
    meta = store.create_run("Q", "standard")
    res = store.record_claims(meta.id, [
        {"id": "c1", "claim": "A", "classification": "nonsense",
         "confidence": "high"},
    ])
    assert res["upserted"] == []
    assert res["errors"]


def test_status_reports_gaps(store):
    meta = store.create_run("Q", "standard")
    store.record_claims(meta.id, [
        {"id": "c1", "claim": "unknown", "classification": "unresolved",
         "confidence": "low"},
    ])
    status = store.status(meta.id)
    assert len(status["evidence_gaps"]) == 1


# -- report saving ---------------------------------------------------------

def test_save_report(store, runs_dir):
    meta = store.create_run("Q", "standard")
    res = store.save_report(meta.id, "# Report\n\nbody", "report.md")
    assert res["ok"]
    assert (runs_dir / meta.id / "report.md").read_text().startswith("# Report")
    assert store.status(meta.id)["report_saved"] is True


@pytest.mark.parametrize("bad", ["../escape.md", "a/b.md", "report.exe", "rep;rm.md", "report"])
def test_save_report_rejects_bad_filenames(store, bad):
    meta = store.create_run("Q", "standard")
    with pytest.raises(StorageError):
        store.save_report(meta.id, "x", bad)


def test_save_report_allows_json(store):
    meta = store.create_run("Q", "standard")
    res = store.save_report(meta.id, "{}", "report.json")
    assert res["ok"]


# -- url normalization -----------------------------------------------------

@pytest.mark.parametrize("url,expected", [
    ("https://www.Example.com/Path/", "https://example.com/Path"),
    ("http://example.com:80/a", "http://example.com/a"),
    ("https://example.com/a?utm_source=x&b=2&a=1", "https://example.com/a?a=1&b=2"),
    ("https://example.com/a#frag", "https://example.com/a"),
    ("not a url", "not a url"),
])
def test_normalize_url(url, expected):
    assert normalize_url(url) == expected
