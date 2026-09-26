#pytest tests/test_tickets.py -v
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_store
from app.store import DataStore

_test_store = DataStore()
def get_test_store() -> DataStore:
    return _test_store

app.dependency_overrides[get_store] = get_test_store
client = TestClient(app)

def test_create_ticket():
    response = client.post("/tickets", json = {"title": "Can opener needs fixin", "priority": "High", "assignee_id" : 7, "related_document_id" : 1})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Can opener needs fixin"
    assert "id" in data 

def test_get_ticket_not_found():
    response = client.get("/tickets/999")
    assert response.status_code == 404

def test_list_tickets():
    response = client.get("/tickets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_ticket_invalid_priority():
    response = client.post("/tickets", json = {"title": "Can opener needs fixin", "priority": "Urgente", "assignee_id" : 7, "related_document_id" : 1})
    assert response.status_code == 422