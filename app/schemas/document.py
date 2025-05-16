from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    title: str
    # Para simplificar, o endpoint POST receberá a URL/caminho diretamente
    # Em um cenário real, usaria UploadFile do FastAPI para upload de arquivo
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

    model_config = ConfigDict(from_attributes=True) # Permite mapear do ORM model
