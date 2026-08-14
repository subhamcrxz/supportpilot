from pathlib import Path

from app.domain.models import AnalysisResult
from app.policy.policy_engine import PolicyEngine
from app.providers.base import AIProvider
from app.retrieval.knowledge_base import CloudDeskKnowledgeBase


class TicketAnalyzer:
    def __init__(
        self,
        knowledge_base: CloudDeskKnowledgeBase,
        policy_engine: PolicyEngine,
        provider: AIProvider,
    ):
        self.knowledge_base = knowledge_base
        self.policy_engine = policy_engine
        self.provider = provider

    def analyze(self, ticket_id: str) -> AnalysisResult:
        ticket = self.knowledge_base.get_ticket(ticket_id)

        policy = self.policy_engine.evaluate(ticket)

        answer = self.provider.generate(
            ticket=ticket,
            context=ticket.required_sources,
        )

        return AnalysisResult(
            ticket_id=ticket.id,
            category=ticket.category,
            severity=ticket.severity,
            difficulty=ticket.difficulty,
            action=policy.action,
            answer=answer,
            requires_human=policy.requires_human,
            policy_flags=policy.flags,
            sources=ticket.required_sources,
        )


def create_analyzer(repo_root: Path) -> TicketAnalyzer:
    from app.providers.deterministic import DeterministicProvider

    return TicketAnalyzer(
        knowledge_base=CloudDeskKnowledgeBase(repo_root),
        policy_engine=PolicyEngine(),
        provider=DeterministicProvider(),
    )