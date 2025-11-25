from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import ORMBaseModel


class Team(ORMBaseModel):
    __tablename__ = "teams"

    name = Column(String(50))
    description = Column(String(255))

    projects = relationship("Project", back_populates="team")
    members = relationship("TeamMember", back_populates="team")
