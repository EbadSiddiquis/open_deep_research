# TX FOG / grease-trap & TCEQ transporter regs — research audit bundle

Tracked copy of deep-research run `20260624-201024-tx-fog-grease-trap-tceq-regs-bda74e`
(run executed 2026-06-24). The live run folder lives under the gitignored
`.research_runs/` tree; this is the version-controlled snapshot of its audit trail.

## Contents

| Path | Role |
|------|------|
| `report.md` | The cited research report — the answer (exec summary, per-subquestion findings, "couldn't resolve" section, sources). **Start here.** |
| `audit/run.json` | Run identity: run id, exact question, depth, timestamp. |
| `audit/request.md` | The original request, verbatim. |
| `audit/plan.json` | Research brief (goal, scope, source-preference rules) + the 3 subquestions. |
| `audit/sources.json` | Evidence ledger — 15 sources, each with an id (`sq1-s1`…), url, publisher, excerpt, query. |
| `audit/claims.json` | Verification ledger — 13 claims (c1–c13) with classification, confidence, and supporting/contradicting source ids. |
| `audit/conflicts.json` | The one flagged source disagreement (30 TAC §312 "Subchapter F vs G" labeling) — now resolved; see `verification/`. |
| `audit/notes.md` | Scratch notes (empty this run). |

## Verification (`verification/`)

An independent second research pass (run `20260624-205425-tx-fog-grease-trap-verify-57bf0a`)
re-answered the same questions blind to this report, then diffed the results.
**Outcome: zero contradictions; the two previously-weak items were upgraded to verified.**

| Path | Role |
|------|------|
| `verification/comparison-report.md` | The diff: prior report vs. independent pass, item by item. |
| `verification/audit/` | The verification run's provenance (run.json, request.md, sources.json). |

Resolved by this pass: the **$10 TCEQ sticker fee** (now verbatim § 312.142(j); claim c13 upgraded
`unresolved`→`fact`) and the **30 TAC §312 "Subchapter F vs G"** conflict (resolved toward **Subchapter F**).

## How to verify any value

1. Find the figure in `report.md`.
2. Locate the backing claim in `audit/claims.json` → read its `supporting_source_ids`.
3. Resolve those ids in `audit/sources.json` to the actual URL + excerpt.
4. Check `confidence` — anything `low`/`unresolved` is a soft value. After the verification pass,
   the only remaining open items are documentation-level (raw SOS/Municode subsection text), not values.

## Deliverables (`migrations/`)

The runnable schema derived from this research — PostgreSQL migrations for the
`trucks` / `trip_tickets` / `custody_events` custody schema (30 TAC §312.142/§312.145)
and the `jurisdiction_fog_rules` config table seeded with the 4 cities. See
`migrations/README.md` for apply/rollback commands and caveats.

| Path | Role |
|------|------|
| `migrations/0001_custody_schema.up.sql` / `.down.sql` | TCEQ custody/manifest schema + enums |
| `migrations/0002_jurisdiction_fog_rules_and_seed.up.sql` / `.down.sql` | per-city FOG rules table + 4-city seed + sample trip ticket |

Copy these into the product repo's `migrations/` directory and renumber to fit its
sequence when wiring up.
