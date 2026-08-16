from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from app.auth import require_api_key
from app.domain.models import AnalysisResult, TicketAnalysisRequest
from app.pipeline.analyze_ticket import create_analyzer
from app.providers.gemini import (
    GeminiProviderError,
    GeminiRateLimitError,
    GeminiUnavailableError,
)

router = APIRouter(
    prefix="/analyze",
    tags=["analysis"],
    dependencies=[Depends(require_api_key)],
)

REPO_ROOT = Path(__file__).resolve().parents[4]

analyzer = create_analyzer(REPO_ROOT)


@router.post(
    "/ticket/{ticket_id}",
    response_model=AnalysisResult,
)
def analyze_ticket(ticket_id: str) -> AnalysisResult:
    try:
        return analyzer.analyze(ticket_id)

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except GeminiRateLimitError as exc:
        raise HTTPException(
            status_code=429,
            detail="AI service quota temporarily exceeded. Please try again later.",
        ) from exc

    except GeminiUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Please try again later.",
        ) from exc

    except GeminiProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail="AI provider request failed. Please try again later.",
        ) from exc


@router.post(
    "/request",
    response_model=AnalysisResult,
)
def analyze_request(
    request: TicketAnalysisRequest,
) -> AnalysisResult:
    try:
        return analyzer.analyze_request(request)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except GeminiRateLimitError as exc:
        raise HTTPException(
            status_code=429,
            detail="AI service quota temporarily exceeded. Please try again later.",
        ) from exc

    except GeminiUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Please try again later.",
        ) from exc

    except GeminiProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail="AI provider request failed. Please try again later.",
        ) from exc