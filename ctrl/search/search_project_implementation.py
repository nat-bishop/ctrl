import click
import ctrl.display.display as display
import ctrl.database.query as query
import ctrl.database.utils as utils
import ctrl.utils.helpers as helpers
from typing import Optional
from datetime import date


def search(name: Optional[str],
           creators: Optional[list[str]],
           tags: Optional[list[str]],
           from_date: Optional[date],
           to_date: Optional[date],
           gui_enabled: bool) -> None:

    projects = utils.perform_db_op(query.get_projects, name, from_date, to_date, tags, creators)
    if not projects:
        click.echo("no projects found that match search params")
    elif len(projects) == 1:
        name = projects[0]
        click.echo("found project:")
        helpers.print_project(name)
        if gui_enabled:
            display.display_project_output(name)
            click.echo("")
    else:
        click.echo("projects found:")
        click.echo("")
        for proj_name in projects:
            helpers.print_project(proj_name)
            click.echo("")
            if gui_enabled:
                display.display_project_output(proj_name)
                click.echo("")