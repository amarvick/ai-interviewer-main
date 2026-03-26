-- Adds ai_token_total to track cumulative AI token usage per interview session.

ALTER TABLE interview_sessions
    ADD COLUMN IF NOT EXISTS ai_token_total INTEGER NOT NULL DEFAULT 0;
