from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.emp_pro_rel import EmpProRel


def get_all_assignments(
    db: Session
) -> list[EmpProRel]:

    result = db.execute(
        select(EmpProRel)
    )

    return result.scalars().all()


def get_assignment(
    emp_id: int,
    pro_id: int,
    db: Session
) -> EmpProRel | None:

    result = db.execute(
        select(EmpProRel)
        .where(
            EmpProRel.emp_id == emp_id,
            EmpProRel.pro_id == pro_id
        )
    )

    return result.scalar_one_or_none()


def get_employee_projects(
    emp_id: int,
    db: Session
) -> list[EmpProRel]:

    result = db.execute(
        select(EmpProRel)
        .where(EmpProRel.emp_id == emp_id)
    )

    return result.scalars().all()


def get_project_employees(
    pro_id: int,
    db: Session
) -> list[EmpProRel]:

    result = db.execute(
        select(EmpProRel)
        .where(EmpProRel.pro_id == pro_id)
    )

    return result.scalars().all()


def create_assignment(
    assignment: EmpProRel,
    db: Session
) -> EmpProRel:

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


def delete_assignment(
    assignment: EmpProRel,
    db: Session
) -> None:

    db.delete(assignment)
    db.commit()