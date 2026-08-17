from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import CurrentUser
from app.auth import permission
from app.auth.permission import Permission
from app.entities.emp_pro_rel import EmpProRel
from app.repository import emp_pro_rel as EmpProRelRepository
from app.repository import employee as EmployeeRepository
from app.repository import project as ProjectRepository
from app.service.employee_service import get_current_employee
from app.schemas.emp_pro_rel import EmpProRelCreate


def get_all_assignments(
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

    if current_employee.role.role_name == "DEVELOPER":
        return EmpProRelRepository.get_employee_projects(current_employee.emp_id, db)

    return EmpProRelRepository.get_all_assignments(db)


def get_assignment(
    emp_id: int,
    pro_id: int,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    assignment = EmpProRelRepository.get_assignment(
        emp_id,
        pro_id,
        db
    )

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    if permission.has_permission(
        current_employee.role.role_name,
        Permission.VIEW
    ):
        return assignment

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Permission denied"
    )


def create_assignment(
    assignment_create: EmpProRelCreate,
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
            detail="You don't have permission to assign employees"
        )

    employee = EmployeeRepository.get_employee_by_id(
        assignment_create.emp_id,
        db
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    project = ProjectRepository.get_project_by_id(
        assignment_create.pro_id,
        db
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    existing = EmpProRelRepository.get_assignment(
        assignment_create.emp_id,
        assignment_create.pro_id,
        db
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee is already assigned to this project"
        )

    assignment = EmpProRel(
        emp_id=assignment_create.emp_id,
        pro_id=assignment_create.pro_id
    )

    return EmpProRelRepository.create_assignment(
        assignment,
        db
    )


def delete_assignment(
    emp_id: int,
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
            detail="You don't have permission to remove assignments"
        )

    assignment = EmpProRelRepository.get_assignment(
        emp_id,
        pro_id,
        db
    )

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    try:
        EmpProRelRepository.delete_assignment(
            assignment,
            db
        )
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to remove assignment: {str(exc)}"
        )