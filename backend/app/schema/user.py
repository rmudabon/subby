from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str = Field(exclude=True)
    last_name: str = Field(exclude=True)

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
