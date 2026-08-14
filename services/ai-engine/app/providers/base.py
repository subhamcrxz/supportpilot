from abc import ABC, abstractmethod

from app.providers.provider_models import ProviderContext, ProviderResponse


class AIProvider(ABC):
    @abstractmethod
    def generate(self, context: ProviderContext) -> ProviderResponse:
        """Generate a structured response for a support ticket."""
        raise NotImplementedError