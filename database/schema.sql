-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Main questions table
CREATE TABLE IF NOT EXISTS questions (
    id                      SERIAL PRIMARY KEY,
    question_id             VARCHAR(50) UNIQUE NOT NULL,
    question_type           VARCHAR(100) NOT NULL,
    question_text           TEXT NOT NULL,
    instructions            TEXT,
    options                 TEXT,
    correct_answer          TEXT,
    correct_answer_position VARCHAR(10),
    explanation             TEXT,
    difficulty              VARCHAR(20),
    domain                  VARCHAR(100),
    question_purpose        TEXT,
    tags                    TEXT,
    schema_type             TEXT,
    embedding               vector(384),
    created_at              TIMESTAMP DEFAULT NOW(),
    updated_at              TIMESTAMP DEFAULT NOW()
);

-- IVFFlat index for fast similarity search
-- Use 'lists' = roughly sqrt(total_rows)
-- Start with 10 for small datasets, increase as you grow
CREATE INDEX IF NOT EXISTS questions_embedding_idx
ON questions
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 10);

-- Index for fast filtering by question type
CREATE INDEX IF NOT EXISTS questions_type_idx
ON questions (question_type);

-- Index for fast duplicate check by exact text
CREATE INDEX IF NOT EXISTS questions_text_idx
ON questions USING hash (question_text);
