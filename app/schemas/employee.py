from pydantic import BaseModel, Field, ConfigDict, EmailStr

from app.schemas.role import RoleResponse


class EmployeeBase(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr


class EmployeeCreate(EmployeeBase):
    role_id: int = Field(
        gt=0
    )


class EmployeeUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=50
    )

    role_id: int | None = Field(
        default=None,
        gt=0
    )


class EmployeeResponse(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)

    emp_id: int
    clerk_emp_id: str | None
    role: RoleResponse