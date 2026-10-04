from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, computed_field


class UserCreate(BaseModel):
    email: EmailStr = Field(...)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    password: SecretStr = Field(...)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str = Field(exclude=True)
    last_name: str = Field(exclude=True)

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
