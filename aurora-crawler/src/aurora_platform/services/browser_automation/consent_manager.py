import logging
from playwright.async_api import Page
from sqlmodel import Session, select
from src.aurora_platform.models.consent_model import Consent

logger = logging.getLogger(__name__)


class ConsentManager:
    """
    Gerencia pop-ups de consentimento (cookies, LGPD, etc) em páginas web.
    """

    def __init__(self, db_session: Session, user_id: str):
        self.db = db_session
        self.user_id = user_id
        # Pode ser expandido para suportar múltiplos padrões de consentimento
        self.selectors = [
            "button:has-text('Aceitar')",
            "button:has-text('Accept')",
            "button:has-text('Concordo')",
            "button:has-text('OK')",
            "button:has-text('Continuar')",
        ]

    def _get_consent_from_db(self, action_key: str) -> Consent | None:
        statement = select(Consent).where(
            Consent.user_id == self.user_id, Consent.action == action_key
        )
        return self.db.exec(statement).first()

    def request_consent(self, action: str, target: str) -> bool:
        print(f"\n🔒 SOLICITAÇÃO DE CONSENTIMENTO")
        print(f"Ação: {action.upper()} em {target}")
        response = input("Permitir? (s/n): ").strip().lower()

        action_key = f"{action}::{target}"
        consent_record = self._get_consent_from_db(action_key)

        if response == "s":
            if consent_record:
                consent_record.is_granted = True
            else:
                consent_record = Consent(
                    user_id=self.user_id, action=action_key, is_granted=True
                )

            self.db.add(consent_record)
            self.db.commit()
            self.db.refresh(consent_record)
            return True
        return False

    def has_consent(self, action: str, target: str) -> bool:
        action_key = f"{action}::{target}"
        consent_record = self._get_consent_from_db(action_key)
        return bool(consent_record.is_granted) if consent_record else False

    async def handle_consent(self, page: Page):
        """
        Tenta clicar em botões de consentimento conhecidos.
        """
        for selector in self.selectors:
            try:
                btn = await page.query_selector(selector)
                if btn:
                    await btn.click()
                    logger.info(f"Consentimento aceito com seletor: {selector}")
                    break
            except Exception as e:
                logger.debug(f"Erro ao tentar clicar no consentimento: {e}")
