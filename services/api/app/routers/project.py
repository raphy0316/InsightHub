from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from ..db.session import get_db
from sqlalchemy.orm import Session
from ..schemas.common import Response
from ..services.project_service import ProjectService
from ..schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from ..models.user import User
from ..core.security import get_current_user, get_current_user_optional

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=Response[ProjectRead])
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project_data = project_in.model_copy(update={"owner_user_id": current_user.id})
    
    project = ProjectService.create_project(db, project_data)
    return Response(
        success=True,
        message="Project created successfully",
        data=project
    )


@router.get("/{project_id}", response_model=Response[ProjectRead])
async def read_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    project = ProjectService.get_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if project.status == "private":
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required to view private projects"
            )
        
        ProjectService.authenticate_user(db, project_id, current_user.id)

    return Response(
        success=True,
        message="Project retrieved successfully",
        data=ProjectRead.model_validate(project)
    )

@router.put("/{project_id}", response_model=Response[ProjectRead])
async def update_project(
    project_id: UUID,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ProjectService.authenticate_user(db, project_id, current_user.id)
    updated_project = ProjectService.edit_project(db, project_id, project_in)
    
    return Response(
        success=True,
        message="Project updated successfully",
        data=updated_project
    )

@router.delete("/{project_id}", response_model=Response[None])
async def delete_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = ProjectService.get_by_id(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if current_user.id != project.owner_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project owner can delete the project"
        )
    
    ProjectService.delete_project(db, project_id)
    
    return Response(
        success=True,
        message="Project deleted successfully",
        data=None
    )