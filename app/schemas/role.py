from pydantic import BaseModel, ConfigDict, Field


class RoleBase(BaseModel):
    role_name: str = Field(
        min_length=3,
        max_length=50
    )


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    role_name: str = Field(
        min_length=3,
        max_length=50
    )


class RoleResponse(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    role_id: int