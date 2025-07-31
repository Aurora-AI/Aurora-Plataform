"""Testes para configurações"""

import pytest
from aurora_platform.config import settings, Settings


def test_settings_import():
    """Testa importação das configurações"""
    assert settings is not None
    assert isinstance(settings, Settings)


def test_default_values():
    """Testa valores padrão das configurações"""
    assert settings.CHROMADB_HOST == "localhost"
    assert settings.CHROMADB_PORT == 8000
    assert settings.DOWNLOAD_TIMEOUT == 30
    assert settings.MAX_FILE_SIZE_MB == 50
    assert settings.MAX_PDFS_PER_URL == 5
    assert settings.PROJECT_VERSION == "1.0.0"


def test_settings_class():
    """Testa criação da classe Settings"""
    new_settings = Settings()
    assert new_settings.CHROMADB_HOST == "localhost"
