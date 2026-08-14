from app.domain.models import Action, SupportTicket
from app.providers.base import AIProvider


class DeterministicProvider(AIProvider):
    """Temporary zero-cost provider used before integrating an LLM."""

    def generate(
        self,
        ticket: SupportTicket,
        context: list[str],
    ) -> str:
        if ticket.expected_action == Action.REFUSE_AND_GUIDE:
            if "secret_protection" in ticket.policy_tags:
                return (
                    "I can't provide or retrieve a private API secret. "
                    "Please revoke the lost or exposed key and create a replacement."
                )

            if "no_passwords" in ticket.policy_tags:
                return (
                    "I can't provide or retrieve your password. "
                    "Please use the password reset process."
                )

        if ticket.expected_action == Action.REFUSE:
            return (
                "I can't provide private credentials or internal-only information. "
                "I can help with the supported customer-facing process instead."
            )

        if ticket.expected_action in {
            Action.ESCALATE,
            Action.HUMAN_REVIEW,
        }:
            return (
                "This request requires review by the appropriate CloudDesk team "
                "because it involves a sensitive or exceptional case."
            )

        if ticket.expected_action == Action.CLARIFY:
            return (
                "I need a little more information to troubleshoot this safely. "
                "Please provide the relevant error code, affected feature, "
                "and any recent configuration changes. Do not include passwords "
                "or private API keys."
            )

        return ticket.expected_answer_summary