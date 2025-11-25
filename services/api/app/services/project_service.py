from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.project import Project
from ..models.team_member import TeamMember
from ..schemas.project import ProjectCreate, ProjectRead, ProjectUpdate


class ProjectService:
    @staticmethod
    def create_project(db: Session, project_in: ProjectCreate) -> ProjectRead:
        project = Project(
            name=project_in.name,
            description=project_in.description,
            status=project_in.status,
            team_id=project_in.team_id,
            owner_user_id=project_in.owner_user_id,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return ProjectRead.model_validate(project)

    @staticmethod
    def authenticate_user(db: Session, project_id: UUID, user_id: UUID) -> Project:
        """Check if user has access to project (is team member or owner)"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        # Check if user is the owner
        if project.owner_user_id == user_id:
            return project
        
        # Check if user is a team member
        team_member = db.query(TeamMember).filter(
            TeamMember.team_id == project.team_id,
            TeamMember.user_id == user_id
        ).first()
        
        if not team_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project"
            )
        
        return project

    @staticmethod
    def get_by_id(db: Session, project_id: UUID | str) -> Project | None:
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def edit_project(db: Session, project_id: UUID | str, project_in: ProjectUpdate) -> ProjectRead:
        project = ProjectService.get_by_id(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        if project_in.name is not None:
            project.name = project_in.name
        if project_in.description is not None:
            project.description = project_in.description
        if project_in.status is not None:
            project.status = project_in.status
        
        db.commit()
        db.refresh(project)
        return ProjectRead.model_validate(project)

    @staticmethod
    def delete_project(db: Session, project_id: UUID | str) -> None:
        project = ProjectService.get_by_id(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        db.delete(project)
        db.commit()