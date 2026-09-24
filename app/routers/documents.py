from fastapi import APIRouter, Depends
from app.models.document import Document, DocumentCreate
from app.store import DataStore
from app.dependencies import get_store

#groups related routes together
router = APIRouter()

@router.post("/documents")
def create_document(data: DocumentCreate, store: DataStore = Depends(get_store)) -> Document:
    return store.create_document(data)

