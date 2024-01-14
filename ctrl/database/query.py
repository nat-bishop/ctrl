from typing import Optional, Any
from datetime import date
import click


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


def get_user_id(cursor, name: str) -> int:
    return get_record(cursor,'UserID', 'Users', 'Name', name)


def get_project_id(cursor, name: str) -> int:
    return get_record(cursor, 'ProjectID', 'Projects', 'Title', name)


def get_asset_id(cursor, name: str) -> int:
    return get_record(cursor, 'AssetID', 'Assets', 'Title', name)


def get_tag_id(cursor, name: str) -> int:
    return get_record(cursor, 'TagID', 'Tags', 'Name', name)


def update_records(cursor, table_name: str, update_data: dict[Any], where_col_name: str, where_val: Any) -> None:
    if not update_data:
        raise ValueError('no update_data provided')

    # Prepare the SET part of the SQL query
    set_clause = ', '.join([f"{key} = %s" for key in update_data.keys()])
    values = list(update_data.values())

    # The SQL query to update the project
    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_col_name} = %s"
    values.append(where_val)

    # Execute the query
    cursor.execute(query, values)


def get_all_records(cursor, select_cols: list[str], table_name: str, where_col_name: Optional[str] = None, where_val: Optional[Any] = None) -> Optional[list[tuple[Any]]]:
    select_str = ', '.join(select_cols)
    query = f"SELECT {select_str} FROM {table_name} "
    if where_col_name and where_val:
        query += f"WHERE {where_col_name} = %s "
        cursor.execute(query, (where_val,))
    else:
        cursor.execute(query)
    return cursor.fetchall()


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
    cursor.execute(query, (partial_lower,))
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
                  col_value: Any) -> None:
    query = (f"DELETE FROM {table_name} "
             f"WHERE {col_name} = %s")
    cursor.execute(query, (col_value,))


def get_tags_union(cursor, project_names: list[str]):
    param_str = ', '.join(['%s'] * len(project_names))
    query = (f"SELECT DISTINCT t.Name "
             f"FROM Tags t "
             f"JOIN Project_Tags pt ON t.TagID = pt.TagID "
             f"JOIN Projects p ON pt.ProjectID = p.ProjectID "
             f"WHERE p.Title IN ({param_str}) ")
    cursor.execute(query, project_names)
    return [item[0] for item in cursor.fetchall()]


def get_creators_union(cursor, project_names: list[str]):
    param_str = ', '.join(['%s'] * len(project_names))
    query = (f"SELECT DISTINCT u.Name "
             f"FROM Users u "
             f"JOIN Project_Users pu ON u.UserID = pu.UserID "
             f"JOIN Projects p ON pu.ProjectID = p.ProjectID "
             f"WHERE p.Title IN ({param_str}) ")
    cursor.execute(query, project_names)
    return [item[0] for item in cursor.fetchall()]


def get_projects(cursor,
                 partial_name: Optional[str],
                 start_date: Optional[date],
                 end_date: Optional[date],
                 tags: Optional[list[str]],
                 creators: Optional[list[str]]) -> list[str]:
    """retruns list of project names that fit search criteria"""

    query = (f"SELECT p.Title "
             f"FROM Projects p ")

    exists_querys = []
    params = []

    if tags:
        for tag in tags:
            exists_querys.append((f"SELECT 1 FROM Project_Tags pt "
                                  f"JOIN Tags t ON pt.TagID = t.TagID "
                                  f"WHERE t.Name = %s AND pt.ProjectID = p.ProjectID "))
            params.append(tag)
    if creators:
        for user in creators:
            exists_querys.append((f"SELECT 1 FROM Project_Users pu "
                                  f"JOIN Users u ON pu.UserID = u.UserID "
                                  f"WHERE u.Name = %s AND pu.ProjectID = p.ProjectID "))
            params.append(user)

    if exists_querys:
        exists_str = ") AND EXISTS ( ".join(exists_querys)
        query += (f"WHERE "
                  f"EXISTS ( "
                  f"{exists_str} "
                  f") ")

    first_query = True
    if start_date:
        if not first_query:
            query += "AND "
        else:
            query += "WHERE "
            first_query = False
        query += f"p.DateCreated >= %s "
        params.append(start_date)

    if end_date:
        if not first_query:
            query += "AND "
        else:
            query += "WHERE "
            first_query = False
        query += f"p.DateCreated <= %s "
        params.append(end_date)

    if partial_name:
        if not first_query:
            query += "AND "
        else:
            query += "WHERE "
            first_query = False
        query += f"LOWER(p.Title) LIKE %s"
        partial_lower = f"{partial_name.lower()}%"
        params.append(partial_lower)

    cursor.execute(query, params)
    return [item[0] for item in cursor.fetchall()]


def get_assets(cursor,
               partial_name: Optional[str],
               creators: Optional[list[str]],
               tags: Optional[list[str]],
               asset_type: Optional[str],
               rights: Optional[str],
               software: Optional[str],
               projects: Optional[list[str]],
               start_date: Optional[date],
               end_date: Optional[date]):

    query = (f"SELECT a.Title "
             f"FROM Assets a ")

    exists_querys = []
    params = []

    if tags:
        for tag in tags:
            exists_querys.append((f"SELECT 1 FROM Asset_Tags at "
                                  f"JOIN Tags t ON at.TagID = t.TagID "
                                  f"WHERE t.Name = %s AND at.AssetID = a.AssetID "))
            params.append(tag)
    if creators:
        for user in creators:
            exists_querys.append((f"SELECT 1 FROM Asset_Users au "
                                  f"JOIN Users u ON au.UserID = u.UserID "
                                  f"WHERE u.Name = %s AND au.AssetID = a.AssetID "))
            params.append(user)
    if projects:
        for proj in projects:
            exists_querys.append((f"SELECT 1 FROM Asset_Projects ap "
                                  f"JOIN Projects p ON ap.ProjectID = p.ProjectID "
                                  f"WHERE p.Title = %s AND ap.AssetID = a.AssetID "))
            params.append(proj)

    first_query = True
    if exists_querys:
        first_query = False
        exists_str = ") AND EXISTS ( ".join(exists_querys)
        query += (f"WHERE "
                  f"EXISTS ( "
                  f"{exists_str} "
                  f") ")

    if start_date:
        if not first_query:
            query += "AND "
        else:
            query += "WHERE "
            first_query = False
        query += f"a.DateCreated >= %s "
        params.append(start_date)

    if end_date:
        if not first_query:
            query += "AND "
        else:
            query += "WHERE "
            first_query = False
        query += f"a.DateCreated <= %s "
        params.append(end_date)

    if asset_type:
        if not first_query:
            query += "AND "
        else:
            query += "WHERE "
            first_query = False
        query += f"a.Type = %s"
        params.append(asset_type)

    if rights:
        if not first_query:
            query += "AND "
        else:
            query += "WHERE "
            first_query = False
        query += f"a.Rights = %s"
        params.append(rights)

    if software:
        if not first_query:
            query += "AND "
        else:
            query += "WHERE "
            first_query = False
        query += f"a.Mediator = %s"
        params.append(software)

    if partial_name:
        if not first_query:
            query += "AND "
        else:
            query += "WHERE "
            first_query = False
        query += f"LOWER(p.Title) LIKE %s"
        partial_lower = f"{partial_name.lower()}%"
        params.append(partial_lower)

    cursor.execute(query, params)
    return [item[0] for item in cursor.fetchall()]