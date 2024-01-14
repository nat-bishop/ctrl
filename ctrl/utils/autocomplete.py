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
    return [x for x in tools if x.lower().startswith(incomplete.lower())]


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


def assets(ctx, param, incomplete):
    import ctrl.database.utils as utils
    import ctrl.database.query as query
    res = utils.perform_db_op(query.get_records_partial, 'Title', 'Assets', 'Title', incomplete)
    return ['"'+item+'"' for item in res]


def asset_viewing_path(ctx, param, incomplete):
    target_path = ctx.params.get('target_path')
    return [path.relative_to(target_path).as_posix() for path in target_path.glob(f'**/{incomplete}*')]


def tags(ctx, param, incomplete):
    import ctrl.database.utils as utils
    import ctrl.database.query as query
    res = utils.perform_db_op(query.get_records_partial, 'Name', 'Tags', 'Name', incomplete)
    return ['"'+item+'"' for item in res]


def search_tags_project(ctx, param, incomplete):
    import ctrl.database.utils as utils
    import ctrl.database.query as query
    project_names = utils.perform_db_op(query.get_projects,
                                        ctx.params.get('project_name'),
                                        None,
                                        None,
                                        ctx.params.get('tags'),
                                        ctx.params.get('creators'))
    tags = utils.perform_db_op(query.get_tags_union, project_names)
    return ['"'+item+'"' for item in tags if item.lower().startswith(incomplete.lower()) and item not in ctx.params.get('tags')]


def search_creators_project(ctx, param, incomplete):
    import ctrl.database.utils as utils
    import ctrl.database.query as query
    project_ids = utils.perform_db_op(query.get_projects,
                                      ctx.params.get('project_name'),
                                      None,
                                      None,
                                      ctx.params.get('tags'),
                                      ctx.params.get('creators'))
    creators = utils.perform_db_op(query.get_creators_union, project_ids)
    return ['"'+item+'"' for item in creators if item.lower().startswith(incomplete.lower())]


def search_names_project(ctx, param, incomplete):
    import ctrl.database.utils as utils
    import ctrl.database.query as query
    project_names = utils.perform_db_op(query.get_projects,
                                        ctx.params.get('project_name'),
                                        None,
                                        None,
                                        ctx.params.get('tags'),
                                        ctx.params.get('creators'))
    return ['"'+item+'"' for item in project_names if item.lower().startswith(incomplete.lower())]


def search_assets(ctx, param, incomplete):
    import ctrl.database.query as query
    import ctrl.database.utils as utils
    asset_names = utils.perform_db_op(query.get_assets,
                                      incomplete,
                                      ctx.params.get('creators'),
                                      ctx.params.get('tags'),
                                      ctx.params.get('asset_type'),
                                      ctx.params.get('rights'),
                                      ctx.params.get('software'),
                                      ctx.params.get('projects'),
                                      ctx.params.get('from_date'),
                                      ctx.params.get('to_date'))

    return ['"'+item+'"' for item in asset_names if item.lower().startswith(incomplete.lower())]
