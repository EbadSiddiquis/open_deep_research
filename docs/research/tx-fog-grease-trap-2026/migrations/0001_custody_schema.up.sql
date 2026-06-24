-- =====================================================================
-- MIGRATION 0001 — UP: TCEQ grease/grit-trap waste hauling schema
-- Authority: 30 TAC Chapter 312 (Subch. "Transporters")
--   §312.142  transporter registration
--   §312.145  trip ticket (manifest), signatures, retention
-- Dialect: PostgreSQL 14+
-- Source run: 20260624-201024-tx-fog-grease-trap-tceq-regs-bda74e
-- =====================================================================

-- ---------------------------------------------------------------------
-- ENUMs
-- ---------------------------------------------------------------------
CREATE TYPE custody_event_type AS ENUM (
    'generator_handoff',   -- §312.145(a)(2),(3),(8): generator signs, waste collected
    'transport',           -- §312.145(a)(1),(4): transporter/driver leg
    'disposal_receipt'     -- §312.145(a)(5),(6),(7): receiving facility acknowledges
);

CREATE TYPE signer_role AS ENUM (
    'generator',
    'transporter',
    'facility_representative'
);

CREATE TYPE signature_method AS ENUM ('wet', 'electronic');
-- §312.145(a)(2) & (a)(7) explicitly allow electronic signature for
-- the generator and facility-representative signatures.

-- ---------------------------------------------------------------------
-- TRUCKS
-- registration_ref = the TCEQ-assigned transporter registration number
-- (§312.142(c) "assigned registration number"; same value §312.145(a)(1)
-- calls the "commission registration number of transporter").
-- NOTE: the registration is legally held at the TRANSPORTER/business level,
-- but §312.142(c) requires a current copy "in each vehicle operated under
-- that registration" — so it is modeled here per-vehicle (denormalized).
-- If you add a `transporters` table later, make registration_ref a FK to it.
-- ---------------------------------------------------------------------
CREATE TABLE trucks (
    id                          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    label                       TEXT NOT NULL,                 -- internal unit name/number
    vin                         TEXT,
    plate                       TEXT,

    -- §312.142(c) — the regulatory identifier. Required to legally haul.
    registration_ref            TEXT NOT NULL,                 -- TCEQ transporter registration number
    registration_expires_at     DATE NOT NULL,                 -- §312.142(d): expires Aug 31, biennial renewal
    authorization_copy_in_vehicle BOOLEAN NOT NULL DEFAULT FALSE, -- §312.142(c): copy carried in each vehicle
    sticker_date                DATE,                          -- RG-389: dated authorization sticker on truck door

    is_active                   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT trucks_registration_ref_not_blank CHECK (length(trim(registration_ref)) > 0)
);

CREATE INDEX trucks_registration_ref_idx ON trucks (registration_ref);
COMMENT ON COLUMN trucks.registration_ref IS
    'TCEQ-assigned transporter registration number (30 TAC §312.142(c) / §312.145(a)(1)).';

-- ---------------------------------------------------------------------
-- TRIP_TICKETS  (the manifest header — one per collection/deposit)
-- §312.145(a): "a record of each individual collection and deposit ...
-- in the form of a trip ticket".
-- §312.145(b): 5-part distribution, return-to-generator <=15 days,
-- 5-year retention, annual June 1–May 31 summary by July 1.
-- ---------------------------------------------------------------------
CREATE TABLE trip_tickets (
    id                      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ticket_number           TEXT NOT NULL UNIQUE,        -- your manifest serial
    truck_id                BIGINT NOT NULL REFERENCES trucks (id),

    -- §312.145(a)(1): transporter identity is captured via truck_id->registration_ref,
    -- but snapshot the reg number on the ticket so historical records are immutable.
    transporter_registration_ref TEXT NOT NULL,

    -- §312.145(a)(3),(8): waste classification + trap volume (header-level summary)
    waste_type              TEXT NOT NULL,               -- e.g. 'grease_trap', 'grit_trap'
    trap_volume_gal         NUMERIC(10,2),               -- (a)(8) volume of the grease/grit trap

    -- §312.145(b) chain-of-custody / retention workflow state
    deposited_at            DATE,                        -- (a)(5) date deposited
    returned_to_generator_at DATE,                       -- (b): transporter returns a copy within 15 days of deposit
    retain_until            DATE,                        -- (b): retain copies 5 years (deposit + 5y)

    status                  TEXT NOT NULL DEFAULT 'open',-- open|collected|deposited|closed
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- §312.145(b): the copy must be returned to the generator within 15 days of deposit.
    CONSTRAINT trip_ticket_return_within_15_days CHECK (
        returned_to_generator_at IS NULL
        OR deposited_at IS NULL
        OR returned_to_generator_at <= deposited_at + INTERVAL '15 days'
    ),
    -- §312.145(b): 5-year retention floor.
    CONSTRAINT trip_ticket_retention_5y CHECK (
        retain_until IS NULL
        OR deposited_at IS NULL
        OR retain_until >= deposited_at + INTERVAL '5 years'
    )
);

