"""Environment configuration for the Claude-native research MCP server.

Tavily is the default search/extract API and is entirely optional. Three further
optional retrieval backends can be enabled with their own keys: Exa (semantic
search), Firecrawl (deep extraction), and Jina Reader (clean-markdown extraction,
which also works keyless). The server starts and all non-search tools work
whether or not any of these are set. No model-provider API key is read or
required -- these are retrieval backends only; Claude remains the reasoner.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load a local .env if present. Never log its contents.
load_dotenv()

DEFAULT_RUNS_DIR = ".research_runs"
DEFAULT_MAX_RESULTS = 5
DEFAULT_SEARCH_DEPTH = "advanced"

# Hard safety limits (not user-tunable) to keep this a personal, local tool.
TAVILY_TIMEOUT_SECONDS = 30.0
TAVILY_MAX_RETRIES = 2
# Cap on stored/returned content per source to bound memory and token usage.
MAX_CONTENT_CHARS = 50_000


@dataclass(frozen=True)
class Settings:
    """Resolved runtime settings for the server."""

    tavily_api_key: str | None
    tavily_max_results: int
    tavily_search_depth: str
    runs_dir: str
    exa_api_key: str | None = None
    firecrawl_api_key: str | None = None
    jina_api_key: str | None = None

    @property
    def tavily_configured(self) -> bool:
        """Whether a non-empty Tavily API key is available."""
        return bool(self.tavily_api_key and self.tavily_api_key.strip())

    @property
    def exa_configured(self) -> bool:
        """Whether a non-empty Exa API key is available."""
        return bool(self.exa_api_key and self.exa_api_key.strip())

    @property
    def firecrawl_configured(self) -> bool:
        """Whether a non-empty Firecrawl API key is available."""
        return bool(self.firecrawl_api_key and self.firecrawl_api_key.strip())

    @property
    def jina_configured(self) -> bool:
        """Whether a Jina API key is available (Jina Reader also works keyless)."""
        return bool(self.jina_api_key and self.jina_api_key.strip())


def _int_env(name: str, default: int) -> int:
    """Read an int env var, falling back to the default on any bad value."""
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def load_settings() -> Settings:
    """Build Settings from the current environment.

    Reads TAVILY_*, EXA_API_KEY, FIRECRAWL_API_KEY, JINA_API_KEY, and
    RESEARCH_RUNS_DIR. All API keys are held in memory and must never be echoed
    back to the client or written into a run folder.
    """
    return Settings(
        tavily_api_key=os.environ.get("TAVILY_API_KEY") or None,
        tavily_max_results=_int_env("TAVILY_MAX_RESULTS", DEFAULT_MAX_RESULTS),
        tavily_search_depth=(
            os.environ.get("TAVILY_SEARCH_DEPTH") or DEFAULT_SEARCH_DEPTH
        ).strip(),
        runs_dir=(os.environ.get("RESEARCH_RUNS_DIR") or DEFAULT_RUNS_DIR).strip(),
        exa_api_key=os.environ.get("EXA_API_KEY") or None,
        firecrawl_api_key=os.environ.get("FIRECRAWL_API_KEY") or None,
        jina_api_key=os.environ.get("JINA_API_KEY") or None,
    )
