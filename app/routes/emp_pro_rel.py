from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.auth import CurrentUser, get_current_user
from app.schemas.emp_pro_rel import (
    EmpProRelCreate,
    EmpProRelResponse
)
from app.service import emp_pro_rel_service
from app.util.database import get_db


router = APIRouter(
    prefix="/api/assignments",
    tags=["Employee Projects"]
)


@router.get(
    "",
    response_model=list[EmpProRelResponse],
    status_code=status.HTTP_200_OK
)
def get_all_assignments(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return emp_pro_rel_service.get_all_assignments(
        current_user,
        db
    )


@router.get(
    "/{emp_id}/{pro_id}",
    response_model=EmpProRelResponse,
    status_code=status.HTTP_200_OK
)
def get_assignment(
    emp_id: int,
    pro_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return emp_pro_rel_service.get_assignment(
        emp_id,
        pro_id,
        current_user,
        db
    )


@router.post(
    "",
    response_model=EmpProRelResponse,
    status_code=status.HTTP_201_CREATED
)
def create_assignment(
    assignment_create: EmpProRelCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return emp_pro_rel_service.create_assignment(
        assignment_create,
        current_user,
        db
    )


@router.delete(
    "/{emp_id}/{pro_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_assignment(
    emp_id: int,
    pro_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    emp_pro_rel_service.delete_assignment(
        emp_id,
        pro_id,
        current_user,
        db
    )