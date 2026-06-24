# Independent Verification Pass — Comparison Report

**Verify run:** `20260624-205425-tx-fog-grease-trap-verify-57bf0a`
**Compared against prior run:** `20260624-201024-tx-fog-grease-trap-tceq-regs-bda74e` (`docs/research/tx-fog-grease-trap-2026/report.md`)
**Method:** fresh 3-subagent research dispatched blind to the prior report (questions only, per `questions.md`), then diffed per `compare-prompt.md`.

## Verdict: zero contradictions; two prior soft-spots upgraded to verified.

| Item | Prior | Independent pass | Agree |
|------|-------|------------------|-------|
| Houston section | § 47-512 (Ch. 47 Art. XI Div. 9) | § 47-512 (Ch. 47 Art. XI Div. 9) | yes |
| Houston trigger | 25% wetted height | 25% wetted height § 47-512(c)(1) | yes |
| Houston interval | 90-day + 180-day floor | 90-day §(b) + 180-day floor §(f) | yes |
| Dallas | 25% / 90 d, § 19-126.2(c) | 25% / 90 d, § 19-126.2(c) | yes |
| SAWS | 25% wetted height / 90 d, § 34-527(b) | 25% wetted height / 90 d, § 34-527(b) | yes |
| Austin | 50% wetted height / 90 d, § 15-10-197 | 50% wetted height / 90 d, § 15-10-197 | yes |
| Universal? | interval universal, trigger varies (Austin 50%) | same | yes |
| TCEQ | 30 TAC 312; § 312.142 reg, § 312.145 manifest | same | yes |
| Trip ticket fields/signers/retention | 8 fields, 3 signers, 5-part, 5-yr, annual Jul 1 | same + §312.145(c),(d) detail | yes |

## Upgraded items
1. **$10 sticker fee** — prior run had this `unresolved`/low (claim c13, via a summarizer). Independent pass found verbatim **§ 312.142(j)**: "The commission issues authorization stickers for all registered motor transport vehicles and the fee per motor transport vehicle is $10." → now a verified fact.
2. **30 TAC §312 Subchapter F vs G** (prior `conflicts.json` entry) — independent pass independently places §§312.141–312.150 in **Subchapter F ("Liquid Waste Transporters")**, agreeing with Cornell LII against the dated RG-086 "Subchapter G" label. → resolves toward F. (Section numbers were never in dispute.)

## Additive detail (no conflict; worth folding into the data model)
- § 312.142(c): registration must be "produced and shown to the operator of the facility receiving the waste at the time of delivery."
- Yellow grease (rendered fryer grease) is EXEMPT from 30 TAC 312 — regulated under 25 TAC 221 by DSHS. Exclude yellow-grease loads from the manifest flow.
- § 312.145(d): if a transporter cannot produce its registration, the receiving facility must notify the TCEQ regional office within 3 days — candidate custody_events alert.

## Independent-pass sources
Houston: v1-s1/s2 (Municode § 47-512, Div. 9). Per-city: v2-s1..s6 (Municode, Dallas DWU FAQ, SAWS ordinance PDF, Austin Water pages, SAWS slides). TCEQ: v3-s1..s4 (§312.142, §312.145, RG-389, §312.143 header).

## Caveat on independence
Both passes drew on the same primary corpus (Municode, SAWS PDF, Cornell LII reproduction of the TAC, TCEQ RG-389). Agreement reflects convergent reading of the same primary sources, not two disjoint evidence bases — which is expected and desirable for regulatory values, but means this is corroboration of *reading accuracy*, not source diversity. Dallas and Austin verbatim *code* subsections remain pulled from official guidance citing the section rather than the raw code text in both passes (Municode JS-blocked) — the one spot where a future pull of the raw subsection would add strength.
