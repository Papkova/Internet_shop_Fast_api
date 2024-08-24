import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from . import models, Hash


oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')


def authenticate_user(email: str, password: str):
    user = models.User.filter(models.User.email == email).first()
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is not active')
    if not user:
        return False
    if not Hash.verify(password, user.hashed_password):
        return False
    return user