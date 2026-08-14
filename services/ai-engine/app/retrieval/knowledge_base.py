from pathlib import Path

from app.domain.models import SupportTicket


class CloudDeskKnowledgeBase:
    """Loads CloudDesk evaluation data from the repository."""

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