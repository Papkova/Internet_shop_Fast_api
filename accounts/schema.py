import peewee
from typing import Any, List
from pydantic import BaseModel, EmailStr
from pydantic.utils import GetterDict


class PeeWeeGetterDict(GetterDict):
    def get(self, key:Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(BaseModel):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
        getter_dict = PeeWeeGetterDict


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Activate(BaseModel):
    email: EmailStr
    token: str