CREATE INDEX trip_tickets_truck_idx ON trip_tickets (truck_id);
CREATE INDEX trip_tickets_retain_until_idx ON trip_tickets (retain_until);

-- ---------------------------------------------------------------------
-- CUSTODY_EVENTS  (one signed transfer per row; 3 per complete trip ticket)
-- Each row = one of the three signatures the rule requires:
--   generator (a)(2) -> transporter (a)(4) -> facility rep (a)(7).
-- Columns are conditionally required by event_type via CHECK constraints.
-- ---------------------------------------------------------------------
CREATE TABLE custody_events (
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    trip_ticket_id      BIGINT NOT NULL REFERENCES trip_tickets (id) ON DELETE RESTRICT,
    event_type          custody_event_type NOT NULL,

    -- §312.145: every transfer is signed. Rule requires a DATE (not clock time);
    -- event_date is the regulatory field, occurred_at is an optional finer-grained superset.
    event_date          DATE NOT NULL,
    occurred_at         TIMESTAMPTZ,                  -- optional; time-of-day is your design choice, not mandated

    -- signature block (applies to all three event types)
    signer_role         signer_role NOT NULL,
    signer_name         TEXT NOT NULL,               -- (a)(2)/(a)(4)/(a)(7)
    signature_method    signature_method NOT NULL DEFAULT 'wet',
    signature_ref       TEXT,                        -- e-sig payload id / image ref

    -- waste detail (set on generator_handoff; (a)(3),(8))
    waste_type          TEXT,
    amount              NUMERIC(10,2),               -- (a)(3) amount collected/transported
    amount_unit         TEXT,                        -- e.g. 'gal'
    trap_volume_gal     NUMERIC(10,2),               -- (a)(8) volume of the grease/grit trap

    -- generator party (generator_handoff; (a)(2))
    generator_name      TEXT,
    generator_address   TEXT,
    generator_phone     TEXT,

    -- transporter party (transport; (a)(1))
    transporter_registration_ref TEXT,              -- commission registration number

    -- receiving facility party (disposal_receipt; (a)(5),(6),(7))
    facility_name       TEXT,
    facility_permit_ref TEXT,                        -- (a)(6) permit or site registration number
    facility_location   TEXT,                        -- (a)(5)/(a)(6) place deposited / location
    facility_operator   TEXT,                        -- (a)(6) operator
    amount_received     NUMERIC(10,2),               -- (a)(7) amount of waste received

    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- one of each signed leg per ticket
    CONSTRAINT custody_events_unique_leg UNIQUE (trip_ticket_id, event_type),

    -- electronic signatures only permitted where the rule allows them
    -- (generator (a)(2) and facility rep (a)(7); transporter leg is wet/responsible-person).
    CONSTRAINT custody_events_esig_allowed CHECK (
        signature_method = 'wet'
        OR event_type IN ('generator_handoff', 'disposal_receipt')
    ),

    -- §312.145(a)(2),(3),(8): generator handoff must carry generator identity + waste detail
    CONSTRAINT custody_events_generator_fields CHECK (
        event_type <> 'generator_handoff'
        OR (signer_role = 'generator'
            AND generator_name IS NOT NULL
            AND waste_type IS NOT NULL
            AND amount IS NOT NULL
            AND trap_volume_gal IS NOT NULL)
    ),

    -- §312.145(a)(1),(4): transport leg must carry the commission registration number
    CONSTRAINT custody_events_transport_fields CHECK (
        event_type <> 'transport'
        OR (signer_role = 'transporter'
            AND transporter_registration_ref IS NOT NULL)
    ),

    -- §312.145(a)(5),(6),(7): disposal/receipt must identify facility + amount received
    CONSTRAINT custody_events_facility_fields CHECK (
        event_type <> 'disposal_receipt'
        OR (signer_role = 'facility_representative'
            AND facility_permit_ref IS NOT NULL
            AND facility_location IS NOT NULL
            AND facility_operator IS NOT NULL
            AND amount_received IS NOT NULL)
    )
);

CREATE INDEX custody_events_trip_ticket_idx ON custody_events (trip_ticket_id);
CREATE INDEX custody_events_type_idx ON custody_events (event_type);

COMMENT ON TABLE custody_events IS
    'Signed chain-of-custody transfers for a trip ticket (30 TAC §312.145). '
    'Three legs per complete manifest: generator_handoff -> transport -> disposal_receipt.';
