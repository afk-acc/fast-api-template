import datetime
from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel
from app.repository.generated_models import SLanguage
from app.repository.schemas import BaseLocale


class SPermission(BaseLocale):
    id: int
    system_name: str
    names: SLanguage


class SRole(BaseLocale):
    id: int
    names: SLanguage
    system_name: str

class SPRole(SRole):
    permissions: List[SPermission]

class SUUser(BaseModel):
    lastname: str | None
    name: str | None
    patronymic: str | None


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
    role: SPRole

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
    # avatar: Optional[str]
    lastname: Optional[str]
    name: Optional[str]
    patronymic: Optional[str]
    role: SRole

class SPUserAuth(BaseModel):
    access_token: str
    data: SCurrentUser


class SUserRegister(BaseModel):
    email: str
    password: str


