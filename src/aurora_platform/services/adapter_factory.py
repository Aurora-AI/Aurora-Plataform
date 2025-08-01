# src/aurora_platform/services/adapter_factory.py


from .llm_adapters.azure_adapter import AzureOpenAIAdapter
from .llm_adapters.base import BaseLLMAdapter
from .llm_adapters.deepseek_adapter import DeepSeekAdapter
from .llm_adapters.google_adapter import VertexAIAdapter


class AdapterFactory:
    """
    Fábrica responsável por criar a instância correta do adaptador de LLM
    com base no nome do provedor.
    """

    @staticmethod
    def get_adapter(provider_name: str) -> BaseLLMAdapter:
        provider_name = provider_name.lower()
        if provider_name == "google":
            return VertexAIAdapter()
        elif provider_name == "azure":
            return AzureOpenAIAdapter()
        elif provider_name == "deepseek":
            return DeepSeekAdapter()
        else:
            raise ValueError(
                f"Provedor de LLM desconhecido: '{provider_name}'. "
                "Os provedores suportados são: google, azure, deepseek."
            )
