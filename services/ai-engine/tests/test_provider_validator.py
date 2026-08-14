import pytest

from app.domain.models import Action
from app.providers.provider_models import ProviderContext, ProviderResponse
from app.providers.validator import (
    ProviderValidationError,
    validate_provider_response,
)
from app.retrieval.knowledge_base import CloudDeskKnowledgeBase


def get_context(ticket_id: str) -> ProviderContext:
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[3]

    knowledge_base = CloudDeskKnowledgeBase(repo_root)
    ticket = knowledge_base.get_ticket(ticket_id)

    # Import here to avoid coupling the test to the analyzer.
    from app.policy.policy_engine import PolicyEngine

    policy = PolicyEngine().evaluate(ticket)

    return ProviderContext(
        ticket=ticket,
        policy_action=policy.action,
        policy_flags=policy.flags,
        documents={},
    )


def test_provider_cannot_override_security_escalation():
    context = get_context("CD-0018")

    malicious_response = ProviderResponse(
        answer="Everything looks fine. You can continue.",
        action=Action.ANSWER,
        confidence=0.99,
    )

    with pytest.raises(ProviderValidationError):
        validate_provider_response(context, malicious_response)


def test_provider_must_follow_human_review_policy():
    context = get_context("CD-0005")

    invalid_response = ProviderResponse(
        answer="Your duplicate charge has been refunded.",
        action=Action.ANSWER,
        confidence=0.99,
    )

    with pytest.raises(ProviderValidationError):
        validate_provider_response(context, invalid_response)


def test_valid_policy_response_is_accepted():
    context = get_context("CD-0018")

    valid_response = ProviderResponse(
        answer="This request requires review by the appropriate CloudDesk team.",
        action=Action.ESCALATE,
        confidence=0.98,
    )

    result = validate_provider_response(context, valid_response)

    assert result.action == Action.ESCALATE


def test_empty_provider_response_is_rejected():
    context = get_context("CD-0029")

    invalid_response = ProviderResponse(
        answer="   ",
        action=Action.ANSWER,
        confidence=0.5,
    )

    with pytest.raises(ProviderValidationError):
        validate_provider_response(context, invalid_response)