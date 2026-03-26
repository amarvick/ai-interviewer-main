-- Migration: add per-problem reference talking points for AI rubric context
-- Run with:
-- docker exec -i ai_interviewer_db psql -U postgres -d ai_interviewer < backend/docs/problem_reference_talking_points.sql

BEGIN;

ALTER TABLE problems
    ADD COLUMN IF NOT EXISTS reference_talking_points JSON;

UPDATE problems
SET reference_talking_points = '[]'::json
WHERE reference_talking_points IS NULL;

COMMIT;
