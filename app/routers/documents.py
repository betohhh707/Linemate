from fastapi import APIRouter, Depends, HTTPException
from app.models.document import Document, DocumentCreate
from app.store import DataStore
from app.dependencies import get_store

#groups related routes together
router = APIRouter()

@router.post("/documents")
def create_document(data: DocumentCreate, store: DataStore = Depends(get_store)) -> Document:
    return store.create_document(data)

@router.get("/documents")
def list_documents(store: DataStore = Depends(get_store))-> list[Document]:
    return store.list_documents()

@router.get("/documents/{document_id}")
def get_document(document_id: int, store: DataStore = Depends(get_store)) -> Document:
    doc = store.get_document(document_id)
    if doc is None:
        raise HTTPException(status_code=404, detail= f"Document {document_id} does not exist")
    return doc