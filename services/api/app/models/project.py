from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import ORMBaseModel


class Project(ORMBaseModel):
    __tablename__ = "projects"

    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(
        Enum("public", "private", name="project_status"),
        nullable=False,
        default="public",
    )

    team = relationship("Team", back_populates="projects")
    owner = relationship("User", foreign_keys=[owner_user_id], back_populates="projects")
