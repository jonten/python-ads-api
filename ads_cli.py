#!/usr/bin/env python -W ignore::DeprecationWarning

import asyncio
import asyncclick as click
from beautifultable import BeautifulTable
from app import main
from app import db


@click.group()
async def cli():
    await asyncio.sleep(0.1)

def create_table(ads: list):
    table = BeautifulTable()
    for row in ads:
        table.rows.append(row)

    table.columns.header = ["ID", "Subject", "Body", "Price"]
    return table

@cli.command()
@click.argument("ad_id", type=int)
async def list_ad(ad_id):
    """
    List an ad with a specific AD_ID.
    """
    results = await db.db_get_ad(ad_id)
    table_results = create_table(results)
    click.echo(table_results)

@cli.command()
async def list_all():
    """
    List all ads in the database.
    """
    results = await db.db_get_ads()
    table_results = create_table(results)
    click.echo(table_results)


@cli.command()
@click.argument("new_ad", nargs=(3))
async def create_ad(new_ad):
    """
    Create a new ad with a SUBJECT, BODY, EMAIL and PRICE.
    """
    answer = "{\"subject\": \"new_ad[0]\", \"body\": \"new_ad[1]\", \"email\": \"new_ad[2]\", \"price\": \"new_ad[3]\"}" 
    results = await db.db_create_ad(answer)
    click.echo(f"Creating ad {answer}")


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

