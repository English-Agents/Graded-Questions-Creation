import os
from psycopg2 import pool
from pgvector.psycopg2 import register_vector

DB_CONFIG = {
    "host":            os.getenv("DB_HOST", "localhost"),
    "port":            int(os.getenv("DB_PORT", "5432")),
    "dbname":          os.getenv("DB_NAME", "questions_db"),
    "user":            os.getenv("DB_USER", "postgres"),
    "password":        os.getenv("DB_PASSWORD", ""),
    "connect_timeout": 5,   # fail fast — never hang startup waiting for DB
}

# Render hosted PostgreSQL requires SSL — local Docker does not
if os.getenv("DB_HOST", "localhost") not in ("localhost", "127.0.0.1"):
    DB_CONFIG["sslmode"] = "require"

# Lazy singleton — pool is created on first use, not at import time.
# Creating the pool at module level caused Render startup to hang when
# the PostgreSQL service wasn't ready yet (TCP connect blocked for minutes).
_pool = None

def _get_pool():
    global _pool
    if _pool is None:
        _pool = pool.SimpleConnectionPool(minconn=1, maxconn=10, **DB_CONFIG)
    return _pool

def get_connection():
    conn = _get_pool().getconn()
    register_vector(conn)
    return conn

def release_connection(conn):
    _get_pool().putconn(conn)
