from typing import Optional

import click
import ctrl.utils.helpers as helpers
import ctrl.database.query as query
from datetime import date
from pathlib import Path
import ctrl.config as config
import ctrl.new.tag_utils as tag_utils


def new(cursor, name: str, tools: list[str], tags: Optional[list[str]], description: str, creators: Optional[list[str]]) -> None:
    proj_path = helpers.get_proj_path(name)
    if proj_path:
        click.echo("project already exists")
        helpers.print_project(proj_path)
    else:
        if not creators:
            click.echo(click.style('WARNING', fg='red') + ': no creator selected for new project.')

        if not tags:
            click.echo(click.style('WARNING', fg='red') + ': no tags selected for new project.')

        proj_path = Path(config.ART_ROOT_PATH, helpers.sent_to_camel(name))
        _add_project_db(cursor, tags, creators, proj_path, name, description)
        _add_project_dirs(proj_path, tools)


def _add_project_db(cursor, tags:Optional[list[str]], creators: list[str], proj_path: Path, name: str, desc: str) -> None:
    user_ids = []
    for user in creators:
        user_ids.append(query.get_record(cursor, 'Name', 'Users', 'UserID', user))
    data = {'PayloadPath': str(proj_path),
            'Title': name,
            'Description': desc,
            'DateCreated': date.now()}

    project_id = query.insert_record(cursor, 'Projects', data, 'ProjectID')
    data['ProjectID'] = project_id
    for user in user_ids:
        data['UserID'] = user
        query.insert_record(cursor, 'Project_Users', data)

    if tags:
        updated_tags = tag_utils.create_tags(cursor, tags)
        data = {'ProjectID': project_id}
        for id in updated_tags:
            data['TagID'] = id
            query.insert_record(cursor, 'Asset_Tags', data)

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

