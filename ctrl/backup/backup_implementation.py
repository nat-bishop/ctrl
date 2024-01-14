import subprocess
import shutil
from datetime import datetime
import click
import ctrl.config as config
from pathlib import Path
import ctrl.database.utils as db_utils
import zipfile


def backup() -> None:
    backup_root_path = Path(config.BACKUP_PATH)
    if not backup_root_path.exists():
        raise ValueError(f'path {backup_root_path}, does not exist')

    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    zip_dir = backup_root_path / f"backup_{timestamp}"
    click.echo(f'making backup directory: {zip_dir}')
    zip_dir.mkdir()
    pg_dump_file = zip_dir / f"database_dump_{timestamp}.sql"
    click.echo(f"dumping pg backup file to: {pg_dump_file}")
    _backup_postgres_db(config.DB_NAME, config.DB_USER, pg_dump_file)

    projects_backup_dir = zip_dir / f"projects_backup_{timestamp}"
    projects_backup_dir.mkdir()
    click.echo(f"backing up projects directory too: {projects_backup_dir}")
    _copy_with_progress(Path(config.ART_ROOT_PATH), projects_backup_dir)

    assets_backup_dir = zip_dir / f"assets_backup_{timestamp}"
    assets_backup_dir.mkdir()
    click.echo(f"backing up assets directory too: {assets_backup_dir}")
    _copy_with_progress(Path(config.ASSET_ROOT_PATH), assets_backup_dir)

    _zip_with_progress(zip_dir)


def _backup_postgres_db(db_name: str, user, output_file) -> None:
    command = f'pg_dump -U {user} {db_name} > {output_file}'
    subprocess.run(command, shell=True, check=True)


def _copy_with_progress(src: Path, dst: Path) -> None:
    files_and_dirs = src.rglob('*')
    total_size = 0
    files = []
    for item in files_and_dirs:
        if item.is_file():
            total_size += item.stat().st_size
            files.append(item)

    with click.progressbar(length=total_size, label='Copying files', show_pos=True) as bar:
        for file in files:

            dst_path = dst / file.relative_to(src)
            try:
                shutil.copy2(file, dst_path)
            except IOError as io_err:
                dst_path.parent.mkdir(parents=True)
                shutil.copy2(file, dst_path)
            bar.update(file.stat().st_size)


def _zip_with_progress(backup_dir: Path) -> None:
    zip_file = backup_dir.with_suffix('.zip')
    total_size = 0
    files = list(backup_dir.rglob('*'))
    for item in files:
        total_size += item.stat().st_size

    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf, \
         click.progressbar(length=total_size, label='Zipping backup', show_pos=True) as bar:
        for file in files:
            zipf.write(file, file.relative_to(backup_dir))
            bar.update(file.stat().st_size)

    shutil.rmtree(backup_dir)
