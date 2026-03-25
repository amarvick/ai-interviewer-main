-- Adds reference_pseudocode column to problems table.
-- Run inside your database (psql example shown).

ALTER TABLE problems
    ADD COLUMN IF NOT EXISTS reference_pseudocode TEXT;

-- Existing rows will default to NULL; rerun the seed script to populate data:
-- cd backend && python scripts/seed_problem_two_sum.py
