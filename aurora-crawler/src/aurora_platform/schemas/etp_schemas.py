from pydantic import BaseModel


class ETPRequest(BaseModel):
    topic: str
