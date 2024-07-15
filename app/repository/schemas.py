from pydantic import BaseModel

from app.repository.generated_models import SLanguage


class SBaseListResponse(BaseModel):
    page: int
    total: int
    limit: int
    data: list

class BaseLocale(BaseModel):
    names: SLanguage