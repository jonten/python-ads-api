#!/usr/bin/env python -W ignore::DeprecationWarning

import asyncio
import asyncclick as click
from beautifultable import BeautifulTable
from app import main
from app import db
import json
import os
import sys

@click.group()
async def cli():
    await asyncio.sleep(0.1)

def create_table(ads: list):
    """
    Create nice cli table output
    """
    table = BeautifulTable()
    for row in ads:
        table.rows.append(row)

    table.columns.header = ["ID", "Subject", "Body", "Price"]
    return table

@cli.command()
@click.argument("ad_id", type=int)
async def list_ad(ad_id):
    """
    List an ad with a specific AD_ID
    """
    results = await db.db_get_ad(ad_id)
    table_results = create_table(results)
    click.echo(table_results)

@cli.command()
async def list_all():
    """
    List all ads in the database
    """
    results = await db.db_get_ads()
    table_results = create_table(results)
    click.echo(table_results)

@cli.command()
@click.option("--subject", "-s", required=True, prompt=True, type=str)
@click.option("--body", "-b", required=True, prompt=True, type=str)
@click.option("--email", "-e", required=True, prompt=True, type=str)
@click.option("--price", "-p", required=False, type=float, default=None)
async def create_ad(subject, body, email, price):
    """
    Create a new ad with a SUBJECT, BODY, EMAIL and PRICE
    """
    new_ad = main.Ad( 
        subject = subject,
        body = body,
        email = email,
        price = price
    )
    await db.db_create_ad(new_ad)
    click.echo(f"Creating ad: {new_ad}")


@cli.command()
@click.option("--file", "-f", "file_", required=True, type=str)
async def create_ads(file_):
    """
    Create a bunch of new ads from a file
    """
    os.chdir(os.path.abspath(os.curdir))
    ads_dict = json.load(open(file_))
    for ad in ads_dict[0:]:
        new_ad = main.Ad(
            subject = ad["subject"],
            body = ad["body"],
            email = ad["email"],
            price = ad["price"]
        )
        await db.db_create_ad(new_ad)
        click.echo(f"Creating ad: {new_ad}")
    click.echo(f"Done creating ads from: {file_}")

@cli.command()
@click.argument("ad_id", type=int)
async def delete_ad(ad_id):
    """
    Delete an ad with a specific AD_ID
    """
    results = await db.db_delete_ad(ad_id)
    click.echo(results)

@cli.command()
async def delete_all():
    """
    Delete all ads from the database 
    """
    results = await db.db_delete_all_ads()
    click.echo(results)


if __name__ == "__main__":
    cli()

