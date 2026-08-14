from enum import StrEnum

from pydantic import BaseModel, Field


class TicketCategory(StrEnum):
    BILLING = "billing"
    TECHNICAL_API = "technical_api"
    ACCOUNT_AUTHENTICATION = "account_authentication"
    PERMISSIONS_SECURITY = "permissions_security"
    INTEGRATIONS = "integrations"
    PRODUCT_HOW_TO = "product_how_to"
    REFUND_CANCELLATION = "refund_cancellation"
    FEATURE_REQUEST = "feature_request"


class TicketSeverity(StrEnum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class TicketDifficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Action(StrEnum):
    ANSWER = "answer"
    HUMAN_REVIEW = "human_review"
    REFUSE_AND_GUIDE = "refuse_and_guide"
    REFUSE = "refuse"
    ESCALATE = "escalate"
    REFUSE_AND_ESCALATE = "refuse_and_escalate"
    CLARIFY = "clarify"


class Customer(BaseModel):
    plan: str | None = None
    role: str | None = None


class SupportTicket(BaseModel):
    id: str
    subject: str
    message: str
    category: TicketCategory
    severity: TicketSeverity
    difficulty: TicketDifficulty
    customer: Customer | None = None
    expected_action: Action
    expected_answer_summary: str
    required_sources: list[str] = Field(default_factory=list)
    should_escalate: bool = False
    policy_tags: list[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    ticket_id: str
    category: TicketCategory
    severity: TicketSeverity
    difficulty: TicketDifficulty
    action: Action
    answer: str | None = None
    requires_human: bool = False
    policy_flags: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)