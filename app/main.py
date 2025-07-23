from fastapi import FastAPI
from app.api.v1.endpoints import stats, config
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title="People Tracking API",
    default_response_class=ORJSONResponse,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    version="1.0.0",
    description="API for managing and tracking people in defined areas using computer vision.",
)

app.include_router(stats.router)
app.include_router(config.router)
