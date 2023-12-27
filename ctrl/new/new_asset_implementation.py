import shutil
from pathlib import Path
from typing import Optional
from datetime import date
import click
import ctrl.database.query as query
import ctrl.utils.helpers as helpers
import ctrl.config as config


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
              creators: Optional[list[str, ...]] ,
              date_created: date,
              parent_name: str,
              original_name: str) -> None:

    if not creators:
        click.echo(click.style('WARNING', fg='red') + ': no creator selected for new asset.')

    if not thumbnail_path:
        click.echo(click.style('WARNING', fg='red') + ': no thumbnail_path selected for new asset.')

    updated_tags = _create_tags(cursor, tags)

    click.confirm('proceed with asset creation?', abort=True)

    # creating asset record
    dest_path = Path(config.ASSET_ROOT_PATH, name)
    data = {'AssetPath': name,
            'ThumbnailPath': thumbnail_path,
            'ViewingPath': viewing_path,
            'Type': type,
            'Title': name,
            'Description': description,
            'Mediator': mediator,
            'DateCreated': date_created,
            'Rights': rights}
    asset_id = query.insert_record(cursor, 'Assets', data, 'AssetID')

    # creating asset_tags records
    data = {'AssetID': asset_id}
    for tag_id in updated_tags:
        data['TagID'] = tag_id
        query.insert_record(cursor, 'Asset_Tags', data)

    # creating asset_variations record
    if original_name:
        variation_desc = click.prompt(f"variation description for {name} that is a variation of {original_name}")
        original_id = query.get_record(cursor, 'AssetID', 'Assets', 'Title', original_name)
        data = {'OriginalAssetID': original_id,
                'VariationAssetID': asset_id,
                'VariationDescription': variation_desc}
        query.insert_record(cursor, 'Asset_Variations', data)

    # creating Asset_Parts
    if parent_name:
        parent_id = query.get_record(cursor, 'AssetID', 'Assets', 'Title', parent_name)
        data = {'ParentAssetID': parent_id,
                'PartAssetID': asset_id}
        query.insert_record(cursor, 'Asset_Parts', data)

    # creating asset_users
    for user in creators:
        user_id = query.get_record(cursor, 'UserID', 'Users', 'Name', user)
        if not user_id:
            click.echo(f'error, user {user} not found in database')
            raise ValueError
        data = {'AssetID': asset_id,
                'UserID': user_id}
        query.insert_record(cursor, 'Asset_Users', data)

    click.echo('created database records')
    shutil.copytree(target_path, dest_path, dirs_exist_ok=False)
    click.echo(f'created asset at dir: {dest_path}')


def _create_tags(cursor, tags: Optional[list[str, ...]]) -> list[int]:
    """returns tagids, creates if they do not exist"""
    if not tags:
        click.echo(click.style('WARNING', fg='red') + ': no tags selected for new asset.')

    tag_list = query.get_all_records(cursor, 'Tags')
    tag_IDs = []

    for tag in tags:
        id = _tag_exists(tag, tag_list)
        if id:
            # tag already exists
            tag_IDs.append(id)
            continue

        # tag is new
        similarities = _find_similar_tags(tag, tag_list)
        data = {'Name': tag}
        if not similarities and click.confirm(f'tag: {tag} does not exist, and has no word vector, create anyway?'):
            tag_IDs.append(query.insert_record(cursor, 'Tags', data, 'TagID'))
        else:
            click.echo(f"tag: {tag} does not exist, similar tags:")
            top_sims = similarities[:10]
            for count, (similar_tag, similar_val) in enumerate(top_sims):
                click.echo(f"{count}. {similar_tag} {int(100 * similar_val)}")

            click.echo("")
            if click.confirm(f"proceed with {tag}?"):
                tag_IDs.append(query.insert_record(cursor, 'Tags', data, 'TagID'))
            elif click.confirm(f"use similar tag instead?"):
                index = click.prompt(f"tag number", type=click.IntRange(0, len(top_sims) - 1), show_choices=True)
                tag_name, _ = top_sims[index]
                tag_id = query.get_record(cursor, 'TagID', 'Tags', 'Name', tag_name)
                tag_IDs.append(tag_id)

    return tag_IDs


def _tag_exists(tag: str, tag_list: list[tuple[int, str]]) -> Optional[int]:
    for id, name in tag_list:
        if name == tag:
            return id
    return None


def _find_similar_tags(tag: str, tag_list: list[str]) -> Optional[list[tuple[str, float]]]:
    import spacy
    nlp = spacy.load("en_core_web_lg")

    standardized_tag = helpers.standardize_word(tag)
    token1 = nlp(standardized_tag)
    if not token1.has_vector:
        # tag does not have word vector
        return None

    similarities = []

    for t in tag_list:
        standardized_t = helpers.standardize_word(t)
        token2 = nlp(standardized_t)

        if token2.has_vector:
            similarity = token1.similarity(token2)
            similarities.append((standardized_t, similarity))

    # Sort the list by similarity score in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities
