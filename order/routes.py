from fastapi import APIRouter
from accounts import User
from fastapi import Depends

router = APIRouter(
    tags=['carts'],
    prefix='/carts'
)


@router.get('/list')
async def carts(user: User = Depends()):
    pass