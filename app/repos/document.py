from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.document import Document as DocumentModel
from app.schemas.document import DocumentCreate

class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(self, document_data: DocumentCreate, owner_id: int) -> DocumentModel:
        """Creates a new document in the database for a user."""
        # Cria uma instância do modelo ORM a partir dos dados do schema e do owner_id
        db_document = DocumentModel(
            title=document_data.title,
            file_url=document_data.file_url,
            document_type=document_data.document_type,
            owner_id=owner_id
        )

        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)

        return db_document

    def get_documents_by_owner(self, owner_id: int) -> List[DocumentModel]:
        """Retrieves all documents belonging to a specific user"""
        return self.db.query(DocumentModel).filter(DocumentModel.owner_id == owner_id).all()

    def get_document_by_id_and_owner(self, document_id: int, owner_id: int) -> Optional[DocumentModel]:
        """Retrieves a document by ID, ensuring it belongs to the specified user."""
        return self.db.query(DocumentModel).filter(
            DocumentModel.id == document_id,
            DocumentModel.owner_id == owner_id
        ).first()