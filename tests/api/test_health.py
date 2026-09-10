from fastapi.testclient import TestClient


def test_health_returns_healthy_status(
    api_client: TestClient
) -> None:
    response = api_client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"] == (
        "application/json"
    )
    assert response.json() == {
        "status": "healthy"
    }


def test_openapi_documents_health_endpoint(
    api_client: TestClient
) -> None:
    response = api_client.get("/openapi.json")

    assert response.status_code == 200

    paths = response.json()["paths"]

    assert "/health" in paths
    assert "get" in paths["/health"]