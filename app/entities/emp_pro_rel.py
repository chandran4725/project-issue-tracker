from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.util.database import Base


class EmpProRel(Base):
    __tablename__ = "emp_pro_rel"

    emp_id: Mapped[int] = mapped_column(
        ForeignKey("employee.emp_id"),
        primary_key=True
    )

    pro_id: Mapped[int] = mapped_column(
        ForeignKey("project.pro_id"),
        primary_key=True
    )

    employee: Mapped["Employee"] = relationship( # type: ignore
        "Employee",
        back_populates="project_assignments"
    )

    project: Mapped["Project"] = relationship( # type: ignore
        "Project",
        back_populates="employee_assignments"
    )