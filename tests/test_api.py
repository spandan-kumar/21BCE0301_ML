from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Document Retrieval API"}

def test_create_document():
    response = client.post(
        "/documents/",
        json={"content": "Test document", "metadata": {"source": "test"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["content"] == "Test document"
    assert data["metadata"] == {"source": "test"}

def test_get_document():
    # First, create a document
    create_response = client.post(
        "/documents/",
        json={"content": "Test document", "metadata": {"source": "test"}}
    )
    print(f"Create response status: {create_response.status_code}")
    print(f"Create response content: {create_response.content}")
    
    created_doc = create_response.json()
    

    response = client.get(f"/documents/{created_doc['id']}")
    print(f"Get response status: {response.status_code}")
    print(f"Get response content: {response.content}")
    assert response.status_code == 200
    assert response.json() == created_doc

def test_search_documents():

    client.post("/documents/", json={"content": "Python is great", "metadata": {"source": "test"}})
    client.post("/documents/", json={"content": "FastAPI is awesome", "metadata": {"source": "test"}})
    
    response = client.get("/documents/search?query=Python")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["content"] == "Python is great"