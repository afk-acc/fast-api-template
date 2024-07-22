from typing import List

from pydantic import BaseModel

from app.repository.schemas import SBaseListResponse
from app.users.schemas import SCurrentUser


class SGUser(SBaseListResponse):
    data: List[SCurrentUser]


class SUUser(BaseModel):
    role_id: int
