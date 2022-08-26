from fastapi.testclient import TestClient

from main import api

client = TestClient(api)

def test_can_fetch_devices():
    response = client.get("/devices")
    assert response.status_code == 200
