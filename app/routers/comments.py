from app.store import DataStore
from app.dependencies import get_store
from app.models.comment import Comment, CommentCreate
from fastapi import Depends, APIRouter, HTTPException

router = APIRouter()

@router.post("/tickets/{ticket_id}/comments")
def create_comment(ticket_id: int, data: CommentCreate, store: DataStore = Depends(get_store))->Comment:
    #python will attemply to run the code, if at any point during that attempt something raises the exception 
    #matching the exception, excecution will jump to the except block
    try:
        return store.create_comment(ticket_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail = str(e))
