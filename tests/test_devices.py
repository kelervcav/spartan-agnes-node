from fastapi.testclient import TestClient

from main import api

client = TestClient(api)

def test_can_fetch_devices():
    response = client.get("/api/devices")
    assert response.status_code == 200

def test_can_store_device():
    response = client.post(
        "/api/devices",
        # headers={"X-Token": "coneofsilence"},
        json={"name": "foobar", "unit": 1, "address": 2},
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "name": "foobar",
            "unit": 1,
            "address": 2
        },
        "status": 200      
    }

