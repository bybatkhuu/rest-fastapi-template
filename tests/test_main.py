from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_ping() -> None:
    _response = client.get("/api/v1/ping")
    assert _response.status_code == 200
    return


def test_health() -> None:
    _response = client.get("/api/v1/health")
    assert _response.status_code == 200
    return
