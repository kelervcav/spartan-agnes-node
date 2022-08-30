from fastapi.testclient import TestClient

from main import api

client = TestClient(api)

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

def test_can_fetch_devices():
    response = client.get("/api/devices")
    assert response.status_code == 200
    
def test_can_fetch_device():
    response = client.get("/api/devices/1")
    assert response.status_code == 200

def test_can_update_device():
    response = client.put(
        "/api/devices/1",
        # headers={"X-Token": "coneofsilence"},
        json={"name": "testing", "unit": 100, "address": 25},
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "name": "testing",
            "unit": 100,
            "address": 25
        },
        "status": 200      
    }

def test_can_delete_device():
    response = client.delete("/api/devices/1")
    assert response.status_code == 200

