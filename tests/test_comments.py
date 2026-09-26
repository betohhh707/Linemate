#pytest tests/test_comments.py -v
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_store
from app.store import DataStore

_test_store = DataStore()
def get_test_store() -> DataStore:
    return _test_store

app.dependency_overrides[get_store] = get_test_store
client = TestClient(app)

def test_create_comment():
    ticket_response = client.post("/tickets", json = {"title": "...", "priority": "High", "assignee_id" : 7})
    ticket_id = ticket_response.json()["id"]
    
    comment_response = client.post(f"/tickets/{ticket_id}/comments", json={"author_id": 3, "body": "Fixed it"})
    assert comment_response.status_code == 200
    data = comment_response.json()
    assert data["body"] == "Fixed it"
    assert data["ticket_id"] == ticket_id

def test_create_comment_ticket_not_found():
    comment_response = client.post("/tickets/999/comments", json={"author_id": 3, "body": "Fixed it"})
    assert comment_response.status_code == 404

def test_create_comment_blank_body():
    ticket_response = client.post("/tickets", json={"title": "Ice machine broken", "priority": "High", "assignee_id": 5})
    ticket_id = ticket_response.json()["id"]

    comment_response = client.post(f"/tickets/{ticket_id}/comments", json={"author_id": 3, "body": "   "})
    assert comment_response.status_code == 422