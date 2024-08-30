import os
import jwt
import settings
import redis
import binascii
from passlib.context import CryptContext


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcpypt(self, password: str):
        return pwd_ctx.hash(password)

    def verify(self, plain_password: str, hashed_password: str):
        return pwd_ctx.verify(plain_password, hashed_password)


redis = redis.Redis().from_url("redis://")


def _generate_code():
    return binascii.hexlify(os.urandom(20)).decode("utf-8")


def get_user_from_payload(token, models):
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
    user = models.User.filter(models.User.id == payload.get("id")).first()
    return user


def get_from_redis(id, mode):
    name = f"{id}_{mode.lower()}"
    return redis.get(name=name)


def token_add_redis(id, mode):
    token = _generate_code()
    name = f"{id}_{mode.lower()}"
    redis.set(name=name, value=token, ex=14000)
    return token


def delete_token_redis(id, mode):
    name = f"{id}_{mode.lower()}"
    redis.delete(name=name)

