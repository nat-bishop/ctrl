from pathlib import Path
import click
import ctrl.utils.autocomplete as autocomplete
import ctrl.utils.constants as constants
from datetime import date


@click.group()
def cli():
    pass


@cli.command()
@click.argument('source_path', required=True, type=click.Path(exists=True, resolve_path=True, file_okay=False, path_type=Path))
@click.argument('target_path', required=True, type=click.Path(file_okay=False, resolve_path=True,path_type=Path))
def sync(source_path, target_path):
    """Sync directory at SOURCE_PATH to directory at TARGET_PATH."""
    from ctrl.sync.sync_implementation import sync
    sync(source_path, target_path)


@cli.group()
def search():
    """Tool for searching assets or projects."""
    pass


@search.command(name='project')
@click.argument('project_name', shell_complete=autocomplete.projects, required=True, type=str)
@click.option('--amount', '-a', default=10, required=False, type=int,
              help='max number of results')
@click.option('--gui/--no-gui', default=True,
              help='display project with gui')
def search_project(project_name, amount, gui):
    """Search for PROJECT_NAME, or find similar."""
    from ctrl.search.search_project_implementation import search
    search(project_name, amount, gui)


@cli.group()
def new():
    """Tool for creating new projects or files."""
    pass


@new.command(name='project')
@click.argument('project_name', required=True, type=str)
@click.argument("tools", nargs=-1, type=click.Choice(constants.TOOLS))
@click.option('--tags', '-t', multiple=True, shell_complete=autocomplete.asset_tags,
              help='either pick from predefined list or create a new tag')
@click.option('--description', '-d', type=str, prompt=True)
@click.option('--creators', '-c', required=False, shell_complete=autocomplete.users, multiple=True,
              help='authors of project')
@click.confirmation_option(prompt='create new project?')
def new_project(project_name, tools, tags, description, creators):
    """Create new project PROJECT_NAME with TOOLS, DESCRIPTION and CREATORS."""
    from ctrl.new.new_project_implementation import new
    import ctrl.database.utils as utils
    if not creators:
        creators = []
    utils.perform_db_op(new, project_name, tools, tags, description, creators)


@new.command(name='user')
@click.argument('user_name', required=True, type=str)
@click.option('--bio', type=str, prompt=True)
def new_user(user_name, bio):
    """Create new user with USER_NAME and BIO"""
    from ctrl.new.new_user_implementation import new_user
    new_user(user_name, bio)


@new.command(name='file')
@click.argument('project_name', shell_complete=autocomplete.projects, required=True, type=str)
@click.argument('tool', type=click.Choice(constants.TOOLS), required=True)
@click.argument('file_name', required=True)
@click.argument('type', required=True, type=click.Choice(constants.FILE_TYPE))
@click.confirmation_option(prompt='create new file?')
def new_file(name, tool, file_name, type):
    """Creates new file with the following attributes:

    PROJECT_NAME is the name of the project
    TOOL is the tool the file is used in
    FILE_NAME is the name of the file
    TYPE is the type of file (render, model, ect.)"""
    from ctrl.new.new_file_implementation import new_file
    new_file(name, tool, file_name, type)


@new.command(name='asset')
@click.argument('target_path', type=click.Path(exists=True, resolve_path=True, path_type=Path, file_okay=False))
@click.argument('name', type=str)
@click.argument('type', type=click.Choice(constants.ASSET_TYPES))
@click.argument('viewing_path', type=click.Path(path_type=Path), shell_complete=autocomplete.asset_viewing_path)
@click.argument('thumbnail-path', type=click.Path(path_type=Path), shell_complete=autocomplete.asset_viewing_path)
@click.argument('rights', type=click.Choice(constants.RIGHTS, case_sensitive=False))
@click.option('--mediator', '-m', type=click.Choice(constants.SOFTWARES, case_sensitive=False),
              help='software version used to create asset')
@click.option('--description', '-d', type=str, prompt=True,
              help='description of asset, is prompted if not set in commandline')
@click.option('--tags', '-t', multiple=True, shell_complete=autocomplete.asset_tags,
              help='either pick from predefined list or create a new tag')
@click.option('--creators', '-c', multiple=True, shell_complete=autocomplete.users,
              help='creators of the asset')
@click.option('--date-created', '-d', type=click.DateTime(formats=["%Y-%m-%d"]), default=str(date.today()),
              help='date asset was created, defaults to today')
@click.option('--parent-name', '-p', shell_complete=autocomplete.projects,
              help='name of parent asset if this asset is a part')
@click.option('--original-name', '-o', shell_complete=autocomplete.projects,
              help='name of original asset if this asset is a variation')
def new_asset(target_path, name, type, viewing_path, mediator, rights, description, thumbnail_path, tags, creators, date_created, parent_name, original_name):
    """Creates new asset with following attributes:

    TARGET_PATH is the path of the asset files. These will be copied to a read-only location for storage \n
    NAME is the name of the asset, this does not have to be unique \n
    TYPE is the type of asset, from a predefined list (model, texture, ect.) \n
    VIEWING_PATH is the path to the file that is used for viewing asset (ex. main usd file) \n
    THUMBNAIL_PATH is the path to the image file for previewing asset \n
    RIGHTS is the usage rights of the asset"""
    from ctrl.new.new_asset_implementation import new_asset
    import ctrl.database.utils as utils
    utils.perform_db_op(new_asset, target_path, name, type, viewing_path, mediator, rights, description, thumbnail_path, tags, creators, date_created, parent_name, original_name)


@cli.command()
@click.argument('project_name', shell_complete=autocomplete.projects, required=True, type=str)
@click.argument('tool', shell_complete=autocomplete.tools, required=True)
@click.argument('file', shell_complete=autocomplete.project_files, required=True)
def open(project_name, tool, file):
    """Opens FILE for TOOL in PROJECT_NAME"""
    from ctrl.open.open_implementation import open
    open(project_name, tool, file)


@cli.command()
@click.argument('tool', type=click.Choice(constants.TOOLS), required=True)
@click.option('--name', '-n', required=False,
              help='optional new name')
@click.option('--type', '-t', required=False, type=click.Choice(constants.FILE_TYPE),
              help='optional new file type')
def save(tool, name, type):
    """save current open session for TOOL"""
    from ctrl.save.save_implementation import save
    save(tool, name, type)


@cli.group()
def delete():
    """Tool for deleting assets, users and projects"""
    pass


@delete.command(name='user')
@click.argument('name', shell_complete=autocomplete.users)
@click.confirmation_option(prompt='delete user?')
def delete_user(name):
    """delete user NAME"""
    from ctrl.delete.delete_user_implementation import delete_user
    from ctrl.database.utils import perform_db_op
    perform_db_op(delete_user, name)


@delete.command(name='project')
@click.argument('project', shell_complete=autocomplete.projects)
@click.confirmation_option(prompt='delete project?')
def delete_project(name):
    """delete user NAME"""
    from ctrl.delete.delete_project_implementation import delete_project
    from ctrl.database.utils import perform_db_op
    perform_db_op(delete_project, name)