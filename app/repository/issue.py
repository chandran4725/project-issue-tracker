from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.issue import Issues


def get_all_issues(
    db: Session
) -> list[Issues]:

    result = db.execute(
        select(Issues)
    )

    return result.scalars().all()


def get_issue_by_id(
    issue_id: int,
    db: Session
) -> Issues | None:

    result = db.execute(
        select(Issues)
        .where(Issues.issue_id == issue_id)
    )

    return result.scalar_one_or_none()


def get_issues_by_employee(
    emp_id: int,
    db: Session
) -> list[Issues]:

    result = db.execute(
        select(Issues)
        .where(Issues.emp_id == emp_id)
    )

    return result.scalars().all()


def get_issues_by_project(
    pro_id: int,
    db: Session
) -> list[Issues]:

    result = db.execute(
        select(Issues)
        .where(Issues.pro_id == pro_id)
    )

    return result.scalars().all()


def create_issue(
    issue: Issues,
    db: Session
) -> Issues:

    db.add(issue)
    db.commit()
    db.refresh(issue)

    return issue


def update_issue(
    issue: Issues,
    db: Session
) -> Issues:

    db.commit()
    db.refresh(issue)

    return issue


def delete_issue(
    issue: Issues,
    db: Session
) -> None:

    db.delete(issue)
    db.commit()