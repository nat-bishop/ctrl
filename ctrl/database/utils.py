import psycopg2
from contextlib import closing
from typing import Any


def execute_query(query: str, params: tuple[Any, ...] = None, fetch=False) -> list[tuple[Any, ...]] | None:
    with closing(psycopg2.connect(dbname="natsdb", user="natbishop", password="12345678", host="localhost")) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith("SELECT") or fetch:
                res = cursor.fetchall()
                conn.commit()
                return res
            conn.commit()


import psycopg2
from psycopg2 import OperationalError, DatabaseError

# Database Configuration
DATABASE_PARAMS = {
    'dbname': 'natsdb',
    'user': 'natbishop',
    'password': '12345678',
    'host': 'localhost'
}

def get_db_connection():
    try:
        return psycopg2.connect(**DATABASE_PARAMS)
    except OperationalError as e:
        print(f"Cannot connect to the database: {e}")
        raise

def perform_database_operation(operation_func, *args, **kwargs):
    """
    Performs a database operation within a transaction.
    The operation is a function that gets passed a cursor and any other arguments.
    """
    with get_db_connection() as conn:
        try:
            with conn.cursor() as cur:
                result = operation_func(cur, *args, **kwargs)
            return result
        except DatabaseError as e:
            conn.rollback()
            raise e