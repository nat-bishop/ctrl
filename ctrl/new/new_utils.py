import shutil
from pathlib import Path
from typing import Optional

import click

import ctrl.database.query as query
import ctrl.utils.helpers as helpers
import ctrl.utils.constants as constants


def create_tags(cursor, tags: list[str]) -> list[int]:
    """returns tagids, creates if they do not exist"""
    import spacy
    nlp = spacy.load("en_core_web_lg")

    res = query.get_all_records(cursor, ['Name'], 'Tags')
    tag_list = [item[0] for item in res]
    tag_IDs = []

    for tag in tags:
        if tag in tag_list:
            # tag already exists
            tag_IDs.append(query.get_tag_id(cursor, tag))
            continue
        click.clear()
        # tag is new
        similarities = _find_similar_tags(nlp, tag, tag_list)
        data = {'Name': tag}
        if not _has_vector(nlp, tag):
            if click.confirm(f'tag: {tag} does not exist, and has no word vector, create anyway?'):
                tag_IDs.append(query.insert_record(cursor, 'Tags', data, 'TagID'))
        else:
            click.echo(f"tag: {tag} does not exist, similar tags:")
            top_sims = similarities[:25]
            for count, (similar_tag, similar_val) in enumerate(top_sims):
                click.echo(f"{count}. {similar_tag} {int(100 * similar_val)}")

            click.echo("")
            if click.confirm(f"proceed with {tag}?"):
                tag_IDs.append(query.insert_record(cursor, 'Tags', data, 'TagID'))
            elif click.confirm(f"use similar tag instead?"):
                index = click.prompt(f"tag number", type=click.IntRange(0, len(top_sims) - 1), show_choices=True)
                tag_name, _ = top_sims[index]
                tag_id = query.get_tag_id(cursor, tag_name)
                tag_IDs.append(tag_id)

    return tag_IDs


def new_tool_dirs(proj_path: Path, tool: str) -> None:
    if not proj_path.exists():
        click.echo(f"error, proj path: {proj_path} does not exist")
        exit(1)
    if tool not in constants.TOOLS:
        click.echo(f"error, tool {tool} not in constants.TOOLS")
        exit(1)

    (proj_path / tool).mkdir()
    (proj_path / tool / 'projectFiles').mkdir()
    (proj_path / tool / 'exports').mkdir()

    # add workspace
    if tool == 'maya':
        # add workspace
        workspace_path = proj_path / 'workspace.mel'
        template_path = Path(__file__).parents[2] / 'templates' / 'workspace.mel'
        shutil.copy(template_path, workspace_path)
        click.echo(f"creating maya workspace at: {workspace_path}")


def _has_vector(nlp, word: str):
    return nlp(word).has_vector


def _find_similar_tags(nlp, tag: str, tag_list: list[str]) -> Optional[list[tuple[str, float]]]:

    standardized_tag = helpers.standardize_word(tag)
    token1 = nlp(standardized_tag)

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

