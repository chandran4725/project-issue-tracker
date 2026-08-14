from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.auth import CurrentUser, get_current_user
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse
)
from app.service import project_service
from app.util.database import get_db


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)


@router.get(
    "",
    response_model=list[ProjectResponse],
    status_code=status.HTTP_200_OK
)
def get_all_projects(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return project_service.get_all_projects(
        current_user,
        db
    )


@router.get(
    "/{pro_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK
)
def get_project(
    pro_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return project_service.get_project_by_id(
        pro_id,
        current_user,
        db
    )


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    project_create: ProjectCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return project_service.create_project(
        project_create,
        current_user,
        db
    )


@router.patch(
    "/{pro_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK
)
def update_project(
    pro_id: int,
    project_update: ProjectUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return project_service.update_project(
        pro_id,
        project_update,
        current_user,
        db
    )


@router.delete(
    "/{pro_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_project(
    pro_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project_service.delete_project(
        pro_id,
        current_user,
        db
    )