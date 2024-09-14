from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.services import document_service
from app.core.schemas import DocumentSearch

router = APIRouter()

@router.post("/")
async def search_documents(search: DocumentSearch, db: Session = Depends(get_db)):
    results = document_service.search_documents(db, search.query)
    if not results:
        raise HTTPException(status_code=404, detail="No documents found")
    return results
