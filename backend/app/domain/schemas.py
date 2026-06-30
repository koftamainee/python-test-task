from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: UUID
    text: str
    rubrics: list[str]
    created_date: datetime

    model_config = {"from_attributes": True}


class DeleteResponse(BaseModel):
    ok: bool



