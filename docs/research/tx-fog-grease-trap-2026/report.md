# Texas FOG / Grease-Trap Pretreatment & TCEQ Transporter Rules — Config & Data-Model Reference (2026)

**Run:** `20260624-201024-tx-fog-grease-trap-tceq-regs-bda74e`
**Audience:** founder hardcoding per-jurisdiction config + designing a TCEQ-compliant custody/manifest data model.
**Sourcing standard:** primary/official only for the load-bearing numbers (Municode / American Legal codes, SAWS & city pretreatment docs, Texas Administrative Code via Cornell LII + TCEQ publications). Law-firm/SEO/vendor pages used only as leads.

---

## Executive summary

- **The "90-day interval" IS effectively universal across all four cities; the "25% trigger" is NOT.** Houston, Dallas, and San Antonio (SAWS) use a **25%** trigger; **Austin uses 50%**. Configure trigger-percent **per jurisdiction**, not as a global constant. (The 90-day maximum interval holds for all four, but each has its own statutory hook and its own secondary mechanics — waivers, response windows, hard floors.)
- **Houston: "Chapter 47" is correct but incomplete.** The live, enforced section is **Houston Code of Ordinances § 47-512** (Ch. 47, Art. XI, Div. 9). 90-day baseline, 25%-of-**wetted-height** accelerator, and a **180-day hard floor** that survives any waiver.
- **Hauling grease/grit-trap waste in Texas is governed by 30 TAC Chapter 312** — registration at **§ 312.142**, trip-ticket/manifest + recordkeeping at **§ 312.145**. The "30 TAC 312" guess is confirmed.
- **Data model:** `trucks.registration_ref` = the **TCEQ-assigned transporter registration number** (§ 312.142(c)). `custody_events` must model **three signed transfer events** — generator handoff, transport leg, disposal/receipt — to satisfy the § 312.145 trip-ticket fields, plus retention/return workflow state.

---

## SQ1 — Houston ordinance citation + thresholds

