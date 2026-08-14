from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import CurrentUser
from app.auth import permission
from app.auth.permission import Permission
from app.entities.role import Role
from app.repository import role as RoleRepository
from app.service.employee_service import get_current_employee
from app.schemas.role import RoleCreate, RoleUpdate


def get_all_roles(
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_EMPLOYEE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    return RoleRepository.get_all_roles(db)


def get_role_by_id(
    role_id: int,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_EMPLOYEE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    role = RoleRepository.get_role_by_id(
        role_id,
        db
    )

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    return role


def create_role(
    role_create: RoleCreate,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    if current_employee.role.role_name != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ADMIN can create roles"
        )

    existing = RoleRepository.get_role_by_name(
        role_create.role_name,
        db
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role already exists"
        )

    role = Role(
        role_name=role_create.role_name
    )

    return RoleRepository.create_role(
        role,
        db
    )


def update_role(
    role_id: int,
    role_update: RoleUpdate,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    if current_employee.role.role_name != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ADMIN can update roles"
        )

    role = RoleRepository.get_role_by_id(
        role_id,
        db
    )

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    role.role_name = role_update.role_name

    return RoleRepository.update_role(
        role,
        db
    )


def delete_role(
    role_id: int,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    if current_employee.role.role_name != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ADMIN can delete roles"
        )

    role = RoleRepository.get_role_by_id(
        role_id,
        db
    )

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    RoleRepository.delete_role(
        role,
        db
    )