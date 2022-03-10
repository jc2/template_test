import pytest

from clients.github import fetch_repo_info, is_popular


def test_github_fetch_ok():
    response = fetch_repo_info("django", "django")
    assert isinstance(response, dict)
    assert isinstance(response.get("stargazers_count"), int)
    assert isinstance(response.get("forks_count"), int)


@pytest.mark.parametrize(
    "username,repo,expected_popular",
    [
        ("django", "django", True),
        ("jc2", "cluster_client", False),
    ]
)
def test_github_popular_ok(username, repo, expected_popular):
    response = is_popular(username, repo)
    assert response == expected_popular
