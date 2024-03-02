from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator
from pydantic import Field


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    referred_by: Optional[str] = Field(default='string or null')

    @field_validator("password")
    def check_password(cls, value):
        value = str(value)
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")
        return value


class UserInDB(BaseModel):
    name: str
    email: str
    hashed_password: str
    referred_by: Optional[str]
