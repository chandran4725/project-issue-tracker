from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.role import Role


def get_all_roles(db: Session) -> list[Role]:
    result = db.execute(
        select(Role)
    )

    return result.scalars().all()


def get_role_by_id(
    role_id: int,
    db: Session
) -> Role | None:

    result = db.execute(
        select(Role)
        .where(Role.role_id == role_id)
    )

    return result.scalar_one_or_none()


def get_role_by_name(
    role_name: str,
    db: Session
) -> Role | None:

    result = db.execute(
        select(Role)
        .where(Role.role_name == role_name)
    )

    return result.scalar_one_or_none()


def create_role(
    role: Role,
    db: Session
) -> Role:

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


def update_role(
    role: Role,
    db: Session
) -> Role:

    db.commit()
    db.refresh(role)

    return role


def delete_role(
    role: Role,
    db: Session
) -> None:

    db.delete(role)
    db.commit()