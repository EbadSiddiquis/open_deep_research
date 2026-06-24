# Compare prompt — reconcile a fresh research pass against the prior report

> Use this AFTER an independent research pass has produced its own findings.
> Attach: this file + `report.md` (prior) + `audit/sources.json` + `audit/claims.json`
> + `audit/conflicts.json`, plus the NEW report you just generated.

## Task

You are auditing two independent research efforts that answered the same questions
(`questions.md`). Compare the PRIOR report (`report.md`, backed by `audit/claims.json`
and `audit/sources.json`) against the NEW findings I'm providing.

For each load-bearing regulatory value, produce a row:

| Item | Prior value (+ citation) | New value (+ citation) | Agree? | If not, which is right & why |
|------|--------------------------|------------------------|--------|------------------------------|

Cover at minimum:
- Houston FOG governing section + pump-out trigger + cleaning interval(s)
- Dallas / San Antonio (SAWS) / Austin trigger % and interval, with citations
- Whether "25% / 90-day" is universal or varies (and which city deviates)
- TCEQ TAC chapter/section for transporter registration + the trip-ticket fields,
  signers, and retention rules

## Rules

1. **Treat the prior report as a claim to test, not as ground truth.** Where it cites a
   primary source in `audit/sources.json`, check the value against that source's excerpt.
2. **Flag every disagreement** — a different number, a different section citation, a
   different measurement basis (e.g. "wetted height" vs "design capacity" vs "% volume").
3. **Re-examine the items the prior run marked weak**: anything `unresolved` or
   `confidence: low` in `audit/claims.json` (e.g. the $10 sticker fee, claim c13), and the
   one entry in `audit/conflicts.json` (30 TAC §312 "Subchapter F vs G").
4. **Don't invent agreement.** If you couldn't verify a value in either source set, say so.
5. End with: (a) values both passes confirm (safe to hardcode), (b) values that conflict
   (need a tiebreak / primary re-check), (c) values neither pass could verify.
