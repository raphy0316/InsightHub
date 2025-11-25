from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class TeamMemberBase(BaseModel):
    user_id: UUID
    team_id: UUID

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMemberRead(BaseModel):
    id: UUID
    user_id: UUID
    team_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
