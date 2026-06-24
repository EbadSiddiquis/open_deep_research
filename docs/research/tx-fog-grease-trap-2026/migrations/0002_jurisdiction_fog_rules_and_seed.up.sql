-- =====================================================================
-- MIGRATION 0002 — UP: jurisdiction FOG rules table + seed data
-- Depends on 0001 (seeds a sample trip ticket into trucks/trip_tickets/
-- custody_events). Source run: 20260624-201024-tx-fog-grease-trap-tceq-regs-bda74e
-- Dialect: PostgreSQL 14+
-- =====================================================================

-- ENUMs for the per-jurisdiction maintenance rules
CREATE TYPE fog_trigger_basis AS ENUM (
    'wetted_height',        -- depth: bottom of device to invert of outlet pipe
    'interceptor_contents'  -- volume/contents fraction as worded by the code
);

CREATE TYPE fog_trigger_semantics AS ENUM (
    'accelerator',  -- threshold forces MORE frequent than the baseline interval (Houston)
    'or_sooner'     -- pump at interval OR when threshold met, whichever first
);

-- ---------------------------------------------------------------------
-- JURISDICTION_FOG_RULES — per-city grease-interceptor maintenance config
-- ---------------------------------------------------------------------
CREATE TABLE jurisdiction_fog_rules (
    id                      TEXT PRIMARY KEY,            -- e.g. 'tx_houston'
    city                    TEXT NOT NULL,
    state                   TEXT NOT NULL DEFAULT 'TX',
    utility                 TEXT,                        -- e.g. 'SAWS'

    interval_days           INT  NOT NULL,               -- max scheduled cleaning interval
    hard_floor_days         INT,                         -- waiver-proof max; null = none
    trigger_pct             INT  NOT NULL,               -- percent-full pump-out threshold
    trigger_basis           fog_trigger_basis    NOT NULL,
    trigger_contents        TEXT[] NOT NULL,             -- what counts toward the %
    trigger_semantics       fog_trigger_semantics NOT NULL,
    response_window_days    INT,                         -- deadline after trigger observed; null = n/a
    response_window_unit    TEXT,                        -- e.g. 'working_days'
    interval_waivable       BOOLEAN NOT NULL DEFAULT FALSE,
    fog_discharge_limit_mg_l INT,                        -- null = not captured this run

    citation                TEXT NOT NULL,
    citation_url            TEXT NOT NULL,
    citation_url_secondary  TEXT,
    confidence              TEXT NOT NULL DEFAULT 'high',
    notes                   TEXT,

    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fog_trigger_pct_range CHECK (trigger_pct BETWEEN 1 AND 100),
    CONSTRAINT fog_response_window_pair CHECK (
        (response_window_days IS NULL AND response_window_unit IS NULL)
        OR (response_window_days IS NOT NULL AND response_window_unit IS NOT NULL)
    )
);

-- ---------------------------------------------------------------------
-- SEED: four-jurisdiction config (all values from primary sources)
-- ---------------------------------------------------------------------
INSERT INTO jurisdiction_fog_rules
    (id, city, state, utility, interval_days, hard_floor_days, trigger_pct,
     trigger_basis, trigger_contents, trigger_semantics,
     response_window_days, response_window_unit, interval_waivable,
     fog_discharge_limit_mg_l, citation, citation_url, citation_url_secondary,
     confidence, notes)
VALUES
('tx_houston', 'Houston', 'TX', NULL,
 90, 180, 25,
 'wetted_height', ARRAY['floating_materials','sediment','oils','greases'], 'accelerator',
 NULL, NULL, TRUE,
 200,
 'Houston Code of Ordinances § 47-512 (Ch. 47 Art. XI Div. 9)',
 'https://library.municode.com/tx/houston/codes/code_of_ordinances?nodeId=COOR_CH47WASE_ARTXITRTRCEWA_DIV9GETRDIWA_SD1GERE_S47-512CLMARE',
 'https://www.houstonconsumer.org/services/permits/special-waste-permits/special-waste-generators',
 'high',
 '25% is an accelerator above the 90-day baseline (forces more-frequent pumping). 90-day waivable via Notice of Waiver; 180-day floor is NOT waivable. FOG limit 200 mg/L since 2023-12-02.'),

('tx_dallas', 'Dallas', 'TX', NULL,
 90, NULL, 25,
 'interceptor_contents', ARRAY['floating_materials','sediment','oils','grease'], 'or_sooner',
 NULL, NULL, FALSE,
 NULL,
 'Dallas City Code Ch. 19 § 19-126.2(c)',
 'https://codelibrary.amlegal.com/codes/dallas/latest/dallas_tx/0-0-0-110074',
 'https://dallascityhall.com/departments/waterutilities/pretreatmentprogram/Pages/faqs2.aspx',
 'high',
 'Official Water Utilities FAQ quotes the codified subsection. Codified full text not extracted verbatim (amlegal errored). A separate brochure loosely says "25% of design capacity" — code-FAQ phrasing treated as authoritative.'),

