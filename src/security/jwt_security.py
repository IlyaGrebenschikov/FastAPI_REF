from datetime import datetime, timedelta

import jwt

from src.core.settings import get_secret_settings


def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + timedelta(minutes=get_secret_settings().jwt_expiration)
    data.update({"exp": expiration})
    token = jwt.encode(data, get_secret_settings().secret_key, algorithm=get_secret_settings().secret_algh)
    return token


def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(
            token,
            get_secret_settings().secret_key,
            algorithms=[get_secret_settings().secret_algh]
        )
        return decoded_data
    except jwt.PyJWTError:
        return None
