from sqlalchemy import INTEGER, VARCHAR, TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.util.database import Base


class Issues(Base):
    __tablename__ = "issue"

    issue_id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True
    )

    issue_title: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False
    )

    issue_desc: Mapped[str] = mapped_column(
        TEXT,
        nullable=False
    )

    pro_id: Mapped[int] = mapped_column(
        INTEGER,
        ForeignKey("project.pro_id"),
        nullable=False
    )

    emp_id: Mapped[int] = mapped_column(
        INTEGER,
        ForeignKey("employee.emp_id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        VARCHAR(20),
        nullable=False,
        default="PENDING"
    )

    project: Mapped["Project"] = relationship( # type: ignore
        "Project"
    )

    employee: Mapped["Employee"] = relationship( # type: ignore
        "Employee"
    )