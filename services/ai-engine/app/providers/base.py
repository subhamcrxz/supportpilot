from abc import ABC, abstractmethod

from app.domain.models import SupportTicket


class AIProvider(ABC):
    @abstractmethod
    def generate(
        self,
        ticket: SupportTicket,
        context: list[str],
    ) -> str:
        """Generate a response for a support ticket."""
        raise NotImplementedError