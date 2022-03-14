from fastapi import FastAPI


from routers import health, core

app = FastAPI()

app.include_router(health.router)
app.include_router(core.router)
