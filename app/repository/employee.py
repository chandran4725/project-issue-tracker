from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.employee import Employee


def get_all_employees(db: Session) -> list[Employee]:
    result = db.execute(
        select(Employee)
    )

    return result.scalars().all()


def get_employee_by_id(
    emp_id: int,
    db: Session
) -> Employee | None:

    result = db.execute(
        select(Employee)
        .where(Employee.emp_id == emp_id)
    )

    return result.scalar_one_or_none()


def get_employee_by_clerk_id(
    clerk_emp_id: str,
    db: Session
) -> Employee | None:

    result = db.execute(
        select(Employee)
        .where(Employee.clerk_emp_id == clerk_emp_id)
    )

    return result.scalar_one_or_none()


def get_employee_by_email(
    email: str,
    db: Session
) -> Employee | None:

    result = db.execute(
        select(Employee)
        .where(Employee.email == email)
    )

    return result.scalar_one_or_none()


def create_employee(
    employee: Employee,
    db: Session
) -> Employee:

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


def update_employee(
    employee: Employee,
    db: Session
) -> Employee:

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(
    employee: Employee,
    db: Session
) -> None:

    db.delete(employee)
    db.commit()