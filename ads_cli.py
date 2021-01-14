#!/usr/bin/env python -W ignore::DeprecationWarning

import anyio
import asyncio
import asyncclick as click
from beautifultable import BeautifulTable
from app import main
from app import db
#from app.main import Ad
#from functools import update_wrapper

#def coroutine(f):
#    f = asyncio.coroutine(f)
#    def wrapper(*args, **kwargs):
#        loop = asyncio.get_event_loop()
#        return loop.run_until_complete(f(*args, **kwargs))
#    return update_wrapper(wrapper, f)


@click.group()
async def cli():
    await anyio.sleep(0.1)
    click.echo(f"Admin CLI application")

def create_table(ads: list):
    table = BeautifulTable()
    for row in ads:
        table.rows.append(row)

    #table.columns.header = ["Subject", "Body", "Email", "Price"]
    return table

@cli.command()
@click.option("--list", "-l", type=int, help="Lists an ad with a specific ID")
async def list_ad(ad_id):
    """
    List an ad with a specific AD_ID.
    """
    results = await db.db_get_ad(ad_id)
    click.echo(f"List ad with ID: {ad_id}")
    click.echo(results)

@cli.command()
@click.option("--list-all", "-a", help="Lists all ads")
async def list_all_ads(list_all):
    """
    List all ads in the database.
    """
    results = await db.db_get_ads()
    table_results = create_table(results)
    click.echo(f"List of all ads")
    click.echo(table_results)


@click.command()
async def create(new_ad):
    """
    Create a new ad with a SUBJECT, BODY, EMAIL and an optional PRICE.
    """
    result = await db.db_create_ad(new_ad)
    click.echo(f"Creating ad: {new_ad.SUBJECT}, {new_ad.BODY}, {new_ad.EMAIL}, {new_ad.PRICE}")


# @app.command()
# def delete(
#     username: str,
#     force: bool = typer.Option(
#         ...,
#         prompt="Are you sure you want to delete the user?",
#         help="Force deletion without confirmation.",
#     ),
# ):
#     """
#     Delete a user with USERNAME.

#     If --force is not used, will ask for confirmation.
#     """
#     if force:
#         typer.echo(f"Deleting user: {username}")
#     else:
#         typer.echo("Operation cancelled")


# @app.command()
# def delete_all(
#     force: bool = typer.Option(
#         ...,
#         prompt="Are you sure you want to delete ALL users?",
#         help="Force deletion without confirmation.",
#     )
# ):
#     """
#     Delete ALL users in the database.

#     If --force is not used, will ask for confirmation.
#     """
#     if force:
#         typer.echo("Deleting all users")
#     else:
#         typer.echo("Operation cancelled")


# @app.command()
# def init():
#     """
#     Initialize the users database.
#     """
#     typer.echo("Initializing user database")


if __name__ == "__main__":
    cli()

