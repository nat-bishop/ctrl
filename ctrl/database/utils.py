import psycopg2
from pathlib import Path
from contextlib import closing
from datetime import datetime


def execute_query(query: str, params: list[str] = None, fetch=False) -> list[tuple[str]]:
    with closing(psycopg2.connect(dbname="natsdb", user="natbishop", password="12345678", host="localhost")) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if query.strip().upper().startswith("SELECT") or fetch:
                return cursor.fetchall()
            conn.commit()

def insert_project(relative_path: Path, title: str, description: str, date_created: datetime):
    pass


