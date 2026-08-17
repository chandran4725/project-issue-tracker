from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import CurrentUser
from app.auth import permission
from app.auth.permission import Permission
from app.entities.issue import Issues
from app.repository import issue as IssueRepository
from app.repository import employee as EmployeeRepository
from app.repository import project as ProjectRepository
from app.service.employee_service import get_current_employee
from app.schemas.issue import IssueCreate, IssueUpdate


from app.repository import emp_pro_rel as EmpProRelRepository


def get_all_issues(
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

    all_issues = IssueRepository.get_all_issues(db)

    if current_employee.role.role_name == "DEVELOPER":
        user_assignments = EmpProRelRepository.get_employee_projects(current_employee.emp_id, db)
        assigned_pro_ids = {a.pro_id for a in user_assignments}
        return [
            i for i in all_issues
            if i.pro_id in assigned_pro_ids or i.emp_id == current_employee.emp_id
        ]

    return all_issues


def get_issue_by_id(
    issue_id: int,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    issue = IssueRepository.get_issue_by_id(
        issue_id,
        db
    )

    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
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
        if issue.pro_id not in assigned_pro_ids and issue.emp_id != current_employee.emp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied: Issue belongs to an unassigned project"
            )

    return issue


def create_issue(
    issue_create: IssueCreate,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_ISSUE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create issues"
        )

    if current_employee.role.role_name == "DEVELOPER":
        user_assignments = EmpProRelRepository.get_employee_projects(current_employee.emp_id, db)
        assigned_pro_ids = {a.pro_id for a in user_assignments}
        if issue_create.pro_id not in assigned_pro_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create issues for projects assigned to you"
            )

    employee = EmployeeRepository.get_employee_by_id(
        issue_create.emp_id,
        db
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    project = ProjectRepository.get_project_by_id(
        issue_create.pro_id,
        db
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    issue = Issues(
        issue_title=issue_create.issue_title,
        issue_desc=issue_create.issue_desc,
        pro_id=issue_create.pro_id,
        emp_id=issue_create.emp_id,
        status=issue_create.status
    )

    return IssueRepository.create_issue(
        issue,
        db
    )


def update_issue(
    issue_id: int,
    issue_update: IssueUpdate,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    issue = IssueRepository.get_issue_by_id(
        issue_id,
        db
    )

    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )

    if current_employee.role.role_name == "DEVELOPER":
        user_assignments = EmpProRelRepository.get_employee_projects(current_employee.emp_id, db)
        assigned_pro_ids = {a.pro_id for a in user_assignments}
        if issue.pro_id not in assigned_pro_ids and issue.emp_id != current_employee.emp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied: Cannot update issue for unassigned project"
            )

    if current_employee.emp_id != issue.emp_id:

        if not permission.has_permission(
            current_employee.role.role_name,
            Permission.MANAGE_ISSUE
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

    issue.status = issue_update.status

    return IssueRepository.update_issue(
        issue,
        db
    )


def delete_issue(
    issue_id: int,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    issue = IssueRepository.get_issue_by_id(
        issue_id,
        db
    )

    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )

    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_ISSUE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete issues"
        )

    IssueRepository.delete_issue(
        issue,
        db
    )