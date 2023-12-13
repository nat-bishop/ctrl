import shutil
import sys
from pathlib import Path

import click
import dirsync


def sync(source_path: Path, target_path: Path) -> None:
    if source_path.name != target_path.name:
        click.echo("folder names do not match")
        sys.exit()

    if not target_path.exists():
        click.echo("target folder does not exist")
        click.echo("")
        styled_output = click.style(f"copy '{click.format_filename(source_path)}' into new dir '{click.format_filename(target_path)}'?", fg="red")
        click.confirm(styled_output, abort=True)
        shutil.copytree(source_path, target_path, dirs_exist_ok=False)
        click.echo("copied")
        sys.exit()
    else:
        styled_output = click.style(f"sync '{click.format_filename(source_path)}' into '{click.format_filename(target_path)}'?", fg="red")
        click.confirm(styled_output, abort=True)
        dirsync.sync(source_path, target_path, 'update', verbose=True, create=False)
