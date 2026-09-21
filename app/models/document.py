from datetime import datetime, UTC
from enum import Enum
from pydantic import BaseModel, Field, field_validator

#category string constants 
class DocumentCategory(str, Enum):
    RECIPE = "Recipe"
    SOP = "SOP"
    INCIDENT_REPORT ="Incident Report"
    ONBOARDING = "Onboarding"

#schema class for validation using pydantic BaseModel class
class DocumentCreate(BaseModel):
    title: str
    category: DocumentCategory
    body: str
    owner_id: int

#schema for edge case. inherits from documentCreate. Client doesn't create their own document id and date for last reviewed at.
#store is the one assigning the id and pydantic auto stamps a date 
class Document(DocumentCreate):
    id: int
    last_reviewed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
