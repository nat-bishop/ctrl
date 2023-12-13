from pathlib import Path


def projects_autocomplete(ctx, param, incomplete):
    import ctrl.config as config
    import ctrl.utils.helpers as helpers
    projects_dir = Path(config.ART_ROOT_PATH, 'projects')
    return [x.name for x in helpers.get_subdirs(projects_dir) if x.name.lower().startswith(incomplete.lower())]


def tools_autocomplete(ctx, param, incomplete):
    import ctrl.utils.helpers as helpers
    proj_path = helpers.proj_abs_path(ctx.params.get('project_name'))
    tools = helpers.get_tools(proj_path)
    return [x.name for x in tools if x.name.lower().startswith(incomplete.lower())]


def project_files_autocomplete(ctx, param, incomplete):
    import ctrl.utils.helpers as helpers
    proj_path = helpers.proj_abs_path(ctx.params.get('project_name'))
    tool_path = proj_path / ctx.params.get('tool') / 'projectFiles'
    newest_files = helpers.get_latest_files(tool_path).keys()
    return [x for x in newest_files if x.lower().startswith(incomplete.lower())]