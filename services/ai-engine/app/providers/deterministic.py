from app.domain.models import Action
from app.providers.base import AIProvider
from app.providers.provider_models import ProviderContext, ProviderResponse


class DeterministicProvider(AIProvider):
    """Zero-cost deterministic provider used as a safe fallback."""

    def generate(self, context: ProviderContext) -> ProviderResponse:
        ticket = context.ticket
        action = context.policy_action
        tags = set(context.policy_flags) | set(ticket.policy_tags)

        if action == Action.REFUSE_AND_GUIDE:
            if "secret_protection" in tags or "secret_request" in tags:
                answer = (
                    "For security reasons, CloudDesk cannot provide or retrieve "
                    "existing private API keys or credentials. Please revoke the "
                    "lost or exposed key and generate a replacement through your "
                    "account settings."
                )
            elif "no_passwords" in tags:
                answer = (
                    "I can't provide or retrieve your password. "
                    "Please use the password reset process."
                )
            else:
                answer = (
                    "I can't fulfill this request directly, but I can guide you "
                    "through the supported CloudDesk process."
                )

        elif action == Action.REFUSE:
            answer = (
                "I can't provide private credentials or internal-only information. "
                "I can help with the supported customer-facing process instead."
            )

        elif action in {
            Action.HUMAN_REVIEW,
            Action.ESCALATE,
            Action.REFUSE_AND_ESCALATE,
        }:
            answer = (
                "This request requires review by the appropriate CloudDesk team "
                "because it involves a sensitive or exceptional case."
            )

        elif action == Action.CLARIFY:
            answer = (
                "I need a little more information to troubleshoot this safely. "
                "Please provide the relevant error code, affected feature, and "
                "any recent configuration changes. Do not include passwords or "
                "private API keys."
            )

        else:
            # Evaluation tickets have a labelled answer summary. Live tickets
            # do not, so use the summary only when one exists.
            answer = ticket.expected_answer_summary.strip()

            if not answer:
                answer = (
                    "Thanks for reaching out. I can help with this request. "
                    "Please provide any relevant details about the issue, "
                    "including the affected feature and any recent changes."
                )

        return ProviderResponse(
            answer=answer,
            action=action,
            confidence=1.0,
        )