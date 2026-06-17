"""Deterministic local storage for research runs.

Responsible for run-folder creation, JSON persistence, URL normalization,
source/claim storage, deduplication, and report saving. All file access is
confined to the runs directory; run ids and filenames are validated to prevent
path traversal. No network and no model calls happen here.
"""

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic import ValidationError

from claude_research_mcp.models import ClaimRecord, RunMetadata, SourceRecord

# A run id is a short, filesystem-safe token. Anything else is rejected before
# it can touch the filesystem.
_RUN_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_FILENAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
_SLUG_RE = re.compile(r"[^a-z0-9]+")

# Query parameters that are tracking noise and should be dropped when
# normalizing URLs for deduplication.
_TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "fbclid", "mc_cid", "mc_eid", "ref", "ref_src", "igshid",
}

# Files written into every run folder.
RUN_FILE = "run.json"
REQUEST_FILE = "request.md"
PLAN_FILE = "plan.json"
SOURCES_FILE = "sources.json"
CLAIMS_FILE = "claims.json"
CONFLICTS_FILE = "conflicts.json"
NOTES_FILE = "notes.md"
REPORT_FILE = "report.md"

# Reports may only be saved with these extensions.
_ALLOWED_REPORT_SUFFIXES = {".md", ".json"}


class StorageError(Exception):
    """Raised for invalid run ids, filenames, or missing runs."""


def _now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _slugify(text: str, max_len: int = 32) -> str:
    """Turn arbitrary text into a short, lowercase, filesystem-safe slug."""
    slug = _SLUG_RE.sub("-", text.lower()).strip("-")
    return slug[:max_len].strip("-")


def normalize_url(url: str) -> str:
    """Normalize a URL for deduplication.

    Lowercases scheme and host, drops default ports and fragments, removes
    tracking query parameters, sorts the remaining parameters, and strips a
    trailing slash from the path. Returns the input unchanged if it cannot be
    parsed as an http(s) URL.
    """
    if not url:
        return url
    try:
        parts = urlsplit(url.strip())
    except ValueError:
        return url.strip()
    if parts.scheme not in ("http", "https") or not parts.netloc:
        return url.strip()

    scheme = parts.scheme.lower()
    host = parts.hostname or ""
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]
    # Preserve a non-default port only.
    netloc = host
    if parts.port and not (
        (scheme == "http" and parts.port == 80)
        or (scheme == "https" and parts.port == 443)
    ):
        netloc = f"{host}:{parts.port}"

    path = parts.path.rstrip("/") or "/"

    kept = [
        (k, v)
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if k.lower() not in _TRACKING_PARAMS
    ]
    kept.sort()
    query = urlencode(kept)

    return urlunsplit((scheme, netloc, path, query, ""))


