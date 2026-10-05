from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
    model_validator,
)

from .helpers import find_invalid_null_fields


class UserCreate(BaseModel):
    email: EmailStr = Field(...)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(default=None)
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)

    @model_validator(mode="after")
    def reject_null_for_required_fields(self):
        invalid_fields = find_invalid_null_fields(self)
        if invalid_fields:
            field_names = ", ".join(sorted(invalid_fields))
            raise ValueError(f"{field_names} must not be null")

        return self


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str = Field(exclude=True)
    last_name: str = Field(exclude=True)

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
