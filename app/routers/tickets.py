from app.store import DataStore
from fastapi import APIRouter, Depends, HTTPException
from app.models.ticket import Ticket, TicketCreate
from app.dependencies import get_store

router = APIRouter()

@router.post("/tickets")
def create_ticket(data: TicketCreate, store: DataStore = Depends(get_store))->Ticket:
    return store.create_ticket(data)

@router.get("/tickets")
def list_tickets(store: DataStore = Depends(get_store))->list[Ticket]:
    return store.list_tickets()

@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, store: DataStore = Depends(get_store))-> Ticket:
    tkt = store.get_ticket(ticket_id)
    if tkt is None:
        raise HTTPException(status_code=404, detail= f"Ticket {ticket_id} does not exist")
    return tkt
