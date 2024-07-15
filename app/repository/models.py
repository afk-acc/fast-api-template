from pydantic import create_model

from app.repository.base import Base
from app.database import async_session_maker
from sqlalchemy import insert
from sqlalchemy.orm import Mapped


class Language(Base):
    code: Mapped[str]
    name: Mapped[str]

    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls).values(**data).returning(cls)
            res = await session.execute(query)
            await session.commit()
            DynamicModel = await get_dynamic_model()
            with open("app/repository/generated_models.py", "w") as f:
                f.write("from pydantic import BaseModel\n\n")
                f.write(f"class S{cls.__name__}(BaseModel):\n")
                for field_name, field_type in DynamicModel.__annotations__.items():
                    f.write(f"    {field_name}: {field_type.__name__} | None\n")
            return res.scalar()


async def get_dynamic_model():
    attributes = await Language.get_all()
    fields = {}

    for attribute in attributes:
        fields[attribute.code] = (str, ...)

    # Создание динамической модели
    DynamicModel = create_model('DynamicModel', **fields)
    return DynamicModel
