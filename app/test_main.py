from fastapi.testclient import TestClient
import random

from app.main import app

client = TestClient(app)


def test_smart_api():
    response = client.get("/api/smart/300")
    if response.status_code == 200:
        assert type(response.json()['Time']) == type(random.randint(1,300))

    if response.status_code == 429:
        assert response.json() == {"detail": "EXPO API has too many request!"}

    if response.status_code == 408:
        assert response.json() == {"detail": "Attempt limit exceeded."}

    if response.status_code == 404:
        assert response.json() == {"detail": "Item are not found."}


def test_smart_api_check_body():
    response = client.get("/api/smart/300")
    assert response.headers["Content-Type"] == "application/json"


