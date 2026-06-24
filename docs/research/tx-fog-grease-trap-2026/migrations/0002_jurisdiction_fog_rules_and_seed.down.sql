-- =====================================================================
-- MIGRATION 0002 — DOWN (rollback)
-- Reverse order: sample data (seeded into 0001 tables) -> table -> enums.
-- DELETEs are scoped to SAMPLE- sentinels so a rollback cannot touch real data.
-- =====================================================================

-- 1) remove the sample manifest data seeded into the 0001 tables
DELETE FROM custody_events
 WHERE trip_ticket_id IN (
     SELECT id FROM trip_tickets WHERE ticket_number = 'SAMPLE-TT-000001'
 );
DELETE FROM trip_tickets WHERE ticket_number = 'SAMPLE-TT-000001';
DELETE FROM trucks WHERE registration_ref = 'SAMPLE-REG-0000000';

-- 2) drop the jurisdiction rules table (its seed rows go with it)
DROP TABLE IF EXISTS jurisdiction_fog_rules;

-- 3) drop the enums this migration introduced (only after the table is gone)
DROP TYPE IF EXISTS fog_trigger_semantics;
DROP TYPE IF EXISTS fog_trigger_basis;
