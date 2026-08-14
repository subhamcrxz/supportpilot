from app.domain.models import Action
from app.providers.provider_models import ProviderContext, ProviderResponse


class ProviderValidationError(ValueError):
    """Raised when an AI provider returns an unsafe or invalid response."""


def validate_provider_response(
    context: ProviderContext,
    response: ProviderResponse,
) -> ProviderResponse:
    """
    Validate an AI provider response against SupportPilot's policy decision.

    The policy engine is authoritative. An AI provider may generate language,
    but it cannot override a hard policy action.
    """

    # The provider must not override the policy engine's decision.
    if response.action != context.policy_action:
        raise ProviderValidationError(
            "AI provider attempted to override the policy action: "
            f"policy={context.policy_action.value}, "
            f"provider={response.action.value}"
        )

    # Human-review decisions must never become customer-facing automatic answers.
    if context.policy_action in {
        Action.HUMAN_REVIEW,
        Action.ESCALATE,
        Action.REFUSE_AND_ESCALATE,
    }:
        if not response.answer.strip():
            raise ProviderValidationError(
                "Human-review or escalation responses must contain a safe explanation."
            )

    # A provider response must always contain useful text.
    if not response.answer.strip():
        raise ProviderValidationError(
            "AI provider returned an empty answer."
        )

    return response