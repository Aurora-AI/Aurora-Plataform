from apscheduler.schedulers.background import BackgroundScheduler
from typing import Sequence, Dict, Any


class ChangeMonitorService:
    def __init__(self, scraper, kb):
        self.scraper = scraper
        self.kb = kb
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def add_monitoring_task(
        self, url: str, css_selector: str, interval: int, collection: str
    ):
        def check_changes():
            current_content = self.scraper.scrape_content(url, css_selector)
            if self._content_changed(url, current_content):
                self.kb.add_documents([{"content": current_content}], collection)

        self.scheduler.add_job(check_changes, "interval", minutes=interval)

    def _content_changed(self, url: str, current: str) -> bool:
        # Implementar lógica de comparação com histórico
        # Exemplo: sempre retorna True para fins de teste
        return True
