# TCEQ FOG / grease-trap migrations

Generated from deep-research run `20260624-201024-tx-fog-grease-trap-tceq-regs-bda74e`.
All regulatory values trace to primary sources cited inline in `../../report.md`.

## Files

| File | Purpose |
|------|---------|
| `0001_custody_schema.up.sql`   | `trucks`, `trip_tickets`, `custody_events` + enums (30 TAC §312.142/§312.145) |
| `0001_custody_schema.down.sql` | Tear down the custody schema |
| `0002_jurisdiction_fog_rules_and_seed.up.sql`   | `jurisdiction_fog_rules` table + 4-city seed + 1 sample trip ticket |
| `0002_jurisdiction_fog_rules_and_seed.down.sql` | Remove sample data, drop rules table + enums |

## Apply / rollback (psql)

```sh
# up
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f 0001_custody_schema.up.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f 0002_jurisdiction_fog_rules_and_seed.up.sql

# down (reverse order)
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f 0002_jurisdiction_fog_rules_and_seed.down.sql
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f 0001_custody_schema.down.sql
```

## Notes / caveats

- **Order matters:** `0002` depends on `0001` (the sample trip ticket is seeded into the
  `0001` tables). Apply `0001` first; roll back `0002` first.
- **PostgreSQL 14+** (uses `GENERATED ALWAYS AS IDENTITY`, enum types, `TEXT[]`).
- **Dialect-specific.** For MySQL/SQLite, replace enum types with `TEXT` + `CHECK`,
  `TEXT[]` with a join table or JSON, and `now()`/`TIMESTAMPTZ` accordingly.
- **`registration_ref` is denormalized onto `trucks`** per the data-model spec, but the
  TCEQ registration is legally a transporter/business-level credential merely evidenced
  per vehicle (§312.142(c)). Promote to a `transporters` table if you onboard multi-truck haulers.
- **Sample rows are sentinel-prefixed (`SAMPLE-`)** so the `0002` down-migration can delete
  them without risk to real records. If your migration runner expects each down to undo only
  its own DDL, move those three `DELETE`s into a separate fixtures script.
- **Unverified in this run:** the exact `$10` per-vehicle sticker fee (guidance-level only);
  Dallas/SAWS FOG discharge limits (left NULL — do not infer). See `../../report.md`
  "What we could not fully resolve."
- **Lawyer check worth doing:** electronic signatures are explicitly allowed for the generator
  (§312.145(a)(2)) and facility (§312.145(a)(7)) legs; the transporter leg is encoded as
  wet-signature-only as the conservative reading.
