from . import models, schema
from .utils import Hash


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(create_user: schema.UserCreate):
    hashed_password = Hash.bcpypt(create_user.password)
    db_user = models.User(email= create_user.email, hashed_password=hashed_password, is_active=False, is_admin=False)
    db_user.save()
    return db_user