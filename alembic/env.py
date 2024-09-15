from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate
import numpy as np
import faiss

class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db
        self.index = None
        self.document_ids = []
        self.build_faiss_index()

    def build_faiss_index(self):
        documents = self.db.query(Document).all()
        if not documents:
            return

        embeddings = [doc.embedding for doc in documents]
        self.document_ids = [doc.id for doc in documents]

        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings, dtype=np.float32))

    def create(self, document: DocumentCreate) -> Document:
        db_document = Document(**document.dict())
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        
        if self.index is None:
            self.build_faiss_index()
        else:
            self.index.add(np.array([db_document.embedding], dtype=np.float32))
            self.document_ids.append(db_document.id)

        return db_document

    def get_by_id(self, document_id: int) -> Optional[Document]:
        return self.db.query(Document).filter(Document.id == document_id).first()

    def get_all(self) -> List[Document]:
        return self.db.query(Document).all()

    def update(self, document_id: int, document: DocumentUpdate) -> Optional[Document]:
        db_document = self.get_by_id(document_id)
        if db_document:
            old_embedding = db_document.embedding
            for key, value in document.dict(exclude_unset=True).items():
                setattr(db_document, key, value)
            self.db.commit()
            self.db.refresh(db_document)

            if old_embedding != db_document.embedding:
                self.build_faiss_index()  

        return db_document

    def delete(self, document_id: int) -> bool:
        db_document = self.get_by_id(document_id)
        if db_document:
            self.db.delete(db_document)
            self.db.commit()

            self.build_faiss_index() 

            return True
        return False

    def search(self, query: str) -> List[Document]:
        return self.db.query(Document).filter(Document.content.ilike(f"%{query}%")).all()

    def get_by_embedding(self, embedding: List[float], limit: int = 5) -> List[Document]:
        if self.index is None:
            return []

        embedding_np = np.array([embedding], dtype=np.float32)
        distances, indices = self.index.search(embedding_np, limit)
        
        similar_document_ids = [self.document_ids[i] for i in indices[0]]
        similar_documents = self.db.query(Document).filter(Document.id.in_(similar_document_ids)).all()
        
        sorted_documents = sorted(similar_documents, key=lambda x: similar_document_ids.index(x.id))
        
        return sorted_documents
