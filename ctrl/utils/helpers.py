import click
import re
import string
from datetime import datetime
from pathlib import Path

import ctrl.utils.constants as constants
import ctrl.database.utils as utils
import ctrl.database.query as query


def print_asset(name: str) -> None:
    utils.perform_db_op(_print_asset_db, name)


def _print_asset_db(cursor, name):
    asset_id = query.get_asset_id(cursor, name)
    if not asset_id:
        click.echo(f'error, asset: {name} not found')

    res = query.get_all_records(cursor,
                                ['ThumbnailPath', 'ViewingPath', 'Type', 'Description', 'Mediator', 'DateCreated', 'Rights'],
                                'Assets',
                                'AssetID',
                                asset_id)

    thumbnail_path, view_path, asset_type, desc, creation_software, date_created, rights = res[0]
    user_ids = query.get_all_records(cursor, ['UserID'], 'Asset_Users', 'AssetID', asset_id)
    users = [query.get_record(cursor, 'Name', 'Users', 'UserID', item[0]) for item in user_ids]
    users_str = ", ".join(users)

    tag_ids = query.get_all_records(cursor, ['TagID'], 'Asset_Tags', 'AssetID', asset_id)
    tags = [query.get_record(cursor, 'Name', 'Tags', 'TagID', item[0]) for item in tag_ids]
    tags_str = ", ".join(tags)

    project_ids = query.get_all_records(cursor, ['ProjectID'], 'Asset_Projects', 'AssetID', asset_id)
    projects = [query.get_record(cursor, 'Title', 'Project', 'ProjectID', item[0]) for item in project_ids]
    projects_str = ", ".join(projects)

    child_asset_ids = query.get_all_records(cursor, ['PartAssetID'], 'Asset_Parts', 'ParentAssetID', asset_id)
    child_assets = [query.get_record(cursor, 'Title', 'Assets', 'AssetID', item[0]) for item in child_asset_ids]
    child_assets_str = ", ".join(child_assets)

    parent_asset_ids = query.get_all_records(cursor, ['ParentAssetID'], 'Asset_Parts', 'PartAssetID', asset_id)
    parent_assets = [query.get_record(cursor, 'Title', 'Assets', 'AssetID', item[0]) for item in parent_asset_ids]
    parent_assets_str = ", ".join(parent_assets)

    variations_ids = query.get_all_records(cursor, ['VariationAssetID'], 'Asset_Variations', 'OriginalAssetID', asset_id)
    variations = [query.get_record(cursor, 'Title', 'Assets', 'AssetID', item[0]) for item in variations_ids]
    variations_str = ", ".join(variations)

    variation_parent_id = query.get_record(cursor, 'OriginalAssetID', 'Asset_Variations', 'VariationAssetID', asset_id)

    click.echo(f"name: " + click.style(name, bold=True))
    click.echo(f"file type: {asset_type}")
    click.echo(f"creators: {users_str}")
    click.echo(f"description: {desc}")
    click.echo(f"date created: {date_created}")
    click.echo(f"tags: {tags_str}")
    click.echo(f"creation software: {creation_software}")
    click.echo(f"usage rights: {rights}")
    click.echo(f"main view path: {view_path}")
    if thumbnail_path:
        click.echo(f"thumbnail view path: {thumbnail_path}")
    if projects:
        click.echo(f"projects using assets: {projects_str}")
    if parent_assets:
        click.echo(f"parent assets: {parent_assets_str}")
    if child_assets:
        click.echo(f"child assets: {child_assets_str}")
    if variation_parent_id:
        variation_parent = query.get_record(cursor, 'Title', 'Assets', 'AssetID', variation_parent_id)
        variation_desc = query.get_record(cursor, 'VariationDescription', 'Asset_Variations', 'VariationAssetID', variation_parent_id)
        click.echo(f"original asset: {variation_parent}")
        click.echo(f"variation description: {variation_desc}")
    if variations:
        click.echo(f"other variation assets: {variations_str}")


def print_project(name: str) -> None:
    """prints info about project"""
    utils.perform_db_op(_print_project_db, name)


