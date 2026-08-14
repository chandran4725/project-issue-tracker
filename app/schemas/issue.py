from pydantic import BaseModel, ConfigDict, Field

from app.enums.issue_status import IssueStatus


class IssueBase(BaseModel):
    issue_title: str = Field(
        min_length=3,
        max_length=100
    )

    issue_desc: str = Field(
        min_length=1
    )


class IssueCreate(IssueBase):
    pro_id: int = Field(gt=0)
    emp_id: int = Field(gt=0)
    status: IssueStatus

class IssueUpdate(BaseModel):
    status: IssueStatus


class IssueResponse(IssueBase):
    model_config = ConfigDict(from_attributes=True)

    issue_id: int
    pro_id: int
    emp_id: int
    status: IssueStatus