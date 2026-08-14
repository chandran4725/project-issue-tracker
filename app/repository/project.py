from sqlalchemy import select
from sqlalchemy.orm import Session

from app.entities.project import Project


def get_all_projects(db: Session) -> list[Project]:
    result = db.execute(
        select(Project)
    )

    return result.scalars().all()


def get_project_by_id(
    pro_id: int,
    db: Session
) -> Project | None:

    result = db.execute(
        select(Project)
        .where(Project.pro_id == pro_id)
    )

    return result.scalar_one_or_none()


def create_project(
    project: Project,
    db: Session
) -> Project:

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def update_project(
    project: Project,
    db: Session
) -> Project:

    db.commit()
    db.refresh(project)

    return project


def delete_project(
    project: Project,
    db: Session
) -> None:

    db.delete(project)
    db.commit()