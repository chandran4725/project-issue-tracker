from sqlalchemy import INTEGER, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.util.database import Base


class Role(Base):
    __tablename__ = "role"

    role_id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True
    )

    role_name: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False,
        unique=True
    )

    employees: Mapped[list["Employee"]] = relationship( # type: ignore
        "Employee",
        back_populates="role"
    )