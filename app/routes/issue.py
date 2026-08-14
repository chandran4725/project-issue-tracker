from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.auth import CurrentUser, get_current_user
from app.schemas.issue import (
    IssueCreate,
    IssueUpdate,
    IssueResponse
)
from app.service import issue_service
from app.util.database import get_db


router = APIRouter(
    prefix="/api/issues",
    tags=["Issues"]
)


@router.get(
    "",
    response_model=list[IssueResponse],
    status_code=status.HTTP_200_OK
)
def get_all_issues(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return issue_service.get_all_issues(
        current_user,
        db
    )


@router.get(
    "/{issue_id}",
    response_model=IssueResponse,
    status_code=status.HTTP_200_OK
)
def get_issue(
    issue_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return issue_service.get_issue_by_id(
        issue_id,
        current_user,
        db
    )


@router.post(
    "",
    response_model=IssueResponse,
    status_code=status.HTTP_201_CREATED
)
def create_issue(
    issue_create: IssueCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return issue_service.create_issue(
        issue_create,
        current_user,
        db
    )


@router.patch(
    "/{issue_id}",
    response_model=IssueResponse,
    status_code=status.HTTP_200_OK
)
def update_issue(
    issue_id: int,
    issue_update: IssueUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return issue_service.update_issue(
        issue_id,
        issue_update,
        current_user,
        db
    )


@router.delete(
    "/{issue_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_issue(
    issue_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    issue_service.delete_issue(
        issue_id,
        current_user,
        db
    )