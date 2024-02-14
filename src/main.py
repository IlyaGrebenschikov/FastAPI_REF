from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.security import get_auth_settings

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# @app.post("/register")
# def register_user(username: str, password: str):
#     hashed_password = pwd_context.hash(password)
#     return {"username": username, "hashed_password": hashed_password}


print(a := pwd_context.hash('12345'))
print(pwd_context.verify('12345', a))

