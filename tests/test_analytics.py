from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_store
from app.store import DataStore

_test_store = DataStore()
def get_test_store() -> DataStore:
    return _test_store

app.dependency_overrides[get_store] = get_test_store
client = TestClient(app)

def test_workload_distribution():
    ticket_response = client.post("/tickets", json={"title": "Can opener needs fixin", "priority": "High", "assignee_id": 3})
    assert ticket_response.status_code == 200

    workload_response = client.get("/analytics/workload")
    assert workload_response.status_code == 200
    data = workload_response.json()
    assert isinstance(data, list)
    assert any(entry["station"] == "Pastry" and entry["priority"] == "High" for entry in data)

def test_ownership_mismatch_detected():
    document_response = client.post("/documents", json={"title": "Knife Sharpening SOP", "category": "SOP", "body": "Steps here", "owner_id": 4})
    document_id = document_response.json()["id"]
    ticket_response = client.post("/tickets", json = {"title": "Can opener needs fixin", "priority": "High", "assignee_id" : 3, "related_document_id" : document_id})
    ticket_id = ticket_response.json()["id"]

    ownership_response = client.get("/analytics/ownership-mismatches")
    assert ownership_response.status_code == 200
    data = ownership_response.json()
    assert len(data) >= 1
    assert any(entry["ticket_id"] == ticket_id for entry in data)

def test_stale_documents_no_crash():
    document_response = client.post("/documents", json={"title": "Knife Sharpening SOP", "category": "SOP", "body": "Steps here", "owner_id": 4})
    stale_response = client.get("/analytics/stale-documents")
    assert stale_response.status_code == 200
    data = stale_response.json()
    assert isinstance(data,list)