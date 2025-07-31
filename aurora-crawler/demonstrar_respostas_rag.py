#!/usr/bin/env python3
"""
Script para demonstrar as respostas do sistema RAG
Executa consultas e mostra as respostas completas retornadas
"""
import chromadb
from datetime import datetime


class RAGResponseDemo:
    def __init__(self, collection_name: str = "amb_noticias"):
        """Inicializa o demonstrador de respostas RAG"""
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_collection(name=collection_name)
        self.total_docs = self.collection.count()

        print(f"🎯 Demonstração de Respostas do Sistema RAG")
        print(f"📚 Base de conhecimento: {collection_name}")
        print(f"📊 Total de documentos: {self.total_docs}")
        print("=" * 80)

    def query_and_show_response(
        self, query: str, n_results: int = 3, show_full_text: bool = False
    ):
        """Executa uma consulta e mostra a resposta completa"""
        print(f'\n🔍 CONSULTA: "{query}"')
        print("-" * 60)

        try:
            results = self.collection.query(query_texts=[query], n_results=n_results)

            if (
                results
                and hasattr(results, "get")
                and results.get("documents")
                and results["documents"]
                and results["documents"][0]
            ):
                docs = results["documents"][0]

                # Extrair metadados com segurança
                metadatas = []
                if (
                    hasattr(results, "get")
                    and results.get("metadatas")
                    and results["metadatas"]
                    and results["metadatas"][0]
                ):
                    metadatas = results["metadatas"][0]
                else:
                    metadatas = [{}] * len(docs)

                # Extrair distâncias com segurança
                distances = []
                if (
                    hasattr(results, "get")
                    and results.get("distances")
                    and results["distances"]
                    and results["distances"][0]
                ):
                    distances = results["distances"][0]
                else:
                    distances = [0.0] * len(docs)

                print(f"📊 Documentos encontrados: {len(docs)}")
                print(f"⏱️ Consulta executada em: {datetime.now().strftime('%H:%M:%S')}")

                for i, doc in enumerate(docs):
                    metadata = metadatas[i] if i < len(metadatas) else {}
                    distance = distances[i] if i < len(distances) else 0

                    print(f"\n📄 RESULTADO {i+1}:")
                    print(f"   📋 Título: {metadata.get('title', 'N/A')}")
                    print(f"   📅 Data: {metadata.get('publication_date', 'N/A')}")
                    print(f"   🔗 Link: {metadata.get('link', 'N/A')}")
                    print(f"   📏 Distância semântica: {distance:.4f}")
                    print(f"   📝 Conteúdo:")

                    if show_full_text:
                        print(f"   {doc}")
                    else:
                        # Mostrar primeiros 400 caracteres
                        preview = doc[:400] + "..." if len(doc) > 400 else doc
                        print(f"   {preview}")
            else:
                print("❌ Nenhum resultado encontrado")

        except Exception as e:
            print(f"❌ Erro ao executar consulta: {e}")

    def demonstrate_responses(self):
        """Demonstra respostas para diferentes tipos de consultas"""

        # 1. Consulta básica
        print("\n" + "=" * 80)
        print("1️⃣ CONSULTA BÁSICA - MEDICINA GERAL")
        print("=" * 80)
        self.query_and_show_response("residência médica", 2)

        # 2. Consulta complexa
        print("\n" + "=" * 80)
        print("2️⃣ CONSULTA COMPLEXA - PROCESSO ESPECÍFICO")
        print("=" * 80)
        self.query_and_show_response(
            "Como funciona o processo de certificação de especialistas médicos no Brasil",
            2,
        )

        # 3. Consulta temporal
        print("\n" + "=" * 80)
        print("3️⃣ CONSULTA TEMPORAL - EVENTOS RECENTES")
        print("=" * 80)
        self.query_and_show_response("congresso medicina geral 2025", 2)

        # 4. Consulta sobre COVID-19
        print("\n" + "=" * 80)
        print("4️⃣ CONSULTA TEMÁTICA - PANDEMIA COVID-19")
        print("=" * 80)
        self.query_and_show_response("covid pandemia AMB orientações médicos", 2)

        # 5. Consulta sobre telemedicina
        print("\n" + "=" * 80)
        print("5️⃣ CONSULTA ESPECÍFICA - TELEMEDICINA")
        print("=" * 80)
        self.query_and_show_response(
            "telemedicina consultas online AMB posicionamento", 2
        )

        # 6. Consulta sobre formação médica
        print("\n" + "=" * 80)
        print("6️⃣ CONSULTA EDUCACIONAL - FORMAÇÃO MÉDICA")
        print("=" * 80)
        self.query_and_show_response(
            "formação médica qualidade ensino AMB preocupações", 2
        )

    def show_full_response_example(self):
        """Mostra um exemplo completo de resposta sem truncar"""
        print("\n" + "=" * 80)
        print("🔍 EXEMPLO DE RESPOSTA COMPLETA - SEM TRUNCAMENTO")
        print("=" * 80)
        self.query_and_show_response(
            "AMB defesa profissional médicos", 1, show_full_text=True
        )


if __name__ == "__main__":
    demo = RAGResponseDemo()

    print("\n🎯 Vamos ver as respostas reais do sistema RAG!")
    print("Pressione Enter para continuar ou Ctrl+C para sair...")
    input()

    demo.demonstrate_responses()

    print("\n" + "=" * 80)
    print("💡 RESPOSTA COMPLETA DE EXEMPLO")
    print("=" * 80)
    print("Quer ver uma resposta completa sem truncamento? (s/n)")
    choice = input().lower()

    if choice == "s":
        demo.show_full_response_example()

    print("\n🎉 Demonstração concluída!")
    print("Estas são as respostas reais que o sistema RAG retorna para as consultas.")
