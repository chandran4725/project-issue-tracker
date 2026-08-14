from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProjectBase(BaseModel):
    pro_title: str = Field(
        min_length=4,
        max_length=100
    )

    pro_desc: str = Field(
        min_length=1
    )


class ProjectCreate(ProjectBase):
    start_date: date
    deadline: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date > self.deadline:
            raise ValueError(
                "Start date cannot be after deadline"
            )

        return self


class ProjectUpdate(BaseModel):
    pro_title: str | None = Field(
        default=None,
        min_length=4,
        max_length=100
    )

    pro_desc: str | None = Field(
        default=None,
        min_length=1
    )

    start_date: date | None = None
    deadline: date | None = None


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    pro_id: int
    start_date: date
    deadline: date