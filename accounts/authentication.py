import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status

import settings
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

def get_current_user(token: str = Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        user = models.User.filter(models.User.id == payload.get("id")).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Protected"
        )
    return user


def get_current_user_admin(token: str = Depends(oauth_scheme)):
    try:
        user = get_user_from_payload(token, models)
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Protected"
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="In"
        )
    return user
