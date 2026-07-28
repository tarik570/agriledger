from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnimalCreate(BaseModel):
    tag_number: str
    species: str
    breed: str
    weight: float
    health_status: str

class AnimalResponse(AnimalCreate):
    id: int
    blockchain_hash: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
