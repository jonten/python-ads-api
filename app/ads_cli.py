import typer
from app import main
#from app.main import Ad

app = typer.Typer(help="Ads Admin CLI")

@app.command()
def list_ad(ad_id:int = None):
    """
    List an ad with a specific AD_ID.
    """
    db.db_get_ad(ad_id)
    typer.echo(f"List ad with ID: {ad_id}")

@app.command()
def list_all_ads():
    """
    List all ads in the database.
    """
    db.db_get_ads()
    typer.echo(f"List all ads")


@app.command()
def create(new_ad: Ad):
    """
    Create a new ad with a SUBJECT, BODY, EMAIL and an optional PRICE.
    """
    db.db_create_ad(new_ad)
    typer.echo(f"Creating ad: {new_ad.SUBJECT}, {new_ad.BODY}, {new_ad.EMAIL}, {new_ad.PRICE}")


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


#if __name__ == "__main__":
#    app()
