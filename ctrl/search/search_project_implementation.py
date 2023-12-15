import os

import click
import sys
import ctrl.utils.helpers as helpers
import ctrl.display.display as display


def search(name: str, amount: int, gui_enabled: bool) -> None:
    proj_path = helpers.proj_abs_path(name)
    if proj_path.exists():
        click.echo("project found")
        helpers.print_project(proj_path)
        if gui_enabled:
            display.display_project_output(proj_path)
        sys.exit()
    else:
        click.echo("project not found")
        click.echo("")
        click.echo(f"similar projects to '{name}':")
        subdirs = [x.name for x in helpers.get_subdirs(proj_path)]
        similar_list = helpers.find_similarity(name, subdirs)
        similar_list = similar_list[:amount]
        for count, (name, similarNum) in enumerate(similar_list):
            click.echo(f"{count}. {name} {int(100 * similarNum)}")
        click.echo("")
        click.echo("more info?")
        result = click.prompt("enter number", type=int)
        project, _ = similar_list[result]
        proj_path = helpers.proj_abs_path(project)
        if gui_enabled:
            display.display_project_output(proj_path)
        click.echo("")
        helpers.print_project(proj_path)
