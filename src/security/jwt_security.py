import jwt
import secrets
from datetime import datetime, timedelta


class Secret:
    @staticmethod
    def create_secret_key() -> str:
        return secrets.token_hex(32)

    @staticmethod
    def get_algh() -> str:
        return 'HS256'


def get_secret() -> Secret:
    return Secret()


class Auth:
    def __init__(self):
        self.secret_key = Secret.create_secret_key()
        self.algh = Secret.get_algh()
        self.expiration_time = timedelta(minutes=30)

    def create_jwt_token(self, data: dict):
        expiration = datetime.utcnow() + self.expiration_time
        data.update({"exp": expiration})
        token = jwt.encode(data, self.secret_key, algorithm=self.algh)
        return token

    def verify_jwt_token(self, token: str):
        try:
            decoded_data = jwt.decode(token, self.secret_key, algorithms=[self.algh])
            return decoded_data
        except jwt.PyJWTError:
            return None


def get_auth_settings() -> Auth:
    return Auth()
