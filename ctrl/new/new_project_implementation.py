import click
import ctrl.utils.helpers as helpers
import ctrl.database.utils as db
from pathlib import Path


def new(name: str, tools: list[str], creators: list[str]) -> None:
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


def add_project_db(creators: list[str], proj_path: Path, name: str) -> None:
    create_users_db(creators)



def create_users_db(users: list[str]) -> None:
    """Creates user in db if they dont exist"""
    user_query = "SELECT * FROM Users;"
    res = db.execute_query(user_query)
    user_names = [item[1].lower() for item in res]
    for user in users:
        if user.lower() not in user_names:
            click.confirm(f"could not find user: {user}, create new user in database?")
            bio = click.prompt("bio for new user: ", type=str)
            click.echo("")
            add_user_query = "INSERT INTO Users (Name, Bio) VALUES (%s, %s)"
            params = (user, bio)
            db.execute_query(add_user_query, params)
            click.echo(f"added user: {user} to database")





def add_project_dirs(proj_path):
    pass

