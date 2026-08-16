from pathlib import Path

from app.domain.models import AnalysisResult, TicketAnalysisRequest
from app.intake.classifier import TicketClassifier
from app.policy.policy_engine import PolicyEngine
from app.providers.base import AIProvider
from app.providers.deterministic import DeterministicProvider
from app.providers.gemini import GeminiProvider
from app.providers.provider_models import ProviderContext
from app.providers.validator import validate_provider_response
from app.retrieval.knowledge_base import (
    CATEGORY_DOCUMENTS,
    CloudDeskKnowledgeBase,
)


class TicketAnalyzer:
    def __init__(
        self,
        knowledge_base: CloudDeskKnowledgeBase,
        policy_engine: PolicyEngine,
        provider: AIProvider,
        live_provider: AIProvider | None = None,
    ):
        self.knowledge_base = knowledge_base
        self.policy_engine = policy_engine
        self.provider = provider
        self.live_provider = live_provider or provider
        self.classifier = TicketClassifier()

    def analyze(self, ticket_id: str) -> AnalysisResult:
        """Analyze a labelled CloudDesk evaluation ticket."""
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

    def analyze_request(
        self,
        request: TicketAnalysisRequest,
    ) -> AnalysisResult:
        """Analyze a new customer ticket submitted to the live API."""
        ticket = self.classifier.classify(request)

        policy = self.policy_engine.evaluate(ticket)

        preferred_documents = CATEGORY_DOCUMENTS.get(
            ticket.category.value,
            [],
        )

        relevant_documents = self.knowledge_base.retrieve(
            query=f"{request.subject}\n{request.message}",
            limit=3,
            preferred_documents=preferred_documents,
        )

        provider_context = ProviderContext(
            ticket=ticket,
            policy_action=policy.action,
            policy_flags=policy.flags,
            documents=relevant_documents,
        )

        # Live customer requests use Gemini for answer generation.
        # The deterministic policy engine remains authoritative.
        provider_response = self.live_provider.generate(provider_context)

        provider_response = validate_provider_response(
            provider_context,
            provider_response,
        )

        return AnalysisResult(
            ticket_id=ticket.id,
            category=ticket.category,
            severity=ticket.severity,
            difficulty=ticket.difficulty,
            action=policy.action,
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
        live_provider=GeminiProvider(),
    )
