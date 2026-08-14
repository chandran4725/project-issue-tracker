from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import CurrentUser
from app.auth import permission
from app.auth.permission import Permission
from app.entities.project import Project
from app.repository import project as ProjectRepository
from app.service.employee_service import get_current_employee
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_all_projects(
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.VIEW
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    return ProjectRepository.get_all_projects(db)


def get_project_by_id(
    pro_id: int,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    project = ProjectRepository.get_project_by_id(
        pro_id,
        db
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.VIEW
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    return project


def create_project(
    project_create: ProjectCreate,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_PROJECT
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create projects"
        )

    project = Project(
        pro_title=project_create.pro_title,
        pro_desc=project_create.pro_desc,
        start_date=project_create.start_date,
        deadline=project_create.deadline
    )

    return ProjectRepository.create_project(
        project,
        db
    )


def update_project(
    pro_id: int,
    project_update: ProjectUpdate,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_PROJECT
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update projects"
        )

    project = ProjectRepository.get_project_by_id(
        pro_id,
        db
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    project.pro_title = project_update.pro_title
    project.pro_desc = project_update.pro_desc
    project.start_date = project_update.start_date

    return ProjectRepository.update_project(
        project,
        db
    )


def delete_project(
    pro_id: int,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_PROJECT
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete projects"
        )

    project = ProjectRepository.get_project_by_id(
        pro_id,
        db
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    ProjectRepository.delete_project(
        project,
        db
    )