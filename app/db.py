import asyncpg

class DbZeroRowsProcessed(Exception):
    """Create Exception class for handling zero processed rows in DB"""

async def db_create_ad(new_ad):
    """Function for creating new ads in the database"""
    conn = await asyncpg.connect(user="adsuser", database="adsdb")
    query = "INSERT INTO ads (subject, body, email, price) VALUES ($1, $2, $3, $4)"
    await conn.execute(query, new_ad.subject, new_ad.body, new_ad.email, new_ad.price)

async def db_delete_ad(ad_id:int = None):
    """Function for deleting one ad from the database"""

    conn = await asyncpg.connect(user="adsuser", database="adsdb")
    query = "DELETE FROM ads WHERE id=$1"
    results = await conn.execute(query, ad_id)
    if results.endswith("0"):
        raise DbZeroRowsProcessed()
    return results

async def db_get_ad(ad_id:int = None):
    """Function for getting one ad from the database"""
    conn = await asyncpg.connect(user="adsuser", database="adsdb")
    query = "SELECT id, subject, body, price FROM ads WHERE id=$1"
    results = await conn.fetch(query, ad_id)
    if len(results) == 0:
        raise DbZeroRowsProcessed()
    return results

async def db_get_ads(sort_by_price = False,
    sort_by_created = False):
    """Function for getting all ads from the database"""
    conn = await asyncpg.connect(user="adsuser", database="adsdb")
    if sort_by_price:
        query = "SELECT id, subject, body, price FROM ads ORDER BY price DESC"
    elif sort_by_created:
        query = "SELECT id, subject, body, price FROM ads ORDER BY created DESC"
    else:
        query = "SELECT id, subject, body, price FROM ads"
    results = await conn.fetch(query)
    return results

async def create_db():
    """Startup function for setting up the database/connection"""
    try:
        conn = await asyncpg.connect('postgresql://localhost/adsdb')
    except asyncpg.InvalidCatalogNameError:
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            database='template1',
        )
        await sys_conn.execute(
            'CREATE USER "adsuser"'
        )

        await sys_conn.execute(
            'CREATE DATABASE "adsdb" OWNER "adsuser"'
        )
        await sys_conn.close()

        # Connect to the newly created database.
        conn = await asyncpg.connect(user="adsuser", database="adsdb")

        # Create table if not exist
        await conn.execute('''
        CREATE TABLE IF NOT EXISTS ads(
            ad_id serial PRIMARY KEY,
            subject text,
            body text,
            price numeric,
            email text,
            created timestamp DEFAULT NOW()
        )
    ''')
    return conn


def close_connection():
    """Shutdown function for closing the database connection"""
    conn = None
    conn.close()
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")
