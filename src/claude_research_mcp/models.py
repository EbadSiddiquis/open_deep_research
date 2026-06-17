"""Pydantic data models for research runs, sources, and claims.

These schemas define the on-disk JSON shapes. They intentionally contain no
reasoning logic -- Claude fills them in; the storage layer persists them.
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field

# Allowed claim classifications. "unresolved" marks a claim whose truth value
# could not be settled from the gathered evidence.
Classification = Literal["fact", "estimate", "opinion", "inference", "unresolved"]
Confidence = Literal["high", "medium", "low"]
Depth = Literal["quick", "standard", "deep"]


class SourceRecord(BaseModel):
    """A single retrieved source.

    Fields that cannot be observed from the source must be left null/empty --
    do not invent publication dates, titles, publishers, URLs, or excerpts.
    """

    id: str
    url: str
    normalized_url: str
    title: str
    publisher: Optional[str] = None
    published_at: Optional[str] = None
    retrieved_at: str
    source_type: Optional[str] = None
    excerpt: str = ""
    raw_content: Optional[str] = None
    query: Optional[str] = None


class ClaimRecord(BaseModel):
    """A claim and the source ids that support or contradict it."""

    id: str
    claim: str
    classification: Classification
    supporting_source_ids: list[str] = Field(default_factory=list)
    contradicting_source_ids: list[str] = Field(default_factory=list)
    confidence: Confidence
    notes: str = ""


class RunMetadata(BaseModel):
    """Top-level metadata for a research run (run.json)."""

    id: str
    question: str
    depth: Depth
    name: Optional[str] = None
    created_at: str
    status: str = "active"
