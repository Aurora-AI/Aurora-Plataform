#!/usr/bin/env python3
"""
Protocolo de Teste de Estresse do RAG - Base de Conhecimento AMB
Executa uma bateria completa de testes cognitivos no sistema RAG
"""
import chromadb
import time
from datetime import datetime
from typing import List, Dict, Tuple
import json


class RAGStressTester:
    def __init__(self, collection_name: str = "amb_noticias"):
        """Inicializa o testador do sistema RAG"""
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_collection(name=collection_name)
        self.total_docs = self.collection.count()
        self.test_results = []

        print(f"🎯 Inicializando Teste de Estresse RAG")
        print(f"📚 Base de conhecimento: {collection_name}")
        print(f"📊 Total de documentos: {self.total_docs}")
        print("=" * 80)

    def run_query_test(
        self, query: str, expected_count: int = 5, test_name: str = ""
    ) -> Dict:
        """Executa uma consulta e mede performance"""
        start_time = time.time()

        try:
            results = self.collection.query(
                query_texts=[query], n_results=expected_count
            )

            end_time = time.time()
            response_time = end_time - start_time

            # Analisar resultados
            docs_found = 0
            has_metadata = False

            if results and hasattr(results, "get") and results.get("documents"):
                docs = results["documents"]
                if docs and len(docs) > 0 and docs[0]:
                    docs_found = len(docs[0])

                if (
                    results.get("metadatas")
                    and results["metadatas"]
                    and len(results["metadatas"]) > 0
                ):
                    has_metadata = bool(results["metadatas"][0])

            # Calcular relevância baseada na presença de termos-chave
            relevance_score = self.calculate_relevance(query, results)

            test_result = {
                "test_name": test_name,
                "query": query,
                "response_time_ms": round(response_time * 1000, 2),
                "documents_found": docs_found,
                "has_metadata": has_metadata,
                "relevance_score": relevance_score,
                "status": "SUCCESS" if docs_found > 0 else "NO_RESULTS",
                "timestamp": datetime.now().isoformat(),
            }

            return test_result

        except Exception as e:
            return {
                "test_name": test_name,
                "query": query,
                "response_time_ms": 0,
                "documents_found": 0,
                "has_metadata": False,
                "relevance_score": 0.0,
                "status": "ERROR",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def calculate_relevance(self, query: str, results) -> float:
        """Calcula score de relevância baseado na presença de termos-chave"""
        if not results or not results.get("documents") or not results["documents"][0]:
            return 0.0

        query_terms = query.lower().split()
        relevance_scores = []

        for doc in results["documents"][0]:
            doc_lower = doc.lower()
            matches = sum(1 for term in query_terms if term in doc_lower)
            score = matches / len(query_terms) if query_terms else 0
            relevance_scores.append(score)

        return (
            round(sum(relevance_scores) / len(relevance_scores), 3)
            if relevance_scores
            else 0.0
        )

    def test_basic_queries(self) -> List[Dict]:
        """Teste 1: Consultas básicas sobre medicina"""
        print("🔍 TESTE 1: Consultas Básicas sobre Medicina")

        basic_queries = [
            ("residência médica", "Consulta sobre residência médica"),
            ("especialização médica", "Consulta sobre especialização"),
            ("AMB", "Consulta sobre a própria AMB"),
            ("medicina geral", "Consulta sobre medicina geral"),
            ("congresso médico", "Consulta sobre eventos médicos"),
            ("formação médica", "Consulta sobre formação profissional"),
            ("saúde pública", "Consulta sobre saúde pública"),
            ("covid", "Consulta sobre pandemia COVID-19"),
            ("telemedicina", "Consulta sobre telemedicina"),
            ("ética médica", "Consulta sobre ética profissional"),
        ]

        results = []
        for query, test_name in basic_queries:
            result = self.run_query_test(query, 5, test_name)
            results.append(result)

            status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
            print(
                f"  {status_icon} {test_name}: {result['documents_found']} docs em {result['response_time_ms']}ms"
            )

        print(
            f"📊 Básicas concluídas: {len([r for r in results if r['status'] == 'SUCCESS'])}/{len(results)}"
        )
        return results

    def test_complex_queries(self) -> List[Dict]:
        """Teste 2: Consultas complexas e específicas"""
        print("\n🧠 TESTE 2: Consultas Complexas e Específicas")

        complex_queries = [
            (
                "Como funciona o processo de certificação de especialistas médicos no Brasil",
                "Certificação de especialistas",
            ),
            (
                "Quais são os principais desafios da residência médica no país",
                "Desafios da residência",
            ),
            (
                "AMB posicionamento sobre telemedicina e consultas online",
                "Posicionamento AMB telemedicina",
            ),
            (
                "Regulamentação e diretrizes para médicos durante pandemia COVID-19",
                "Regulamentação COVID-19",
            ),
            (
                "Formação médica continuada e atualização profissional",
                "Educação médica continuada",
            ),
            (
                "Defesa profissional e direitos dos médicos no Brasil",
                "Defesa profissional médica",
            ),
            (
                "Relacionamento entre AMB e sociedades de especialidades médicas",
                "AMB e sociedades",
            ),
            (
                "Combate ao exercício ilegal da medicina e fiscalização",
                "Combate exercício ilegal",
            ),
            (
                "Políticas de saúde e participação da AMB no governo federal",
                "Políticas de saúde AMB",
            ),
            (
                "Congressos médicos e eventos científicos organizados pela AMB",
                "Eventos científicos AMB",
            ),
        ]

        results = []
        for query, test_name in complex_queries:
            result = self.run_query_test(query, 3, test_name)
            results.append(result)

            status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
            relevance_icon = "🎯" if result["relevance_score"] > 0.5 else "⚡"
            print(
                f"  {status_icon} {relevance_icon} {test_name}: {result['documents_found']} docs, relevância {result['relevance_score']}"
            )

        print(
            f"📊 Complexas concluídas: {len([r for r in results if r['status'] == 'SUCCESS'])}/{len(results)}"
        )
        return results

    def test_temporal_queries(self) -> List[Dict]:
        """Teste 3: Consultas temporais e cronológicas"""
        print("\n📅 TESTE 3: Consultas Temporais e Cronológicas")

        temporal_queries = [
            ("notícias AMB 2025", "Notícias recentes 2025"),
            ("eventos médicos 2024", "Eventos 2024"),
            ("pandemia covid 2020 2021", "Período pandemia"),
            ("congresso medicina geral 2025", "CMG 2025"),
            ("mudanças residência médica últimos anos", "Mudanças recentes residência"),
            ("posicionamentos AMB 2023 2024", "Posicionamentos recentes"),
            ("telemedicina antes depois pandemia", "Evolução telemedicina"),
            ("formação médica mudanças temporais", "Evolução formação médica"),
            ("políticas saúde governo atual", "Políticas atuais"),
            ("novas diretrizes médicas recentes", "Diretrizes recentes"),
        ]

        results = []
        for query, test_name in temporal_queries:
            result = self.run_query_test(query, 4, test_name)
            results.append(result)

            status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
            print(
                f"  {status_icon} {test_name}: {result['documents_found']} docs em {result['response_time_ms']}ms"
            )

        print(
            f"📊 Temporais concluídas: {len([r for r in results if r['status'] == 'SUCCESS'])}/{len(results)}"
        )
        return results

    def test_edge_cases(self) -> List[Dict]:
        """Teste 4: Casos extremos e edge cases"""
        print("\n⚡ TESTE 4: Casos Extremos e Edge Cases")

        edge_queries = [
            ("xyz medicina quântica espacial", "Consulta sem resultados esperados"),
            ("", "Consulta vazia"),
            ("a", "Consulta muito curta"),
            (
                "Como a Associação Médica Brasileira estabelece políticas para a formação continuada de médicos especialistas no contexto das mudanças tecnológicas e demandas epidemiológicas contemporâneas incluindo telemedicina inteligência artificial diagnóstico digital",
                "Consulta extremamente longa",
            ),
            ("AMB AMB AMB AMB AMB", "Consulta repetitiva"),
            (
                "médico doutor medicina saúde hospital clínica paciente",
                "Consulta com muitas palavras-chave",
            ),
            ("123456789", "Consulta numérica"),
            ("!@#$%^&*()", "Consulta com símbolos"),
            ("COVID-19 SARS-CoV-2 pandemia coronavirus", "Termos técnicos específicos"),
            ("notícia mais recente AMB", "Consulta por recência"),
        ]

        results = []
        for query, test_name in edge_queries:
            result = self.run_query_test(query, 5, test_name)
            results.append(result)

            status_icon = (
                "✅"
                if result["status"] == "SUCCESS"
                else ("⚠️" if result["status"] == "NO_RESULTS" else "❌")
            )
            print(f"  {status_icon} {test_name}: {result['documents_found']} docs")

        print(f"📊 Edge cases concluídas: {len(results)} testes executados")
        return results

    def run_performance_benchmark(self) -> Dict:
        """Teste de benchmark de performance"""
        print("\n🚀 TESTE DE PERFORMANCE: Benchmark de Velocidade")

        benchmark_query = "residência médica AMB"
        num_iterations = 20

        response_times = []
        successful_queries = 0

        print(f"Executando {num_iterations} consultas idênticas...")

        for i in range(num_iterations):
            result = self.run_query_test(benchmark_query, 5, f"Benchmark {i+1}")
            response_times.append(result["response_time_ms"])
            if result["status"] == "SUCCESS":
                successful_queries += 1

            if (i + 1) % 5 == 0:
                print(f"  ⏱️ Progresso: {i+1}/{num_iterations} consultas")

        # Calcular estatísticas
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        success_rate = (successful_queries / num_iterations) * 100

        benchmark_result = {
            "test_name": "Performance Benchmark",
            "total_queries": num_iterations,
            "successful_queries": successful_queries,
            "success_rate_percent": round(success_rate, 2),
            "avg_response_time_ms": round(avg_time, 2),
            "min_response_time_ms": round(min_time, 2),
            "max_response_time_ms": round(max_time, 2),
            "queries_per_second": round(1000 / avg_time, 2) if avg_time > 0 else 0,
        }

        print(f"📊 Benchmark concluído:")
        print(f"  ✅ Taxa de sucesso: {success_rate}%")
        print(f"  ⏱️ Tempo médio: {avg_time:.2f}ms")
        print(f"  🚀 Consultas por segundo: {benchmark_result['queries_per_second']}")

        return benchmark_result

    def generate_report(self, all_results: List[Dict], benchmark: Dict) -> str:
        """Gera relatório completo dos testes"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"relatorio_teste_rag_{timestamp}.json"

        # Calcular estatísticas gerais
        total_tests = len(all_results)
        successful_tests = len([r for r in all_results if r["status"] == "SUCCESS"])
        avg_response_time = (
            sum(r["response_time_ms"] for r in all_results) / total_tests
            if total_tests > 0
            else 0
        )
        avg_relevance = (
            sum(r["relevance_score"] for r in all_results) / total_tests
            if total_tests > 0
            else 0
        )

        report = {
            "test_summary": {
                "execution_date": datetime.now().isoformat(),
                "total_documents_in_kb": self.total_docs,
                "total_tests_executed": total_tests,
                "successful_tests": successful_tests,
                "success_rate_percent": (
                    round((successful_tests / total_tests) * 100, 2)
                    if total_tests > 0
                    else 0
                ),
                "average_response_time_ms": round(avg_response_time, 2),
                "average_relevance_score": round(avg_relevance, 3),
            },
            "performance_benchmark": benchmark,
            "detailed_test_results": all_results,
            "test_categories": {
                "basic_queries": len(
                    [r for r in all_results if "Consulta" in r.get("test_name", "")]
                ),
                "complex_queries": len(
                    [
                        r
                        for r in all_results
                        if any(
                            x in r.get("test_name", "")
                            for x in ["Certificação", "Desafios", "Posicionamento"]
                        )
                    ]
                ),
                "temporal_queries": len(
                    [
                        r
                        for r in all_results
                        if any(
                            x in r.get("test_name", "")
                            for x in ["2025", "2024", "recentes"]
                        )
                    ]
                ),
                "edge_cases": len(
                    [
                        r
                        for r in all_results
                        if any(
                            x in r.get("test_name", "")
                            for x in ["sem resultados", "vazia", "longa", "repetitiva"]
                        )
                    ]
                ),
            },
        }

        # Salvar relatório
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return filename

    def run_full_stress_test(self):
        """Executa o protocolo completo de teste de estresse"""
        print("🎯 INICIANDO PROTOCOLO DE TESTE DE ESTRESSE DO RAG")
        print("📅 Data/Hora:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("=" * 80)

        start_time = time.time()

        # Executar todas as baterias de teste
        basic_results = self.test_basic_queries()
        complex_results = self.test_complex_queries()
        temporal_results = self.test_temporal_queries()
        edge_results = self.test_edge_cases()

        # Executar benchmark de performance
        benchmark_result = self.run_performance_benchmark()

        # Consolidar todos os resultados
        all_results = basic_results + complex_results + temporal_results + edge_results

        total_time = time.time() - start_time

        # Gerar relatório
        report_file = self.generate_report(all_results, benchmark_result)

        # Exibir sumário final
        print("\n" + "=" * 80)
        print("🎉 TESTE DE ESTRESSE RAG CONCLUÍDO")
        print("=" * 80)
        print(f"⏱️ Tempo total de execução: {total_time:.2f} segundos")
        print(f"📊 Total de testes: {len(all_results)}")
        print(
            f"✅ Testes bem-sucedidos: {len([r for r in all_results if r['status'] == 'SUCCESS'])}"
        )
        print(
            f"📈 Taxa de sucesso geral: {((len([r for r in all_results if r['status'] == 'SUCCESS']) / len(all_results)) * 100):.1f}%"
        )
        print(
            f"⚡ Tempo médio de resposta: {sum(r['response_time_ms'] for r in all_results) / len(all_results):.2f}ms"
        )
        print(f"📄 Relatório salvo em: {report_file}")
        print("=" * 80)

        return report_file


if __name__ == "__main__":
    tester = RAGStressTester()
    report_file = tester.run_full_stress_test()
    print(f"\n🎯 Para análise detalhada, consulte o arquivo: {report_file}")
