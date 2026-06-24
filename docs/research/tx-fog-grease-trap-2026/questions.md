# Research questions (answer-free) — TX FOG / grease-trap & TCEQ transporter regs

> Hand THIS file (and nothing from the prior report) to a fresh Claude for an
> independent research pass. It contains only the questions + scope, so the new
> research isn't anchored to the existing answers.

## Brief

Produce true, citable regulatory values (not approximations) as of 2026, for a
Texas-focused waste-hauling software product, to (a) hardcode per-jurisdiction
grease-interceptor config and (b) design a TCEQ-compliant custody/manifest data
model (`trucks.registration_ref` + `custody_events`).

**Source standard:** prefer PRIMARY/official sources — municipal Code of Ordinances
(Municode / American Legal), SAWS rate/rule documents, Texas Administrative Code /
TCEQ rules. Avoid law-firm summaries, SEO blogs, vendor marketing except as leads.
Surface where sources disagree or a number can't be verified.

**Out of scope:** federal EPA pretreatment baseline (40 CFR 403) except where a TX
city explicitly incorporates it; non-TX jurisdictions; septic/land-application
permitting beyond what's needed to define the transporter manifest.

## Subquestions

**SQ1 — Houston ordinance citation + thresholds.** In the *current* Houston Code of
Ordinances, which chapter/article/section governs grease traps/interceptors & FOG
pretreatment for food-service establishments? Verify or correct the "Chapter 47"
assumption (map to FOG specifically; give exact article/section). Quote the enforced
pump-out trigger (e.g. 25% rule / FOG-depth rule) and any mandated minimum
cleaning/pumping interval (e.g. 90 days), with section numbers and ordinance language.

**SQ2 — Per-municipality thresholds.** For Houston, Dallas, San Antonio (SAWS), and
Austin, find each jurisdiction's OWN grease-interceptor maintenance rule — pump-out
trigger (percent-full / FOG+solids depth) and mandated maximum cleaning interval
(days/months) — with the governing ordinance/SAWS-rule citation for each. State
whether the "90-day / 25%" figure is universal or varies; give each city's actual
numbers for true per-jurisdiction config, and flag any city using a different standard.

**SQ3 — TCEQ transporter requirements.** Under the Texas Administrative Code (identify
the exact title/chapter for grease/grit trap waste — e.g. 30 TAC ch. 312), what is
required to legally haul grease-trap & grit-trap waste in TX? (a) the transporter
registration requirement and what the registration number is / how it's issued; and
(b) the manifest/"trip ticket" requirement — required fields, who signs, chain-of-
custody & recordkeeping obligations. Map to a data model: what belongs in
`trucks.registration_ref`, and what events/signatures `custody_events` must capture.
