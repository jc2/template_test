from unittest.mock import patch


from fastapi.testclient import TestClient

from app import app
from clients.github import GitHubClientError

client = TestClient(app)


@patch('routers.core.is_popular')
def test_app_score_ok_1(mock_is_popular):
    mock_is_popular.return_value = True

    response = client.get("/api/v1/score/test/test")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get("is_popular")


@patch('routers.core.is_popular')
def test_app_score_ok_2(mock_is_popular):
    mock_is_popular.return_value = False

    response = client.get("/api/v1/score/test/test")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert not response.json().get("is_popular")


@patch('routers.core.is_popular')
def test_app_score_bad(mock_is_popular):
    def is_popular(*args, **kwargs):
        raise GitHubClientError(1, "test")

    mock_is_popular.side_effect = is_popular

    response = client.get("/api/v1/score/test/test")

    assert response.status_code == 400
    assert isinstance(response.json(), dict)
    assert response.json().get("detail")