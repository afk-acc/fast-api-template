import datetime
from typing import Union, List

from fastapi import UploadFile
from pydantic import BaseModel
from pydantic.v1 import EmailStr


class SUserRegister(BaseModel):
    email: str
    password: str




class SUserAuth(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class SUserUpdate(BaseModel):
    image: UploadFile


class SRole(BaseModel):
    id: int
    name: str


class SCurrentUser(BaseModel):
    id: int
    email: str
    avatar: Union[str, None]
    role: SRole
    class Config:
        from_attributes = True

class SUser(BaseModel):
    id: int
    email: str
    avatar: str
