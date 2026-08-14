from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.domain.models import AnalysisResult
from app.pipeline.analyze_ticket import create_analyzer

router = APIRouter(prefix="/analyze", tags=["analysis"])

REPO_ROOT = Path(__file__).resolve().parents[4]
analyzer = create_analyzer(REPO_ROOT)


@router.post("/ticket/{ticket_id}", response_model=AnalysisResult)
def analyze_ticket(ticket_id: str) -> AnalysisResult:
    try:
        return analyzer.analyze(ticket_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc