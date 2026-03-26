-- Migration: add stable slug column for problems
-- Run with:
-- docker exec -i ai_interviewer_db psql -U postgres -d ai_interviewer < backend/docs/problem_slug_update.sql

BEGIN;

ALTER TABLE problems
    ADD COLUMN IF NOT EXISTS slug VARCHAR(120);

WITH generated AS (
    SELECT
        id,
        CASE
            WHEN title IS NULL OR title = '' THEN id
            ELSE regexp_replace(lower(title), '[^a-z0-9]+', '-', 'g')
        END AS base_slug
    FROM problems
),
deduped AS (
    SELECT
        g.id,
        CASE
            WHEN g.base_slug = '' THEN g.id
            ELSE g.base_slug
        END AS cleaned_slug,
        ROW_NUMBER() OVER (PARTITION BY g.base_slug ORDER BY g.id) AS slug_rank
    FROM generated g
)
UPDATE problems AS p
SET slug = CASE
    WHEN d.slug_rank = 1 THEN d.cleaned_slug
    ELSE d.cleaned_slug || '-' || d.slug_rank
END
FROM deduped d
WHERE p.id = d.id
  AND (p.slug IS NULL OR p.slug = '');

ALTER TABLE problems
    ALTER COLUMN slug SET NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_problems_slug ON problems (slug);

COMMIT;
