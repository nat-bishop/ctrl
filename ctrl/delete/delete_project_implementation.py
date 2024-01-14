import shutil
import click
import ctrl.utils.helpers as helpers
import ctrl.database.query as query


def delete_project(cursor, name):
    proj_id = query.get_project_id(cursor, name)
    if not proj_id:
        raise ValueError(f"project: {name} not found")

    path = query.get_record(cursor,'PayloadPath', 'Projects', 'ProjectID', proj_id)
    helpers.print_project(name)
    click.confirm(click.style(f'WARNING: this will destroy all files in project folder:{path} Proceed?', fg='red'), abort=True)

    query.delete_record(cursor, 'Asset_Projects', 'ProjectID', proj_id)
    query.delete_record(cursor, 'Project_Users', 'ProjectID', proj_id)
    query.delete_record(cursor, 'Project_Tags', 'ProjectID', proj_id)
    query.delete_record(cursor, 'Projects', 'ProjectID', proj_id)

    shutil.rmtree(path)
