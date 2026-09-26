from fastapi import APIRouter, Depends
from app.store import DataStore
from app.dependencies import get_store

router = APIRouter()

@router.get("/analytics/workload")
def workload_distribution(store: DataStore = Depends(get_store)):
    return store.get_workload_distribution()