-- =====================================================================
-- MIGRATION 0001 — DOWN (rollback): tear down the custody/manifest schema
-- Reverse order: child tables before parents, then data-dependent types.
-- =====================================================================
DROP TABLE IF EXISTS custody_events;
DROP TABLE IF EXISTS trip_tickets;
DROP TABLE IF EXISTS trucks;

DROP TYPE IF EXISTS signature_method;
DROP TYPE IF EXISTS signer_role;
DROP TYPE IF EXISTS custody_event_type;
