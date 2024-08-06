import os
import datetime
import jwt
from flask import request

SECRET_KEY = os.environ.get("SECRET_KEY")


class UserObject:
    def __init__(self, user_id, nickname):
        self.user_id = user_id
        self.nickname = nickname

    def to_dict(self):
        """Convert UserObject to a dictionary."""
        return {"user_id": self.user_id, "nickname": self.nickname}


def create_access_token(user_obj):
    """Create JWT access token"""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    token = jwt.encode(
        {**user_obj.to_dict(), "exp": expiration}, SECRET_KEY, algorithm="HS256"
    )
    return token


def decode_access_token(token):
    """Decode JWT access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_dict = UserObject(payload["user_id"], payload["nickname"]).to_dict()
        return user_dict, None
    except jwt.ExpiredSignatureError:
        return None, "Token has expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"


def get_token_from_header():
    """Extracts the token from the Authorization header"""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        return token
    return None
