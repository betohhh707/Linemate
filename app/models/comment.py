from datetime import datetime, UTC
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Optional

#ticket_id wil come from the URL path when routing so it won't go in this class
class CommentCreate(BaseModel):
    author_id: int
    body: str

    @field_validator("body")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be blank or whitespace-only")
        return v.strip()

#router will hand the comment class the ticket_id. 
class Comment(CommentCreate):
    id: int
    ticket_id: int 
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
