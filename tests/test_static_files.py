from fastapi.testclient import TestClient
from ..src.main import app

client = TestClient(app)


def test_index_file():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_logo_file():
    response = client.get("/logo.png")

    assert response.status_code == 200
    assert "image/png" in response.headers["content-type"]

def test_file_not_found():
    response = client.get("/unknown")

    assert response.status_code == 404
