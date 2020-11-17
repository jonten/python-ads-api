from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import asyncpg


conn = None
row = None

class Ad(BaseModel):
    subject: str
    body: str
    email: EmailStr
    price: Optional[float] = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Default API endpoint is /ads and documentation endpoint is /docs"}

@app.post("/ads/", status_code=201)
async def create_ad(ad: Ad):
    await db_create_ad(ad)
    return ad


async def db_create_ad(ad):
    conn = await asyncpg.connect(user="adsuser", database="adsdb")
    query = "INSERT INTO ads  (subject, body, email, price) VALUES ($1, $2, $3, $4)"
    await conn.execute(query, ad.subject, ad.body, ad.email, ad.price)


@app.on_event("startup")
async def startup_event():
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
    conn.close()
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")
