import click

import ctrl.utils.helpers as helpers


def new(name: str, tools: list[str]) -> None:
    proj_path = helpers.proj_abs_path(name)
    if proj_path.exists():
        click.echo("project already exists")
        helpers.print_project(proj_path)
    else:
        click.confirm(f"create project at directory: {proj_path}?", abort=True)
        for tool in tools:
            (proj_path / tool).mkdir(parents=True)

        (proj_path / 'assets').mkdir(parents=True)
        (proj_path / 'references').mkdir(parents=True)
        (proj_path / 'outputs').mkdir(parents=True)

        click.echo(" ")
        click.echo("created project files")
