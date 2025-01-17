from fastapi.testclient import TestClient
from ..src.main import app

client = TestClient(app)


def test_search_query():
    response = client.get("/api/search", params={"query": "911"})

    assert response.status_code == 200
    assert len(response.json()) > 0
