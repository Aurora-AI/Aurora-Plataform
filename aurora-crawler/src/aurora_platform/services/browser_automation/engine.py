import logging
from typing import Optional
from playwright.async_api import async_playwright
from .consent_manager import ConsentManager
from .local_llm_service import LocalLLMService

logger = logging.getLogger(__name__)


class BrowserEngine:
    """
    Motor de automação de navegador para navegação segura e extração de conteúdo.
    """

    def __init__(
        self, db_session, user_id, llm_service: Optional[LocalLLMService] = None
    ):
        self.llm_service = llm_service or LocalLLMService()
        self.consent_manager = ConsentManager(db_session, user_id)

    async def fetch_and_summarize(self, url: str) -> dict:
        """
        Navega até a URL, lida com consentimento e sumariza o conteúdo principal.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                logger.info(f"Acessando: {url}")
                await page.goto(url, timeout=30000)
                await self.consent_manager.handle_consent(page)
                content = await page.content()
                text = await page.evaluate(
                    """() => {
                    // Remove scripts e estilos
                    document.querySelectorAll('script, style').forEach(e => e.remove());
                    return document.body.innerText;
                }"""
                )
                summary = self.llm_service.summarize(text)
                return {
                    "url": url,
                    "summary": summary,
                    "raw_text": text[
                        :10000
                    ],  # Limite opcional para evitar payloads grandes
                }
            finally:
                await browser.close()
