from fastapi import FastAPI
from app.api.v1.endpoints import stats, config

app = FastAPI(title="People Tracking API")

app.include_router(stats.router)
app.include_router(config.router)
