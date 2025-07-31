import requests
import time


class AzureOpenAIAdapter:
    def __init__(self, endpoint: str, api_key: str, deployment_name: str):
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.deployment_name = deployment_name
        self.api_version = "2024-02-15-preview"  # Atualize conforme necessário

    def complete(
        self, prompt: str, temperature: float = 0.2, max_tokens: int = 512
    ) -> str:
        url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        headers = {"Content-Type": "application/json", "api-key": self.api_key}
        payload = {
            "messages": [
                {"role": "system", "content": "Você é um assistente especialista."},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
        }
        start = time.time()
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        latency = time.time() - start
        response.raise_for_status()
        data = response.json()
        # Extrai o texto da resposta
        content = (
            data["choices"][0]["message"]["content"] if data.get("choices") else ""
        )
        # Opcional: pode retornar também latency, usage, etc.
        return content
