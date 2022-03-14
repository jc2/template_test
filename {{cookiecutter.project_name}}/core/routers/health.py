from fastapi import APIRouter, HTTPException

from clients.github import test_connection as github_test


router = APIRouter(
    prefix="/health",
)


@router.get("/healthy")
def health():
    depenpendecies = [
        github_test
    ]
    for dependency in depenpendecies:
        try:
            dependency()
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Healthcheck not passed: {str(e)}")
    else:
        return {"status": "ok"}
