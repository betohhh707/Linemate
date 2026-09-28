from fastapi import APIRouter, Depends
from app.store import DataStore
from app.dependencies import get_store

router = APIRouter()

@router.get("/analytics/workload")
def workload_distribution(store: DataStore = Depends(get_store)):
    return store.get_workload_distribution()

@router.get("/analytics/ownership-mismatches")
def ownership_mismatches(store: DataStore = Depends(get_store)) -> list[dict]:
    return store.get_ownership_mismatches()

@router.get("/analytics/stale-documents")
def stale_documents(store: DataStore = Depends(get_store)) -> list[dict]:
    return store.get_stale_documents()