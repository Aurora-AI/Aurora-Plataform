import json
import time
from typing import List, Dict, Any
from aurora_platform.services.azure_openai_adapter import AzureOpenAIAdapter
from aurora_platform.config import settings


class AgentProfilingService:
    def __init__(
        self,
        suite_path: str = "benchmarking_suite.json",
        results_path: str = "profiling_results.json",
    ):
        self.suite_path = suite_path
        self.results_path = results_path
        self.temperatures = [0.1, 0.5, 0.9]
        self.max_tokens = 512
        self.adapter = AzureOpenAIAdapter(
            endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            deployment_name="aurora-flagship-reasoning",
        )

    def load_suite(self) -> List[Dict[str, Any]]:
        with open(self.suite_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_results(self, results: List[Dict[str, Any]]):
        with open(self.results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    def run_benchmarks(self):
        suite = self.load_suite()
        all_results = []
        for problem in suite:
            for temp in self.temperatures:
                start = time.time()
                response = self.adapter.complete(
                    problem.get("prompt_pai", ""),
                    temperature=temp,
                    max_tokens=self.max_tokens,
                )
                latency = time.time() - start
                tokens_used = len(response.split())  # Aproximação simples
                result_entry = {
                    "id": problem["id"],
                    "category": problem["category"],
                    "prompt": problem.get("prompt_pai", ""),
                    "temperature": temp,
                    "latency": latency,
                    "tokens_used": tokens_used,
                    "response": response,
                }
                all_results.append(result_entry)
        self.save_results(all_results)
        return all_results

    def run_decomposition_benchmark(self):
        suite = self.load_suite()
        all_results = []
        for problem in suite:
            if problem["category"] == "tarefa_decomponivel":
                # Executa o prompt pai
                for temp in self.temperatures:
                    start = time.time()
                    response_pai = self.adapter.complete(
                        problem["prompt_pai"],
                        temperature=temp,
                        max_tokens=self.max_tokens,
                    )
                    latency_pai = time.time() - start
                    tokens_pai = len(response_pai.split())
                    result_entry_pai = {
                        "id": problem["id"],
                        "category": problem["category"],
                        "prompt": problem["prompt_pai"],
                        "temperature": temp,
                        "latency": latency_pai,
                        "tokens_used": tokens_pai,
                        "response": response_pai,
                        "type": "pai",
                    }
                    all_results.append(result_entry_pai)
                # Executa os prompts filhos
                for filho in problem.get("prompts_filhos", []):
                    for temp in self.temperatures:
                        start = time.time()
                        response_filho = self.adapter.complete(
                            filho["prompt"],
                            temperature=temp,
                            max_tokens=self.max_tokens,
                        )
                        latency_filho = time.time() - start
                        tokens_filho = len(response_filho.split())
                        result_entry_filho = {
                            "id": filho["subtask_id"],
                            "category": filho["category"],
                            "prompt": filho["prompt"],
                            "temperature": temp,
                            "latency": latency_filho,
                            "tokens_used": tokens_filho,
                            "response": response_filho,
                            "type": "filho",
                            "parent_id": problem["id"],
                        }
                        all_results.append(result_entry_filho)
        self.save_results(all_results)
        return all_results

    def generate_performance_report(self) -> str:
        with open(self.results_path, "r", encoding="utf-8") as f:
            results = json.load(f)
        report = ["# Relatório de Faixa de Performance do Agente Profiler\n"]
        grouped = {}
        for entry in results:
            key = (entry["category"], entry["temperature"])
            grouped.setdefault(key, []).append(entry)
        for (category, temp), entries in grouped.items():
            latencies = [e["latency"] for e in entries]
            tokens = [e["tokens_used"] for e in entries]
            report.append(f"## Categoria: {category} | Temperature: {temp}")
            report.append(f"- Média de Latência: {sum(latencies)/len(latencies):.2f}s")
            report.append(f"- Média de Tokens: {sum(tokens)/len(tokens):.1f}")
            report.append(f"- Total de Execuções: {len(entries)}\n")
        return "\n".join(report)
