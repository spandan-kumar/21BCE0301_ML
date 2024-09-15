from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.db.database import get_db
from app.services.embedding_service import EmbeddingService

class DocumentService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = DocumentRepository(db)
        self.embedding_service = EmbeddingService()

    def create_document(self, document: DocumentCreate) -> DocumentResponse:
        
        embedding = self.embedding_service.get_embedding(document.content)
        document.embedding = embedding

        created_document = self.repository.create(document)
        return DocumentResponse.from_orm(created_document)

    def get_document(self, document_id: int) -> Optional[DocumentResponse]:
        document = self.repository.get_by_id(document_id)
        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return DocumentResponse.from_orm(document)

    def get_all_documents(self) -> List[DocumentResponse]:
        documents = self.repository.get_all()
        return [DocumentResponse.from_orm(doc) for doc in documents]

    def update_document(self, document_id: int, document: DocumentUpdate) -> DocumentResponse:
        existing_document = self.repository.get_by_id(document_id)
        if not existing_document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        # If content is updated, regenerate the embedding
        if document.content:
            embedding = self.embedding_service.get_embedding(document.content)
            document.embedding = embedding

        updated_document = self.repository.update(document_id, document)
        return DocumentResponse.from_orm(updated_document)

    def delete_document(self, document_id: int) -> bool:
        deleted = self.repository.delete(document_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return True

    def search_documents(self, query: str) -> List[DocumentResponse]:
        documents = self.repository.search(query)
        return [DocumentResponse.from_orm(doc) for doc in documents]

    def get_similar_documents(self, query: str, limit: int = 5) -> List[DocumentResponse]:
        query_embedding = self.embedding_service.get_embedding(query)
        similar_documents = self.repository.get_by_embedding(query_embedding, limit)
        return [DocumentResponse.from_orm(doc) for doc in similar_documents]
