import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.schemas.document import DocumentCreate, Document as DocumentResponseSchema
from app.models.document import Document as DocumentModel
from app.models.user import User as UserModel


def create_test_document(db: Session, owner_id: int, title: str = "Test Document", file_url: str = "http://example.com/doc.pdf", document_type: str = "Other") -> DocumentModel:
    """Creates a document directly in the database."""
    document = DocumentModel(
        title=title,
        file_url=file_url,
        document_type=document_type,
        owner_id=owner_id
    )
    db.add(document)
    
    db.flush()
    db.refresh(document)
    return document

def test_create_document_successful(client: TestClient, db: Session, test_user: UserModel, user_auth_token: str):
    """
    Test creating a new document for the authenticated user.
    """
    document_data = DocumentCreate(
        title="My ID Card",
        file_url="http://example.com/id.jpg",
        document_type="RG"
    )

    response = client.post(
        "/api/v1/documents/", # Adjust URL if needed
        json=document_data.model_dump(),
        headers={"Authorization": user_auth_token} # Include auth token
    )

    assert response.status_code == 201
    response_data = response.json()

    assert "id" in response_data
    assert isinstance(response_data["id"], int)
    assert response_data["title"] == document_data.title
    assert response_data["file_url"] == document_data.file_url
    assert response_data["document_type"] == document_data.document_type
    assert response_data["owner_id"] == test_user.id

    # Direct DB verification using the db fixture
    created_document_in_db = db.query(DocumentModel).filter(DocumentModel.id == response_data["id"]).first()
    assert created_document_in_db is not None
    assert created_document_in_db.title == document_data.title
    assert created_document_in_db.owner_id == test_user.id


def test_create_document_unauthorized(client: TestClient, db: Session):
    """
    Test attempting to create a document without authentication.
    """
    document_data = DocumentCreate(
        title="Unauthorized Doc",
        file_url="http://example.com/unauth.pdf",
        document_type="Other"
    )

    response = client.post(
        "/api/v1/documents/",
        json=document_data.model_dump()
    )

    assert response.status_code == 401


def test_list_documents_successful(client: TestClient, db: Session, test_user: UserModel, user_auth_token: str):
    """
    Test listing documents for the authenticated user.
    """
    doc1 = create_test_document(db, test_user.id, title="Doc 1")
    doc2 = create_test_document(db, test_user.id, title="Doc 2")

    other_user = UserModel(email="other@example.com", hashed_password="hashedpassword")
    db.add(other_user)
    
    db.flush() # Use flush
    db.refresh(other_user)
    other_doc = create_test_document(db, other_user.id, title="Other User's Doc")


    response = client.get(
        "/api/v1/documents/",
        headers={"Authorization": user_auth_token}
    )

    assert response.status_code == 200
    response_data = response.json()

    assert isinstance(response_data, list)

    assert len(response_data) == 2

    titles = [doc["title"] for doc in response_data]
    assert "Doc 1" in titles
    assert "Doc 2" in titles
    assert "Other User's Doc" not in titles


def test_list_documents_unauthorized(client: TestClient):
    """
    Test attempting to list documents without authentication.
    """
    response = client.get(
        "/api/v1/documents/"
    )

    assert response.status_code == 401


def test_list_documents_empty(client: TestClient, db: Session, user_auth_token: str):
    """
    Test listing documents when the user has no documents.
    """
    # Ensure the test_user is created, but no documents are added explicitly here
    # The db fixture and test_user fixture ensure a clean user exists.

    response = client.get(
        "/api/v1/documents/",
        headers={"Authorization": user_auth_token}
    )

    assert response.status_code == 200
    response_data = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) == 0


def test_get_document_by_id_successful(client: TestClient, db: Session, test_user: UserModel, user_auth_token: str):
    """
    Test getting a specific document by ID for the owner.
    """
    test_doc = create_test_document(db, test_user.id, title="Specific Doc")

    response = client.get(
        f"/api/v1/documents/{test_doc.id}",
        headers={"Authorization": user_auth_token}
    )

    assert response.status_code == 200
    response_data = response.json()

    assert response_data["id"] == test_doc.id
    assert response_data["title"] == test_doc.title
    assert response_data["owner_id"] == test_user.id


def test_get_document_by_id_not_found(client: TestClient, user_auth_token: str):
    """
    Test getting a non-existent document by ID for the authenticated user.
    """
    non_existent_id = 9999

    response = client.get(
        f"/api/v1/documents/{non_existent_id}",
        headers={"Authorization": user_auth_token}
    )

    assert response.status_code == 404
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Document not found"


def test_get_document_by_id_unauthorized_owner(client: TestClient, db: Session, test_user: UserModel, user_auth_token: str):
    """
    Test attempting to get a document that belongs to another user.
    """
    other_user = UserModel(email="intruder@example.com", hashed_password="hashedpassword")
    db.add(other_user)
   
    db.flush() # Use flush
    db.refresh(other_user)
    other_doc = create_test_document(db, other_user.id, title="Intruder's Doc")

    response = client.get(
        f"/api/v1/documents/{other_doc.id}",
        headers={"Authorization": user_auth_token}
    )

    assert response.status_code == 404
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Document not found"


def test_get_document_by_id_unauthorized_no_auth(client: TestClient, db: Session, test_user: UserModel):
    """
    Test attempting to get a document by ID without any authentication.
    """
    test_doc = create_test_document(db, test_user.id, title="Doc without Auth")

    response = client.get(
        f"/api/v1/documents/{test_doc.id}"
    )

    assert response.status_code == 401
