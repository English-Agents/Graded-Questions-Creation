import numpy as np
from database.config import get_connection, release_connection


def fetch_all_questions_from_db(question_type=None):
    """
    Fetches existing questions for diversity log and similarity checking.
    Returns list of dicts.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if question_type:
            cursor.execute(
                """
                SELECT question_id, question_text, correct_answer,
                       correct_answer_position, domain
                FROM questions
                WHERE question_type = %s
                """,
                (question_type,)
            )
        else:
            cursor.execute(
                """
                SELECT question_id, question_text, correct_answer,
                       correct_answer_position, domain
                FROM questions
                """
            )
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        release_connection(conn)


def fetch_all_embeddings_from_db(question_type=None):
    """
    Fetches stored embeddings for similarity checking.
    Returns numpy array of shape (n_questions, 384).
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if question_type:
            cursor.execute(
                """
                SELECT embedding FROM questions
                WHERE question_type = %s
                  AND embedding IS NOT NULL
                """,
                (question_type,)
            )
        else:
            cursor.execute(
                """
                SELECT embedding FROM questions
                WHERE embedding IS NOT NULL
                """
            )
        rows = cursor.fetchall()
        if not rows:
            return np.array([]).reshape(0, 384)
        return np.array([row[0] for row in rows])
    finally:
        cursor.close()
        release_connection(conn)


def check_similarity_in_db(embedding, question_type=None,
                            similarity_threshold=0.85):
    """
    Uses pgvector cosine similarity to find near-duplicate questions in DB.
    Returns list of similar questions found, empty list if none.
    This is faster than loading all embeddings for large datasets.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        embedding_list = embedding.tolist()

        if question_type:
            cursor.execute(
                """
                SELECT question_id, question_text,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM questions
                WHERE question_type = %s
                  AND embedding IS NOT NULL
                  AND 1 - (embedding <=> %s::vector) > %s
                ORDER BY similarity DESC
                LIMIT 5
                """,
                (embedding_list, question_type,
                 embedding_list, similarity_threshold)
            )
        else:
            cursor.execute(
                """
                SELECT question_id, question_text,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM questions
                WHERE embedding IS NOT NULL
                  AND 1 - (embedding <=> %s::vector) > %s
                ORDER BY similarity DESC
                LIMIT 5
                """,
                (embedding_list, embedding_list, similarity_threshold)
            )
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        cursor.close()
        release_connection(conn)


def insert_question_to_db(question, embedding):
    """
    Inserts a new accepted question with its embedding into PostgreSQL.
    Also syncs to Google Sheets if configured.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        emb_value = embedding.tolist() if embedding is not None else None
        cursor.execute(
            """
            INSERT INTO questions (
                question_id, question_type, question_text,
                instructions, options, correct_answer,
                correct_answer_position, explanation,
                difficulty, domain, question_purpose,
                tags, schema_type, embedding
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                CASE WHEN %s IS NULL THEN NULL ELSE %s::vector END
            )
            ON CONFLICT (question_id) DO NOTHING
            RETURNING id
            """,
            (
                question.get("question_id"),
                question.get("question_type"),
                question.get("question_text"),
                question.get("instructions"),
                question.get("options"),
                question.get("correct_answer"),
                question.get("correct_answer_position"),
                question.get("explanation"),
                question.get("difficulty"),
                question.get("domain"),
                question.get("question_purpose"),
                question.get("tags"),
                question.get("schema_type"),
                emb_value,
                emb_value,
            )
        )
        conn.commit()
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        release_connection(conn)


def check_exact_duplicate_in_db(question_text, question_type=None):
    """
    Fast exact text check before doing the more expensive
    embedding similarity check.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if question_type:
            cursor.execute(
                """
                SELECT question_id FROM questions
                WHERE LOWER(TRIM(question_text)) = LOWER(TRIM(%s))
                  AND question_type = %s
                LIMIT 1
                """,
                (question_text, question_type)
            )
        else:
            cursor.execute(
                """
                SELECT question_id FROM questions
                WHERE LOWER(TRIM(question_text)) = LOWER(TRIM(%s))
                LIMIT 1
                """,
                (question_text,)
            )
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        release_connection(conn)