### Citation (Chapter 47 confirmed; live section identified)
FOG pretreatment for food-service establishments lives in:
**Houston Code of Ordinances → Ch. 47 (Water and Sewers) → Art. XI (Transportation and Treatment of Certain Wastes) → Div. 9 → § 47-512 (Cleaning and maintenance requirements).** Adjacent: § 47-513 (interceptor requirement), § 47-514 (discharge parameters / FOG limit).
Sources: [§ 47-512, Municode](https://library.municode.com/tx/houston/codes/code_of_ordinances?nodeId=COOR_CH47WASE_ARTXITRTRCEWA_DIV9GETRDIWA_SD1GERE_S47-512CLMARE); [City of Houston Health Dept., Special Waste Generators](https://www.houstonconsumer.org/services/permits/special-waste-permits/special-waste-generators).

> **The "Chapter 47" assumption is correct, but the enforceable citation you should store is `§ 47-512`** — Article XI is titled "Transportation and Treatment of Certain Wastes," not "grease traps," so a generic "Chapter 47" pointer would be ambiguous.

### Cleaning interval (verbatim)
- **§ 47-512(b):** *"Each interceptor or holding tank shall be fully evacuated at least once every 90 days."* (Waivable via an approved Notice of Waiver.)
- **§ 47-512(f):** *"…a grease trap or holding tank shall be fully evacuated, cleaned, inspected, and, if needed, repaired or otherwise maintained, at least once every 180 days."* — **a hard floor a waiver cannot remove.**

### Pump-out trigger (verbatim — note it is a depth/height measure)
- **§ 47-512(c):** evacuation must occur **more frequently than every 90 days** when *"Twenty-five percent or more of the wetted height of the grease trap or interceptor, as measured from the bottom of the device to the invert of the outlet pipe, contains floating materials, sediment, oils or greases."*

**Implementation nuance:** In Houston the 25% condition is an **accelerator above** the 90-day baseline, not the baseline itself. The headline scheduled rule is the 90-day pump; the 25%-wetted-height condition forces a *more frequent* pump. And it is **25% of wetted height (a depth), not 25% of volume** — a distinction most vendor blogs get wrong.

### Related current values (same primary text)
- FOG discharge limit **200 mg/L average** (§ 47-514; reduced from 400 mg/L, effective Dec 2 2023).
- § 47-512 last amended by **Ord. 2020-1024 (Dec 2 2020)** → the quoted text is current.

---

## SQ2 — Per-municipality thresholds: is "90-day / 25%" universal?

**Verdict: interval universal (90 days), trigger varies (25% vs 50%).** Store these as four independent config rows.

| City | Trigger (pump when…) | Max interval | Governing citation | Confidence |
|------|----------------------|--------------|--------------------|------------|
| **Houston** | **25%** of **wetted height** contains floating materials/sediment/oils/greases (accelerator) | **90 days** baseline; **180-day** hard floor | **§ 47-512(b),(c),(f)** (Ch. 47, Art. XI, Div. 9) | High (primary) |
| **Dallas** | **25%** or more of the interceptor contains floating materials, sediment, oils, or grease | **90 days** ("not less than every 90 days") | **Dallas City Code Ch. 19, § 19-126.2(c)** | High (official FAQ quotes the codified subsection) |
| **San Antonio (SAWS)** | **25%** of **wetted height** (bottom→invert) contains floating materials/sediment/FOG — **clean within 2 working days** of crossing it | **not less often than 90 days** | **San Antonio City Code § 34-527(b)** (SAWS FOG Ordinance) | High (primary) |
| **Austin** | **50%** or more of the **wetted height** of the trap (**NOT 25%**) | every **90 days** | **Austin City Code § 15-10-197** | High (official austintexas.gov citing the code) |

**Verbatim anchors**
- **Dallas (official FAQ, quoting the code):** *"The Dallas City Code, Chapter 19, Sec 19-126.2(c) specifies all grease traps must be completely emptied and cleaned by a licensed hauler. The interceptors must be cleaned as often as necessary but not less than every 90 days, or whenever 25% or more of the interceptor contains floating materials, sediment, oils, or grease."* — [Dallas Water Utilities Pretreatment FAQ](https://dallascityhall.com/departments/waterutilities/pretreatmentprogram/Pages/faqs2.aspx) (code link: [amlegal Ch. 19](https://codelibrary.amlegal.com/codes/dallas/latest/dallas_tx/0-0-0-110074)).
- **SAWS:** *"…at a frequency not less often than every ninety (90) days and within two (2) working days whenever twenty-five (25) percent or more of the wetted height of the interceptor, measured from the bottom of the device to the invert of the outlet pipe, contains floating materials, sediment, fats, oils, or grease."* — [§ 34-527(b), SAWS FOG Ordinance](https://www.saws.org/wp-content/uploads/2019/03/FOGOrdinance6-11Final.pdf).
- **Austin:** *"…pumped out at least once every 90 days, or sooner if grease and solids make up 50% or more of the wetted height of the trap…"* — [Austin Water, Grease Trap Maintenance (§ 15-10-197)](https://www.austintexas.gov/water/grease-trap-maintenance).
- **Houston:** see SQ1 — § 47-512(b)/(c).

**Config takeaways**
- One global `cleaning_interval_days = 90` is *defensible* for all four — but encode it per-jurisdiction anyway because the **secondary mechanics differ** (Houston 180-day floor + waiver; SAWS 2-working-day response window; Austin/Houston/SAWS measure wetted height).
- `trigger_pct` MUST be per-jurisdiction: **Houston 25, Dallas 25, San Antonio 25, Austin 50.**
- `trigger_basis`: Houston/SAWS/Austin = **wetted height (depth, bottom→invert)**; Dallas code-FAQ phrases it as **"25% of the interceptor"** (FOG+solids), not "design capacity."

---

## SQ3 — TCEQ grease-trap-waste transporter requirements

### Governing rule (30 TAC 312 confirmed)
**Title 30 TAC Chapter 312** (Sludge Use, Disposal, and Transportation):
- **§ 312.142 — Transporter Registration**
- **§ 312.145 — Transporters: Recordkeeping (trip ticket / manifest)**

Sources: [§ 312.142 (Cornell LII / TAC)](https://www.law.cornell.edu/regulations/texas/30-Tex-Admin-Code-SS-312-142); [§ 312.145 (Cornell LII / TAC)](https://www.law.cornell.edu/regulations/texas/30-Tex-Admin-Code-SS-312-145); [TCEQ RG-389](https://www.tceq.texas.gov/downloads/assistance/publications/rg-389.pdf/@@download/file/rg-389.pdf).
*Subchapter-letter caveat:* section numbers are firm; TCEQ's older RG-086 labels them "Subchapter G" while Cornell files them under "Subchapter F." **Cite by section number.**

### (a) Registration requirement → `trucks.registration_ref`
- **§ 312.142(a):** persons transporting *"grit trap waste, or grease trap waste … shall apply for registration with the commission … and receive a registration from the executive director prior to commencing operations."*
- **§ 312.142(c):** must *"maintain a current copy of the registration authorization, as annotated by the executive director with an assigned registration number, at their designated place of business and in each vehicle operated under that registration."*
- TCEQ RG-389 operational expectation: each registered vehicle carries a copy of the registration **and a dated sticker on the truck door**.
- Renewal: expires **Aug 31**, renewed **biennially** (§ 312.142(d)).

→ **`trucks.registration_ref` = the TCEQ-assigned transporter registration number** (the same value § 312.145(a)(1) calls the "commission registration number of transporter"). The registration is held at the **transporter/business** level but must be evidenced **per vehicle** — model the number once and reference it from each truck; consider companion fields `registration_expires_at` (Aug 31, biennial), `authorization_copy_in_vehicle` (bool), `sticker_date`.

### (b) Trip ticket / manifest → `custody_events`
**§ 312.145(a)** — a trip ticket is required for *each* collection/deposit and must contain:
1. transporter name, address, phone, **commission registration number**;
2. generator name, **signature (or e-signature)**, address, phone, **date collected**;
3. **type and amount(s)** of waste;
4. name and **signature(s) of responsible person(s) collecting, transporting, and depositing**;
5. **date and place deposited**;
6. receiving-facility ID — **permit/site registration number, location, operator**;
7. **signature (or e-signature) of facility on-site representative acknowledging receipt** and amount received;
8. the **volume of the grease/grit trap** (or septic tank).

**Three required signatures:** (i) generator, (ii) transporter/responsible persons, (iii) receiving-facility representative.

**§ 312.145(b)** — chain-of-custody & retention:
- Trip tickets **divided into five parts**: generator (at pickup), receiving facility, transporter (retains one), **one returned by transporter to the generator within 15 days** after deposit, one to local authority if needed.
- **Retain copies 5 years**; available to TCEQ on request.
- **Annual summary** to the executive director by **July 1**, covering **June 1–May 31**.

→ **`custody_events` model** (each row = one signed transfer in the chain):

| `event_type` | Required signer (`signer_role`) | Required captured fields | Rule |
|---|---|---|---|
| `generator_handoff` | generator (sig/e-sig) | generator name/address/phone, `date_collected`, `waste_type`, `amount`, `trap_volume` | § 312.145(a)(2),(3),(8) |
| `transport` | responsible person / driver | transporter name/address/phone, **commission registration number** | § 312.145(a)(1),(4) |
| `disposal_receipt` | receiving-facility on-site rep (sig/e-sig) | facility permit/site-reg #, location, operator, `date_deposited`, place, `amount_received` | § 312.145(a)(5),(6),(7) |

Companion workflow/retention state (required by § 312.145(b), schema is your design): `returned_to_generator_at` (≤15 days after deposit), `retain_until` (deposit + 5 years), and an annual-summary reporting job (July 1 / June 1–May 31 window).

**Required vs. inferred:** dates are explicitly required; the rule mandates **date** (not clock time) for collection/deposit — a full `datetime` is a safe superset but the time-of-day component is your design choice, not a mandate. Electronic signatures are explicitly allowed for the **generator** and **facility** signatures.

---

## What we could not fully resolve

1. **Exact `$10` per-vehicle sticker fee** for TCEQ registration — came via a page summarizer, not verbatim rule text. The *existence* of a dated per-vehicle sticker is corroborated by TCEQ RG-389; treat the **dollar figure as guidance-level** until checked against the current TCEQ fee schedule / § 312.142 verbatim. *(claim c13, low confidence.)*
2. **Live SOS-hosted TAC text** (texreg.sos.state.tx.us) only returned a JS redirect and could not be read directly; verbatim § 312.142/§ 312.145 quotes come from **Cornell LII** (faithful TAC reproduction) + TCEQ publications. Three independent sources agree on substance, but we lack the SOS page itself as a second *primary* image of the quotes.
3. **Dallas measurement basis wording:** the official **code-citing FAQ** says "25% … contains floating materials, sediment, oils, or grease" (FOG+solids), while a separate Dallas **brochure** loosely says "25% of design capacity." We treat the **code-FAQ phrasing as authoritative**; the codified § 19-126.2(c) full text was not extracted verbatim (amlegal page errored), so the exact statutory wording is corroborated-but-not-quoted.
4. **Houston proposed changes:** a 2023 Health Dept. page referenced *proposed* Chapter 47 amendments. Those are proposals; the enforced § 47-512 text (Ord. 2020-1024) stands. Re-verify before a future release if Houston adopts new O/G frequencies.

---

## Sources
- **Houston:** [§ 47-512, Municode](https://library.municode.com/tx/houston/codes/code_of_ordinances?nodeId=COOR_CH47WASE_ARTXITRTRCEWA_DIV9GETRDIWA_SD1GERE_S47-512CLMARE) · [Houston Health Dept., Special Waste Generators](https://www.houstonconsumer.org/services/permits/special-waste-permits/special-waste-generators)
- **Dallas:** [Dallas Water Utilities Pretreatment FAQ (quotes § 19-126.2(c))](https://dallascityhall.com/departments/waterutilities/pretreatmentprogram/Pages/faqs2.aspx) · [Dallas City Code Ch. 19 (amlegal)](https://codelibrary.amlegal.com/codes/dallas/latest/dallas_tx/0-0-0-110074) · [Dallas "25% Rule" brochure](https://dallascityhall.com/departments/codecompliance/DCH%20documents/pdf/GreaseTrap_brochure.pdf)
- **San Antonio (SAWS):** [§ 34-527(b), SAWS FOG Ordinance (PDF)](https://www.saws.org/wp-content/uploads/2019/03/FOGOrdinance6-11Final.pdf)
- **Austin:** [Austin Water, Grease Trap Maintenance (§ 15-10-197)](https://www.austintexas.gov/water/grease-trap-maintenance)
- **TCEQ / TAC:** [30 TAC § 312.142](https://www.law.cornell.edu/regulations/texas/30-Tex-Admin-Code-SS-312-142) · [30 TAC § 312.145](https://www.law.cornell.edu/regulations/texas/30-Tex-Admin-Code-SS-312-145) · [TCEQ RG-389](https://www.tceq.texas.gov/downloads/assistance/publications/rg-389.pdf/@@download/file/rg-389.pdf) · [TCEQ RG-086](https://texashistory.unt.edu/ark:/67531/metapth624156/m2/1/high_res_d/rg-086.pdf)

*Structured sources and claims for this run are saved under `.research_runs/20260624-201024-tx-fog-grease-trap-tceq-regs-bda74e/` (`sources.json`, `claims.json`).*
