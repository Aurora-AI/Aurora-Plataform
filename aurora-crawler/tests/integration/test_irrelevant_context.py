#!/usr/bin/env python3
import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from aurora_platform.services.knowledge_query_service import KnowledgeQueryService


def test_irrelevant_context():
    # Simular o cenário original com contexto irrelevante
    irrelevant_context = """
    Ir para o conteúdo
    REDELOG
    Sobre a Redelog
    Quem Somos
    Informes
    Compras Centralizadas
    Logística em Dados
    Biblioteca
    Sobre a Sublog
    Cadernos Logísticos
    Panorama das Contratações Públicas
    Audiências e Consultas Públicas
    Relatório Redes
    BASE DE CONHECIMENTO
    Fase de Planejamento
    Fase Preparatória
    Fase Externa
    Gestão Contratual
    Gestão de Bens Serviços
    """

    # Criar instância do serviço
    from aurora_platform.services.knowledge_service import KnowledgeBaseService

    kb_service = KnowledgeBaseService()
    query_service = KnowledgeQueryService(kb_service)

    # Testar com contexto irrelevante
    question = "Qual é o melhor modelo para trabalhos focados em RAG"

    print(f"Pergunta: {question}")
    print("=" * 50)
    print("Contexto fornecido: REDELOG (irrelevante)")
    print("=" * 50)

    # Aplicar template diretamente
    result = query_service._apply_cot_template(irrelevant_context, question)

    print(f"Resposta: {result['final_answer']}")
    print(f"\nCadeia de Pensamento:\n{result['reasoning']}")

    # Testar com contexto relevante
    print("\n" + "=" * 70)
    print("TESTE COM CONTEXTO RELEVANTE:")
    print("=" * 70)

    relevant_context = """
    Gemini API | Google AI for Developers
    Modelos Gemini para embedding e RAG
    O modelo Gemini 2.5 Flash oferece capacidades avançadas
    para retrieval-augmented generation
    """

    result2 = query_service._apply_cot_template(relevant_context, question)

    print(f"Resposta: {result2['final_answer']}")
    print(f"\nCadeia de Pensamento:\n{result2['reasoning']}")


if __name__ == "__main__":
    test_irrelevant_context()
