from app.domain.models import Action
from app.providers.provider_models import ProviderContext, ProviderResponse

WORKFLOW_CLAIMS = (
    "i have escalated",
    "i've escalated",
    "we have escalated",
    "we've escalated",
    "your request has been escalated",
    "your ticket has been escalated",
    "this ticket has been escalated",
    "has been escalated to",
    "has been sent to the security team",
    "has been sent to the support team",
    "the security team has been notified",
    "the support team has been notified",
    "a member of the security team will contact",
    "a member of the support team will contact",
    "someone from the security team will contact",
    "someone from the support team will contact",
    "the team will contact you",
)


REFUSAL_ESCALATION_LANGUAGE = (
    "requires review",
    "requires human review",
    "human review",
    "security team",
    "support team",
    "escalate",
    "escalated",
)


class ProviderValidationError(ValueError):
    """Raised when an AI provider returns an unsafe or invalid response."""


def validate_provider_response(
    context: ProviderContext,
    response: ProviderResponse,
) -> ProviderResponse:
    """
    Validate an AI provider response against SupportPilot's policy decision.

    The policy engine is authoritative. An AI provider may generate
    customer-facing language, but it cannot override the policy action
    or falsely imply that unsupported workflow actions have occurred.
    """

    # The provider must not override the policy engine's decision.
    if response.action != context.policy_action:
        raise ProviderValidationError(
            "AI provider attempted to override the policy action: "
            f"policy={context.policy_action.value}, "
            f"provider={response.action.value}"
        )

    answer_lower = response.answer.lower()

    # The provider must never claim that a workflow action has already
    # occurred when SupportPilot has not actually executed that workflow.
    for phrase in WORKFLOW_CLAIMS:
        if phrase in answer_lower:
            raise ProviderValidationError(
                "Provider response falsely claims that a workflow action "
                f"has occurred: '{phrase}'"
            )

    # A plain refusal must not imply that the request will be escalated
    # or reviewed by another team.
    if context.policy_action == Action.REFUSE:
        for phrase in REFUSAL_ESCALATION_LANGUAGE:
            if phrase in answer_lower:
                raise ProviderValidationError(
                    "Provider refusal implies human escalation or review "
                    f"despite policy action={context.policy_action.value}: "
                    f"'{phrase}'"
                )

    # Human-review or escalation decisions must contain a customer-facing
    # explanation.
    if context.policy_action in {
        Action.HUMAN_REVIEW,
        Action.ESCALATE,
        Action.REFUSE_AND_ESCALATE,
    }:
        if not response.answer.strip():
            raise ProviderValidationError(
                "Human-review or escalation responses must contain "
                "a safe explanation."
            )

    # Every provider response must contain useful text.
    if not response.answer.strip():
        raise ProviderValidationError(
            "AI provider returned an empty answer."
        )

    return response