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
