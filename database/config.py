import os
from psycopg2 import pool
from pgvector.psycopg2 import register_vector

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     os.getenv("DB_PORT", "5432"),
    "dbname":   os.getenv("DB_NAME", "questions_db"),
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

# Connection pool — reuse connections instead of opening new ones
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **DB_CONFIG
)

def get_connection():
    conn = connection_pool.getconn()
    register_vector(conn)
    return conn

def release_connection(conn):
    connection_pool.putconn(conn)
