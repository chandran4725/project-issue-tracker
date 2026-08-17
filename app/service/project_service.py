from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import CurrentUser
from app.auth import permission
from app.auth.permission import Permission
from app.entities.project import Project
from app.repository import project as ProjectRepository
from app.service.employee_service import get_current_employee
from app.schemas.project import ProjectCreate, ProjectUpdate


from app.repository import emp_pro_rel as EmpProRelRepository


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

    all_projects = ProjectRepository.get_all_projects(db)

    if current_employee.role.role_name == "DEVELOPER":
        user_assignments = EmpProRelRepository.get_employee_projects(current_employee.emp_id, db)
        assigned_pro_ids = {a.pro_id for a in user_assignments}
        return [p for p in all_projects if p.pro_id in assigned_pro_ids]

    return all_projects


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

    if current_employee.role.role_name == "DEVELOPER":
        user_assignments = EmpProRelRepository.get_employee_projects(current_employee.emp_id, db)
        assigned_pro_ids = {a.pro_id for a in user_assignments}
        if pro_id not in assigned_pro_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not assigned to this project"
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

    try:
        from app.repository import issue as IssueRepository

        # Delete dependent assignments
        project_assignments = EmpProRelRepository.get_project_employees(pro_id, db)
        for assign in project_assignments:
            EmpProRelRepository.delete_assignment(assign, db)

        # Delete dependent issues
        project_issues = IssueRepository.get_issues_by_project(pro_id, db)
        for iss in project_issues:
            IssueRepository.delete_issue(iss, db)

        ProjectRepository.delete_project(
            project,
            db
        )
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete project: {str(exc)}"
        )