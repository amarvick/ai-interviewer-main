-- Migration: add per-submission test counts
-- Run with:
-- docker exec -i ai_interviewer_db psql -U postgres -d ai_interviewer < backend/docs/submission_test_counts_migration.sql

BEGIN;

ALTER TABLE submissions
    ADD COLUMN IF NOT EXISTS tests_passed INTEGER NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS tests_total INTEGER NOT NULL DEFAULT 0;

COMMIT;
