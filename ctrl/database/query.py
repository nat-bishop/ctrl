import psycopg2
from typing import Optional, Any


def get_record(cursor: psycopg2.cursor,
               table_name: str,
               src_col_name: str,
               src_value: Any,
               target_col_name: str) -> Optional[Any]:
    query = (f"SELECT {target_col_name}"
             f"FROM {table_name}"
             f"WHERE {src_col_name} = %s")

    cursor.execute(query, (src_value, ))
    return_value = cursor.fetchall()

    if len(return_value) > 1:
        raise ValueError("error: retrieved more than 1 record")

    if not return_value:
        return None
    else:
        return return_value[0][0]


def insert_record(cursor: psycopg2.cursor,
                  table_name: str,
                  data: dict[str, Any],
                  return_col: Optional[str] = None) -> Optional[Any]:

    keys = data.keys()
    values = data.values()
    insert_columns = ', '.join(keys)
    insert_placeholders = ', '.join(['%s'] * len(keys))

    query = (f"INSERT INTO {table_name} ({insert_columns}) "
             f"VALUES ({insert_placeholders})")

    if return_col:
        query += f" RETURNING {return_col}"

    cursor.execute(query, list(values))

    if return_col:
        return cursor.fetchone()[0]


def delete_record(cursor: psycopg2.cursor,
                  table_name: str,
                  col_name: str,
                  col_value: str) -> None:
    query = (f"DELETE FROM {table_name} "
             f"WHERE {col_name} = %s")
    cursor.execute(query, (col_value, ))