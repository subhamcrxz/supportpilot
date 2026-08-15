import os
from pathlib import Path

import pytest

from app.domain.models import Action
from app.policy.policy_engine import PolicyEngine
from app.providers.gemini import GeminiProvider
from app.providers.provider_models import ProviderContext
from app.providers.validator import validate_provider_response
from app.retrieval.knowledge_base import CloudDeskKnowledgeBase

pytestmark = pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY is not set",
)


TEST_CASES = [
    ("CD-0029", Action.ANSWER),
    ("CD-0018", Action.ESCALATE),
    ("CD-0014", Action.REFUSE_AND_GUIDE),
    ("CD-0032", Action.REFUSE),
    ("CD-0028", Action.REFUSE_AND_ESCALATE),
]


@pytest.mark.parametrize("ticket_id,expected_action", TEST_CASES)
def test_gemini_respects_policy(ticket_id: str, expected_action: Action):
    repo_root = Path(__file__).resolve().parents[3]

    knowledge_base = CloudDeskKnowledgeBase(repo_root)
    policy_engine = PolicyEngine()

    ticket = knowledge_base.get_ticket(ticket_id)
    policy = policy_engine.evaluate(ticket)

    assert policy.action == expected_action

    documents = knowledge_base.load_documents()

    context = ProviderContext(
        ticket=ticket,
        policy_action=policy.action,
        policy_flags=policy.flags,
        documents={
            source: documents[source]
            for source in ticket.required_sources
            if source in documents
        },
    )

    provider = GeminiProvider()

    response = provider.generate(context)

    validated = validate_provider_response(
        context,
        response,
    )

    print()
    print("=" * 70)
    print(f"Ticket:     {ticket_id}")
    print(f"Policy:     {policy.action.value}")
    print(f"Gemini:     {validated.action.value}")
    print(f"Confidence: {validated.confidence}")
    print(f"Answer:     {validated.answer}")
    print("=" * 70)

    assert validated.action == policy.action
    assert validated.answer.strip()
    assert 0.0 <= validated.confidence <= 1.0