('tx_san_antonio_saws', 'San Antonio', 'TX', 'SAWS',
 90, NULL, 25,
 'wetted_height', ARRAY['floating_materials','sediment','fats','oils','grease'], 'or_sooner',
 2, 'working_days', FALSE,
 NULL,
 'San Antonio City Code § 34-527(b) (SAWS FOG Ordinance)',
 'https://www.saws.org/wp-content/uploads/2019/03/FOGOrdinance6-11Final.pdf',
 NULL,
 'high',
 'Must clean within 2 WORKING DAYS of crossing the 25% wetted-height threshold, at a frequency not less often than every 90 days.'),

('tx_austin', 'Austin', 'TX', NULL,
 90, NULL, 50,
 'wetted_height', ARRAY['grease','solids'], 'or_sooner',
 NULL, NULL, FALSE,
 200,
 'Austin City Code § 15-10-197',
 'https://www.austintexas.gov/water/grease-trap-maintenance',
 NULL,
 'high',
 'KEY DEVIATION: trigger is 50% of wetted height, NOT 25%. Same 90-day interval. FOG limit 200 mg/L (§ 15-10-23).');


-- =====================================================================
-- SEED — sample complete trip ticket (one truck, one manifest, 3 legs)
-- Values prefixed SAMPLE-/placeholder; replace before production use.
-- Doubles as a CHECK-constraint smoke test for the 0001 schema.
-- =====================================================================

-- 1) a registered truck
INSERT INTO trucks
    (label, vin, plate, registration_ref, registration_expires_at,
     authorization_copy_in_vehicle, sticker_date, is_active)
VALUES
    ('Unit 12', 'SAMPLE-VIN-1HGCM82633A004352', 'TX-SAMPLE-123',
     'SAMPLE-REG-0000000', DATE '2027-08-31',   -- §312.142(d): expires Aug 31, biennial
     TRUE, DATE '2025-09-01', TRUE);

-- 2) the trip ticket (manifest header), tied to that truck
INSERT INTO trip_tickets
    (ticket_number, truck_id, transporter_registration_ref,
     waste_type, trap_volume_gal, deposited_at,
     returned_to_generator_at, retain_until, status)
SELECT
    'SAMPLE-TT-000001',
    t.id,
    t.registration_ref,
    'grease_trap', 1000.00,
    DATE '2026-06-20',                          -- (a)(5) date deposited
    DATE '2026-06-25',                          -- (b) returned within 15 days of deposit
    DATE '2031-06-20',                          -- (b) retain 5 years
    'closed'
FROM trucks t
WHERE t.registration_ref = 'SAMPLE-REG-0000000';

-- 3) the three signed custody legs for that ticket
--    generator_handoff -> transport -> disposal_receipt
WITH tt AS (
    SELECT id AS trip_ticket_id, transporter_registration_ref
    FROM trip_tickets WHERE ticket_number = 'SAMPLE-TT-000001'
)
INSERT INTO custody_events
    (trip_ticket_id, event_type, event_date, occurred_at,
     signer_role, signer_name, signature_method, signature_ref,
     waste_type, amount, amount_unit, trap_volume_gal,
     generator_name, generator_address, generator_phone,
     transporter_registration_ref,
     facility_name, facility_permit_ref, facility_location, facility_operator,
     amount_received)
SELECT
    tt.trip_ticket_id, 'generator_handoff', DATE '2026-06-20',
    TIMESTAMPTZ '2026-06-20 09:15:00-05',
    'generator', 'SAMPLE Diner LLC', 'electronic', 'esig:sample-gen-001',  -- (a)(2) e-sig allowed
    'grease_trap', 950.00, 'gal', 1000.00,                                 -- (a)(3),(8)
    'SAMPLE Diner LLC', '123 Sample St, Houston, TX', '713-555-0100',      -- (a)(2)
    NULL,
    NULL, NULL, NULL, NULL,
    NULL
FROM tt
UNION ALL
SELECT
    tt.trip_ticket_id, 'transport', DATE '2026-06-20',
    TIMESTAMPTZ '2026-06-20 10:05:00-05',
    'transporter', 'SAMPLE Driver Name', 'wet', NULL,                      -- transporter leg: wet sig
    NULL, NULL, NULL, NULL,
    NULL, NULL, NULL,
    tt.transporter_registration_ref,                                       -- (a)(1) commission reg number
    NULL, NULL, NULL, NULL,
    NULL
FROM tt
UNION ALL
SELECT
    tt.trip_ticket_id, 'disposal_receipt', DATE '2026-06-20',
    TIMESTAMPTZ '2026-06-20 13:40:00-05',
    'facility_representative', 'SAMPLE Facility Rep', 'electronic', 'esig:sample-fac-001', -- (a)(7) e-sig allowed
    NULL, NULL, NULL, NULL,
    NULL, NULL, NULL,
    NULL,
    'SAMPLE Disposal Facility', 'SAMPLE-PERMIT-WDW00000',                   -- (a)(6) permit/site reg #
    '456 Sample Plant Rd, Houston, TX', 'SAMPLE Facility Operator Inc',     -- (a)(5),(6) location, operator
    950.00                                                                  -- (a)(7) amount received
FROM tt;
