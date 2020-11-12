from fastapi import FastAPI
import asyncpg


app = FastAPI()

conn = None
row = None
ads = None

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
            created timestamp
        )
    ''')
    return conn


@app.on_event("shutdown")
def shutdown_event():
    conn.close()
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")


@app.get("/")
async def root():
    return {"message": "Hello World"}