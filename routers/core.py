from fastapi import APIRouter, HTTPException

from clients.github import is_popular, GitHubClientError

router = APIRouter(
    prefix="/api/v1",
)


@router.get("/score/{username}/{repo_name}")
def get_score(username: str, repo_name: str):

    try:
        response = is_popular(username, repo_name)
    except GitHubClientError as e:
        raise HTTPException(status_code=400,
                            detail=f"Error ocurring calling Github: Error number: {e.code} - {e.message}")

    return {"is_popular": response}
