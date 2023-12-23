from typing import Optional, Any


def get_record(cursor,
               select_col_name: str,
               table_name: str,
               where_col_name: str,
               where_col_value: Any) -> Optional[Any]:
    query = (f"SELECT {select_col_name} "
             f"FROM {table_name} "
             f"WHERE {where_col_name} = %s")

    cursor.execute(query, (where_col_value,))
    return_value = cursor.fetchall()

    if len(return_value) > 1:
        raise ValueError("error: retrieved more than 1 record")

    if not return_value:
        return None
    else:
        return return_value[0][0]


def get_records_partial(cursor,
                       select_col_name: str,
                       table_name: str,
                       where_col_name: str,
                       partial_value: str) -> list[Any, ...]:
    """Retrieves all records that match partial_name. Uses LOWER for now"""
    query = (f"SELECT {select_col_name} "
             f"FROM {table_name} "
             f"WHERE LOWER({where_col_name}) LIKE %s")
    partial_lower = f"{partial_value.lower()}%"
    cursor.execute(query, (partial_lower, ))
    res = cursor.fetchall()
    return [item[0] for item in res]


def insert_record(cursor,
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


def delete_record(cursor,
                  table_name: str,
                  col_name: str,
                  col_value: str) -> None:
    query = (f"DELETE FROM {table_name} "
             f"WHERE {col_name} = %s")
    cursor.execute(query, (col_value, ))