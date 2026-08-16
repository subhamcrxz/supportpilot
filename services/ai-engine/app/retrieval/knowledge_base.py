import re
from pathlib import Path

from app.domain.models import SupportTicket

CATEGORY_DOCUMENTS = {
    "billing": [
        "billing.md",
        "refund-policy.md",
    ],
    "technical_api": [
        "api.md",
        "api-errors.md",
        "troubleshooting.md",
    ],
    "account_authentication": [
        "authentication.md",
        "accounts.md",
    ],
    "permissions_security": [
        "users-and-permissions.md",
        "security.md",
        "escalation-policy.md",
    ],
    "integrations": [
        "integrations.md",
    ],
    "product_how_to": [
        "getting-started.md",
        "common-questions.md",
    ],
    "refund_cancellation": [
        "refund-policy.md",
        "billing.md",
    ],
    "feature_request": [
        "features.md",
        "common-questions.md",
    ],
}

class CloudDeskKnowledgeBase:
    """Loads and retrieves CloudDesk support documentation."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.clouddesk_root = repo_root / "evals" / "clouddesk"

    def load_tickets(self) -> list[SupportTicket]:
        import json

        path = self.clouddesk_root / "tickets" / "tickets.json"

        with path.open("r", encoding="utf-8") as file:
            raw_tickets = json.load(file)

        return [SupportTicket.model_validate(ticket) for ticket in raw_tickets]

    def get_ticket(self, ticket_id: str) -> SupportTicket:
        for ticket in self.load_tickets():
            if ticket.id == ticket_id:
                return ticket

        raise KeyError(f"CloudDesk ticket not found: {ticket_id}")

    def load_documents(self) -> dict[str, str]:
        documents: dict[str, str] = {}

        directories = [
            self.clouddesk_root / "company",
            self.clouddesk_root / "product",
            self.clouddesk_root / "support",
            self.clouddesk_root / "knowledge-base",
        ]

        for directory in directories:
            if not directory.exists():
                continue

            for path in directory.glob("*.md"):
                documents[path.name] = path.read_text(encoding="utf-8")

        return documents

    def retrieve(
        self,
        query: str,
        limit: int = 3,
        preferred_documents: list[str] | None = None,
    ) -> dict[str, str]:
        """
        Retrieve the most relevant support documents using local keyword
        matching plus optional document preferences.
        """
        documents = self.load_documents()

        if not documents:
            return {}

        query_terms = self._tokenize(query)
        preferred = set(preferred_documents or [])

        scored: list[tuple[int, str, str]] = []

        for name, content in documents.items():
            document_terms = self._tokenize(
                f"{name}\n{content}"
            )

            keyword_score = sum(
                1
                for term in query_terms
                if term in document_terms
            )

            preference_score = 0

            if name in preferred:
                preference_score = 100

            score = keyword_score + preference_score

            if score > 0:
                scored.append((score, name, content))

        scored.sort(
            key=lambda item: (-item[0], item[1])
        )

        return {
            name: content
            for _, name, content in scored[:limit]
        }

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        words = re.findall(
            r"[a-zA-Z0-9_]+",
            text.lower(),
        )

        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "to",
            "of",
            "in",
            "on",
            "for",
            "is",
            "are",
            "i",
            "me",
            "my",
            "we",
            "our",
            "can",
            "you",
            "please",
            "this",
            "that",
            "with",
        }

        return {
            word
            for word in words
            if len(word) > 2 and word not in stop_words
        }