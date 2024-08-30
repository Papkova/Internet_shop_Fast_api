import jwt
import schema
import settings
import cruds
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from . import authenticate_user
from .authentication import get_current_user
from starlette.responses import JSONResponse
from .utils import get_from_redis, delete_token_redis, token_add_redis

router = APIRouter(
    tags=['Accounts'],
    prefix="/accounts"
)


@router.post("/token", dependencies=[Depends(get_db())])
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    user = {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin
    }

    token = jwt.encode(user, settings.JWT_SECRET)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/user/me", response_model=schema.User, dependencies=[Depends(get_db())])
async def detail_user(user: schema.User = Depends(get_current_user())):
    return user


@router.post("/user/", response_model=schema.User, dependencies=Depends(get_db()))
async def register(user: schema.UserCreate):
    user_db = cruds.get_user_by_email(email=user.email)
    if user_db:
        raise HTTPException(status_code=400, detail="email already exists")
    user = cruds.create_user(user)
    return user


@router.post("/user/activate/", dependencies=Depends(get_db()))
async def activate(data: schema.Activate):
    user = cruds.get_user_by_email(email=data.email)
    content = {"massage": "Wrong token"}
    response = JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
    if not user:
        return response
    token_redis = get_from_redis(user.id, "register")
    if not token_redis:
        return response

    if data.token != token_redis.decode("UTF-8"):
        return response

    user.is_active = True
    user.save()

    delete_token_redis(user.id, "register")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"massage": "Active account"})


@router.put("/user/change_password",dependencies=[Depends(get_db)])
async def change_password(data: schema.ChangePassword, user: schema.User = Depends(get_current_user())):
    if Hash.verify(data.old_password, user.hashed_password):
        user.hashed_password = Hash.bcpypt(data.new_password)
        user.save()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User password changed"})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Old password is incorrect"})

