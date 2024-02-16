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

    @staticmethod
    def create_jwt_token(data: dict):
        expiration = datetime.utcnow() + timedelta(minutes=30)
        data.update({"exp": expiration})
        token = jwt.encode(data, Secret.create_secret_key(), algorithm=Secret.get_algh())
        return token

    @staticmethod
    def verify_jwt_token(token: str):
        try:
            decoded_data = jwt.decode(token, Secret.create_secret_key(), algorithms=[Secret.get_algh()])
            return decoded_data
        except jwt.PyJWTError:
            return None


def get_auth_settings() -> Auth:
    return Auth()

# print(get_auth_settings().verify_jwt_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJzY29wZXMiOltdLCJleHAiOjE3MDgxMDA3OTR9.nW3Iw6zESVhZsQexplztRNeK8r3iNfNBZL2hFKdVa0s'))