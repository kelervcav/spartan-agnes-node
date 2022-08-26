from fastapi.testclient import TestClient

from main import api

client = TestClient(api)

def test_can_fetch_home_page():
    response = client.get("/")
    assert response.status_code == 200
