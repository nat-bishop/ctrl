import click


def projects(ctx, param, incomplete):
    import ctrl.database.utils as utils
    import ctrl.database.query as query
    res = utils.perform_db_op(query.get_records_partial, 'Title', 'Projects', 'Title', incomplete)
    return ['"'+item+'"' for item in res]


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


def users(ctx, param, incomplete):
    import ctrl.database.utils as utils
    import ctrl.database.query as query
    res = utils.perform_db_op(query.get_records_partial, 'Name', 'Users', 'Name', incomplete)
    return ['"'+item+'"' for item in res]


def asset_viewing_path(ctx, param, incomplete):
    target_path = ctx.params.get('target_path')
    return [path.relative_to(target_path).as_posix() for path in target_path.glob(f'**/{incomplete}*')]


def asset_tags(ctx, param, incomplete):
    import ctrl.database.utils as utils
    import ctrl.database.query as query
    res = utils.perform_db_op(query.get_records_partial, 'Name', 'Tags', 'Name', incomplete)
    return ['"'+item+'"' for item in res]