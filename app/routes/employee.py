from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from fastapi import Cookie

from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)
from app.service import employee_service
from app.auth.auth import CurrentUser, get_current_user
from app.util.database import get_db


from pydantic import BaseModel


class SyncClerkRequest(BaseModel):
    email: str | None = None
    name: str | None = None


router = APIRouter(
    prefix="/api/employee",
    tags=["employee"]
)


@router.post(
    "/sync-clerk",
    response_model=EmployeeResponse
)
def sync_clerk_employee(
    payload: SyncClerkRequest | None = None,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    email = payload.email if payload else None
    name = payload.name if payload else None
    return employee_service.sync_clerk_employee(
        email,
        name,
        current_user,
        db
    )


@router.get(
    "",
    response_model=list[EmployeeResponse]
)
def get_all_employees(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return employee_service.get_all_employees(
        current_user,
        db
    )


@router.get(
    "/{emp_id}",
    response_model=EmployeeResponse
)
def get_employee(
    emp_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return employee_service.get_employee_by_id(
        emp_id,
        current_user,
        db
    )


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee_create: EmployeeCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return employee_service.create_employee(
        employee_create,
        current_user,
        db
    )

@router.patch(
    "/{emp_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK
)
def update_employee(
    emp_id: int,
    employee_update: EmployeeUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return employee_service.update_employee(
        emp_id,
        employee_update,
        current_user,
        db
    )
    
@router.delete(
    "/{emp_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_employee(
    emp_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return employee_service.delete_employee(
        emp_id,
        current_user,
        db
    )