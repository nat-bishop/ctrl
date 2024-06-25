import os

import click
from typing import Optional
import ctrl.utils.helpers as helpers


def open(name: str, tool: Optional[str], file: Optional[str]) -> None:
    proj_path = helpers.get_proj_path(name)
    if not file:
        os.startfile(proj_path)
    else:
        project_files_path = proj_path / tool / 'projectFiles'
        newest_files = helpers.get_latest_files(project_files_path)
        file_path = newest_files[file]
        click.echo(f"launching file: {file}")
        os.startfile(file_path)