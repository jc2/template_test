from fastapi import FastAPI, HTTPException

from clients.github import is_popular, GitHubClientError, test_connection

app = FastAPI()


@app.get("/health")
def health():
    depenpendecies = [
        test_connection
    ]
    for dependency in depenpendecies:
        try:
            dependency()
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Healthcheck not passed: {str(e)}")
    else:
        return {"status": "ok"}


@app.get("/api/v1/score/{username}/{repo_name}")
def get_score(username: str, repo_name: str):

    try:
        response = is_popular(username, repo_name)
    except GitHubClientError as e:
        raise HTTPException(status_code=400,
                            detail=f"Error ocurring calling Github: Error number: {e.code} - {e.message}")

    return {"is_popular": response}
