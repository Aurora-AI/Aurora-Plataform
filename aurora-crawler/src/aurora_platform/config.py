import os


class Settings:
    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: str = os.getenv(
        "AZURE_OPENAI_ENDPOINT", "https://seu-endpoint.openai.azure.com"
    )
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "CHAVE_NAO_DEFINIDA")
    PROJECT_VERSION: str = "1.0.0"
    # ChromaDB Configuration
    CHROMA_MODE: str = os.getenv(
        "CHROMA_MODE", "EMBEDDED"
    )  # "EMBEDDED" ou "CLIENT_SERVER"
    CHROMA_HOST: str = os.getenv("CHROMA_HOST", "localhost")
    CHROMA_PORT: int = int(os.getenv("CHROMA_PORT", "8001"))

    # Legacy (manter compatibilidade)
    CHROMADB_HOST: str = os.getenv("CHROMADB_HOST", "localhost")
    CHROMADB_PORT: int = int(os.getenv("CHROMADB_PORT", "8000"))

    # Scraper settings
    DOWNLOAD_TIMEOUT: int = int(os.getenv("DOWNLOAD_TIMEOUT", "30"))
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    MAX_PDFS_PER_URL: int = int(os.getenv("MAX_PDFS_PER_URL", "5"))

    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "aurora-secret-key-2024")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
