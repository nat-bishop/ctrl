from pathlib import Path
import click
import ctrl.utils.autocomplete as autocomplete
import ctrl.utils.constants as constants


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
@click.argument('project_name', shell_complete=autocomplete.projects_autocomplete, required=True, type=str)
@click.option('--amount', '-a', default=10, required=False, type=int,
              help='max number of results')
@click.option('--gui/--no-gui', default=True,
              help='display project with gui')
@click.option('--usd-view-type', '-u', type=click.Choice(['view', 'record']), default='record',
              help='display usd file with usdview or usdrecord')
def search_project(project_name, amount, gui, usd_view_type):
    """Search for PROJECT_NAME, or find similar."""
    from ctrl.search.search_project_implementation import search
    search(project_name, amount, gui, usd_view_type)


@cli.group()
def new():
    """Tool for creating new projects or files."""
    pass


@new.command(name='project')
@click.argument('project_name', required=True, type=str)
@click.argument("tools", nargs=-1, type=click.Choice(constants.TOOLS))
def new_project(name, tools):
    """Create new project PROJECT_NAME with TOOLS."""
    from ctrl.new.new_project_implementation import new
    new(name, tools)


@new.command(name='file')
@click.argument('project_name', shell_complete=autocomplete.projects_autocomplete, required=True, type=str)
@click.argument('tool', type=click.Choice(constants.TOOLS), required=True)
@click.argument('file_name', required=True)
@click.argument('type', required=True, type=click.Choice(constants.FILE_TYPE))
def new_file(name, tool, file_name, type):
    """Creates new file with the following attributes:

    PROJECT_NAME is the name of the project
    TOOL is the tool the file is used in
    FILE_NAME is the name of the file
    TYPE is the type of file (render, model, ect.)"""
    from ctrl.new.new_file_implementation import new_file
    new_file(name, tool, file_name, type)


@cli.command()
@click.argument('project_name', shell_complete=autocomplete.projects_autocomplete, required=True, type=str)
@click.argument('tool', shell_complete=autocomplete.tools_autocomplete, required=True)
@click.argument('file', shell_complete=autocomplete.project_files_autocomplete, required=True)
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
