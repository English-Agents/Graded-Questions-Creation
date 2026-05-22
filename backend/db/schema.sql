-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ─────────────────────────────────────────────
-- Skill taxonomy (lookup)
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS skills (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE   -- "Grammar & Vocabulary" | "Reading" | "Writing"
);

INSERT INTO skills (name) VALUES
    ('Grammar & Vocabulary'),
    ('Reading'),
    ('Writing')
ON CONFLICT (name) DO NOTHING;

-- ─────────────────────────────────────────────
-- Course hierarchy
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS courses (
    id      SERIAL PRIMARY KEY,
    name    TEXT NOT NULL,
    subject TEXT NOT NULL DEFAULT 'English'
);

CREATE TABLE IF NOT EXISTS modules (
    id          SERIAL PRIMARY KEY,
    course_id   INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    order_index INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS topics (
    id        SERIAL PRIMARY KEY,
    module_id INT NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    name      TEXT NOT NULL,
    metadata  JSONB NOT NULL DEFAULT '{}'
);

-- ─────────────────────────────────────────────
-- Pool configuration  (admin sets targets)
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS pool_configs (
    id            SERIAL PRIMARY KEY,
    topic_id      INT  NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    skill_id      INT  NOT NULL REFERENCES skills(id),
    marks         INT  NOT NULL,
    question_type TEXT NOT NULL,
    difficulty    TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
    target_count  INT  NOT NULL DEFAULT 0,
    current_count INT  NOT NULL DEFAULT 0,
    UNIQUE (topic_id, skill_id, marks, question_type, difficulty)
);

-- ─────────────────────────────────────────────
-- Question pool
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS questions (
    id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    pool_config_id    INT         NOT NULL REFERENCES pool_configs(id) ON DELETE CASCADE,
    text              TEXT        NOT NULL,
    question_type     TEXT        NOT NULL,
    marks             INT         NOT NULL,
    difficulty        TEXT        NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
    bloom_level       INT         CHECK (bloom_level BETWEEN 1 AND 6),
    answer_key        TEXT,
    options           JSONB,      -- {a, b, c, d, correct} for choice-based questions
    validation_status TEXT        NOT NULL DEFAULT 'pending'
                                  CHECK (validation_status IN ('pending', 'approved', 'rejected')),
    rejection_reason  TEXT,
    chroma_id         TEXT,       -- embedding ID in ChromaDB for dedup
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_questions_pool_config  ON questions(pool_config_id);
CREATE INDEX IF NOT EXISTS idx_questions_status        ON questions(validation_status);
CREATE INDEX IF NOT EXISTS idx_questions_difficulty    ON questions(difficulty);

-- ─────────────────────────────────────────────
-- Sample / reference questions (uploaded per topic)
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sample_questions (
    id            SERIAL PRIMARY KEY,
    topic_id      INT  NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    skill         TEXT NOT NULL,
    marks         INT  NOT NULL,
    question_type TEXT NOT NULL,
    difficulty    TEXT NOT NULL,
    text          TEXT NOT NULL,
    answer_key    TEXT,
    options       JSONB,
    bloom_level   INT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sample_questions_topic ON sample_questions(topic_id);
