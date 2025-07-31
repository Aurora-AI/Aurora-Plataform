import asyncio
import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from aurora_platform.services.scraper_service import DeepDiveScraperServiceV2


@pytest.mark.asyncio
async def test_scraper():
    scraper = DeepDiveScraperServiceV2()
    # Test with a sample PDF URL (you can replace with actual URL)
    test_url = "https://example.com/sample.pdf"
    try:
        print(f"Testing scraper with URL: {test_url}")
        files = await scraper.download_pdfs_from_url(test_url)
        print(f"Downloaded files: {files}")
        # Clean up
        for file_path in files:
            if os.path.exists(file_path):
                os.remove(file_path)
    except Exception as e:
        print(f"Test failed: {e}")
