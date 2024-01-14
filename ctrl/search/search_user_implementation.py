import ctrl.database.utils as utils
import ctrl.database.query as query
import click
import sys


def search_user(name):
    utils.perform_db_op(_search_user_db, name)


def _search_user_db(cursor, name):
    res = query.get_all_records(cursor,
                                ['UserID', 'Name', 'Bio'],
                                'Users',
                                'Name',
                                name)

    if not res:
        click.echo(f"no users found with name: {name}")
        sys.exit(1)
    elif len(res) > 1:
        click.echo(f"more than one user found that matches: {name}")
    else:
        user_id, name, bio = res[0]
        query_str = (f"SELECT pu.ProjectID "
                     f"FROM Project_Users pu "
                     f"WHERE pu.Userid = %s ")
        cursor.execute(query_str, (user_id,))
        res = cursor.fetchall()
        proj_list = [query.get_record(cursor,
                                      'Title',
                                      'Projects',
                                      'ProjectID',
                                      item[0])
                     for item in res]
        proj_str = ", ".join(proj_list)

        query_str = (f"SELECT au.AssetID "
                     f"FROM Asset_Users au "
                     f"WHERE au.Userid = %s ")
        cursor.execute(query_str, (user_id,))
        res = cursor.fetchall()
        asset_list = [query.get_record(cursor,
                                       'Title',
                                       'Assets',
                                       'AssetID',
                                       item[0])
                      for item in res]
        asset_str = ", ".join(asset_list)

        click.echo(f"")
        click.echo(f"name: {name}")
        click.echo(f"bio: {bio}")
        click.echo(f"projects: {proj_str}")
        click.echo(f"assets: {asset_str}")
