from app.store import DataStore
_store = DataStore()

def get_store() -> DataStore:
    return _store
    