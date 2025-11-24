from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class TeamBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str

class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


