import pytest
from app.services.document_service import DocumentService
from app.db.repositories.document_repository import DocumentRepository

@pytest.fixture
def document_service(db):
    return DocumentService(DocumentRepository(db))

@pytest.mark.asyncio
async def test_create_document(document_service):
    content = "Test content"
    metadata = {"source": "test"}
    document = await document_service.create_document(content, metadata)
    assert document.content == content
    assert document.metadata == metadata

@pytest.mark.asyncio
async def test_get_document(document_service):
    content = "Test content"
    metadata = {"source": "test"}
    created_doc = await document_service.create_document(content, metadata)
    retrieved_doc = await document_service.get_document(created_doc.id)
    assert retrieved_doc.id == created_doc.id
    assert retrieved_doc.content == content
    assert retrieved_doc.metadata == metadata

@pytest.mark.asyncio
async def test_search_documents(document_service):
    await document_service.create_document("Python is great", {"source": "test"})
    await document_service.create_document("FastAPI is awesome", {"source": "test"})
    results = await document_service.search_documents("Python")
    assert len(results) == 1
    assert results[0].content == "Python is great"

@pytest.mark.asyncio
async def test_update_document(document_service):
    doc = await document_service.create_document("Original content", {"source": "test"})
    updated_doc = await document_service.update_document(doc.id, "Updated content", {"source": "updated"})
    assert updated_doc.content == "Updated content"
    assert updated_doc.metadata == {"source": "updated"}

@pytest.mark.asyncio
async def test_delete_document(document_service):
    doc = await document_service.create_document("To be deleted", {"source": "test"})
    result = await document_service.delete_document(doc.id)
    assert result == True
    with pytest.raises(Exception):
        await document_service.get_document(doc.id)