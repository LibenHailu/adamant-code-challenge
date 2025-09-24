from fastapi.testclient import TestClient


def test_root_flow(client: TestClient):

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Adamant Challenge API!",
        "version": "0.0.1",
        "documentation": "/docs",
    }
