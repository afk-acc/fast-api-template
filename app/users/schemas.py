import asyncio
import datetime
from typing import Union, List

from asgiref.sync import async_to_sync
from fastapi import UploadFile
from pydantic import BaseModel, create_model
from pydantic.v1 import EmailStr

from app.users.generated_models import SLanguage


class BaseLocale(BaseModel):
    names: SLanguage


class SPermission(BaseLocale):
    id: int
    system_name: str


class SRole(BaseLocale):
    id: int
    permissions: List[SPermission]


class SCurrentUser(BaseModel):
    id: int
    email: str
    photo: str | None
    lastname: str | None
    name: str | None
    patronymic: str | None
    last_login: datetime.datetime | None
    created_at: datetime.datetime
    is_active: bool
    role: SRole

    class Config:
        from_attributes = True


class SUserAuth(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class SUserUpdate(BaseModel):
    image: UploadFile


class SUser(BaseModel):
    id: int
    email: str
    avatar: str


class SPUserAuth(BaseModel):
    access_token: str
    data: SCurrentUser


class SUserRegister(BaseModel):
    email: str
    password: str
