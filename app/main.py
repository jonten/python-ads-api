# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=invalid-name
"""Pylint checking are disabled for the things above"""

from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from app import db

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
    await db.db_create_ad(new_ad)
    return new_ad

@app.delete("/ads/{ad_id}", status_code=200)
async def delete_ad(ad_id:int = None):
    """Route function for deleting one ad"""
    try:
        deleted_ad = await db.db_delete_ad(ad_id=ad_id)
    except db.DbZeroRowsProcessed as e:
        raise HTTPException(status_code=404, detail="Item not found") from e
    return deleted_ad

@app.get("/ads/{ad_id}", status_code=200)
async def get_ad(ad_id:int = None):
    """Route function for listing one ad"""
    try:
        list_ad = await db.db_get_ad(ad_id=ad_id)
    except db.DbZeroRowsProcessed as e:
        raise HTTPException(status_code=404, detail="Item not found") from e
    return list_ad

@app.get("/ads/", status_code=200)
async def get_ads(sort_by_price:Optional[bool] = False,
    sort_by_created:Optional[bool] = False):
    """Route function for listing all ads"""
    if sort_by_price:
        list_ads = await db.db_get_ads(sort_by_price=sort_by_price)
    elif sort_by_created:
        list_ads = await db.db_get_ads(sort_by_created=sort_by_created)
    else:
        list_ads = await db.db_get_ads()
    return list_ads


@app.on_event("startup")
async def startup_event():
    """Startup event for setting up the database/connection"""
    await db.create_db()

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event for closing the database connection"""
    await db.close_connection()

if __name__ == "__main__":
    app()

