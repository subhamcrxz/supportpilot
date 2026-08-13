"""Health check routes."""

from fastapi import APIRouter
from pydantic import BaseModel


class ServiceHealth(BaseModel):
    status: str
    service: str


router = APIRouter()


@router.get("/health", response_model=ServiceHealth)
async def health() -> ServiceHealth:
    return ServiceHealth(status="ok", service="ai-engine")
