# 🔬 Open Deep Research — Claude-native personal workspace

This is a personal fork of [Open Deep Research](https://github.com/langchain-ai/open_deep_research)
turned into a **Claude-native deep-research workspace**. Instead of calling
hosted model APIs from Python, **Claude Code itself** does all the reasoning —
clarifying, planning, delegating subquestions to subagents, evaluating sources,
finding contradictions, filling gaps, and writing the final report. A small
local **MCP server** provides the deterministic plumbing: research-run storage,
optional Tavily web search, URL extraction, source/claim storage, deduplication,
and report saving.

- **No model-provider API key required.** Reasoning runs on the Claude account
  you're signed into in Claude Code.
- **Tavily is the only external API, and it's optional.** Without it, the server
  still runs and Claude falls back to its client's native web search or to URLs
  and documents you provide.
- The original upstream LangGraph implementation is **preserved** and still
  runnable if you deliberately install the legacy dependencies (see
  [Original upstream mode](#original-upstream-mode-langgraph)).

---

## 🚀 Personal quickstart (Windows / Git Bash)

All commands below are written for **Windows Git Bash**. They also work on
macOS/Linux shells unchanged.

### 1. Install dependencies

Install [`uv`](https://docs.astral.sh/uv/) if you don't have it, then from the
repo root:

```bash
uv sync --extra claude-native
cp .env.example .env
```

This installs only the lightweight Claude-native runtime (`mcp`,
`tavily-python`, `httpx`, `beautifulsoup4`, `markdownify`). It deliberately
installs **no** model-provider SDKs.

#### Development / test tools (optional)

The test and lint toolchain (`pytest`, `pytest-asyncio`, `ruff`, `mypy`) lives
in a separate `dev` dependency-group that is **not** installed by default, so
the runtime install above stays minimal. To install the Claude-native runtime
**plus** the dev tools, add `--group dev`:

```bash
uv sync --extra claude-native --group dev
```

Verify the MCP tools (no network — everything is mocked). These commands are
written for **Windows Git Bash** and work unchanged on macOS/Linux:

```bash
uv run --group dev pytest tests/claude_research_mcp/
uv run --group dev ruff check src/claude_research_mcp tests/claude_research_mcp
```

You should see `46 passed` and `All checks passed!`. The `dev` group contains
**no** model-provider SDKs.

### 2. Authenticate Claude Code with your Claude Max account

Make sure you are signed into Claude Code with your Claude subscription:

```bash
claude          # opens Claude Code; sign in with your Claude (Max) account if prompted
```

> ⚠️ Do **not** set `ANTHROPIC_API_KEY` (or any other model-provider key) if you
> want Claude Code to use your subscription. See
> [Billing safety](#-billing-safety).

### 3. (Optional) Add a Tavily key for live web search

Edit `.env` and set your key (get one at https://www.tavily.com):

```bash
# .env
TAVILY_API_KEY=your-tavily-key
```

Leave it blank to run without live search — everything else still works.

### 4. Register the local MCP server with Claude Code

This repo ships a project-scoped `.mcp.json`, so when you open the project in
Claude Code it will offer to enable the `research-tools` server automatically.
To register it explicitly (e.g. for your user scope), run:

```bash
claude mcp add --transport stdio research-tools -- uv run python -m claude_research_mcp.server
```

Verify it's connected:

```bash
claude mcp list
```

You should see `research-tools` listed. (Tip: you can sanity-check the server
starts on its own with `uv run python -m claude_research_mcp.server` — it will
wait on stdio; press `Ctrl+C` to exit.)

### 5. Run the deep-research workflow

In Claude Code, run the project command:

```
/deep-research Compare the best practice-management systems for a small telehealth clinic
```

You can prefix the request with a depth preset:

```
/deep-research deep  Compare on-call scheduling tools for a 20-person SRE team
/deep-research quick What's the current EU AI Act timeline?
```

Claude will clarify only if essential, create a research brief, break it into
independent subquestions, delegate to subagents where helpful, search via Tavily
(or native web search / your URLs), normalize and compare sources, flag
conflicts and gaps, optionally do one more search pass, then write and save a
cited Markdown report.

### 6. Find your saved reports

Each run is stored under a gitignored folder:

```
.research_runs/<run-id>/
├── request.md      # the original request + depth
├── plan.json       # research brief + subquestions
├── sources.json    # structured SourceRecord list
├── claims.json     # structured ClaimRecord list
├── conflicts.json  # claims with contradicting sources
├── notes.md        # working notes
├── report.md       # the final cited report
└── run.json        # run metadata
```

Open the report:

```bash
ls .research_runs/
cat .research_runs/<run-id>/report.md
```

### 7. Troubleshooting

| Symptom | Fix |
|---|---|
| `research-tools` not listed in `claude mcp list` | Re-run the `claude mcp add` command from step 4 from the repo root. Make sure `uv` is on your `PATH`. |
| Search returns "Tavily is not configured" | Add `TAVILY_API_KEY` to `.env`, or proceed with native web search / provided URLs. |
| `ModuleNotFoundError: claude_research_mcp` | Run `uv sync --extra claude-native`; launch the server from the repo root so the package resolves. |
| Server won't start | Run `uv run python -m claude_research_mcp.server` directly to see the error; check Python ≥ 3.10. |
| Want to confirm tools work | `uv sync --extra claude-native --group dev` then `uv run --group dev pytest tests/claude_research_mcp/ -q` (no network, all mocked). |
| Reports not appearing | Check `RESEARCH_RUNS_DIR` in `.env`; default is `.research_runs/`. |

---

## 💳 Billing safety

- This workflow uses the **Claude account authenticated in Claude Code**. It does
  **not** call the Anthropic API (or any model API) from Python.
- Do **not** set `ANTHROPIC_API_KEY` when you want Claude Code to use your Claude
  subscription — a set key can route usage to separately-billed API credits.
- **Tavily** is a separate, optional service with its own (generous free) billing.
- Usage remains subject to the limits of your Claude subscription.

> 🔒 Privacy note: web search sends your query text to Tavily. Do not put patient,
> financial, identifying, or otherwise confidential information into search
> queries. The workflow will warn you before doing so.

---

## 🧭 How it works

The useful orchestration ideas from Open Deep Research are kept — but implemented
as **Claude instructions and Claude Code agent behavior**, not Python model calls:

| Concept | Where it lives now |
|---|---|
| Research brief | Claude writes it; stored via `update_plan` |
| Supervisor / researcher split | Claude (supervisor) delegates to Claude Code **subagents** (researchers) |
| Independent subquestions, parallel work | Subagents launched concurrently, bounded by the depth preset |
| Bounded iterations | quick / standard / deep presets (limits, not targets) |
| Source compression | Subagents return compressed, cited findings |
| Evidence verification | `record_claims` with supporting/contradicting source ids |
| Gap detection | `research_status` surfaces conflicts and `unresolved` claims |
| Final report | Claude writes it; saved via `save_report` |

The workflow itself is defined in:

- `.claude/commands/deep-research.md` — the `/deep-research` command
- `.claude/skills/deep-research/SKILL.md` — the full methodology + presets +
  source/safety rules

The MCP server lives in `src/claude_research_mcp/` and exposes these tools:
`start_research_run`, `tavily_search`, `extract_urls`, `add_sources`,
`list_sources`, `deduplicate_sources`, `record_claims`, `update_plan`,
`research_status`, `save_report`. **No model reasoning happens inside the
tools** — they only store, search, extract, normalize, and format.

### Presets (limits, not targets)

| Preset | Subquestions | Queries/subq | Sources/subq | Gap pass | Max concurrent subagents |
|---|---|---|---|---|---|
| quick | 2 | 2 | 3 | none | 1 |
| standard | 4 | 3 | 5 | 1 if justified | 2 |
| deep | 6 | 4 | 7 | 1 | 3 |

---

## Original upstream mode (LangGraph)

The original LangGraph implementation is preserved under
`src/open_deep_research/` and still works **if you deliberately install the
legacy dependencies and supply your own model-provider API keys**. It is not
required for the Claude-native workflow above.

```bash
# Install the full legacy stack (OpenAI, Anthropic, Google, Tavily, LangGraph, ...)
uv sync --extra legacy

# Provide model + search credentials in .env (e.g. OPENAI_API_KEY, TAVILY_API_KEY, ...)
# See the upstream project for the full list of supported providers.

# Launch the LangGraph server + Studio UI
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking
```

This opens LangGraph Studio. Configure models and search APIs in the
`Configuration` (`src/open_deep_research/configuration.py`). This mode **does**
call hosted model APIs and is billed accordingly.

### Evaluation (legacy)

The Deep Research Bench evaluation harness in `tests/run_evaluate.py` targets the
legacy LangGraph graph and requires the `legacy` extra plus LangSmith/model
credentials. See the upstream repository for details. It is unrelated to the
Claude-native workflow.

### Legacy Implementations 🏛️

`src/legacy/` contains two earlier upstream approaches, also requiring the
`legacy` extra:

- **`legacy/graph.py`** — plan-and-execute workflow with human-in-the-loop.
- **`legacy/multi_agent.py`** — supervisor-researcher multi-agent architecture.

---

## License

MIT — see [LICENSE](LICENSE). Original work © Lance Martin and the Open Deep
Research contributors; this fork preserves that copyright and license.
