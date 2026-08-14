from pydantic import BaseModel, ConfigDict

from app.schemas.employee import EmployeeResponse
from app.schemas.project import ProjectResponse


class EmpProRelBase(BaseModel):
    emp_id: int
    pro_id: int


class EmpProRelCreate(EmpProRelBase):
    pass


class EmpProRelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    emp_id: int
    pro_id: int
    employee: EmployeeResponse
    project: ProjectResponse