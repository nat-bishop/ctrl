import shutil
import ctrl.config as config
from pathlib import Path
import click


def sync(sync_direction: str, delete: bool) -> None:
    if sync_direction == 'remote_to_source':
        click.echo(click.style('SYNCING TOWARDS SOURCE FROM REMOTE', fg='red'))
        project_source_path = Path(config.REMOTE_ART_ROOT_PATH)
        project_target_path = Path(config.ART_ROOT_PATH)
        asset_source_path = Path(config.REMOTE_ASSET_ROOT_PATH)
        asset_target_path = Path(config.ASSET_ROOT_PATH)
    elif sync_direction == 'source_to_remote':
        click.echo(click.style('SYNCING TOWARDS REMOTE FROM SOURCE', fg='red'))
        project_source_path = Path(config.ART_ROOT_PATH)
        project_target_path = Path(config.REMOTE_ART_ROOT_PATH)
        asset_source_path = Path(config.ASSET_ROOT_PATH)
        asset_target_path = Path(config.REMOTE_ASSET_ROOT_PATH)
    else:
        raise ValueError('wrong sync direction arg')

    click.echo('project sync dry run:')
    sync_directories(project_source_path, project_target_path, delete, dry_run=True)
    click.confirm('proceed with project sync?', abort=True)
    click.echo(f'syncing {project_source_path} to {project_target_path}')
    sync_directories(project_source_path, project_target_path, delete, dry_run=False)

    click.echo('asset sync dry run:')
    sync_directories(asset_source_path, asset_target_path, delete, dry_run=True)
    click.confirm('proceed with asset sync?', abort=True)
    click.echo(f'syncing {asset_source_path} to {asset_target_path}')
    sync_directories(asset_source_path, asset_target_path, delete, dry_run=False)


def list_files(directory: Path) -> list[Path]:
    """List all files in a directory recursively."""
    return [file for file in Path(directory).rglob('*') if file.is_file()]


def file_last_modified_time(file_path: Path) -> float:
    """Return the last modified time of a file."""
    return file_path.stat().st_mtime


def sync_directories(source_dir: Path, target_dir: Path, delete: bool, dry_run: bool = True, size_diff_threshold: float = 0.5) -> None:
    if not source_dir.exists():
        raise ValueError(f"error: source_dir: {source_dir}, does not exist")
    if not target_dir.exists():
        raise ValueError(f"error: source_dir: {target_dir}, does not exist")

    source_files = list_files(source_dir)

    # Mapping of source file paths to their last modified times
    source_files_last_modified = {file: file_last_modified_time(file) for file in source_files}

    for source_file in source_files:
        relative_path = source_file.relative_to(source_dir)
        target_file = target_dir / relative_path

        # if target is too small, print warning
        if target_file.exists() and dry_run:
            target_size = target_file.stat().st_size
            source_size = source_file.stat().st_size
            if target_size < source_size * size_diff_threshold:
                click.echo(click.style("WARNING", fg='red') +
                           f"target file: {target_file} size: {target_size}, source file: {source_file} size: {source_size}")

        # Check if file needs to be updated
        if not target_file.exists() or source_files_last_modified[source_file] > file_last_modified_time(target_file) + 2:
            if dry_run:
                click.echo(f"will copy: {source_file}")
            else:
                click.echo(f"copying: {source_file}")
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, target_file)

    dest_files = list_files(target_dir)

    #if not deleting files, end here
    if not delete:
        return

    for file in dest_files:
        relative_path = file.relative_to(target_dir)
        source_file = source_dir / relative_path

        if not source_file.exists():
            if dry_run:
                click.echo(click.style("WARNING", fg='red') +
                           f"file: {file} is in remote but not in source, so will be deleted")
            else:
                click.echo(f'deleting {file}')
                file.unlink()
