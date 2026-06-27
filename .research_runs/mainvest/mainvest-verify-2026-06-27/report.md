# Reg CF Revenue-Share Deal-Structure Verification — Non-Cannabis Modal Exemplars (MainVest)

*Verification run · 2026-06-27 · run-id `mainvest-verify-2026-06-27` · audits `mainvest-deep-2026-06-27/report.md`*

**Purpose.** The internal report `mainvest-deep-2026-06-27/report.md` characterizes "standard" Reg CF revenue-share deal terms from a single exemplar — **Mantis Management Group** ("Eastcoasterdam"), a **cannabis** issuer with a manual / non-ACH collection clause and no normal banking access. This pass tests that n=1 against **four non-cannabis modal issuers** pulled from SEC EDGAR (all filed via funding portal MainVest, CIK 0001746059), reads their **actual filed Revenue Sharing Notes/Agreements** verbatim, and renders verdicts H1–H4 that drive section-scoped edits to the original report.

**Facts vs. inference.** "Filed fact" = language present in an RSA/Form C exhibit (quoted with file:line from the `pdftotext -layout` extract in this run's `edgar/` folder). "Inference" = e.g., *why* the cannabis issuer used manual collection. All exhibits are independently checkable via the CIK/accession/exhibit given inline.

---

## Exemplar set (all non-cannabis; security type = Debt / Revenue Sharing Note)

| Issuer | CIK | Business | Form C (accession / date) | RSA exhibit | C-AR |
|---|---|---|---|---|---|
| **Lucky Goat Brewing LLC** (Wareham, MA) | 0001792922 | Brewery | 0001746059-19-000062 / 2019-11-05 | `luckygoat_rsn.pdf` | FY2020 (0001746059-21-000183) |
| **WanderLinger Brewing Co LLC** (Chattanooga, TN) | 0001807927 | Brewery | 0001746059-20-000097 / 2020-03-31 | `wanderlinger_noteagmt.pdf` | FY2020 (0001746059-21-000185) |
| **WeHa Brewing Company LLC** (West Hartford, CT) | 0001816410 | Brewery | 0001746059-20-000205 / 2020-07-14 | `weha_noteagmt.pdf` | FY2020 (0001746059-21-000184) |
| **Hattie's Coffee House LLC** (Whitestown, IN) | 0001970335 | Café | 0001746059-23-000075 / 2023-03-28 | `hatties_rsn.pdf` | FY2024 (0001970335-25-000001) + **C-TR** 2025-03-14 |

Cross-reference anomaly: **Mantis Management Group LLC** (CIK 0001874812), cannabis, `mantis_rsn.pdf` — the original report's sole exemplar.

---

## Executive summary

- **H1 (manual vs. ACH) — RESOLVED, Mantis is the anomaly.** All four modal RSAs, §3 "Form of Payments," say verbatim: *"All payments to Holders will be made as Automated Clearing House (ACH) deposits into an account designated by each Holder at the Site."* Mantis's note replaces that exact clause with manual/non-ACH language. **ACH is the standard; manual collection is a cannabis/banking-exclusion artifact, not a structural property of the instrument.** → The report's "structural collectibility/servicing weakness" framing should be **struck and rewritten** as issuer-specific.
- **H2 (multiple band) — RESOLVED, claim slightly off.** Documented caps: WanderLinger **1.1×**; Lucky Goat **1.35×/1.5×**; Hattie's **1.4×/1.6×**; WeHa **1.5×/1.8×**; Mantis **3.0×**. Modal range ≈ **1.1×–1.8×**, not "1.4×–2×." → Replace the uncited "1.4×–2×" with the sourced distribution; Mantis 3.0× flagged as a clear outlier.
- **H3 (guarantee/recourse) — RESOLVED, upgrade to DOCUMENTED.** Every modal offering memo: *"The Notes are not secured by any assets of the Company or any assets of persons associated with the Company,"* plus *"you will not be personally obligated for any debts of the Company."* → Owner non-recourse / no personal-or-corporate guarantee is now a **filed fact**, not RECONSTRUCTED.
- **H4 (revenue verification) — RESOLVED in the opposite direction: structural, not a Mantis quirk.** Every modal RSA defines "Total Revenue" identically and contains **no audit/inspection right and no revenue-reporting covenant**. Payments run off issuer-stated revenue with no contractual verification teeth — in *all five* deals. → The report's UNRESOLVED should be upgraded: contractually, **self-report with no audit right is the documented norm**; only the *operational* verification mechanism remains unknown.
- **Tiering — corrected.** Cohort tiering (an "Early Investors" cap vs. an "All Other Investors" cap, split at the first $20–25k raised) is a **documented standard feature** in 3 of 4 modal deals. The original report's implication that tiering wasn't a normal feature is wrong — Mantis's flat single multiple is the simpler, *non*-tiered variant.
- **Payment frequency — corroborates anomaly.** Modal deals are **quarterly** (all four); Mantis is **annual**. Mantis's annual frequency is atypical too.
- **Escrow citation — re-sourced.** The "qualified third party escrow agent" quote is **not in the Mantis offering memo**; it appears in **Mainvest Holdings Corp Form C** (CIK 1785840), `mainvestformc.pdf`, lines 391–392. The Mantis/modal memos only say *"all committed funds will be returned"* if the target isn't met. → Fix the attribution.

---

## Findings by subquestion

### SQ1 — Modal-issuer deal structure (filed facts)

All four are LLC food/beverage issuers selling **Revenue Sharing Notes** (security type "Debt," $1.00 face) via mainvest.com, on the identical Investment Agreement + Note (Exhibit A) + Revenue Sharing Agreement (Exhibit B) template. Core terms (verbatim from each note's term table):

| Term | Lucky Goat | WanderLinger | WeHa | Hattie's | *Mantis (cannabis)* |
|---|---|---|---|---|---|
| Max Payment Multiple | **1.5× early / 1.35× other** | **1.1×** (flat) | **1.8× early / 1.5× other** | **1.6× early / 1.4× other** | *3.0× (flat)* |
| Revenue % (linear, set post-close) | **5.0–10.7%** | **0.5–2.5%** | **1.3–2.6%** | **3.0–6.0%** | *1.0%* |
| Payment frequency | Quarterly | Quarterly | Quarterly | Quarterly | *Annually* |
| Collection (Form of Payments §3) | **ACH** | **ACH** | **ACH** | **ACH** | *Manual / non-ACH* |
| Seniority / Security | Subordinated / Unsecured | Subordinated / Unsecured | Subordinated / Unsecured | Subordinated / Unsecured | *Subordinated / Unsecured* |
| Payment Deadline / Maturity | 12/31/2026 | 01/01/2027 | 01/01/2027 | 12/31/2028 | *12/31/2032* |
| Accrual Rate | 1.51% | 1.53% | 0.45% | 3.65% | *1.02%* |

Sources: [Lucky Goat — Form C, 2019-11-05](https://www.sec.gov/Archives/edgar/data/1792922/000174605919000062/luckygoat_rsn.pdf) (`luckygoat_rsn.txt` L336–351, footnotes L364–369); [WanderLinger — Form C, 2020-03-31](https://www.sec.gov/Archives/edgar/data/1807927/000174605920000097/wanderlinger_noteagmt.pdf) (`wanderlinger_noteagmt.txt` L367–384); [WeHa — Form C, 2020-07-14](https://www.sec.gov/Archives/edgar/data/1816410/000174605920000205/weha_noteagmt.pdf) (`weha_noteagmt.txt` L351–384); [Hattie's — Form C, 2023-03-28](https://www.sec.gov/Archives/edgar/data/1970335/000174605923000075/hatties_rsn.pdf) (`hatties_rsn.txt` L329–365). Target/max raise sizes appear in each offering memo (`*_offmo.txt`); the revenue rate is finalized **after** close on a linear scale by amount raised (footnote 1 of each note). No minimum-payment or revenue-floor term appears in any note — payments are purely `Purchaser % × Revenue % × Total Revenue`, and a no-revenue quarter yields no payment.

### SQ2 — Manual vs. ACH (H1 verdict: **DOCUMENTED — manual is the anomaly**)

The four modal RSAs, §3 "Form of Payments," are identical and unambiguous:

> *"All payments to Holders will be made as Automated Clearing House (ACH) deposits into an account designated by each Holder at the Site."* — [Lucky Goat RSA §3](https://www.sec.gov/Archives/edgar/data/1792922/000174605919000062/luckygoat_rsn.pdf) (`luckygoat_rsn.txt` L526–528); identical at [WanderLinger](https://www.sec.gov/Archives/edgar/data/1807927/000174605920000097/wanderlinger_noteagmt.pdf) (L556–558), [WeHa](https://www.sec.gov/Archives/edgar/data/1816410/000174605920000205/weha_noteagmt.pdf) (L534–536), [Hattie's](https://www.sec.gov/Archives/edgar/data/1970335/000174605923000075/hatties_rsn.pdf) (L500–502).

Mantis occupies the **same clause slot (§3 "Form of Payments")** with the inverse text:

> *"Any repayments owned under the Revenue Sharing Note will be fully administered by the Company likely not processed by a financial institution. This means it is unlikely that the Company will be able to provide payments via Automated Clearing House (ACH) transactions, and may need to rely on other sources, such as personal checks and/or third party financial applications…"* — `mantis_rsn.txt` L532–536.

**Filed fact:** ACH is the default collection/disbursement mechanism of the instrument. **Inference (high confidence):** Mantis used the manual fallback because cannabis businesses are excluded from federally-regulated banking and ACH rails (Schedule I), so the platform templated a non-ACH variant for that issuer — a banking-exclusion artifact, not a feature of the revenue-share note itself.

### SQ3 — Multiple verification (H2 verdict: **DOCUMENTED — "1.4×–2×" is slightly high at the floor**)

Distribution of stated caps: **1.1×** (WanderLinger, flat), **1.35×** and **1.5×** (Lucky Goat tiers), **1.4×** and **1.6×** (Hattie's tiers), **1.5×** and **1.8×** (WeHa tiers), **3.0×** (Mantis, flat). The non-cannabis modal range is **≈1.1×–1.8×**; early-investor caps cluster **1.5–1.8×**, later-investor caps **1.1–1.5×**. The report's "1.4×–2× typical" overstates the floor (real floor 1.1×) and the ceiling among normal deals (1.8×, not 2.0×). **Mantis's 3.0× is the high outlier**, consistent with its long ~11-year term and cannabis risk.

### SQ4 — Tiering / EaRN (verdict: **cohort tiering is DOCUMENTED-standard; rate-band tiering & EaRN remain unseen in exhibits**)

Three of four modal notes carry a **two-tier Maximum Payment Multiple by investor cohort** — e.g.:

> *"To reward early participation, the investors who contribute the first $25,000.0 raised in the offering will receive a 1.8x cap. Investors who contribute after $25,000.0 has been raised in the offering will receive a 1.5x cap."* — [WeHa note, footnote 2](https://www.sec.gov/Archives/edgar/data/1816410/000174605920000205/weha_noteagmt.pdf) (`weha_noteagmt.txt` L386–388); same pattern at Lucky Goat (first $25k: 1.5× vs 1.35×) and Hattie's (first $20k: 1.6× vs 1.4×).

This is **time-of-entry tiering of the cap**, and it is a normal optional feature. What does **not** appear in any primary exhibit pulled is (a) **revenue-band rate tiering** (rate changing with revenue level) or (b) the **"EaRN" two-phase** escalating/de-escalating mechanism — those remain attributable only to Mainvest's (now-defunct) support center, not to a filed RSA. → The original report's framing that tiering was anomaly-specific is incorrect for cohort tiering; Mantis's flat single multiple is simply the non-tiered variant.

### SQ5 — Repayment / default behavior from C-ARs (verdict: **thin window; reporting attrition is the headline**)

The Form C-ARs are **templated issuer annual reports** (business narrative + financial statements); they contain **no Mainvest-maintained repayment ledger**, so per-note repayment pace/default cannot be read directly from them. The strongest signal is the **filing record itself**:

- **None of the four issuers filed more than one C-AR.** Lucky Goat, WanderLinger, and WeHa each filed a single FY2020 C-AR and then **stopped filing with no C-TR** (lapsed ongoing-reporting obligation). Hattie's filed one FY2024 C-AR (2025-03-06) and a **C-TR terminating reporting eight days later** (2025-03-14). [Hattie's — C-AR, 2025-03-06](https://www.sec.gov/Archives/edgar/data/1970335/000197033525000001/formcar_hattiescoffeehouse.pdf); C-TR accession 0001970335-25-000002.
- Where a C-AR exists, the business was a going concern at the report date (e.g., WanderLinger reported a new Best Brands distribution agreement and a 200-keg expansion in its FY2020 C-AR, `wanderlinger_c_ar.txt` L62, L125). Two issuers (WanderLinger 2021, WeHa 2022) ran **second raises** — a mild positive signal.

**Implication:** Reg CF's annual-report window closes within ~1–2 years (issuers lapse or terminate), well before these 5–7-year notes mature, so the filings give little visibility into late-life repayment or default — a structural limitation, not a Mantis-specific one.

### Secondary — escrow citation re-sourcing (RESOLVED)

The quote in the original report (L38–39), *"Investor funds will be held in escrow with a qualified third party escrow agent meeting the requirements of Regulation CF ('Escrow Agent') until the Target Offering Amount has been met or exceeded and one or more closings occur,"* **does not appear in the Mantis offering memo** (the memo's §G/J only describe target/refund mechanics). It appears verbatim in **[Mainvest Holdings Corp — Form C, 2022-11-03](https://www.sec.gov/Archives/edgar/data/1785840/000178584022000003/mainvestformc.pdf)** (`mainvestformc.txt` L391–392), which also carries an explicit "NOTICE REGARDING THE ESCROW AGENT" (L208–213). The Mantis and modal food/beverage memos instead state only: *"all committed funds will be returned"* if the target isn't met (`mantis_offmem.txt` L220; `luckygoat_offmo.txt` L174). → Re-attribute the escrow quote to Mainvest Holdings Corp Form C L391–392, and/or cite the Mantis "committed funds will be returned" refund language for the Mantis-specific point.

---

## Report-edit determinations (what to change and how strong)

1. **Strike "manual/non-ACH = structural weakness."** Verdict H1 = DOCUMENTED. Rewrite the bullet (orig L68–69) and align the two failure-synthesis lines: manual collection is an **issuer/banking-exclusion artifact of the cannabis exemplar**, not a property of the instrument; the standard clause is ACH. **Apply unconditionally.**
2. **Present the deal table as base → amended, amended governing, with Mantis flagged as the cannabis anomaly.** Add a column/note that the revenue rate is finalized post-close by formula, and that Mantis's terms (3.0× flat, annual, manual, 11-yr) are atypical vs. the modal ACH/quarterly/1.1–1.8× set. **Apply.**
3. **Add the prominent caveat** that the original sole exemplar is a banking-excluded cannabis issuer that may not generalize. **Apply unconditionally** (now backed by four counter-exemplars).
4. **Upgrade revenue-verification basis (H4).** Contractually, **no audit/inspection right exists in any of the five RSAs** and payments run off issuer-stated "Total Revenue"; self-report is the documented norm. Keep the *operational* verification mechanism as UNRESOLVED. **Apply as DOCUMENTED-with-residual-gap.**
5. **Resolve the no-guarantee item (H3) to DOCUMENTED.** Cite the modal memos' *"not secured by any assets of the Company or any assets of persons associated with the Company."* **Apply.**
6. **Fix the escrow citation.** Re-attribute to Mainvest Holdings Corp Form C L391–392 (and Mantis refund language). **Apply.**
7. **Correct the tiering note:** cohort tiering is standard, not anomaly-specific. **Apply** (secondary).

---

## Conflicting / weak evidence

- **"1.4×–2× typical"** is roughly central but not exact: real modal floor is **1.1×** (WanderLinger) and the non-cannabis ceiling is **1.8×** (WeHa early tier). The 2.0× upper bound and 1.4× lower bound are both slightly off; state the sourced 1.1×–1.8× band instead.
- **Tiering terminology:** the documented tiering is **investor-cohort** (time-of-entry) tiering of the *cap*; it is **not** evidence of revenue-band *rate* tiering or the EaRN two-phase mechanic, which remain support-center-only. Don't conflate them.
- **C-AR signal is indirect:** going-concern can be inferred from a filed C-AR, but **repayment pace/default cannot** — the filings carry no repayment ledger. Treat any "real-world repayment" claim as inference, not filed fact.
- **OCR caveat:** term-sheet columns are misaligned in `pdftotext` output; multiples/rates above were read by cross-checking each note's footnotes (which state the tier splits and rate scale in prose) against the table — high confidence, but verify against the source PDF if quoting to the basis point.

## What we couldn't resolve

- **Operational revenue verification.** The *contractual* answer is settled (no audit right, self-report). How Mainvest actually collected/checked revenue operationally (POS, bank-connection, attestation) is still **UNRESOLVED** — no primary filing speaks to it; the platform's support center is defunct.
- **Actual repayment/recovery rates.** No filing discloses per-note repayment progress or default/recovery; the C-AR window closes before maturity. **UNRESOLVED from primary sources.**
- **Mantis final governing cap/scale.** Mantis's four Form C/A amendments + C-U were not re-pulled this pass (lower priority; tiering already settled). The base Form C set **3.0× flat / 1.0%**; whether a C/A changed the final post-close cap is **not re-verified** here — note the table as "base terms; amended terms govern" rather than asserting a final figure.
- **Why the escrow-agent language varies by filing.** The explicit "Escrow Agent" framing appears in the 2022 Mainvest Holdings Form C but not in the food/beverage memos (which use "committed funds will be returned"). Whether this is template/era drift or issuer-type drift is **not resolved**.

## Sources (primary EDGAR filings)

- [Lucky Goat Brewing LLC — Form C, 2019-11-05](https://www.sec.gov/Archives/edgar/data/1792922/000174605919000062/luckygoat_rsn.pdf) — CIK 1792922, accession 0001746059-19-000062, exhibit `luckygoat_rsn.pdf` (term sheet, §3 ACH, tier footnotes); offering memo `luckygoat_offmo.pdf` (security/guarantee, refund); [C-AR FY2020](https://www.sec.gov/Archives/edgar/data/1792922/000174605921000183/luckygoat_c_ar.pdf) (0001746059-21-000183).
- [WanderLinger Brewing Co LLC — Form C, 2020-03-31](https://www.sec.gov/Archives/edgar/data/1807927/000174605920000097/wanderlinger_noteagmt.pdf) — CIK 1807927, accession 0001746059-20-000097, exhibit `wanderlinger_noteagmt.pdf` (1.1× flat, §3 ACH); [C-AR FY2020](https://www.sec.gov/Archives/edgar/data/1807927/000174605921000185/wanderlinger_c_ar.pdf) (0001746059-21-000185).
- [WeHa Brewing Company LLC — Form C, 2020-07-14](https://www.sec.gov/Archives/edgar/data/1816410/000174605920000205/weha_noteagmt.pdf) — CIK 1816410, accession 0001746059-20-000205, exhibit `weha_noteagmt.pdf` (1.8×/1.5× tiers, §3 ACH); [C-AR FY2020](https://www.sec.gov/Archives/edgar/data/1816410/000174605921000184/weha_c_ar.pdf) (0001746059-21-000184).
- [Hattie's Coffee House LLC — Form C, 2023-03-28](https://www.sec.gov/Archives/edgar/data/1970335/000174605923000075/hatties_rsn.pdf) — CIK 1970335, accession 0001746059-23-000075, exhibit `hatties_rsn.pdf` (1.6×/1.4× tiers, §3 ACH); [C-AR FY2024, 2025-03-06](https://www.sec.gov/Archives/edgar/data/1970335/000197033525000001/formcar_hattiescoffeehouse.pdf) (0001970335-25-000001); C-TR 2025-03-14 (0001970335-25-000002).
- [Mainvest Holdings Corp — Form C, 2022-11-03](https://www.sec.gov/Archives/edgar/data/1785840/000178584022000003/mainvestformc.pdf) — CIK 1785840, accession 0001785840-22-000003, exhibit `mainvestformc.pdf` (escrow-agent language, L391–392).
- Cross-reference (cannabis anomaly): [Mantis Management Group LLC — Form C, 2021-07-26](https://www.sec.gov/Archives/edgar/data/1874812/000174605921000363/mantis_rsn.pdf) — CIK 1874812, accession 0001746059-21-000363, exhibit `mantis_rsn.pdf` (3.0× flat, §3 manual/non-ACH).
