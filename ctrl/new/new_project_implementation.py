import click
import ctrl.utils.helpers as helpers
import ctrl.database.utils as db
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
    user_ids = _create_users_db(creators)
    project_query = ("INSERT INTO Projects (PayloadPath, Title, Description, DateCreated) "
                     "VALUES (%s, %s, %s, %s) "
                     "RETURNING ProjectID;")
    params = (str(proj_path), name, desc, datetime.now())
    project_id = db.execute_query(project_query, params, True)[0][0]
    user_query = ("INSERT INTO Project_Users "
                  "VALUES (%s, %s)")
    for user in user_ids:
        params = (project_id, user)
        db.execute_query(user_query, params)

    click.echo("added project to database")


def _create_users_db(users: list[str]) -> list[int]:
    """Creates user in db if they dont exist, returns userids of users"""
    user_query = "SELECT * FROM Users;"
    res = db.execute_query(user_query)
    user_names = [item[1].lower() for item in res]
    user_ids = []
    for user in users:
        if user.lower() not in user_names:
            click.confirm(f"could not find user: {user}, create new user in database?")
            bio = click.prompt("bio for new user: ", type=str)
            click.echo("")
            add_user_query = ("INSERT INTO Users (Name, Bio) "
                              "VALUES (%s, %s) "
                              "RETURNING UserId")
            params = (user, bio)
            user_id = db.execute_query(add_user_query, params, True)[0][0]
            user_ids.append(user_id)
            click.echo(f"added user: {user} to database")
        else:
            find_user_query = ("SELECT UserID "
                               "FROM Users "
                               "WHERE Name = %s")
            user_ids.append(db.execute_query(find_user_query, (user,), True)[0][0])

    return user_ids


def _add_project_dirs(proj_path, tools):
    for tool in tools:
        (proj_path / tool).mkdir(parents=True)
        (proj_path / tool / 'projectFiles').mkdir(parents=True)
        (proj_path / tool / 'exports').mkdir(parents=True)

    (proj_path / 'assets').mkdir(parents=True)
    (proj_path / 'references').mkdir(parents=True)
    (proj_path / 'outputs').mkdir(parents=True)

    click.echo(" ")
    click.echo("created project files")

