from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_store, get_rag
from app.store import DataStore

client = TestClient(app)


class FakeRagService:
    def ask(self, question: str, conversation_id: str | None = None) -> dict:
        return {"answer": "This is a fake answer for testing.", "sources": []}


_test_store = DataStore()
def get_test_store() -> DataStore:
    return _test_store


_test_rag = FakeRagService()
def get_test_rag() -> FakeRagService:
    return _test_rag


app.dependency_overrides[get_store] = get_test_store
app.dependency_overrides[get_rag] = get_test_rag

def test_ask_returns_fake_answer():
    response = client.post("/ask", json = {"question": "What temperature should the walk-in cooler be kept at?"})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "This is a fake answer for testing."

def test_ask_rejects_blank_question():
    response = client.post("/ask", json ={"question": "   "})
    assert response.status_code == 422