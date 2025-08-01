from .base import BaseLLMAdapter


class DeepSeekAdapter(BaseLLMAdapter):
    def generate(self, prompt: str) -> str:
        return f"Resposta [DeepSeek]: {prompt}"
