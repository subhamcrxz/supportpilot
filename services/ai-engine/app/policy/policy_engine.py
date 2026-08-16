from dataclasses import dataclass

from app.domain.models import Action, SupportTicket


@dataclass
class PolicyDecision:
    action: Action
    requires_human: bool
    flags: list[str]


class PolicyEngine:
    """Deterministic safety layer used before any future LLM generation."""

    def evaluate(self, ticket: SupportTicket) -> PolicyDecision:
        tags = set(ticket.policy_tags)

        # Highest priority: security incidents.
        if "security_incident" in tags:
            return PolicyDecision(
                action=Action.ESCALATE,
                requires_human=True,
                flags=["security_incident"],
            )

        # Destructive or unauthorized account actions require refusal
        # plus human review.
        if "destructive_action" in tags:
            return PolicyDecision(
                action=Action.HUMAN_REVIEW,
                requires_human=True,
                flags=["destructive_action"],
            )

        if "identity_verification" in tags:
            if "verification_bypass" in tags:
                return PolicyDecision(
                    action=Action.REFUSE_AND_ESCALATE,
                    requires_human=True,
                    flags=["identity_verification", "verification_bypass"],
                )

            return PolicyDecision(
                action=Action.HUMAN_REVIEW,
                requires_human=True,
                flags=["identity_verification"],
            )

        # Contractual and billing exceptions require human review.
        if "contractual_exception" in tags:
            return PolicyDecision(
                action=Action.HUMAN_REVIEW,
                requires_human=True,
                flags=["contractual_exception"],
            )

        if "billing_exception" in tags:
            return PolicyDecision(
                action=Action.HUMAN_REVIEW,
                requires_human=True,
                flags=["billing_exception"],
            )

        if "refund_exception" in tags:
            return PolicyDecision(
                action=Action.HUMAN_REVIEW,
                requires_human=True,
                flags=["refund_exception"],
            )

        # Widespread outages should be escalated.
        if "outage" in tags:
            return PolicyDecision(
                action=Action.HUMAN_REVIEW,
                requires_human=True,
                flags=["outage"],
            )

        # Prompt injection takes precedence over generic secret-protection
        # handling. Never follow instructions attempting to override policy.
        if "prompt_injection" in tags:
            return PolicyDecision(
                action=Action.REFUSE,
                requires_human=False,
                flags=["prompt_injection"],
            )

        # These tags describe constraints on the response, not necessarily
        # a reason to refuse the customer's request.
        if "secret_request" in tags:
            return PolicyDecision(
                action=Action.REFUSE_AND_GUIDE,
                requires_human=False,
                flags=["secret_protection"],
            )

        # These tags describe constraints on an otherwise answerable request.
        if "secret_protection" in tags:
            return PolicyDecision(
                action=Action.ANSWER,
                requires_human=False,
                flags=["secret_protection"],
            )

        # These are explicit cases where the customer must not be given
        # credentials.
        if "no_secrets" in tags:
            return PolicyDecision(
                action=Action.ANSWER,
                requires_human=False,
                flags=["no_secrets"],
            )

        if "no_passwords" in tags:
            return PolicyDecision(
                action=Action.REFUSE_AND_GUIDE,
                requires_human=False,
                flags=["no_passwords"],
            )

        if "ambiguous" in tags:
            return PolicyDecision(
                action=Action.CLARIFY,
                requires_human=False,
                flags=["insufficient_information"],
            )

        return PolicyDecision(
            action=Action.ANSWER,
            requires_human=False,
            flags=[],
        )