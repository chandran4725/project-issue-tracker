from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import CurrentUser
from app.auth import permission
from app.entities.employee import Employee
from app.repository import employee as EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.auth.permission import Permission
from app.service.clerk_service import invite_employee
from app.repository import role as RoleRepository


def get_current_employee(
    current_user: CurrentUser,
    db: Session,
) -> Employee:

    # 1. Lookup by clerk_emp_id
    employee = EmployeeRepository.get_employee_by_clerk_id(
        current_user.user_id,
        db
    )

    # 2. If not found by clerk_emp_id, try to match by user email
    if not employee and current_user.email:
        employee = EmployeeRepository.get_employee_by_email(
            current_user.email,
            db
        )
        if employee:
            employee.clerk_emp_id = current_user.user_id
            EmployeeRepository.update_employee(employee, db)

    # 3. If still not found, create new Employee with default ADMIN role for self-registered user
    if not employee and current_user.email:
        admin_role = RoleRepository.get_role_by_name("ADMIN", db)
        role_id = admin_role.role_id if admin_role else 1
        emp_name = current_user.email.split("@")[0]
        new_emp = Employee(
            name=emp_name,
            email=current_user.email,
            role_id=role_id,
            clerk_emp_id=current_user.user_id
        )
        employee = EmployeeRepository.create_employee(new_emp, db)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee Profile Not Found"
        )

    return employee


def sync_clerk_employee(
    email: str | None,
    name: str | None,
    current_user: CurrentUser,
    db: Session
) -> Employee:
    target_email = email or current_user.email

    # 1. Lookup by target email FIRST (crucial for invited employees where clerk_emp_id is NULL)
    if target_email:
        employee = EmployeeRepository.get_employee_by_email(target_email, db)
        if employee:
            if employee.clerk_emp_id != current_user.user_id:
                employee.clerk_emp_id = current_user.user_id
            if name and not employee.name:
                employee.name = name
            EmployeeRepository.update_employee(employee, db)
            return employee

    # 2. Lookup by clerk_emp_id
    employee = EmployeeRepository.get_employee_by_clerk_id(current_user.user_id, db)
    if employee:
        return employee

    # 3. Auto-create Employee for self-signup user (default role: ADMIN)
    if target_email:
        admin_role = RoleRepository.get_role_by_name("ADMIN", db)
        role_id = admin_role.role_id if admin_role else 1
        emp_name = name or target_email.split("@")[0]

        new_emp = Employee(
            name=emp_name,
            email=target_email,
            role_id=role_id,
            clerk_emp_id=current_user.user_id
        )
        return EmployeeRepository.create_employee(new_emp, db)

    return get_current_employee(current_user, db)


def get_all_employees(
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

    return EmployeeRepository.get_all_employees(db)


def get_employee_by_id(
    emp_id: int,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    employee = EmployeeRepository.get_employee_by_id(
        emp_id,
        db
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    if permission.has_permission(
        current_employee.role.role_name,
        Permission.VIEW
    ):
        return employee

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Permission denied"
    )


def create_employee(
    employee_create: EmployeeCreate,
    current_user: CurrentUser,
    db: Session
):

    current_employee = get_current_employee(
        current_user,
        db
    )

    # RBAC
    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_EMPLOYEE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create employees"
        )

    # Check local database
    existing = EmployeeRepository.get_employee_by_email(
        employee_create.email,
        db
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this email already exists"
        )

    # Validate role
    role = RoleRepository.get_role_by_id(employee_create.role_id, db)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role not found with the specified role_id"
        )

    # Send Clerk invitation (safely non-blocking for DB creation)
    try:
        invite_employee(
            email=employee_create.email
        )
    except Exception as err:
        print(f"Warning: Clerk invitation error: {err}")

    # Create local employee
    employee = Employee(
        name=employee_create.name,
        email=employee_create.email,
        role_id=employee_create.role_id,
        clerk_emp_id=None
    )

    created = EmployeeRepository.create_employee(
        employee,
        db
    )

    return EmployeeRepository.get_employee_by_id(created.emp_id, db)
    
def update_employee(
    emp_id: int,
    employee_update: EmployeeUpdate,
    current_user: CurrentUser,
    db: Session
):
    current_employee = get_current_employee(
        current_user,
        db
    )
    
    employee = EmployeeRepository.get_employee_by_id(
        emp_id,
        db
    )
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee Not Found"
        )
        
    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_EMPLOYEE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission Denied"
        )
        
    if employee_update.name is not None:
        employee.name = employee_update.name
    if employee_update.role_id is not None:
        employee.role_id = employee_update.role_id
            
    EmployeeRepository.update_employee(employee, db)
    return EmployeeRepository.get_employee_by_id(employee.emp_id, db)

def delete_employee(
    emp_id: int,
    current_user: CurrentUser,
    db: Session
):
    current_employee = get_current_employee(
        current_user,
        db
    )
    
    employee = EmployeeRepository.get_employee_by_id(emp_id, db)
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee Not Found"
        )
    
    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_EMPLOYEE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission Denied"
        )
        
    if current_employee.emp_id == emp_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own active employee profile"
        )

    try:
        from app.repository import emp_pro_rel as EmpProRelRepository
        from app.repository import issue as IssueRepository

        # Delete dependent assignments
        assignments = EmpProRelRepository.get_employee_projects(emp_id, db)
        for assign in assignments:
            EmpProRelRepository.delete_assignment(assign, db)

        # Delete dependent issues
        issues = IssueRepository.get_issues_by_employee(emp_id, db)
        for iss in issues:
            IssueRepository.delete_issue(iss, db)

        EmployeeRepository.delete_employee(employee, db)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete employee: {str(exc)}"
        )
        
