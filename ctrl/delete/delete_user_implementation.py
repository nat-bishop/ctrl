import ctrl.database.query as query
import click


def delete_user(cursor, name):
    id = query.get_record(cursor,'UserID', 'Users', 'Name', name)
    if not id:
        click.echo(f"user: {name} not found")
        exit(1)

    query.delete_record(cursor, 'Asset_Users', 'UserID', id)
    query.delete_record(cursor, 'Project_Users', 'UserID', id)
    query.delete_record(cursor, 'Users', 'UserID', id)
