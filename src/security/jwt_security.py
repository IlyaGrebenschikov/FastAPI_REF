from datetime import datetime
from datetime import timedelta

import jwt

from src.core import get_settings


def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + timedelta(minutes=30)
    data.update({"exp": expiration})
    token = jwt.encode(data, get_settings().secret.secret_key, algorithm=get_settings().secret.secret_algh)
    return token


def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(
            token,
            get_settings().secret.secret_key,
            algorithms=[get_settings().secret.secret_algh]
        )
        return decoded_data
    except jwt.PyJWTError:
        return None
