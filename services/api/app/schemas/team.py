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


class TeamMemberRead(BaseModel):
    id: UUID
    user_id: UUID
    team_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
