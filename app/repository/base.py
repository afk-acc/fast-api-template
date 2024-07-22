from sqlalchemy import select, insert, delete, func
import inflect

from app.database import async_session_maker
from app.exceptions import ModelNotFoundException
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, Integer


class BaseRepository:
    @classmethod
    async def get_all(cls, filter=None):
        async with async_session_maker() as session:
            if filter is not None:
                query = select(cls).filter(filter)
            else:
                query = select(cls)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def paginate(cls, page: int, limit: int, filter=None):
        async with async_session_maker() as session:
            if filter is not None:
                query = select(cls).filter(filter).limit(limit).offset((page - 1) * limit)
            else:
                query = select(cls).limit(limit).offset((page - 1) * limit)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def count(cls, filter=None):
        async with async_session_maker() as session:
            if filter is not None:
                query = select(func.count(cls.id)).filter(filter)
            else:
                query = select(func.count(cls.id))
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def find_one_or_none(cls, filter):
        async with async_session_maker() as session:
            query = select(cls).filter(filter)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_fail(cls, filter):
        async with async_session_maker() as session:
            query = select(cls).filter(filter)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if result is None:
                raise ModelNotFoundException
            return result

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_id_or_fail(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls).filter_by(id=model_id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if result is None:
                raise ModelNotFoundException
            return result

    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls).values(**data).returning(cls)
            res = await session.execute(query)
            await session.commit()
            return res.scalar()

    @classmethod
    async def first_or_create(cls, filter, **data):
        async with async_session_maker() as session:
            query = select(cls).filter(filter)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if not result:
                result = await cls.create(**data)
            return result

    @classmethod
    async def update(cls, model_id, **data):
        async with async_session_maker() as session:
            query = select(cls).filter_by(id=model_id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            for key, value in data.items():
                setattr(result, key, value) if value else None
            if not result:
                raise ModelNotFoundException
            await session.commit()
            return result

    @classmethod
    async def update_by_filter(cls, filter, **data):
        async with async_session_maker() as session:
            query = select(cls).filter(filter)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            for key, value in data.items():
                setattr(result, key, value) if value else None
            if not result:
                raise ModelNotFoundException
            await session.commit()
            return result

    @classmethod
    async def delete(cls, filter):
        async with async_session_maker() as session:
            query = delete(cls).filter(filter)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def insert(cls, data: list):
        async with async_session_maker() as session:
            session.add_all(data)
            await session.commit()


p = inflect.engine()


class Base(DeclarativeBase, BaseRepository):
    id = Column(Integer, primary_key=True, nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:
        return p.plural(cls.__name__.lower())
