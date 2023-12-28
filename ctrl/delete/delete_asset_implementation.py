import shutil
import click
import ctrl.database.query as query


def delete_asset(cursor, name):
    asset_id = query.get_record(cursor,'AssetID', 'Assets', 'Title', name)
    if not asset_id:
        click.echo(f"asset: {name} not found")
        exit(1)

    path = query.get_record(cursor,'AssetPath', 'Assets', 'AssetID', asset_id)
    click.confirm(click.style(f'WARNING: this will destroy all files in asset folder:{path} Proceed?', fg='red'), abort=True)

    query.delete_record(cursor, 'Asset_Projects', 'AssetID', asset_id)
    query.delete_record(cursor, 'Asset_Tags', 'AssetID', asset_id)
    query.delete_record(cursor, 'Asset_Users', 'AssetID', asset_id)
    query.delete_record(cursor, 'Asset_Parts', 'AssetID', asset_id)
    query.delete_record(cursor, 'Asset_Variations', 'AssetID', asset_id)
    query.delete_record(cursor, 'Assets', 'AssetID', asset_id)


    shutil.rmtree(path)