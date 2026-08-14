from datetime import date

from sqlalchemy import INTEGER, VARCHAR, DATE, TEXT
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.util.database import Base


class Project(Base):
    __tablename__ = "project"

    pro_id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True
    )

    pro_title: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False
    )

    pro_desc: Mapped[str] = mapped_column(
        TEXT,
        nullable=False
    )

    start_date: Mapped[date] = mapped_column(
        DATE,
        nullable=False
    )

    deadline: Mapped[date] = mapped_column(
        DATE,
        nullable=False
    )
    
    employee_assignments: Mapped[list["EmpProRel"]] = relationship( # type: ignore
    "EmpProRel",
    back_populates="project"
    )