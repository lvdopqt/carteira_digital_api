from sqlalchemy.orm import Session
from typing import List, Optional

from app.repos.document import DocumentRepository
from app.schemas.document import DocumentCreate, Document as DocumentSchema 
from app.schemas.user import User as UserSchema
from fastapi import HTTPException, status

class DocumentService:
    def __init__(self, document_repo: DocumentRepository):
        self.document_repo = document_repo

    def create_document_for_user(self, document_data: DocumentCreate, current_user: UserSchema) -> DocumentSchema:
        """Cria um documento para o usuário atualmente autenticado."""
        
        db_document = self.document_repo.create_document(document_data, owner_id=current_user.id)

        return DocumentSchema.model_validate(db_document)

    def get_documents_by_user(self, current_user: UserSchema) -> List[DocumentSchema]:
        """Lista todos os documentos do usuário atualmente autenticado."""
        db_documents = self.document_repo.get_documents_by_owner(owner_id=current_user.id)

        return [DocumentSchema.model_validate(doc) for doc in db_documents]

    def get_user_document_by_id(self, document_id: int, current_user: UserSchema) -> Optional[DocumentSchema]:
        """Busca um documento específico do usuário logado."""
        db_document = self.document_repo.get_document_by_id_and_owner(document_id, current_user.id)
        if not db_document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return DocumentSchema.model_validate(db_document)

