from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class TeamBase(BaseModel):
    name: str
    description: str

class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


