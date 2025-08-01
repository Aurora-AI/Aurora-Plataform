from abc import ABC, abstractmethod


class BaseLLMAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Gera uma resposta a partir de um prompt."""
        pass
