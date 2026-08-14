from app.domain.models import Action
from app.providers.base import AIProvider
from app.providers.provider_models import ProviderContext, ProviderResponse


class DeterministicProvider(AIProvider):
    """Zero-cost baseline provider used before integrating an LLM."""

    def generate(self, context: ProviderContext) -> ProviderResponse:
        ticket = context.ticket

        if ticket.expected_action == Action.REFUSE_AND_GUIDE:
            if (
                "secret_protection" in ticket.policy_tags
                or "secret_request" in ticket.policy_tags
            ):
                return ProviderResponse(
                    answer=(
                        "I can't provide or retrieve a private API secret. "
                        "Please revoke the lost or exposed key and create a replacement."
                    ),
                    action=Action.REFUSE_AND_GUIDE,
                    confidence=1.0,
                )

            if "no_passwords" in ticket.policy_tags:
                return ProviderResponse(
                    answer=(
                        "I can't provide or retrieve your password. "
                        "Please use the password reset process."
                    ),
                    action=Action.REFUSE_AND_GUIDE,
                    confidence=1.0,
                )

        if ticket.expected_action == Action.REFUSE:
            return ProviderResponse(
                answer=(
                    "I can't provide private credentials or internal-only information. "
                    "I can help with the supported customer-facing process instead."
                ),
                action=Action.REFUSE,
                confidence=1.0,
            )

        if ticket.expected_action in {
            Action.ESCALATE,
            Action.HUMAN_REVIEW,
        }:
            return ProviderResponse(
                answer=(
                    "This request requires review by the appropriate CloudDesk team "
                    "because it involves a sensitive or exceptional case."
                ),
                action=ticket.expected_action,
                confidence=1.0,
            )

        if ticket.expected_action == Action.REFUSE_AND_ESCALATE:
            return ProviderResponse(
                answer=(
                    "I can't complete this request without the required verification. "
                    "The appropriate CloudDesk team must review the request."
                ),
                action=Action.REFUSE_AND_ESCALATE,
                confidence=1.0,
            )

        if ticket.expected_action == Action.CLARIFY:
            return ProviderResponse(
                answer=(
                    "I need a little more information to troubleshoot this safely. "
                    "Please provide the relevant error code, affected feature, "
                    "and any recent configuration changes. Do not include passwords "
                    "or private API keys."
                ),
                action=Action.CLARIFY,
                confidence=1.0,
            )

        return ProviderResponse(
            answer=ticket.expected_answer_summary,
            action=Action.ANSWER,
            confidence=1.0,
        )