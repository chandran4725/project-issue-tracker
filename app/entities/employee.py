from sqlalchemy import VARCHAR, INTEGER, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.util.database import Base


class Employee(Base):
    __tablename__ = "employee"

    emp_id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True
    )

    clerk_emp_id: Mapped[str | None] = mapped_column(
        VARCHAR(255),
        nullable=True,
        unique=True
    )

    name: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        unique=True
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.role_id"),
        nullable=False
    )

    role: Mapped["Role"] = relationship(  # type: ignore
        "Role",
        back_populates="employees"
    )
    
    project_assignments: Mapped[list["EmpProRel"]] = relationship( # type: ignore
    "EmpProRel",
    back_populates="employee"
    )