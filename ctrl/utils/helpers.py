import click
import re
from datetime import datetime
from pathlib import Path

import ctrl.utils.constants as constants
import ctrl.config as config


def print_project(proj_path: Path, show_tree: bool = False) -> None:
    """prints info about project"""
    from directory_tree import display_tree
    click.echo(f"name: {proj_path.name}")
    tool_names = [x.name for x in get_tools(proj_path)]
    click.echo(f"tools: {', '.join(tool_names)}")
    if show_tree:
        click.echo("dir tree:")
        click.echo("")
        tree_string = display_tree(dir_path=proj_path, string_rep=True, header=True, show_hidden=True)
        click.echo(f"{tree_string}")


def proj_abs_path(name: str) -> Path:
    return Path(config.ART_ROOT_PATH, 'projects', name)


def get_tools(proj_path: Path) -> list[Path]:
    return [path for path in get_subdirs(proj_path) if path.name in constants.TOOLS]


def get_subdirs(path: Path) -> list[Path]:
    return [x for x in path.iterdir() if x.is_dir()]


def get_subfiles(path: Path) -> list[Path]:
    return [x for x in path.iterdir() if x.is_file()]


def get_outputs(proj_path: Path) -> list[Path]:
    return get_subdirs(proj_path / 'outputs')


def camel_to_sent(string: str) -> str:
    return re.sub('([A-Z])', r' \1', string)


def find_similarity(sentence: str, list_of_sentences: list[str]) -> list[tuple[str, float]]:
    import spacy
    # uses nlp returns list of comparisons
    nlp = spacy.load("en_core_web_lg")
    sentence = camel_to_sent(sentence).lower()
    sentence = re.sub('[0-9]', '', sentence)
    similarities = []
    for comparator in list_of_sentences:
        comparator_clean = camel_to_sent(comparator).lower()
        comparator_clean = re.sub('[0-9]', '', comparator_clean)
        similarity = nlp(sentence).similarity(nlp(comparator_clean))
        similarities.append((comparator, similarity))
    return sorted(similarities, key=lambda x: x[1], reverse=True)


def extract_filename(name: str) -> tuple[str, str, str, datetime, str]:
    """Extracts Information From Filename

    :param name: A string the contains the name of the file in form projectName_fileName_type_YYMMDD_HHMM.ext

    :return: projectName, fileName, fileType, time, extension"""
    file_info, extension = name.split('.')
    project_name, file_name, file_type, yymmdd, hhmm = file_info.split('_')
    time = datetime(int('20' + yymmdd[0:2]), int(yymmdd[2:4]), int(yymmdd[4:6]), int(hhmm[0:2]), int(hhmm[2:4]))
    return project_name, file_name, file_type, time, extension


def construct_filename(project_name: str, file_name: str, file_type: str, time: datetime, extension: str) -> str:
    """Constructs filename"""
    string_time = time.strftime("%y%m%d_%H%M")
    return f"{project_name}_{file_name}_{file_type}_{string_time}.{extension}"


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
