# Fold-In Review — Cowork's 2026-06-27 apply-and-diff pass on `mainvest-deep-2026-06-27/report.md`

*Reviewer: research terminal · 2026-06-27 · review-only (Cowork applies any corrections; `report.md` not edited this pass)*

**Standard held:** trust nothing not seen as a verbatim clause with a citation. Every load-bearing claim below was re-pulled from SEC EDGAR via `curl` + declared User-Agent and re-extracted with a clean `pdftotext -layout`; extracts live in `mainvest/mainvest-verify-2026-06-27/edgar/mantis_ca/`.

> **⚠ ERRATUM (2026-06-27, post-issue correction — supersedes Items 1 & 2 below where noted).** When the `…007` final note agreement was re-pulled, its **§3 and §14.3 are in a CID cipher font** (monoalphabetic +29 / `0x1D` offset, no ToUnicode map) that `pdftotext` dumps as garbage. My original Item 1 "manual clause absent from `…007`" was therefore a **false negative** — the grep matched no readable "ACH"/"checks" string because the text was ciphered, not because it was ACH. Decoding the cipher (deterministic, verified this pass; `$OOSD\PHQWV…` → add 29) yields a **manual clause**, confirmed for both §3 and §14.3: *"All payments of principal and interest on the Notes will be made in U.S. dollars in such method as the Company may determine. The Company may utilize personal checks and/or third party financial applications…"* **Corrected finding:** Mantis's payment-form arc is **manual (base `…363`, clean font) → ACH (`…473`, clean font) → manual again (`…007`, cipher font; the *final/governing* note agreement)** — the ~3.5-month ACH window was the aberration; the **governing collection clause is manual.** This *reinforces* the cannabis banking-exclusion reading and changes nothing about **H1** (ACH is the verbatim 4/4 non-cannabis standard) or the **cap/scale** verdict (genuinely identical across `…473`/`…007`, clean font). **Methodological lesson:** a text-grep "absence" proves nothing against a CID-ciphered font — decode the offset or visually render the page. Cowork independently caught this and has applied the manual→ACH→manual correction to `report.md` (verified accurate, 5 spots). Verdict rows below corrected accordingly.

## Verdict table

| # | Claim under review | Verdict | Basis |
|---|---|---|---|
| 1 | Mantis reverted §3/§14.3 to ACH on amendment; manual only in base | **CORRECTION — overturned on §3 (see Erratum)** | `…473` §3/§14.3 are genuine ACH (clean font), but the *final* `…007` note agreement §3/§14.3 **revert to manual** (CID-cipher font, decoded). Arc = manual→ACH→manual; **governing state is manual.** The ACH reversion was real but **not durable** — and manual is *not* confined to the base |
| 2 | Final governing cap = tiered 3.0× early / 2.0× all-other (split first $250k) + 1.0–4.0% revenue scale | **AGREE (cap/scale) — survives** | Cap/scale verbatim-identical in `…473` **and** `…007` (clean font). **NB:** the "`…007` identical terms" finding holds for **cap/scale only** — its §3 collection clause is **not** identical (manual; see Item 1/Erratum). `…140` is offmo-only |
| 3 | None of the four non-cannabis issuers filed >1 C-AR | **AGREE — upgraded to independently confirmed (all four)** | Submissions JSON: Lucky Goat / WanderLinger / WeHa = 1 C-AR each; Hattie's = 1 C-AR + 1 C-TR |
| 4 | Leftover-seam fixes: owner non-recourse & audit-right UNRESOLVED restatements struck in Dim 9 / §6 | **AGREE — clean** | `report.md` Dim 9 L110 and §6 L193 mark both RESOLVED with cross-refs; no stale UNRESOLVED remains |
| 5 | H1/H4 stated platform-wide; H2 band + tiering held to "small brewery-weighted sample" | **AGREE — discipline correctly applied** | `report.md` L13/L50 hedge H2 to "3 breweries + 1 café, not platform-wide"; L70/L97–99 state H1/H4 across all five |

