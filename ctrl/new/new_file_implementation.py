import shutil
import sys
import click
from datetime import datetime
from pathlib import Path

import ctrl.config as config
import ctrl.utils.constants as constants
import ctrl.utils.helpers as helpers


def new_file(name: str, tool: str, file_name: str, type: str) -> None:
    proj_path = helpers.get_proj_path(name)

    if tool not in helpers.get_tools(proj_path):
        click.echo(f"{tool} not found in project {name}")
        click.echo("creating tool dirs")
        (proj_path / tool).mkdir(parents=True)

    extension = constants.FILE_EXTENSIONS[tool]
    new_file = helpers.construct_filename(name, file_name, type, datetime.now(), extension)
    file_path = proj_path / tool / 'projectFiles' / new_file
    template_path = Path(config.CTRL_ROOT_PATH, 'templates', f'{tool}_empty.{extension}')

    if file_path.exists():
        click.echo(f"error, file already exists at {file_path}")
        sys.exit(1)

    shutil.copy(template_path, file_path)
    click.echo(f"opening file: {new_file}")
    click.launch(file_path)
