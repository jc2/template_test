import os

from dotenv import load_dotenv
from fastapi import FastAPI
from routers import health, core

load_dotenv(".env")

app = FastAPI(title=os.getenv("PROJECT_NAME"), version="1.0.0")

app.include_router(health.router)
app.include_router(core.router)
