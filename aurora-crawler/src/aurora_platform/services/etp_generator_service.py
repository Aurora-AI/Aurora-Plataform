import logging
from typing import List, Dict
from .rag_service import answer_query

logger = logging.getLogger(__name__)


class ETPGeneratorService:
    def __init__(self):
        # Define a estrutura do ETP com as seções do modelo
        self.etp_sections = [
            "1. Descrição da necessidade da contratação",
            "2. Descrição dos requisitos da contratação",
            "3. Levantamento de mercado",
            "4. Descrição da solução como um todo",
            "5. Estimativa do valor da contratação",
            "6. Justificativa para o parcelamento ou não da solução",
            "7. Contratações correlatas e/ou interdependentes",
            "8. Declaração da viabilidade da contratação",
        ]
        logger.info("ETPGeneratorService inicializado.")

    def _generate_query_for_section(self, section: str, topic: str) -> str:
        """Gera uma pergunta específica para o RAG Service a partir de uma seção do ETP."""
        # Mapeia a seção para uma pergunta mais elaborada
        query_map = {
            "1. Descrição da necessidade da contratação": f"Descreva a necessidade de contratação de uma solução de software relacionada a '{topic}', focando no problema a ser resolvido.",
            "3. Levantamento de mercado": f"Faça um levantamento de mercado para soluções de '{topic}', identificando possíveis fornecedores e tecnologias existentes.",
            "4. Descrição da solução como um todo": f"Descreva, em termos técnicos, como seria uma solução de software para '{topic}'.",
        }
        # Usa um prompt genérico para seções não mapeadas
        return query_map.get(
            section, f"Discorra sobre '{section}' no contexto de '{topic}'."
        )

    def generate_etp(self, topic: str) -> str:
        """
        Orquestra a geração de um ETP completo, consultando o RAG para cada seção.
        """
        logger.info(f"Iniciando a geração do ETP para o tópico: '{topic}'")
        etp_document_parts = [f"# Estudo Técnico Preliminar (ETP): {topic}\n"]

        for section_title in self.etp_sections:
            logger.info(f"Processando seção: '{section_title}'")

            # Gera a pergunta e consulta o RAG
            query = self._generate_query_for_section(section_title, topic)
            # O RAG Service já foi refatorado para usar o melhor LLM (ex: gemini-1.5-pro)
            answer = answer_query(query=query)

            # Adiciona a seção e a resposta ao documento
            etp_document_parts.append(f"## {section_title}\n\n{answer}\n")

        logger.info("Geração do ETP concluída.")
        return "\n".join(etp_document_parts)
