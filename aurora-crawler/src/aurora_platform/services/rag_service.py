import logging
from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.config import settings
from aurora_platform.services.azure_openai_adapter import AzureOpenAIAdapter

logger = logging.getLogger(__name__)

COT_PROMPT_TEMPLATE = """
Você é um assistente especialista e sua tarefa é responder à pergunta do usuário de forma fundamentada. Siga estritamente os seguintes passos:

1.  **Análise do Contexto:** Analise os fatos-chave do CONTEXTO fornecido abaixo que são relevantes para a PERGUNTA.
2.  **Cadeia de Pensamento:** Construa uma cadeia de pensamento passo a passo, em português, que conecte logicamente os fatos relevantes para formular uma resposta.
3.  **Resposta Final:** Com base na sua cadeia de pensamento, forneça uma resposta final, concisa e precisa.

NÃO use conhecimento externo. Sua resposta deve ser 100% baseada no contexto.

---
CONTEXTO:
{context}
---
PERGUNTA:
{question}
---
SAÍDA ESTRUTURADA:
**Cadeia de Pensamento:**
- [Passo 1 do seu raciocínio]
- ...

**Resposta Final:**
[Sua resposta sintetizada aqui]
"""


def process_results(results: list[dict]) -> tuple[list[str], list[str]]:
    """Processa resultados da busca extraindo conteúdos e IDs"""
    contents = []
    doc_ids = []
    for doc in results or []:
        contents.append(doc.get("content", ""))
        doc_ids.append(doc.get("id", ""))
    return contents, doc_ids


def answer_query(query: str) -> dict:
    """
    Executa o pipeline RAG: busca contexto no ChromaDB via KnowledgeBaseService, gera resposta via AzureOpenAIAdapter (gpt-4o), retorna resposta estruturada.
    """
    try:
        # 1. Recupera contexto relevante
        kb_service = KnowledgeBaseService()
        results = kb_service.retrieve(
            query=query, collection_name="default_knowledge_base", n_results=2
        )
        contents, doc_ids = process_results(results)
        source_documents = [
            {"source": doc_id, "content": content}
            for doc_id, content in zip(doc_ids, contents)
        ]
        context = "\n".join(contents)
        # 2. Monta o prompt
        prompt = COT_PROMPT_TEMPLATE.format(context=context, question=query)
        # 3. Chama o LLM via AzureOpenAIAdapter
        llm = AzureOpenAIAdapter(
            endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            deployment_name="aurora-flagship-reasoning",
        )
        # 4. Gera resposta
        response = llm.complete(prompt)
        # Se response for dict, retorna normalmente
        if isinstance(response, dict):
            return {
                "question": query,
                "answer": response.get("final_answer", ""),
                "chain_of_thought": response.get("reasoning", ""),
                "sources": len(contents),
                "context_used": (
                    context[:500] + "..." if len(context) > 500 else context
                ),
            }
        # Se response for string, faz parsing simples
        chain_of_thought = ""
        final_answer = ""
        if isinstance(response, str):
            cot_split = response.split("**Resposta Final:**")
            if len(cot_split) == 2:
                chain_of_thought = (
                    cot_split[0].replace("**Cadeia de Pensamento:**", "").strip()
                )
                final_answer = cot_split[1].strip()
            else:
                final_answer = response.strip()
        return {
            "question": query,
            "answer": final_answer,
            "chain_of_thought": chain_of_thought,
            "sources": len(contents),
            "context_used": context[:500] + "..." if len(context) > 500 else context,
        }
    except Exception as e:
        logger.error(f"Erro no answer_query: {e}")
        return {
            "question": query,
            "answer": "Erro interno ao processar a consulta.",
            "chain_of_thought": "Não foi possível construir uma cadeia de pensamento devido a erro interno.",
            "sources": 0,
            "context_used": "",
        }
        response = llm.complete(prompt)
        # 4. Extrai cadeia de pensamento e resposta final
        chain_of_thought = ""
        final_answer = ""
        if response:
            # Simples parsing baseado no template
            cot_split = response.split("**Resposta Final:**")
            if len(cot_split) == 2:
                chain_of_thought = (
                    cot_split[0].replace("**Cadeia de Pensamento:**", "").strip()
                )
                final_answer = cot_split[1].strip()
            else:
                final_answer = response.strip()
        return {
            "final_answer": final_answer,
            "chain_of_thought": chain_of_thought,
            "source_documents": source_documents,
        }
