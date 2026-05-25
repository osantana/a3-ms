import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://vapor:vapor@localhost:5432/vapor')

SCHEMA_PATH = Path(__file__).resolve().parent.parent / 'schema.sql'


def get_connection(dsn=None):
    return psycopg.connect(dsn or DATABASE_URL, row_factory=dict_row)


def init_db(dsn=None):
    conn = get_connection(dsn)
    conn.execute(SCHEMA_PATH.read_text())
    conn.commit()
    return conn
