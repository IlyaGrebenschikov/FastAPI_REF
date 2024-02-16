import jwt
from datetime import datetime, timedelta
from src.core import get_settings
from functools import lru_cache


class Auth:

    @staticmethod
    def create_jwt_token(data: dict):
        expiration = datetime.utcnow() + timedelta(minutes=30)
        data.update({"exp": expiration})
        token = jwt.encode(data, get_settings().secret.secret_key, algorithm=get_settings().secret.secret_algh)
        return token

    @staticmethod
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


@lru_cache(typed=True)
def get_auth_settings() -> Auth:
    return Auth()
