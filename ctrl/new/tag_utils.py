from typing import Optional

import click

from ctrl.database import query as query
from ctrl.utils import helpers as helpers


def create_tags(cursor, tags: list[str]) -> list[int]:
    """returns tagids, creates if they do not exist"""
    import spacy
    nlp = spacy.load("en_core_web_lg")

    tag_list = query.get_all_records(cursor, 'Tags')
    tag_IDs = []

    for tag in tags:
        id = _tag_exists(tag, tag_list)
        if id:
            # tag already exists
            tag_IDs.append(id)
            continue

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
                tag_id = query.get_record(cursor, 'TagID', 'Tags', 'Name', tag_name)
                tag_IDs.append(tag_id)

    return tag_IDs


def _tag_exists(tag: str, tag_list: list[tuple[int, str]]) -> Optional[int]:
    for id, name in tag_list:
        if name == tag:
            return id
    return None


def _has_vector(nlp, word: str):
    return nlp(word).has_vector


def _find_similar_tags(nlp, tag: str, tag_list: list[tuple[int, str]]) -> Optional[list[tuple[str, float]]]:

    standardized_tag = helpers.standardize_word(tag)
    token1 = nlp(standardized_tag)

    similarities = []
    for _, t in tag_list:
        standardized_t = helpers.standardize_word(t)
        token2 = nlp(standardized_t)

        if token2.has_vector:
            similarity = token1.similarity(token2)
            similarities.append((standardized_t, similarity))

    # Sort the list by similarity score in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities
