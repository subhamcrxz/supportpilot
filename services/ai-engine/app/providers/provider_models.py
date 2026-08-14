from pydantic import BaseModel, Field

from app.domain.models import Action, SupportTicket


class ProviderContext(BaseModel):
    ticket: SupportTicket
    policy_action: Action
    policy_flags: list[str] = Field(default_factory=list)
    documents: dict[str, str] = Field(default_factory=dict)


class ProviderResponse(BaseModel):
    answer: str
    action: Action
    confidence: float = Field(ge=0.0, le=1.0)