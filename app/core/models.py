from sqlalchemy import Column, Integer, String, JSON
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    metadata = Column(JSON)

    def __repr__(self):
        return f"<Document(id={self.id}, content={self.content[:50]}...)>"
