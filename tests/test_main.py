from fastapi.testclient import TestClient

from app.main import app, Ad, db_create_ad, db_delete_ad

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Default API endpoint is /ads and documentation endpoint is /docs"}


def test_create_ad():
    response = client.post(
        "/ads/",
        json={"subject": "Snöskoter", "body": "Fin Lynx snöskoter säljes till högstbjudande", "email": "test.testsson@yahoo.com", "price": 5600.50},
    )
    assert response.status_code == 201
    assert response.json() == {
        "subject": "Snöskoter",
        "body": "Fin Lynx snöskoter säljes till högstbjudande",
        "email": "test.testsson@yahoo.com",
        "price": 5600.50,
    }

async def test_db_create_ad():
    ad = Ad(subject="Snöskoter", body="Fin Lynx snöskoter säljes till högstbjudande", email="test.testsson@yahoo.com", price="5600.50")
    await db_create_ad(ad)

def test_delete_ad():
    response = client.delete(
        "/ads",
        json={"ad_id": 3},
    )
    assert response.status_code == 200

async def test_db_delete_ad():
    ad_id = 3
    await db_delete_ad(ad_id)
