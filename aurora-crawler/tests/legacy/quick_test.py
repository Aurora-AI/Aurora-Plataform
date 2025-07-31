"""Teste rápido sem dependências externas"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_imports():
    """Testa se todas as importações funcionam"""
    from aurora_platform.services.knowledge_service import KnowledgeBaseService
    from aurora_platform.services.semantic_analysis_service import (
        SemanticAnalysisService,
    )
    from aurora_platform.services.scraper_service import DeepDiveScraperServiceV2

    assert KnowledgeBaseService is not None
    assert SemanticAnalysisService is not None
    assert DeepDiveScraperServiceV2 is not None


def test_knowledge_service():
    """Testa KnowledgeBaseService básico"""
    from aurora_platform.services.knowledge_service import KnowledgeBaseService

    kb = KnowledgeBaseService()
    kb.add_document(
        "test_doc",
        "Este e um documento de teste",
        {"source": "test"},
        collection_name="test_collection",
    )
    # Teste de persistência: consulta direta ao banco após inserção
    persisted = kb.get_collection("test_collection")
    persisted = persisted.get(ids=["test_doc"]) if persisted is not None else None
    assert persisted is not None
    docs = persisted.get("documents", []) if persisted is not None else []
    if docs is None:
        docs = []
    assert len(docs) == 1
    # Teste de busca automatizada
    results = kb.query_collection(
        query="documento teste", collection_name="test_collection", n_results=1
    )
    assert results is not None


if __name__ == "__main__":
    print("TESTE RAPIDO - Aurora Platform\n")

    print("1. Testando importacoes...")
    imports_ok = test_imports()

    print("\n2. Testando KnowledgeBaseService...")
    kb_ok = test_knowledge_service()

    print(f"\nResultados:")
    print(f"Importacoes: {'OK' if imports_ok else 'FALHOU'}")
    print(f"KnowledgeBase: {'OK' if kb_ok else 'FALHOU'}")

    if imports_ok and kb_ok:
        print("\nSistema basico funcionando! Pode executar: python run.py")
    else:
        print("\nCorrija os erros antes de prosseguir")
