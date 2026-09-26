from enum import Enum
from pydantic import BaseModel


class Station(str, Enum):
    GRILL = "Grill"
    PASTRY = "Pastry"
    PREP = "Prep"
    FRONT_OF_HOUSE = "Front of House"


class CrewMember(BaseModel):
    id: int
    name: str
    station: Station
    