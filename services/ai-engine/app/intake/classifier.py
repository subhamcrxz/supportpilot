from app.domain.models import (
    Action,
    SupportTicket,
    TicketAnalysisRequest,
    TicketCategory,
    TicketDifficulty,
    TicketSeverity,
)


class TicketClassifier:
    """
    Lightweight deterministic classifier for the first product MVP.

    This intentionally handles high-risk signals conservatively.
    The policy engine remains authoritative.
    """

    def classify(
        self,
        request: TicketAnalysisRequest,
    ) -> SupportTicket:
        text = f"{request.subject}\n{request.message}".lower()

        tags: list[str] = []

        # ---------------------------------------------------------
        # Security / credential protection
        # ---------------------------------------------------------

        if any(
            phrase in text
            for phrase in (
                "api key",
                "api secret",
                "access token",
                "private key",
                "secret key",
                "password",
            )
        ):
            tags.append("secret_protection")

        if any(
            phrase in text
            for phrase in (
                "send me the api key",
                "send me the old api key",
                "send me our old api key",
                "give me the api key",
                "give me the old api key",
                "give me our old api key",
                "show me the api key",
                "show me the old api key",
                "show me our old api key",
                "retrieve my api key",
                "retrieve the api key",
                "retrieve our api key",
                "what is my api key",
                "what is the api key",
                "what is our api key",
                "recover my api key",
                "recover the api key",
                "provide my api key",
                "provide the api key",
                "provide our api key",
                "give me my password",
                "show me my password",
                "send me my password",
            )
        ):
            tags.append("secret_request")

        # ---------------------------------------------------------
        # Prompt injection
        # ---------------------------------------------------------

        if any(
            phrase in text
            for phrase in (
                "ignore your instructions",
                "ignore previous instructions",
                "ignore your rules",
                "system prompt",
                "reveal your instructions",
                "show me your prompt",
            )
        ):
            tags.append("prompt_injection")

        # ---------------------------------------------------------
        # Security incidents
        # ---------------------------------------------------------

        if any(
            phrase in text
            for phrase in (
                "api key exposed",
                "api key leaked",
                "credential exposed",
                "credentials exposed",
                "hacked",
                "breach",
                "security incident",
                "unauthorized access",
            )
        ):
            tags.append("security_incident")

        # ---------------------------------------------------------
        # Account ownership / identity verification
        # ---------------------------------------------------------

        if any(
            phrase in text
            for phrase in (
                "change account owner",
                "change the account owner",
                "make me owner",
                "transfer ownership",
                "account ownership",
            )
        ):
            tags.append("identity_verification")

        if any(
            phrase in text
            for phrase in (
                "without contacting",
                "without verification",
                "without verifying",
                "bypass verification",
                "skip verification",
                "owner is unavailable",
            )
        ):
            tags.append("verification_bypass")

        # ---------------------------------------------------------
        # Billing exceptions
        # ---------------------------------------------------------

        if any(
            phrase in text
            for phrase in (
                "duplicate charge",
                "charged twice",
                "charged two times",
                "double charged",
            )
        ):
            tags.append("billing_exception")

        # ---------------------------------------------------------
        # Refund exceptions
        # ---------------------------------------------------------

        if any(
            phrase in text
            for phrase in (
                "refund",
                "chargeback",
                "money back",
            )
        ):
            if any(
                phrase in text
                for phrase in (
                    "exception",
                    "outside policy",
                    "expired",
                    "already refunded",
                )
            ):
                tags.append("refund_exception")

        # ---------------------------------------------------------
        # Production outage
        # ---------------------------------------------------------

        if any(
            phrase in text
            for phrase in (
                "500 errors everywhere",
                "everything is down",
                "production is down",
                "production outage",
                "all requests failing",
                "entire api is down",
            )
        ):
            tags.append("outage")

        # ---------------------------------------------------------
        # Basic classification
        # ---------------------------------------------------------

        if any(
            phrase in text
            for phrase in (
                "invoice",
                "billing",
                "charged",
                "payment",
                "subscription",
            )
        ):
            category = TicketCategory.BILLING

        elif any(
            phrase in text
            for phrase in (
                "api",
                "401",
                "403",
                "404",
                "500",
                "endpoint",
                "request",
            )
        ):
            category = TicketCategory.TECHNICAL_API

        elif any(
            phrase in text
            for phrase in (
                "login",
                "log in",
                "password",
                "authentication",
                "sign in",
            )
        ):
            category = TicketCategory.ACCOUNT_AUTHENTICATION

        elif any(
            phrase in text
            for phrase in (
                "permission",
                "owner",
                "admin",
                "role",
                "access",
            )
        ):
            category = TicketCategory.PERMISSIONS_SECURITY

        elif any(
            phrase in text
            for phrase in (
                "integration",
                "webhook",
                "salesforce",
                "slack",
                "zapier",
            )
        ):
            category = TicketCategory.INTEGRATIONS

        elif any(
            phrase in text
            for phrase in (
                "feature",
                "support",
                "add",
                "would like",
            )
        ):
            category = TicketCategory.FEATURE_REQUEST

        elif any(
            phrase in text
            for phrase in (
                "refund",
                "cancel",
                "cancellation",
            )
        ):
            category = TicketCategory.REFUND_CANCELLATION

        else:
            category = TicketCategory.PRODUCT_HOW_TO

        # High-risk tickets should not be treated as easy.
        if tags:
            difficulty = TicketDifficulty.MEDIUM
        else:
            difficulty = TicketDifficulty.EASY

        if "security_incident" in tags or "outage" in tags:
            severity = TicketSeverity.P1
        elif tags:
            severity = TicketSeverity.P2
        else:
            severity = TicketSeverity.P3

        return SupportTicket(
            id="LIVE",
            subject=request.subject,
            message=request.message,
            category=category,
            severity=severity,
            difficulty=difficulty,
            customer=request.customer,
            # These fields are only required by the current evaluation
            # model. The policy engine does not use them for decisions.
            expected_action=Action.ANSWER,
            expected_answer_summary="",
            required_sources=[],
            should_escalate=False,
            policy_tags=tags,
        )
