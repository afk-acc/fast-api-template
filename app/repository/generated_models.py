from pydantic import BaseModel


class SLanguage(BaseModel):
    ru: str | None
    uz: str | None
    en: str | None
