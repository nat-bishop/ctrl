import shutil
from pathlib import Path
from typing import Optional
from datetime import date
import click
import ctrl.database.query as query
import ctrl.utils.helpers as helpers
import ctrl.config as config
import ctrl.new.new_utils as tag_utils


def new_asset(cursor,
              target_path: Path,
              name: str,
              type: str,
              viewing_path: Path,
              mediator: str,
              rights: str,
              description: str,
              thumbnail_path: Path,
              tags: Optional[list[str, ...]],
              creators: Optional[list[str, ...]],
              date_created: date,
              parent_name: str,
              original_name: str) -> None:

    if not (target_path / viewing_path).exists():
        click.echo(f"error, viewing path: {str(target_path / viewing_path)} does not exist")
        raise ValueError

    if not (target_path / thumbnail_path).exists():
        click.echo(f"error, viewing path: {str(target_path / thumbnail_path)} does not exist")
        raise ValueError

    if not creators:
        click.echo(click.style('WARNING', fg='red') + ': no creator selected for new asset.')

    if not thumbnail_path:
        click.echo(click.style('WARNING', fg='red') + ': no thumbnail_path selected for new asset.')

    if not mediator:
        click.echo(click.style('WARNING', fg='red') + ': no mediator selected for new asset.')

    click.confirm('proceed with asset creation?', abort=True)

    # creating asset record
    dest_path = Path(config.ASSET_ROOT_PATH, helpers.sent_to_camel(name))
    data = {'AssetPath': helpers.sent_to_camel(name),
            'ThumbnailPath': str(thumbnail_path),
            'ViewingPath': str(viewing_path),
            'Type': type,
            'Title': name,
            'Description': description,
            'Mediator': mediator,
            'DateCreated': date_created,
            'Rights': rights}
    asset_id = query.insert_record(cursor, 'Assets', data, 'AssetID')

    if tags:
        # creating asset_tags records
        data = {'AssetID': asset_id}
        updated_tags = tag_utils.create_tags(cursor, tags)
        for tag_id in updated_tags:
            data['TagID'] = tag_id
            query.insert_record(cursor, 'Asset_Tags', data)

    # creating asset_variations record
    if original_name:
        variation_desc = click.prompt(f"variation description for {name} that is a variation of {original_name}")
        original_id = query.get_asset_id(cursor, original_name)
        data = {'OriginalAssetID': original_id,
                'VariationAssetID': asset_id,
                'VariationDescription': variation_desc}
        query.insert_record(cursor, 'Asset_Variations', data)

    # creating Asset_Parts
    if parent_name:
        parent_id = query.get_asset_id(cursor, parent_name)
        data = {'ParentAssetID': parent_id,
                'PartAssetID': asset_id}
        query.insert_record(cursor, 'Asset_Parts', data)

    # creating asset_users
    for user in creators:
        user_id = query.get_user_id(cursor, user)
        if not user_id:
            click.echo(f'error, user {user} not found in database')
            raise ValueError
        data = {'AssetID': asset_id,
                'UserID': user_id}
        query.insert_record(cursor, 'Asset_Users', data)

    click.echo('created database records')
    shutil.copytree(target_path, dest_path, dirs_exist_ok=False)
    click.echo(f'created asset at dir: {dest_path}')


