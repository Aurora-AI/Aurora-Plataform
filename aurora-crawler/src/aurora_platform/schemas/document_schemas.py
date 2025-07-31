from fastapi import UploadFile
from pydantic import BaseModel, Field


class DocumentIngestRequest(BaseModel):
    collection_name: str = Field(
        ...,
        description="O nome da coleção de conhecimento onde o documento será salvo.",
    )
