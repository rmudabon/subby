from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    display_name: str
