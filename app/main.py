# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=f-string-without-interpolation

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import asyncpg

class Ad(BaseModel):
    """Create Ad class with a required subject, body, email and a optional price"""
    subject: str
    body: str
    email: EmailStr
    price: Optional[float] = None

app = FastAPI()

@app.get("/", status_code=200)
async def root():
    """Default route with info message"""
    return {"message": "Default API endpoint is /ads and documentation endpoint is /docs"}

@app.post("/ads/", status_code=201)
async def create_ad(new_ad: Ad):
    """Route function for creating new ads"""
    await db_create_ad(new_ad)
    return new_ad

async def db_create_ad(new_ad):
    """Function for creating new ads in the database"""
    conn = await asyncpg.connect(user="adsuser", database="adsdb")
    query = "INSERT INTO ads (subject, body, email, price) VALUES ($1, $2, $3, $4)"
    await conn.execute(query, new_ad.subject, new_ad.body, new_ad.email, new_ad.price)

@app.get("/ads/", status_code=200)
async def get_ads(sort_by_price:Optional[bool] = False,
    sort_by_created:Optional[bool] = False):
    """Route function for listing all ads"""
    if sort_by_price:
        list_ads = await db_get_ads(sort_by_price)
    elif sort_by_created:
        list_ads = await db_get_ads(sort_by_created)
    else:
        list_ads = await db_get_ads()
    return list_ads

async def db_get_ads(sort_by_price:Optional[bool] = False,
    sort_by_created:Optional[bool] = False):
    """Function for getting all ads from the database"""
    conn = await asyncpg.connect(user="adsuser", database="adsdb")
    if sort_by_price:
        query = "SELECT subject, body, price FROM ads ORDER BY price DESC"
    elif sort_by_created:
        query = "SELECT subject, body, price FROM ads ORDER BY created DESC"
    else:
        query = "SELECT subject, body, price FROM ads"
    results = await conn.fetch(query)
    return results


@app.on_event("startup")
async def startup_event():
    """Startup function for setting up the database/connection"""
    try:
        conn = await asyncpg.connect('postgresql://localhost/adsdb')
    except asyncpg.InvalidCatalogNameError:
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            database='template1',
        )
        await sys_conn.execute(
            f'CREATE USER "adsuser"'
        )

        await sys_conn.execute(
            f'CREATE DATABASE "adsdb" OWNER "adsuser"'
        )
        await sys_conn.close()

        # Connect to the newly created database.
        conn = await asyncpg.connect(user="adsuser", database="adsdb")

        # Create table if not exist
        await conn.execute('''
        CREATE TABLE IF NOT EXISTS ads(
            id serial PRIMARY KEY,
            subject text,
            body text,
            price numeric,
            email text,
            created timestamp DEFAULT NOW()
        )
    ''')
    return conn


@app.on_event("shutdown")
def shutdown_event():
    """Shutdown function for closing the database connection"""
    conn = None
    conn.close()
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")