def _print_project_db(cursor, name: str):
    path = query.get_record(cursor, 'PayloadPath', 'Projects', 'Title', name)
    if not path:
        click.echo(f"error, project: {name}, not found")
        exit(1)
    id = query.get_project_id(cursor, name)
    date_created = query.get_record(cursor, 'DateCreated', 'Projects', 'ProjectID', id)

    click.echo(f'name: '+click.style(name, bold=True))
    click.echo(f'path: {path}')
    click.echo(f'date created: {date_created}')

    res = query.get_all_records(cursor,['UserID'], 'Project_Users', 'ProjectID', id)
    user_ids = [item[0] for item in res]
    users = []
    for user_id in user_ids:
        users.append(query.get_record(cursor, 'Name', 'Users', 'UserID', user_id))

    user_str = ', '.join(users)
    click.echo(f'creators: {user_str}')

    res = query.get_all_records(cursor, ['TagID'], 'Project_Tags', 'ProjectID', id)
    tag_ids = [item[0] for item in res]
    tags = []
    for tag_id in tag_ids:
        tags.append(query.get_record(cursor, 'Name', 'Tags', 'TagID', tag_id))

    tag_str = ', '.join(tags)
    click.echo(f'tags: {tag_str}')

    desc = query.get_record(cursor, 'Description', 'Projects', 'ProjectID', id)
    click.echo(f'description: {desc}')


def get_proj_path(name: str) -> Path | None:
    path = utils.perform_db_op(query.get_record, 'PayloadPath', 'Projects', 'Title', name)
    if path:
        return Path(path)
    else:
        return None


def get_tools(proj_path: Path) -> list[str]:
    return [path.name for path in get_subdirs(proj_path) if path.name in constants.TOOLS]


def get_subdirs(path: Path) -> list[Path]:
    return [x for x in path.iterdir() if x.is_dir()]


def get_subfiles(path: Path) -> list[Path]:
    return [x for x in path.iterdir() if x.is_file()]


def get_outputs(proj_path: Path) -> list[Path]:
    return get_subdirs(proj_path / 'outputs')


def camel_to_title(string: str) -> str:
    return re.sub('([A-Z])', r' \1', string).title()


def sent_to_camel(string: str) -> str:
    temp = string.split(" ")
    return temp[0] + ''.join(ele.title() for ele in temp[1:])


def standardize_word(word):
    # Lowercase
    word = word.lower()
    # Remove punctuation
    word = word.translate(str.maketrans('', '', string.punctuation))
    return word


def find_similarity(sentence: str, list_of_sentences: list[str]) -> list[tuple[str, float]]:
    import spacy
    # uses nlp returns list of comparisons
    nlp = spacy.load("en_core_web_lg")
    sentence = camel_to_title(sentence).lower()
    sentence = re.sub('[0-9]', '', sentence)
    similarities = []
    for comparator in list_of_sentences:
        comparator_clean = camel_to_title(comparator).lower()
        comparator_clean = re.sub('[0-9]', '', comparator_clean)
        similarity = nlp(sentence).similarity(nlp(comparator_clean))
        similarities.append((comparator, similarity))
    return sorted(similarities, key=lambda x: x[1], reverse=True)


def extract_filename(file_name: str) -> tuple[str, str, str, datetime, str]:
    """Extracts Information From Filename

    :param file_name: A string the contains the name of the file in form projectName_fileName_type_YYMMDD_HHMM.ext

    :return: projectName, fileName, fileType, time, extension"""
    file_info, extension = file_name.split('.')
    project_name, file_name, file_type, yymmdd, hhmm = file_info.split('_')
    time = datetime(int('20' + yymmdd[0:2]), int(yymmdd[2:4]), int(yymmdd[4:6]), int(hhmm[0:2]), int(hhmm[2:4]))
    return camel_to_title(project_name), file_name, file_type, time, extension


def construct_filename(project_name: str, file_name: str, file_type: str, time: datetime, extension: str) -> str:
    """Constructs filename"""
    string_time = time.strftime("%y%m%d_%H%M")
    return f"{sent_to_camel(project_name)}_{file_name}_{file_type}_{string_time}.{extension}"


def get_latest_files(path: Path) -> dict[str, Path]:
    """Gets the latest version of files in a folder

    :return: dict:
                key: filename_filetype_time
                value: path
    """
    newest_files = {}
    for file_path in get_subfiles(path):
        project_name, name, file_type, time, extension = extract_filename(file_path.name)
        name_type = f"{name}_{file_type}"
        if name_type in newest_files.keys():
            _, latest_time = newest_files[name_type]
        else:
            latest_time = datetime.min

        if time > latest_time:
            newest_files[name_type] = (file_path, time)

    newest_files_with_times = {}
    for key, (path, time) in newest_files.items():
        time_string = time.strftime("%b%d")
        newest_files_with_times[f"{key}_{time_string}"] = path
    return newest_files_with_times
