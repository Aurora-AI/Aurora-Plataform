import os
import tempfile
import aiohttp
import aiofiles
from typing import List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Tag
import PyPDF2
import logging
from aurora_platform.config import settings

logger = logging.getLogger(__name__)


class DeepDiveScraperServiceV2:
    async def fetch_page(self, url: str) -> str:
        """Mock/fake fetch_page for testing purposes."""
        # Em produção, implementar scraping real
        return f"<html><body><p>Conteúdo de teste para {url}</p></body></html>"

    async def deep_dive_scrape(self, url: str):
        """Mock/fake deep_dive_scrape for testing purposes."""
        html = await self.fetch_page(url)
        # Em produção, implementar parsing real
        # Simula chamada ao KnowledgeBaseService
        # Exemplo: self.kb_service.add_document(...)
        return html

    def __init__(self):
        self.temp_dir = tempfile.gettempdir()

    async def download_pdfs_from_url(self, url: str) -> List[str]:
        """Download PDFs from URL and extract text content"""
        try:
            timeout = aiohttp.ClientTimeout(total=settings.DOWNLOAD_TIMEOUT)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Check if URL is direct PDF
                if url.lower().endswith(".pdf"):
                    return await self._download_direct_pdf(session, url)

                # Scrape webpage for PDF links
                pdf_urls = await self._find_pdf_links(session, url)
                if not pdf_urls:
                    raise ValueError("No PDF links found on the webpage")

                # Download all found PDFs
                downloaded_files = []
                for pdf_url in pdf_urls[: settings.MAX_PDFS_PER_URL]:
                    file_path = await self._download_direct_pdf(session, pdf_url)
                    downloaded_files.extend(file_path)

                return downloaded_files

        except Exception as e:
            logger.error(f"Error downloading PDFs from {url}: {e}")
            raise

    async def _find_pdf_links(
        self, session: aiohttp.ClientSession, url: str
    ) -> List[str]:
        """Find PDF links on webpage"""
        try:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                pdf_links = []
                for link in soup.find_all("a", href=True):
                    try:
                        if isinstance(link, Tag) and "href" in link.attrs:
                            href = link["href"]
                        else:
                            href = None
                    except (AttributeError, TypeError):
                        href = None
                    if href and str(href).lower().endswith(".pdf"):
                        full_url = urljoin(url, str(href))
                        pdf_links.append(full_url)

                return pdf_links

        except Exception as e:
            logger.error(f"Error finding PDF links: {e}")
            return []

    async def _download_direct_pdf(
        self, session: aiohttp.ClientSession, pdf_url: str
    ) -> List[str]:
        """Download and extract text from PDF"""
        try:
            async with session.get(pdf_url) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to download PDF: HTTP {response.status}")

                # Save PDF to temp file
                filename = os.path.basename(urlparse(pdf_url).path) or "document.pdf"
                temp_pdf_path = os.path.join(self.temp_dir, f"temp_{filename}")

                async with aiofiles.open(temp_pdf_path, "wb") as f:
                    async for chunk in response.content.iter_chunked(8192):
                        await f.write(chunk)

                # Extract text from PDF
                text_content = self._extract_text_from_pdf(temp_pdf_path)

                # Save extracted text to temp file
                text_filename = f"extracted_{filename}.txt"
                temp_text_path = os.path.join(self.temp_dir, text_filename)

                async with aiofiles.open(temp_text_path, "w", encoding="utf-8") as f:
                    await f.write(text_content)

                # Clean up PDF file
                os.remove(temp_pdf_path)

                logger.info(f"Successfully extracted text from {pdf_url}")
                return [temp_text_path]

        except Exception as e:
            logger.error(f"Error downloading PDF {pdf_url}: {e}")
            raise

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            text_content = ""
            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"

            if not text_content.strip():
                raise ValueError("No text content extracted from PDF")

            return text_content

        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise
