# src/aurora_platform/services/rag_service.py

from aurora_platform.intelligence.vector_store import VectorStore

from .adapter_factory import AdapterFactory
from .knowledge_service import KnowledgeService

# --- MUDANÇA CRÍTICA: Importa a interface e a fábrica ---
from .llm_adapters.base import BaseLLMAdapter


def answer_query(query: str, model_provider: str) -> str:
    """
    Responde a uma pergunta usando a cadeia RAG com um adaptador de LLM dinâmico.
    """
    print(f"INFO: RAG Service iniciado para o provedor: {model_provider}")

    # 1. Obter o adaptador correto usando a fábrica
    try:
        adapter: BaseLLMAdapter = AdapterFactory.get_adapter(model_provider)
    except ValueError as e:
        return str(e)

    # 2. Recuperar o contexto
    vector_store = VectorStore(path="./aurora_knowledge_base/chroma.sqlite3")
    kb_service = KnowledgeService(vector_store)
    retrieved_docs = kb_service.retrieve(query, top_k=2)

    if not retrieved_docs:
        return "Não encontrei informação relevante na minha base de conhecimento para responder a esta pergunta."

    context = "\n\n---\n\n".join([doc.get("text", "") for doc in retrieved_docs])

    # 3. Montar o prompt (lógica inalterada)
    template = """
    Você é um assistente especialista e conciso. Sua tarefa é responder à pergunta do usuário.
    Você DEVE usar APENAS as informações do CONTEXTO fornecido abaixo para formular sua resposta.
    NÃO invente informações nem use conhecimento externo.
    Sintetize a informação em uma resposta clara e direta.

    ---
    CONTEXTO:
    {context}
    ---
    PERGUNTA:
    {query}
    ---
    RESPOSTA SINTETIZADA E CONCISA:
    """
    # Usamos uma substituição de string simples para o prompt final
    final_prompt = template.format(context=context, query=query)

    # 4. Gerar a resposta usando o método padronizado do adaptador
    print("INFO: Invocando o adaptador do LLM para síntese...")
    response = adapter.generate(final_prompt)

    print("INFO: Resposta sintetizada recebida do adaptador.")
    return response
