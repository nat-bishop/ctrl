import shutil
import sys
import click
from datetime import datetime
from pathlib import Path

import ctrl.utils.constants as constants
import ctrl.utils.helpers as helpers
import ctrl.new.new_utils as new_utils


def new_file(name: str, tool: str, file_name: str, type: str) -> None:
    proj_path = helpers.get_proj_path(name)
    if not proj_path:
        click.echo(f"project: {name} not found")
        exit(1)

    if tool not in helpers.get_tools(proj_path):
        click.echo(f"{tool} not found in project {name}")
        click.echo("creating tool dirs")
        new_utils.new_tool_dirs(proj_path, tool)

    extension = constants.FILE_EXTENSIONS[tool]
    new_file = helpers.construct_filename(name, file_name, type, datetime.now(), extension)
    file_path = proj_path / tool / 'projectFiles' / new_file
    template_path = Path(__file__).parents[2] / 'templates' / f'{tool}_empty.{extension}'

    if file_path.exists():
        click.echo(f"error, file already exists at {file_path}")
        sys.exit(1)

    shutil.copy(template_path, file_path)
    click.echo(f"opening file: {new_file}")
    click.launch(str(file_path))
