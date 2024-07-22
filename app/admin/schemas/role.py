from typing import List

from pydantic import BaseModel

from app.repository.generated_models import SLanguage
from app.repository.schemas import SBaseListResponse
from app.users.schemas import SPermission



class SRole(BaseModel):
    names: SLanguage
    id: int
    system_role: bool | None
    permissions: List[SPermission]


class SGRole(SBaseListResponse):
    data: List[SRole]


class SCRole(BaseModel):
    names: SLanguage
    permission_ids: List[int]


class SURole(BaseModel):
    names: SLanguage
    new_permission_ids: List[int]
    remove_permission_ids: List[int]
