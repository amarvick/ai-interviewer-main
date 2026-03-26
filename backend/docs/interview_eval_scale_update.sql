-- Migration: widen interview evaluation score limits to 0-10
-- Run with:
-- docker exec -i ai_interviewer_db psql -U postgres -d ai_interviewer < backend/docs/interview_eval_scale_update.sql

BEGIN;

ALTER TABLE interview_evaluations
    DROP CONSTRAINT IF EXISTS ck_eval_problem_understanding,
    DROP CONSTRAINT IF EXISTS ck_eval_approach_quality,
    DROP CONSTRAINT IF EXISTS ck_eval_code_reasoning,
    DROP CONSTRAINT IF EXISTS ck_eval_code_correctness_reasoning,
    DROP CONSTRAINT IF EXISTS ck_eval_complexity,
    DROP CONSTRAINT IF EXISTS ck_eval_complexity_analysis,
    DROP CONSTRAINT IF EXISTS ck_eval_communication,
    DROP CONSTRAINT IF EXISTS ck_eval_communication_clarity;

ALTER TABLE interview_evaluations
    ADD CONSTRAINT ck_eval_problem_understanding CHECK (problem_understanding_score BETWEEN 0 AND 10),
    ADD CONSTRAINT ck_eval_approach_quality CHECK (approach_quality_score BETWEEN 0 AND 10),
    ADD CONSTRAINT ck_eval_code_reasoning CHECK (code_correctness_reasoning_score BETWEEN 0 AND 10),
    ADD CONSTRAINT ck_eval_complexity CHECK (complexity_analysis_score BETWEEN 0 AND 10),
    ADD CONSTRAINT ck_eval_communication CHECK (communication_clarity_score BETWEEN 0 AND 10);

COMMIT;
