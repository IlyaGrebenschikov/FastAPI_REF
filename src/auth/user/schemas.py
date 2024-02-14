from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator


class User(BaseModel):
    name: str
    email: EmailStr
    password: str

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


if __name__ == '__main__':
    user = User(name='Ilya', email='ilushagr22@mail.com', password='Qwaszxedcrtfgv1')
    print(user)
