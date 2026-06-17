# Claude.ai Project setup — "Deep Research"

This folder turns the deep-research workflow into a **Claude.ai Project** so that
*any* chat inside that Project uses the methodology as its source of truth — a
persistent workspace you can return to and use as a cheat sheet.

> I (Claude Code) can't create the Project for you — that's done in the claude.ai
> web UI. These two files are everything you paste/upload.

## Steps (one-time, ~3 minutes)

1. Go to **claude.ai → Projects → Create Project**. Name it **"Deep Research"**.
2. Open the Project's **"Set custom instructions"** (or "Instructions") box and
   paste the entire contents of [`project-instructions.md`](./project-instructions.md).
3. In the Project's **knowledge** panel ("Add content" / upload), upload
   [`knowledge-deep-research.md`](./knowledge-deep-research.md) (or copy-paste it
   as a text knowledge item).
4. Save. Now start any chat inside the Project and say e.g.
   *"Deep-research, standard depth: <your question>"* — it follows the methodology.

## Important difference from Claude Code

The claude.ai Project **does not have the local `research-tools` MCP server** and
does not save to `.research_runs/`. It uses claude.ai's built-in web search for
sources and produces the report **in the chat**. The *methodology* (clarify →
plan → search → verify → cite → flag gaps) is identical; only the storage/tooling
differs. For the full tool-backed pipeline with saved `report.md` + `sources.json`,
use `/deep-research` in Claude Code in this repo.

## Keeping it in sync

The single source of truth is `../../DEEP_RESEARCH_GUIDE.md` and the live skill at
`../../.claude/skills/deep-research/SKILL.md`. If you change the methodology there,
re-paste `project-instructions.md` into the Project.
