import subprocess
import click
from pathlib import Path

import ctrl.config as config


def save(tool: str, name: str, type: str) -> None:
    """save current open TOOL session"""
    if tool == 'houdini':
        save_hython_path = Path(__file__).parent / 'save_houdini_implementation_hython.py'
        arg_list = [config.HYTHON_PATH, save_hython_path]
        if name:
            arg_list.append('--name')
            arg_list.append(name)
        if type:
            arg_list.append('--type')
            arg_list.append(type)

        click.echo(arg_list)
        ctrl_root = Path(__file__).parents[2]
        completed_process = subprocess.run(arg_list, capture_output=True, timeout=15, cwd=ctrl_root)

        if completed_process.returncode == 0:
            output = completed_process.stdout.decode()
            # Process output
            click.echo(output)
        else:
            click.echo(f"Error: {completed_process.stderr}")
    else:
        click.echo(f"not implemented remote saving for {tool}")