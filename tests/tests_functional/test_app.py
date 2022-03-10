from unittest.mock import patch


from fastapi.testclient import TestClient
from httpx import HTTPError

from app import app
from clients.github import GitHubClientError

client = TestClient(app)


@patch('app.is_popular')
def test_app_score_ok_1(mock_is_popular):
    mock_is_popular.return_value = True

    response = client.get("/api/v1/score/test/test")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get("is_popular")


@patch('app.is_popular')
def test_app_score_ok_2(mock_is_popular):
    mock_is_popular.return_value = False

    response = client.get("/api/v1/score/test/test")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert not response.json().get("is_popular")


@patch('app.is_popular')
def test_app_score_bad(mock_is_popular):
    def is_popular(*args, **kwargs):
        raise GitHubClientError(1, "test")

    mock_is_popular.side_effect = is_popular

    response = client.get("/api/v1/score/test/test")

    assert response.status_code == 400
    assert isinstance(response.json(), dict)
    assert response.json().get("detail")


@patch('app.test_connection')
def test_app_health_ok(mock_test_connection):

    response = client.get("/health")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get("status") == "ok"


@patch('app.test_connection')
def test_app_health_bad(mock_test_connection):
    def test_connection(*args, **kwargs):
        raise HTTPError()

    mock_test_connection.side_effect = test_connection

    response = client.get("/health")

    assert response.status_code == 500
    assert isinstance(response.json(), dict)
    assert response.json().get("detail")
