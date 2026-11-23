from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert body["service"] == "aws-container-platform"


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["health"] == "healthy"


def test_simulate_load():
    res = client.post("/simulate-load", json={"iterations": 5000, "tag": "unit-test"})
    assert res.status_code == 200
    body = res.json()
    assert body["tag"] == "unit-test"
    assert body["iterations"] == 5000
    assert body["elapsed_ms"] >= 0
