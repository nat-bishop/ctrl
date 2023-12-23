import click
import ctrl.utils.helpers as helpers
import ctrl.database.utils as utils
import ctrl.database.query as query
from datetime import datetime
from pathlib import Path
import ctrl.config as config


def new(name: str, tools: list[str], creators: list[str]) -> None:
    proj_path = helpers.get_proj_path(name)
    if proj_path:
        click.echo("project already exists")
        helpers.print_project(proj_path)
    else:
        desc = click.prompt("description for new project")
        proj_path = Path(config.ART_ROOT_PATH, helpers.sent_to_camel(name))
        tools_str = ", ".join(tools)
        creators_str = ", ".join(creators)
        click.echo(f"title: {name}")
        click.echo(f"path: {proj_path}")
        click.echo(f"tools: {tools_str}")
        click.echo(f"creators: {creators_str}")
        click.echo(f"desc: {desc}")
        click.confirm("create project?", abort=True)
        _add_project_dirs(proj_path, tools)
        _add_project_db(creators, proj_path, name, desc)


def _add_project_db(creators: list[str], proj_path: Path, name: str, desc: str) -> None:
    user_ids = []
    for user in creators:
        user_ids.append(utils.perform_db_op(query.get_record, 'Name', 'Users', 'UserID'), user)
    data = {'PayloadPath': str(proj_path),
            'Title': name,
            'Description': desc,
            'DateCreated': datetime.now()}

    project_id = utils.perform_db_op(query.insert_record, 'Projects', data, 'ProjectID')
    data['ProjectID'] = project_id
    for user in user_ids:
        data['UserID'] = user
        utils.perform_db_op(query.insert_record, 'Project_Users', data)

    click.echo("added project to database")


def _add_project_dirs(proj_path: Path, tools: list[str,...]) -> None:
    for tool in tools:
        (proj_path / tool).mkdir(parents=True)
        (proj_path / tool / 'projectFiles').mkdir(parents=True)
        (proj_path / tool / 'exports').mkdir(parents=True)

    (proj_path / 'assets').mkdir(parents=True)
    (proj_path / 'references').mkdir(parents=True)
    (proj_path / 'outputs').mkdir(parents=True)

    click.echo(" ")
    click.echo("created project files")

