import ctrl.database.utils as utils
import ctrl.database.query as query
import click


def new_user(user_name: str, bio: str) -> None:
    data = {'Name': user_name,
            'Bio': bio}
    click.confirm(f"create user: {user_name}, with bio: {bio}", abort=True)
    utils.perform_db_op(query.insert_record, 'Users', data, 'UserID')
    click.echo(f"created user")