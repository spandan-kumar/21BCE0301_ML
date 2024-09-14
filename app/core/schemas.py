from pydantic import BaseModel
from typing import Optional, Dict, Any

class DocumentBase(BaseModel):
    content: str
    metadata: Dict[str, Any]

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int

    class Config:
        orm_mode = True

class DocumentUpdate(BaseModel):
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class DocumentSearch(BaseModel):
    query: str

