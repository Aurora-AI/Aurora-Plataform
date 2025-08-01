from .base import BaseLLMAdapter


class AzureOpenAIAdapter(BaseLLMAdapter):
    def generate(self, prompt: str) -> str:
        return f"Resposta [Azure OpenAI]: {prompt}"
