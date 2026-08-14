"""SupportPilot AI Engine — FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.analyze import router as analyze_router
from app.routes.health import router as health_router

app = FastAPI(
    title="SupportPilot AI Engine",
    description="Independently deployable AI workloads for SupportPilot",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(analyze_router)
