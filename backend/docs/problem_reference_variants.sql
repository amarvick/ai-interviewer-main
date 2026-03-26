-- Adds reference_pseudocode_variants JSON column to problems.

ALTER TABLE problems
    ADD COLUMN IF NOT EXISTS reference_pseudocode_variants JSONB DEFAULT '[]'::jsonb;

-- Optional: backfill existing rows by wrapping current reference_pseudocode
-- update problems
-- set reference_pseudocode_variants = jsonb_build_array(jsonb_build_object(
--     'id', 'primary',
--     'title', 'Primary reference',
--     'pseudocode', reference_pseudocode
-- ))
-- where reference_pseudocode IS NOT NULL
--   and (reference_pseudocode_variants IS NULL OR jsonb_array_length(reference_pseudocode_variants) = 0);
