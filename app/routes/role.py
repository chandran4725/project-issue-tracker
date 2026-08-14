from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.auth import CurrentUser, get_current_user
from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse
)
from app.service import role_service
from app.util.database import get_db


router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"]
)


@router.get(
    "",
    response_model=list[RoleResponse],
    status_code=status.HTTP_200_OK
)
def get_all_roles(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return role_service.get_all_roles(
        current_user,
        db
    )


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    status_code=status.HTTP_200_OK
)
def get_role(
    role_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return role_service.get_role_by_id(
        role_id,
        current_user,
        db
    )


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_role(
    role_create: RoleCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return role_service.create_role(
        role_create,
        current_user,
        db
    )


@router.patch(
    "/{role_id}",
    response_model=RoleResponse,
    status_code=status.HTTP_200_OK
)
def update_role(
    role_id: int,
    role_update: RoleUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return role_service.update_role(
        role_id,
        role_update,
        current_user,
        db
    )


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_role(
    role_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    role_service.delete_role(
        role_id,
        current_user,
        db
    )