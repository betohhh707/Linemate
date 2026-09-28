from app.store import DataStore
from app.seed import seed_documents
from app.rag import RagService

_store = DataStore()
seed_documents(_store)
_rag: RagService | None = None

def get_store() -> DataStore:
    return _store

def get_rag() -> RagService:
    global _rag
    if _rag is None:
        _rag = RagService(_store)
        _rag.index()
    return _rag