from typing import Optional
from datetime import date
import click
import ctrl.database.utils as utils
import ctrl.database.query as query
import ctrl.utils.helpers as helpers


def search_asset(asset_name: Optional[str],
                 creators: Optional[list[str]],
                 tags: Optional[list[str]],
                 asset_type: Optional[str],
                 rights: Optional[str],
                 software: Optional[str],
                 from_date: Optional[date],
                 to_date: Optional[date],
                 projects: Optional[list[str]],
                 gui_enabled: bool) -> None:

    assets = utils.perform_db_op(query.get_assets,
                                 asset_name,
                                 creators,
                                 tags,
                                 asset_type,
                                 rights,
                                 software,
                                 projects,
                                 from_date,
                                 to_date)

    if not assets:
        click.echo("no assets found that match search params")
    elif len(assets) == 1:
        asset_name = assets[0]
        click.echo("found asset: ")
        helpers.print_asset(asset_name)
    else:
        click.echo("projects found:")
        click.echo("")
        for asset_name in assets:
            helpers.print_asset(asset_name)
            click.echo("")