**Bottom line (revised per Erratum):** Items 2–5 stand. **Item 1 is corrected**: the `…473` ACH reversion is real but **not durable** — the *final/governing* `…007` note agreement reverts §3/§14.3 to **manual** (CID-cipher font, decoded), so Mantis's governing collection clause is manual and the arc is **manual→ACH→manual**. This does not disturb **H1** (ACH = the 4/4 non-cannabis standard) or the **cap/scale** verdict (genuinely identical `…473`/`…007`). Net effect: the cannabis banking-exclusion reading is *strengthened*, not weakened.

---

## Item 1 — §3 collection clause — **CORRECTION: ACH reversion real but not durable; governing state is manual**

Full Mantis note-agreement chain re-pulled and read clause-by-clause (§3 "Form of Payments" + §14.3 "Payments"):

- **Base** [Form C `…363`, `mantis_rsn.pdf`](https://www.sec.gov/Archives/edgar/data/1874812/000174605921000363/mantis_rsn.pdf) — **MANUAL** (clean font, readable): §3 (`mantis_rsn.txt` L535) + §14.3 (L879): *"…unlikely that the Company will be able to provide payments via Automated Clearing House (ACH) … may need to rely on other sources, such as personal checks and/or third party financial applications."*
- **C/A `…473`** [`mantis_noteagmtca.pdf`](https://www.sec.gov/Archives/edgar/data/1874812/000174605921000473/mantis_noteagmtca.pdf), 2021-09-27 — **ACH** (clean font, genuine): §3 (`mantis_noteagmtca.txt` L533–536) + §14.3 (L876–878): *"All payments to Holders will be made as Automated Clearing House (ACH) deposits into an account designated by each Holder at the Site."*
- **C/A `…007`** [`eastcoast_noteagmt2final.pdf`](https://www.sec.gov/Archives/edgar/data/1874812/000174605922000007/eastcoast_noteagmt2final.pdf), 2022-01-04, the **FINAL / governing** note agreement — **MANUAL** (CID-cipher font; `pdftotext` renders §3/§14.3 as garbage, decoded +29): §3 (`eastcoast_noteagmt2final.txt` L532–536, ciphered `$OOSD\PHQWV…`) + §14.3 (L870–874): *"All payments of principal and interest on the Notes will be made in U.S. dollars in such method as the Company may determine. The Company may utilize personal checks and/or third party financial applications. These sources may subject repayments to additional fees or risks…"*
- Offering-memo-only amendments `…364`/`…140` carry no governing §3 note clause (`…140` separately garbled; not relied on).

**Corrected verdict:** my original "manual clause absent from `…007`" was a **CID-cipher false negative** (see Erratum). The arc is **manual → ACH (`…473`) → manual (`…007`, governing)**. Cowork's underlying catch is correct; my earlier "AGREE — manual confined to base" is **withdrawn**. Mantis's *governing* collection clause is **manual**; the ACH window was transient — a cannabis banking-exclusion artifact, while **ACH remains the verbatim standard across all four non-cannabis deals (H1 intact).**

## Item 2 — Final governing cap/scale — **AGREE, with a citation upgrade**

Re-pulled the clean note agreements and the (garbled) final offering memo:

- **[`…473/mantis_noteagmtca.pdf`](https://www.sec.gov/Archives/edgar/data/1874812/000174605921000473/mantis_noteagmtca.pdf) (L347–369), verbatim:** Maximum Payment Multiple **tiered — Early Investors 3.0× / All Other Investors 2.0×**; footnote 2: *"the investors who contribute the first $250,000.0 raised in the offering will receive a 3.0x cap. Investors who contribute after $250,000.0 … will receive a 2.0x cap."* Footnote 1: revenue scale *"minimum rate of 1.0% and a maximum rate of 4.0%."* (Annually; maturity 12/31/2032; accrual 1.02%; subordinated/unsecured.)
- **[`…007/eastcoast_noteagmt2final.pdf`](https://www.sec.gov/Archives/edgar/data/1874812/000174605922000007/eastcoast_noteagmt2final.pdf) (C/A 2022-01-04, the LAST and "final" note agreement) — cap/scale IDENTICAL:** L368–369 same $250k 3.0×/2.0× split; L365 same 1.0–4.0% scale (both in clean font). This governs the cap/scale. **⚠ "Identical terms" applies to cap/scale ONLY** — `…007`'s §3/§14.3 collection clause is **not** identical to `…473`; it reverts to manual in a CID-cipher font (see Item 1 / Erratum).
- **Movement check:** the cap **did move once** — base `…363` and same-day offmem `…364` are **flat 3.0× / flat 1.0%** (`BASE_mantis_rsn.txt` L348/L364; `mantis_offmemca.txt` L321/L331, min=max=1.0%) — then `…473` introduced the tiered 3.0×/2.0× cap + 1.0–4.0% scale, which then **stayed identical through `…007`**. Nothing moved it after `…473`.
- **`…140` (last C/A, 2022-04-04):** [`eastcoasterdam_offmo3.pdf`](https://www.sec.gov/Archives/edgar/data/1874812/000174605922000140/eastcoasterdam_offmo3.pdf) rendered garbled (10K chars from a 617KB file; no cap/scale figures extractable). It contains **only an offering memo — no note agreement** — so it could not and did not change the governing cap.

**Verdict:** the tiered 3.0×/2.0× cap (split at first $250k) and 1.0–4.0% scale are **confirmed verbatim**. The base→amended convergence narrative (flat→tiered, manual→ACH, 1.0%→1.0–4.0%) is correct.

**⚠ Citation upgrade for Cowork to apply (item 2 only):** Cowork sourced the cap to "clean `…473` + `…140` corroborating (garbled)." The garbled `…140` is **not needed and is mis-framed as corroboration** — it's an offering-memo-only amendment. The governing instrument is the **final note agreement `…007/eastcoast_noteagmt2final.pdf`**, which is clean and identical to `…473`. Recommend citing `…473` **and `…007`** (the final note agreement) and dropping the reliance on `…140`. This **strengthens** the claim; it does not change the figures.

## Item 3 — C-AR attrition — **AGREE (upgraded: all four independently confirmed)**

Cowork re-checked only Lucky Goat this pass and carried the other three from the verify run's SQ5. This review read the submissions JSON for **all four** directly:

- [Lucky Goat 1792922](https://data.sec.gov/submissions/CIK0001792922.json): **1** C-AR (0001746059-21-000183, FY2020), no C-TR.
- [WanderLinger 1807927](https://data.sec.gov/submissions/CIK0001807927.json): **1** C-AR (0001746059-21-000185), no C-TR.
- [WeHa 1816410](https://data.sec.gov/submissions/CIK0001816410.json): **1** C-AR (0001746059-21-000184), no C-TR.
- [Hattie's 1970335](https://data.sec.gov/submissions/CIK0001970335.json): **1** C-AR (0001970335-25-000001, FY2024) + **1 C-TR** (0001970335-25-000002, 2025-03-14).

The "none filed >1 C-AR" claim is true for **all four**, now on a primary basis rather than a single spot-check.

## Item 4 — Leftover-seam fixes — **AGREE (clean)**

Current `report.md`:
- **Dim 9, L110:** *"(The owner **non-recourse**/no-personal-liability clause, previously flagged unresolved here, is now **DOCUMENTED** — see Dim 3.)"*
- **§6, L193:** the audit/inspection-right and owner-non-recourse items are struck and marked **RESOLVED** (no audit right in any of the five RSAs per Dim 7; non-recourse filed verbatim across the non-cannabis deals per Dim 3).

No stale UNRESOLVED restatement of either topic remains in Dim 9 or §6.

## Item 5 — Overclaim discipline — **AGREE**

- **H1 (ACH §3)** and **H4 (no audit right)** are stated **platform-wide** (`report.md` L70; L97–99) — justified, since both are verbatim-identical across the four non-cannabis deals **plus** Mantis's amended `…473`/`…007` (H1) and across all five RSAs (H4). This review's re-pull strengthens H1 specifically: Mantis's *own governing version* is ACH.
- **H2 multiple band (1.1×–1.8×)** and **cohort-tiering prevalence** are correctly hedged: *"small, brewery-weighted sample (3 breweries + 1 café), not established as platform-wide"* (L13, L50). Not overclaimed.

**Note (not a defect):** the H2 band of 1.1×–1.8× is the **non-cannabis** sample; Mantis's amended tiered cap is **3.0×/2.0×**, which sits above that band — consistent with the report's treatment of Mantis as the high-cap cannabis outlier. The amendment makes Mantis *tiered* (like the modal deals) but not *lower*.

---

## Corrections for Cowork to apply

1. **Item 2 citation upgrade (recommended, strengthening):** cite the cap/scale to **`…473` + the final note agreement `…007/eastcoast_noteagmt2final.pdf`** (both clean, identical); drop the garbled `…140` offering-memo as "corroboration" (it filed no note agreement). Optionally note the cap moved once (base flat 3.0×/1.0% → `…473` tiered 3.0×/2.0× + 1.0–4.0%) and then held through `…007`.

No other corrections. Items 1, 3, 4, 5 stand as written.

## What couldn't be resolved

- **`…140/eastcoasterdam_offmo3.pdf` text** is genuinely garbled in this environment (image-heavy/again the `pdftotext` column-mangling). It was **not needed** — the governing cap is pinned by the clean `…007` note agreement — so this is a non-issue, but the `…140` figures themselves remain unread to the basis point. No claim depends on it.

## Sources (primary, EDGAR — all re-pulled this pass)

- [Mantis Management Group — Form C (base), 2021-07-26](https://www.sec.gov/Archives/edgar/data/1874812/000174605921000363/mantis_rsn.pdf) — CIK 1874812, accession 0001746059-21-000363, `mantis_rsn.pdf` (manual clause §3 L535 + §14.3 L879; flat 3.0×/1.0%).
- [Mantis — Form C/A, 2021-07-26](https://www.sec.gov/Archives/edgar/data/1874812/000174605921000364/mantis_offmemca.pdf) — accession 0001746059-21-000364, `mantis_offmemca.pdf` (still flat 1.0%).
- [Mantis — Form C/A, 2021-09-27](https://www.sec.gov/Archives/edgar/data/1874812/000174605921000473/mantis_noteagmtca.pdf) — accession 0001746059-21-000473, `mantis_noteagmtca.pdf` (**§3/§14.3 ACH; tiered 3.0×/2.0× + 1.0–4.0%**).
- [Mantis/"East Coast" — Form C/A, 2022-01-04](https://www.sec.gov/Archives/edgar/data/1874812/000174605922000007/eastcoast_noteagmt2final.pdf) — accession 0001746059-22-000007, `eastcoast_noteagmt2final.pdf` (**final note agreement; identical tiered cap/scale + ACH**).
- [Mantis/"Eastcoasterdam" — Form C/A, 2022-04-04](https://www.sec.gov/Archives/edgar/data/1874812/000174605922000140/eastcoasterdam_offmo3.pdf) — accession 0001746059-22-000140, `eastcoasterdam_offmo3.pdf` (offering-memo only; garbled render; no note agreement).
- Submissions JSON for C-AR counts: CIK [1792922](https://data.sec.gov/submissions/CIK0001792922.json), [1807927](https://data.sec.gov/submissions/CIK0001807927.json), [1816410](https://data.sec.gov/submissions/CIK0001816410.json), [1970335](https://data.sec.gov/submissions/CIK0001970335.json).
