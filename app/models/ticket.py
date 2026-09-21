from datetime import datetime, UTC
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class TicketPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class TicketStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In-Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

class TicketCreate(BaseModel):
    title: str
    priority: TicketPriority
    assignee_id: int
    related_document_id: Optional[int] = None

class Ticket(TicketCreate):
    id: int
    status: TicketStatus = Field(default=TicketStatus.OPEN)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))