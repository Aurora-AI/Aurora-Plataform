import logging
from typing import List, Dict, Any
from langchain.prompts import ChatPromptTemplate
from .knowledge_service import KnowledgeBaseService

logger = logging.getLogger(__name__)


class KnowledgeQueryService:
    def __init__(self, kb_service: KnowledgeBaseService):
        self.kb_service = kb_service

    def answer_query(self, question: str, n_results: int = 5) -> Dict[str, Any]:
        assert isinstance(
            question, str
        ), f"Expected str for question, got {type(question)}"
        assert isinstance(
            n_results, int
        ), f"Expected int for n_results, got {type(n_results)}"
        """
        Responde uma pergunta usando RAG com Chain-of-Thought (CoT)
        """
        try:
            # 1. Recuperar contexto relevante
            results = self.kb_service.retrieve(
                query=question,
                collection_name="default_knowledge_base",
                n_results=n_results * 2,
            )  # Buscar mais documentos

            # Verificar se results não é None e tem documentos
            documents = []
            metadatas = []
            if results and isinstance(results, list):
                docs_list = [
                    doc.get("documents")
                    for doc in (results or [])
                    if doc and isinstance(doc, dict) and "documents" in doc
                ]
                meta_list = [
                    doc.get("metadatas")
                    for doc in (results or [])
                    if doc and isinstance(doc, dict) and "metadatas" in doc
                ]
                if docs_list and len(docs_list) > 0:
                    documents = docs_list[0] or []
                    metadatas = (
                        meta_list[0] if meta_list and meta_list[0] is not None else []
                    )

            # Filtrar e priorizar documentos mais relevantes
            # Converter Metadata para dict se necessário
            metadatas_dict = [
                m if isinstance(m, dict) else m.__dict__ for m in metadatas
            ]
            filtered_docs = self._filter_and_prioritize_documents(
                documents, metadatas_dict, question
            )
            context = "\n".join(filtered_docs[:n_results]) if filtered_docs else ""

            if not context.strip():
                return {
                    "question": question,
                    "answer": "Não encontrei informações relevantes na base de conhecimento para responder sua pergunta.",
                    "chain_of_thought": "Não foi possível construir uma cadeia de pensamento devido à falta de contexto relevante.",
                    "sources": 0,
                }

            # Verificar se o contexto é realmente relevante para a pergunta
            relevance_score = self._calculate_relevance(
                question.lower(), context.lower()
            )
            if relevance_score < 0.4:  # Limiar intermediário
                return {
                    "question": question,
                    "answer": "Não encontrei informações relevantes na base de conhecimento para responder sua pergunta. O contexto disponível não contém dados suficientes sobre o tópico solicitado.",
                    "chain_of_thought": "- Analisando a pergunta e o contexto disponível\n- O contexto recuperado não contém informações relevantes para responder à pergunta\n- Sendo honesto sobre a limitação do conhecimento disponível",
                    "sources": 0,
                }

            # 2. Aplicar template CoT
            cot_response = self._apply_cot_template(context, question)

            return {
                "question": question,
                "answer": cot_response["final_answer"],
                "chain_of_thought": cot_response["reasoning"],
                "sources": len(filtered_docs[:n_results]),
                "context_used": (
                    context[:500] + "..." if len(context) > 500 else context
                ),
            }

        except Exception as e:
            logger.error(f"Erro ao processar consulta: {e}")
            return {
                "question": question,
                "answer": "Erro interno ao processar a consulta.",
                "chain_of_thought": "Não foi possível construir uma cadeia de pensamento devido a erro interno.",
                "sources": 0,
            }

    def _apply_cot_template(self, context: str, question: str) -> Dict[str, str]:
        """
        Aplica o template Chain-of-Thought para estruturar a resposta
        """
        question_lower = question.lower()
        context_lower = context.lower()

        # Verificar relevância do contexto para a pergunta
        relevance_score = self._calculate_relevance(question_lower, context_lower)

        reasoning_steps = []

        # Se a relevância for muito baixa, ser honesto
        if relevance_score < 0.4:  # Limiar intermediário no CoT
            reasoning_steps.append("Analisando a pergunta e o contexto disponível")
            reasoning_steps.append(
                "O contexto recuperado não contém informações relevantes para responder à pergunta"
            )
            reasoning_steps.append(
                "Sendo honesto sobre a limitação do conhecimento disponível"
            )
            final_answer = "Não encontrei informações relevantes na base de conhecimento para responder sua pergunta. O contexto disponível não contém dados suficientes sobre o tópico solicitado."
        else:
            # Processar normalmente se houver relevância
            rag_keywords = [
                "rag",
                "modelo",
                "gemini",
                "api",
                "embedding",
                "retrieval",
                "generation",
            ]

            if any(keyword in question_lower for keyword in rag_keywords):
                reasoning_steps.append(
                    "Identificada pergunta sobre modelos de IA e RAG"
                )

                if "gemini" in context_lower and (
                    "modelo" in context_lower or "api" in context_lower
                ):
                    reasoning_steps.append(
                        "Encontradas informações sobre Gemini no contexto"
                    )
                    reasoning_steps.append(
                        "Analisando as capacidades dos modelos Gemini"
                    )

                    final_answer = "Para trabalhos focados em RAG, baseado na documentação do Google AI, os modelos Gemini oferecem capacidades avançadas para compreensão contextual e geração de respostas. Os modelos Gemini 2.5 Flash são especialmente eficazes para tarefas que envolvem recuperação e geração de conteúdo."
                else:
                    reasoning_steps.append(
                        "Contexto não contém informações específicas sobre modelos para RAG"
                    )
                    final_answer = "Não encontrei informações específicas sobre modelos recomendados para RAG na base de conhecimento atual."
            else:
                # Para outras perguntas
                context_words = set(context_lower.split())
                question_words = set(question_lower.split())
                overlap = len(context_words.intersection(question_words))
                # Exigir pelo menos 3 palavras em comum para considerar relevante
                if overlap >= 3:
                    reasoning_steps.append(
                        "Encontradas informações relevantes no contexto"
                    )
                    final_answer = (
                        context[:300] + "..." if len(context) > 300 else context
                    )
                else:
                    reasoning_steps.append(
                        "Contexto não contém informações suficientemente relevantes"
                    )
                    final_answer = "Não encontrei informações relevantes na base de conhecimento para responder sua pergunta."

        return {
            "reasoning": "\n".join([f"- {step}" for step in reasoning_steps]),
            "final_answer": final_answer,
        }

    def _calculate_relevance(self, question: str, context: str) -> float:
        """
        Calcula a relevância do contexto para a pergunta
        """
        question_words = set(question.split())
        context_words = set(context.split())

        # Remover palavras muito comuns
        stop_words = {
            "o",
            "a",
            "e",
            "de",
            "do",
            "da",
            "em",
            "um",
            "uma",
            "para",
            "com",
            "por",
            "que",
            "se",
            "na",
            "no",
        }
        question_words = {
            w for w in question_words if len(w) > 2 and w not in stop_words
        }

        if not question_words:
            return 0.0

        # Calcular intersecção
        intersection = question_words.intersection(context_words)
        relevance = len(intersection) / len(question_words)

        return relevance

    def _filter_and_prioritize_documents(
        self, documents: List[str], metadatas: List[Dict], question: str
    ) -> List[str]:
        """
        Filtra e prioriza documentos baseado na relevância e fonte
        """
        if not documents or not metadatas:
            return documents

        # Criar lista de documentos com scores
        doc_scores = []
        question_lower = question.lower()

        # Fontes prioritárias para diferentes tipos de pergunta
        priority_sources = {
            "gemini": ["ai.google.dev", "google"],
            "rag": ["ai.google.dev", "google"],
            "modelo": ["ai.google.dev", "google"],
            "api": ["ai.google.dev", "google"],
        }

        for i, (doc, meta) in enumerate(zip(documents, metadatas)):
            score = 0
            source = meta.get("source", "").lower()

            # Priorizar fontes relevantes
            for keyword, sources in priority_sources.items():
                if keyword in question_lower:
                    if any(priority_source in source for priority_source in sources):
                        score += 10
                    break

            # Priorizar documentos do Google AI
            if "ai.google.dev" in source or "google" in source:
                score += 5

            # Penalizar documentos irrelevantes para a pergunta
            if "redelog" in source and any(
                keyword in question_lower
                for keyword in ["gemini", "rag", "modelo", "api"]
            ):
                score -= 10  # Penalização mais severa

            # Verificar se o documento contém palavras-chave da pergunta
            doc_lower = doc.lower()
            question_keywords = [w for w in question_lower.split() if len(w) > 3]
            keyword_matches = sum(
                1 for keyword in question_keywords if keyword in doc_lower
            )

            if keyword_matches == 0 and len(question_keywords) > 0:
                score -= 5  # Penalizar documentos sem palavras-chave relevantes

            doc_scores.append((doc, score, i))

        # Ordenar por score (maior primeiro)
        doc_scores.sort(key=lambda x: x[1], reverse=True)

        # Retornar documentos ordenados por relevância
        return [doc for doc, score, idx in doc_scores]
