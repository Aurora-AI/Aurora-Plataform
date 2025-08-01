from .base import BaseLLMAdapter


class VertexAIAdapter(BaseLLMAdapter):
    def generate(self, prompt: str) -> str:
        return f"Resposta [Google VertexAI]: {prompt}"
