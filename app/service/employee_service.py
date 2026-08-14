from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import CurrentUser
from app.auth import permission
from app.entities.employee import Employee
from app.repository import employee as EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.auth.permission import Permission
from app.service.clerk_service import invite_employee


def get_current_employee(
    current_user: CurrentUser,
    db: Session,
    email: str | None
) -> Employee:

    employee = EmployeeRepository.get_employee_by_clerk_id(
        current_user.user_id,
        db
    )

    if not employee:
        employee = EmployeeRepository.get_employee_by_email(email,db)
        print(email)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee Profile Not Found"
            )
        employee.clerk_emp_id = current_user.user_id
        print(employee.email)
        return EmployeeRepository.update_employee(employee,db)
    
    

    return employee


def get_all_employees(
    current_user: CurrentUser,
    db: Session,
    email: str | None
):

    current_employee = get_current_employee(
        current_user,
        db,
        email
    )

    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_EMPLOYEE
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

    # Employee can view their own profile
    if current_employee.emp_id == employee.emp_id:
        return employee

    # Admin/Manager can view other employees
    if permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_EMPLOYEE
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

    # Send Clerk invitation
    invite_employee(
        email=employee_create.email
    )

    # Create local employee
    employee = Employee(
        name=employee_create.name,
        email=employee_create.email,
        role_id=employee_create.role_id,
        clerk_emp_id=None
    )

    return EmployeeRepository.create_employee(
        employee,
        db
    )
    
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
        
    if current_employee.emp_id == employee.emp_id:
        employee.name = employee_update.name
        employee.role_id = employee_update.role_id
        
        return EmployeeRepository.update_employee(employee,db)
    
    if not permission.has_permission(
        current_employee.role.role_name,
        Permission.MANAGE_EMPLOYEE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission Denied"
        )
        
    employee.name = employee_update.name
    employee.role_id = employee_update.role_id
            
    return EmployeeRepository.update_employee(employee,db)

def delete_employee(
    emp_id: int,
    current_user: CurrentUser,
    db: Session
):
    current_employee = get_current_employee(
        current_user,
        db
    )
    
    employee = EmployeeRepository.get_employee_by_id(emp_id,db)
    
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
        
    return EmployeeRepository.delete_employee(employee,db)
        
