import os
import traceback
from json import JSONDecodeError

import httpx
from httpx import HTTPError, HTTPStatusError, TimeoutException

from extensions.log import init_log


log = init_log("github_client")

url_base = "https://api.github.com"
repo_api = url_base + "/repos/{}/{}"

token = os.getenv('GITHUB_TOKEN')
if token:
    headers = {
        "Authorization": f"Bearer {token}"
    }
else:
    headers = {}


class GitHubClientError(Exception):

    NOT_ACCESSIIBLE_REPO = 0
    CONNECTION_ERROR = 1
    PARSING_ERROR = 2

    def __init__(self, code, message):
        self.code = code
        self.message = message


def test_connection():
    httpx.get(url_base, timeout=0.5)


def fetch(
    url: str,
    method: str,
    **kwargs,
):
    try:
        response_request = httpx.request(
            method=method,
            url=url,
            **kwargs,
        )
        response_request.raise_for_status()
        data_text = response_request.text
        data_json = response_request.json()
    except TimeoutException as error:
        error_item = {
            "message": f"Client Timeout Error: {error}",
            "url": url,
            "traceback": traceback.format_exc(),
        }
        log.error(msg=", ".join([f"{k}: {v}" for k, v in error_item.items()]))
        raise GitHubClientError(GitHubClientError.CONNECTION_ERROR,
                                f"Can not connect to GitHub API: {str(error)}")

    except HTTPStatusError as error:
        status_code = error.response.status_code
        error_item = {
            "message": f"Dependency error: {error}",
            "url": error.response.url,
            "status_code": status_code,
            "text": error.response.text,
            "traceback": traceback.format_exc(),
        }
        log.error(msg=", ".join([f"{k}: {v}" for k, v in error_item.items()]))

        if status_code == httpx.codes.GATEWAY_TIMEOUT:
            raise GitHubClientError(GitHubClientError.CONNECTION_ERROR,
                                    f"Can not connect to GitHub API: {str(error)}")

        raise GitHubClientError(GitHubClientError.NOT_ACCESSIIBLE_REPO,
                                f"Can not get repo info. Repo does not exist or it is private: {str(error)}")

    except (HTTPError, JSONDecodeError) as error:
        print(error)
        error_item = {
            "message": f"Client Error: {error}",
            "url": url,
            "text": data_text,
            "traceback": traceback.format_exc(),
        }
        log.error(msg=", ".join([f"{k}: {v}" for k, v in error_item.items()]))
        raise GitHubClientError(GitHubClientError.PARSING_ERROR,
                                f"There was a problem parsing data: {str(error)}")

    return data_json


def fetch_repo_info(username, repo):

    url = repo_api.format(username, repo)
    response = fetch(url, "GET", headers=headers, timeout=0.5)
    return response


def is_popular(username, repo):

    repo_info = fetch_repo_info(username, repo)

    try:
        score = int(repo_info.get("stargazers_count", "")) + 2 * int(repo_info.get("forks_count", ""))
    except ValueError as error:
        raise GitHubClientError(GitHubClientError.PARSING_ERROR,
                                f"Error parsing information from client: {str(error)}")

    return True if score >= 500 else False
