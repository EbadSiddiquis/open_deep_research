---
description: Run a cited, multi-source deep-research report (Claude-native, Tavily-optional)
argument-hint: [quick|standard|deep] <research question>
---

Run the **deep-research** workflow for the request below.

Request: $ARGUMENTS

Follow the `deep-research` skill exactly:

1. If the first word of the request is `quick`, `standard`, or `deep`, use it as
   the depth preset and strip it from the question. Otherwise default to
   `standard`.
2. Clarify only if the question is genuinely unanswerable as written (ask 1–3
   focused questions, then continue).
3. Use the local `research-tools` MCP server for run creation, search, source
   and claim storage, deduplication, status, and saving the report.
4. Honor the preset limits, the source-quality rules, and the prompt-injection
   safety rules in the skill. Limits are ceilings — use fewer when the question
   is simple.
5. Produce a cited Markdown report, save it with `save_report`, and tell me the
   `run_id` and the path under `.research_runs/<run-id>/`.

If Tavily is not configured, fall back to native web search or my provided
URLs/documents — never switch to another search API.
