
import click
import ctrl.utils.helpers as helpers
import ctrl.database.query as query
import ctrl.database.utils as utils
from datetime import date
from pathlib import Path
import ctrl.config as config
import ctrl.new.new_utils as new_utils


def new(name: str, tools: list[str], tags: list[str], description: str, creators: list[str]) -> None:
    proj_path = helpers.get_proj_path(name)
    if proj_path:
        click.echo("")
        click.echo("project already exists:")
        helpers.print_project(name)
    else:
        if not creators:
            click.echo(click.style('WARNING', fg='red') + ': no creator selected for new project.')

        if not tags:
            click.echo(click.style('WARNING', fg='red') + ': no tags selected for new project.')

        if not tools:
            click.echo(click.style('WARNING', fg='red') + ': no tools selected for new project.')

        click.confirm('create project?', abort=True)
        proj_path = Path(config.ART_ROOT_PATH, helpers.sent_to_camel(name))
        utils.perform_db_op(_add_project_db, tags, creators, proj_path, name, description)
        _add_project_dirs(proj_path, tools)
        click.echo("")
        click.echo("new project:")
        helpers.print_project(name)


def _add_project_db(cursor, tags: list[str], creators: list[str], proj_path: Path, name: str, desc: str) -> None:
    user_ids = []
    for user in creators:
        user_ids.append(query.get_user_id(cursor, user))
    data = {'PayloadPath': str(proj_path),
            'Title': name,
            'Description': desc,
            'DateCreated': date.today()}

    project_id = query.insert_record(cursor, 'Projects', data, 'ProjectID')
    data = {'ProjectID': project_id}
    for user in user_ids:
        data['UserID'] = user
        query.insert_record(cursor, 'Project_Users', data)

    if tags:
        updated_tags = new_utils.create_tags(cursor, tags)
        data = {'ProjectID': project_id}
        for id in updated_tags:
            data['TagID'] = id
            query.insert_record(cursor, 'Project_Tags', data)
    click.clear()
    click.echo("added project to database")


def _add_project_dirs(proj_path: Path, tools: list[str,...]) -> None:
    proj_path.mkdir()

    for tool in tools:
        new_utils.new_tool_dirs(proj_path, tool)

    (proj_path / 'assets').mkdir()
    (proj_path / 'references').mkdir()
    (proj_path / 'outputs').mkdir()

    click.echo("created project files")