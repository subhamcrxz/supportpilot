from pathlib import Path

from app.domain.models import AnalysisResult
from app.policy.policy_engine import PolicyEngine
from app.providers.base import AIProvider
from app.providers.deterministic import DeterministicProvider
from app.providers.provider_models import ProviderContext
from app.providers.validator import validate_provider_response
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

        all_documents = self.knowledge_base.load_documents()

        relevant_documents = {
            source: all_documents[source]
            for source in ticket.required_sources
            if source in all_documents
        }

        provider_context = ProviderContext(
            ticket=ticket,
            policy_action=policy.action,
            policy_flags=policy.flags,
            documents=relevant_documents,
        )

        provider_response = self.provider.generate(provider_context)

        provider_response = validate_provider_response(
            provider_context,
            provider_response,
        )

        # The deterministic policy engine remains authoritative.
        # The provider may generate the answer, but it cannot override
        # a hard safety decision.
        final_action = policy.action

        return AnalysisResult(
            ticket_id=ticket.id,
            category=ticket.category,
            severity=ticket.severity,
            difficulty=ticket.difficulty,
            action=final_action,
            answer=provider_response.answer,
            requires_human=policy.requires_human,
            policy_flags=policy.flags,
            sources=list(relevant_documents.keys()),
        )


def create_analyzer(repo_root: Path) -> TicketAnalyzer:
    return TicketAnalyzer(
        knowledge_base=CloudDeskKnowledgeBase(repo_root),
        policy_engine=PolicyEngine(),
        provider=DeterministicProvider(),
    )