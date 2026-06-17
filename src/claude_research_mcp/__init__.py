"""Claude-native deep research MCP server.

A small, local Model Context Protocol (MCP) server that provides deterministic
research utilities (run management, Tavily search, URL extraction, source and
claim storage, deduplication, report saving) to Claude Code.

All reasoning, planning, evaluation, and writing is performed by Claude itself.
These tools only perform storage, search, extraction, normalization, and
formatting. No hosted language-model API is called from this package.
"""

__version__ = "0.1.0"
