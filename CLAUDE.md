# Open Deep Research Repository Overview

## Claude-native deep research workspace (primary mode in this fork)

This fork's primary mode is **Claude-native**: Claude Code does all reasoning
(clarify, plan, delegate, evaluate, verify, write). A local stdio MCP server in
`src/claude_research_mcp/` provides deterministic tools only (run storage, Tavily
search, URL extraction, source/claim storage, dedup, report saving) — **no model
reasoning lives in the tools, and no model-provider API key is required**.

- Run it with the `/deep-research` command (`.claude/commands/deep-research.md`),
  which follows the methodology + presets in `.claude/skills/deep-research/SKILL.md`.
- Tavily is the only external API and is **optional** (`TAVILY_API_KEY`); without
  it, fall back to native web search or user-provided URLs — never another API.
- Reports are saved under `.research_runs/<run-id>/` (gitignored).
- Setup: `uv sync --extra claude-native`. See README "Personal quickstart".
- The original upstream LangGraph implementation below is preserved under the
  optional `legacy` extra and is unrelated to this workflow.

## Project Description
Open Deep Research is a configurable, fully open-source deep research agent that works across multiple model providers, search tools, and MCP (Model Context Protocol) servers. It enables automated research with parallel processing and comprehensive report generation.

## Repository Structure

### Root Directory
- `README.md` - Comprehensive project documentation with quickstart guide
- `pyproject.toml` - Python project configuration and dependencies
- `langgraph.json` - LangGraph configuration defining the main graph entry point
- `uv.lock` - UV package manager lock file
- `LICENSE` - MIT license
- `.env.example` - Environment variables template (not tracked)

### Core Implementation (`src/open_deep_research/`)
- `deep_researcher.py` - Main LangGraph implementation (entry point: `deep_researcher`)
- `configuration.py` - Configuration management and settings
- `state.py` - Graph state definitions and data structures  
- `prompts.py` - System prompts and prompt templates
- `utils.py` - Utility functions and helpers
- `files/` - Research output and example files

### Legacy Implementations (`src/legacy/`)
Contains two earlier research implementations:
- `graph.py` - Plan-and-execute workflow with human-in-the-loop
- `multi_agent.py` - Supervisor-researcher multi-agent architecture
- `legacy.md` - Documentation for legacy implementations
- `CLAUDE.md` - Legacy-specific Claude instructions
- `tests/` - Legacy-specific tests

### Security (`src/security/`)
- `auth.py` - Authentication handler for LangGraph deployment

### Testing (`tests/`)
- `run_evaluate.py` - Main evaluation script configured to run on deep research bench
- `evaluators.py` - Specialized evaluation functions  
- `prompts.py` - Evaluation prompts and criteria
- `pairwise_evaluation.py` - Comparative evaluation tools
- `supervisor_parallel_evaluation.py` - Multi-threaded evaluation

### Examples (`examples/`)
- `arxiv.md` - ArXiv research example
- `pubmed.md` - PubMed research example
- `inference-market.md` - Inference market analysis examples

## Key Technologies
- **LangGraph** - Workflow orchestration and graph execution
- **LangChain** - LLM integration and tool calling
- **Multiple LLM Providers** - OpenAI, Anthropic, Google, Groq, DeepSeek support
- **Search APIs** - Tavily, OpenAI/Anthropic native search, DuckDuckGo, Exa
- **MCP Servers** - Model Context Protocol for extended capabilities

## Development Commands
- `uvx langgraph dev` - Start development server with LangGraph Studio
- `python tests/run_evaluate.py` - Run comprehensive evaluations
- `ruff check` - Code linting
- `mypy` - Type checking

## Configuration
All settings configurable via:
- Environment variables (`.env` file)
- Web UI in LangGraph Studio
- Direct configuration modification

Key settings include model selection, search API choice, concurrency limits, and MCP server configurations.