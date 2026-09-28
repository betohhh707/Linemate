from pydantic import BaseModel, Field, field_validator


class AskRequest(BaseModel):
    question: str = Field(..., max_length=1000)
    conversation_id: str | None = None

    @field_validator("question")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be blank or whitespace-only")
        return v.strip()


class Source(BaseModel):
    document_id: int
    title: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]