class RunStore:
    """Manages research-run folders under a single base directory."""

    def __init__(self, runs_dir: str):
        """Store runs under the given base directory (created on first write)."""
        self.base = Path(runs_dir).resolve()

    # -- path safety -------------------------------------------------------

    def _run_dir(self, run_id: str) -> Path:
        """Resolve a run id to its folder, rejecting any traversal attempt."""
        if not _RUN_ID_RE.match(run_id or ""):
            raise StorageError(
                f"Invalid run id: {run_id!r}. Run ids may contain only letters, "
                "digits, hyphen, and underscore."
            )
        candidate = (self.base / run_id).resolve()
        # Defense in depth: the resolved path must stay inside the base dir.
        if candidate != self.base and self.base not in candidate.parents:
            raise StorageError(f"Run id resolves outside the runs directory: {run_id!r}")
        return candidate

    def _existing_run_dir(self, run_id: str) -> Path:
        run_dir = self._run_dir(run_id)
        if not run_dir.is_dir():
            raise StorageError(f"Unknown run id: {run_id!r}")
        return run_dir

    @staticmethod
    def _safe_report_name(filename: str) -> str:
        """Validate a report filename, returning the safe basename."""
        name = Path(filename).name  # strip any directory components
        if name != filename or not _FILENAME_RE.match(name):
            raise StorageError(
                f"Invalid filename: {filename!r}. Use a plain name like 'report.md'."
            )
        if Path(name).suffix.lower() not in _ALLOWED_REPORT_SUFFIXES:
            raise StorageError(
                f"Reports must end in {sorted(_ALLOWED_REPORT_SUFFIXES)}, got {name!r}."
            )
        return name

    # -- json helpers ------------------------------------------------------

    @staticmethod
    def _read_json(path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return default

    @staticmethod
    def _write_json(path: Path, data: Any) -> None:
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    # -- run lifecycle -----------------------------------------------------

    def create_run(self, question: str, depth: str, name: str | None = None) -> RunMetadata:
        """Create a new run folder and scaffold its files."""
        date_part = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        suffix = _slugify(name) if name else _slugify(question)
        short = uuid.uuid4().hex[:6]
        run_id = "-".join(p for p in (date_part, suffix, short) if p)[:64]

        run_dir = self._run_dir(run_id)
        run_dir.mkdir(parents=True, exist_ok=False)

        meta = RunMetadata(
            id=run_id,
            question=question,
            depth=depth,  # type: ignore[arg-type]  -- validated by pydantic
            name=name,
            created_at=_now_iso(),
        )
        self._write_json(run_dir / RUN_FILE, meta.model_dump())
        (run_dir / REQUEST_FILE).write_text(
            f"# Research request\n\n- **Depth:** {depth}\n- **Created:** "
            f"{meta.created_at}\n\n## Question\n\n{question}\n",
            encoding="utf-8",
        )
        self._write_json(run_dir / PLAN_FILE, {"subquestions": []})
        self._write_json(run_dir / SOURCES_FILE, [])
        self._write_json(run_dir / CLAIMS_FILE, [])
        self._write_json(run_dir / CONFLICTS_FILE, [])
        (run_dir / NOTES_FILE).write_text("# Research notes\n\n", encoding="utf-8")
        return meta

    def get_metadata(self, run_id: str) -> RunMetadata:
        """Load and return the run's metadata (run.json)."""
        run_dir = self._existing_run_dir(run_id)
        return RunMetadata(**self._read_json(run_dir / RUN_FILE, {}))

    # -- sources -----------------------------------------------------------

    def list_sources(self, run_id: str) -> list[dict]:
        """Return all stored source records for a run."""
        run_dir = self._existing_run_dir(run_id)
        return self._read_json(run_dir / SOURCES_FILE, [])

    def add_sources(self, run_id: str, sources: list[dict]) -> dict:
        """Validate and append source records, skipping exact-id duplicates."""
        run_dir = self._existing_run_dir(run_id)
        existing = self._read_json(run_dir / SOURCES_FILE, [])
        by_id = {s["id"]: s for s in existing}

        added, errors = [], []
        for i, raw in enumerate(sources):
            try:
                record = SourceRecord(**raw)
            except ValidationError as e:
                errors.append({"index": i, "error": str(e)})
                continue
            if not record.normalized_url:
                record.normalized_url = normalize_url(record.url)
            if record.id in by_id:
                continue  # do not overwrite an existing source
            by_id[record.id] = record.model_dump()
            added.append(record.id)

        merged = list(by_id.values())
        self._write_json(run_dir / SOURCES_FILE, merged)
        return {"added": added, "errors": errors, "total": len(merged)}

    def deduplicate_sources(self, run_id: str) -> dict:
        """Remove sources sharing a normalized URL, keeping the first seen."""
        run_dir = self._existing_run_dir(run_id)
        sources = self._read_json(run_dir / SOURCES_FILE, [])

        seen: dict[str, str] = {}
        kept, removed = [], []
        for s in sources:
            key = s.get("normalized_url") or normalize_url(s.get("url", ""))
            if key in seen:
                removed.append({"id": s.get("id"), "duplicate_of": seen[key]})
                continue
            seen[key] = s.get("id")
            kept.append(s)

        self._write_json(run_dir / SOURCES_FILE, kept)
        return {"kept": len(kept), "removed": removed}

    # -- claims ------------------------------------------------------------

    def record_claims(self, run_id: str, claims: list[dict]) -> dict:
        """Validate and upsert claim records by id; refresh conflicts.json."""
        run_dir = self._existing_run_dir(run_id)
        existing = self._read_json(run_dir / CLAIMS_FILE, [])
        by_id = {c["id"]: c for c in existing}

        upserted, errors = [], []
        for i, raw in enumerate(claims):
            try:
                record = ClaimRecord(**raw)
            except ValidationError as e:
                errors.append({"index": i, "error": str(e)})
                continue
            by_id[record.id] = record.model_dump()
            upserted.append(record.id)

        merged = list(by_id.values())
        self._write_json(run_dir / CLAIMS_FILE, merged)

        # A claim is a conflict when at least one source contradicts it.
        conflicts = [c for c in merged if c.get("contradicting_source_ids")]
        self._write_json(run_dir / CONFLICTS_FILE, conflicts)
        return {"upserted": upserted, "errors": errors, "conflicts": len(conflicts)}

    # -- status ------------------------------------------------------------

    def status(self, run_id: str) -> dict:
        """Summarize the current state of a run for the research_status tool."""
        run_dir = self._existing_run_dir(run_id)
        meta = self._read_json(run_dir / RUN_FILE, {})
        plan = self._read_json(run_dir / PLAN_FILE, {"subquestions": []})
        sources = self._read_json(run_dir / SOURCES_FILE, [])
        claims = self._read_json(run_dir / CLAIMS_FILE, [])
        conflicts = self._read_json(run_dir / CONFLICTS_FILE, [])

        subqs = plan.get("subquestions", []) if isinstance(plan, dict) else []
        completed = [s for s in subqs if s.get("status") == "completed"]
        pending = [s for s in subqs if s.get("status") != "completed"]
        gaps = [c for c in claims if c.get("classification") == "unresolved"]

        return {
            "run_id": meta.get("id", run_id),
            "research_brief": plan.get("brief", "") if isinstance(plan, dict) else "",
            "completed_subquestions": completed,
            "pending_subquestions": pending,
            "source_count": len(sources),
            "conflicts": conflicts,
            "evidence_gaps": gaps,
            "report_saved": (run_dir / REPORT_FILE).exists(),
        }

    def write_plan(self, run_id: str, plan: dict) -> dict:
        """Persist/replace the research brief and subquestion plan."""
        run_dir = self._existing_run_dir(run_id)
        self._write_json(run_dir / PLAN_FILE, plan)
        return {"ok": True}

    # -- report ------------------------------------------------------------

    def save_report(self, run_id: str, content: str, filename: str = REPORT_FILE) -> dict:
        """Save report content into the run folder under a validated filename."""
        run_dir = self._existing_run_dir(run_id)
        name = self._safe_report_name(filename)
        path = run_dir / name
        path.write_text(content, encoding="utf-8")
        return {"ok": True, "path": str(path), "bytes": len(content.encode("utf-8"))}
