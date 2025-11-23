from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from .user import UserRead
from .team import TeamRead


class ProjectBase(BaseModel):
    name: str
    description: str
    status: str


class ProjectCreate(ProjectBase):
    team_id: UUID
    owner_user_id: UUID


class ProjectRead(ProjectBase):
    id: UUID
    created_at: datetime
    owner: UserRead
    team: TeamRead
    
    class Config:
        from_attributes = True

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
