#pytest tests/test_documents.py -v
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_store
from app.store import DataStore

_test_store = DataStore()
def get_test_store() -> DataStore:
    return _test_store

app.dependency_overrides[get_store] = get_test_store
client = TestClient(app)

def test_create_document():
    response = client.post("/documents", json={"title": "Knife Sharpening SOP", "category": "SOP", "body": "Steps here", "owner_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Knife Sharpening SOP"
    assert "id" in data 

def test_get_document_not_found():
    response = client.get("/documents/999")
    assert response.status_code == 404

def test_list_documents():
    response = client.get("/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_document_invalid_category():
    response = client.post("/documents", json={"title": "Knife Sharpening SOP", "category": "jobless", "body": "Steps here", "owner_id": 1})
    assert response.status_code == 422    

