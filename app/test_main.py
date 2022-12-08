from fastapi.testclient import TestClient
import random

from app.main import app

client = TestClient(app)


def test_smart_api():
    response = client.get("/api/smart/300")
    if response.status_code == 200:
        assert isinstance(response.json()['Time'], int)

    if response.status_code == 429:
        assert response.json() == {"detail": "EXPO API has too many request!"}

    if response.status_code == 408:
        assert response.json() == {"detail": "Timeout has been raised."}

    if response.status_code == 404:
        assert response.json() == {"detail": "Item are not found."}
    
    if response.status_code == 500:
        assert response.json() == {"detail": "Internal Server Error"}


def test_smart_api_check_body():
    response = client.get("/api/smart/300")
    assert response.headers["Content-Type"] == "application/json"


