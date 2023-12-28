import shutil
import click
import ctrl.database.query as query


def delete_project(cursor, name):
    proj_id = query.get_record(cursor,'ProjectID', 'Projects', 'Title', name)
    if not proj_id:
        click.echo(f"project: {name} not found")
        exit(1)
    path = query.get_record(cursor,'PayloadPath', 'Projects', 'ProjectID', proj_id)
    click.confirm(click.style(f'WARNING: this will destroy all files in project folder:{path} Proceed?', fg='red'), abort=True)

    query.delete_record(cursor, 'Asset_Projects', 'ProjectID', proj_id)
    query.delete_record(cursor, 'Project_Users', 'ProjectID', proj_id)
    query.delete_record(cursor, 'Project_Tags', 'ProjectID', proj_id)
    query.delete_record(cursor, 'Projects', 'ProjectID', proj_id)

    shutil.rmtree(path)
