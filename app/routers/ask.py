from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_rag
from app.models.ask import AskRequest, AskResponse
from app.rag import RagService

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask(data: AskRequest, rag: RagService = Depends(get_rag)):
    try:
        return rag.ask(data.question, data.conversation_id)
    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="LineMate's language model is unavailable. Make sure Ollama is running.",
        )