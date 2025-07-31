from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Consent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=50)
    action: str = Field(max_length=100)
    is_granted: bool = Field(default=False)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
