from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.document import DocumentCreate, Document as DocumentResponseSchema
from app.schemas.user import User as UserSchema
from app.services.document import DocumentService
from app.repos.document import DocumentRepository

from app.db.session import get_db
from app.core.security import get_current_user


router = APIRouter(tags=["Documents"])

def get_document_repo(db: Session = Depends(get_db)) -> DocumentRepository:
    return DocumentRepository(db)

def get_document_service(document_repo: DocumentRepository = Depends(get_document_repo)) -> DocumentService:
    return DocumentService(document_repo)


@router.post("/", response_model=DocumentResponseSchema, status_code=status.HTTP_201_CREATED)
def create_document_for_current_user(
    document_data: DocumentCreate,
    current_user: UserSchema = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service)
):
    """
    Stores a new digital document for the authenticated user.
    """
    new_document = document_service.create_document_for_user(document_data, current_user)
    return new_document

@router.get("/", response_model=List[DocumentResponseSchema])
def list_documents_for_current_user(
    current_user: UserSchema = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service)
):
    """
    Lists all digital documents for the authenticated user.
    """
    documents = document_service.get_documents_by_user(current_user)
    return documents


@router.get("/{document_id}", response_model=DocumentResponseSchema)
def get_document_by_id(
    document_id: int,
    current_user: UserSchema = Depends(get_current_user),
    document_service: DocumentService = Depends(get_document_service)
):
    """
    Gets a specific digital document for the authenticated user by ID.
    """
    document = document_service.get_user_document_by_id(document_id, current_user)
    return document
