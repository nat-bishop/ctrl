from pathlib import Path


def projects(ctx, param, incomplete):
    import ctrl.database.utils as db
    project_query = "SELECT Title FROM Projects WHERE LOWER(Title) LIKE %s"
    project_inc = f"{incomplete.lower()}%"
    res = db.execute_query(project_query, (project_inc,))
    return ['"'+item[0]+'"' for item in res]


def tools(ctx, param, incomplete):
    import ctrl.utils.helpers as helpers
    proj_path = helpers.get_proj_path(ctx.params.get('project_name'))
    tools = helpers.get_tools(proj_path)
    return [x.name for x in tools if x.name.lower().startswith(incomplete.lower())]


def project_files(ctx, param, incomplete):
    import ctrl.utils.helpers as helpers
    proj_path = helpers.get_proj_path(ctx.params.get('project_name'))
    tool_path = proj_path / ctx.params.get('tool') / 'projectFiles'
    newest_files = helpers.get_latest_files(tool_path).keys()
    return [x for x in newest_files if x.lower().startswith(incomplete.lower())]


def project_users(ctx, param, incomplete):
    import ctrl.database.utils as db
    query = ("SELECT u.Name "
             "FROM Users u "
             "WHERE LOWER(u.Name) LIKE %s")
    user_incomplete = f"{incomplete.lower()}%"

    res = db.execute_query(query, (user_incomplete, ))
    return ['"'+item[0]+'"' for item in res]