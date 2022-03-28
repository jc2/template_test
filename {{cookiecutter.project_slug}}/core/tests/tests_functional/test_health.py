from unittest.mock import patch


from fastapi.testclient import TestClient
from httpx import HTTPError

from app import app

client = TestClient(app)


@patch('routers.health.github_test')
def test_app_health_ok(mock_test_connection):
    mock_test_connection.return_value = True

    response = client.get("/health/healthy")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get("status") == "ok"


@patch('routers.health.github_test')
def test_app_health_bad(mock_test_connection):
    def test_connection(*args, **kwargs):
        raise HTTPError()

    mock_test_connection.side_effect = test_connection

    response = client.get("/health/healthy")

    assert response.status_code == 500
    assert isinstance(response.json(), dict)
    assert response.json().get("detail")
