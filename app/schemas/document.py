from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    title: str
    file_url: str
    document_type: Optional[str] = None


class Document(BaseModel):
    id: int
    title: str
    file_url: str
    document_type: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
