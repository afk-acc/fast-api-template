from typing import Optional, List

from sqlalchemy import select, insert, delete, func, case, update, inspect, Case
import inflect

from app.database import async_session_maker
from app.exceptions import ModelNotFoundException
from sqlalchemy.orm import DeclarativeBase, declared_attr, joinedload
from sqlalchemy import Column, Integer


class BaseRepository:
    @classmethod
    def build_joinedload(cls, include: str):
        parts = include.split('.')
        option = joinedload(getattr(cls, parts[0]))
        current_class = cls
        for i in range(len(parts)-1):
            current_class = getattr(current_class, parts[i]).property.mapper.class_
            option = option.joinedload(getattr(current_class, parts[i+1]))
        return option

    # @classmethod
    # def build_joinedload(cls, include: str):
    #     parts = include.split('.')
    #     option = joinedload(getattr(cls, parts[0]))
    #     current_class = cls
    #     for part in parts[1:]:
    #         current_class = getattr(current_class, parts[0]).property.mapper.class_
    #         option = option.joinedload(getattr(current_class, part))
    #     return option

    @classmethod
    async def find_one_or_none_with(cls, filter, includes: List[str] = None):
        async with async_session_maker() as session:
            query = select(cls)
            if includes:
                for include in includes:
                    query = query.options(cls.build_joinedload(include))
            query = query.filter(filter)

            result = await session.execute(query)
            return result.unique().scalar_one_or_none()

    @classmethod
    async def get_all(cls, filter=None, includes: List[str] = None):
        async with async_session_maker() as session:
            query = select(cls)
            if includes:
                for include in includes:
                    query = query.options(cls.build_joinedload(include))
            if filter is not None:
                query = query.filter(filter)
            result = await session.execute(query)
            return result.unique().scalars().all()

    @classmethod
    async def paginate(cls, page: int, limit: int, filter=None, includes: List[str] = None):
        async with async_session_maker() as session:
            query = select(cls).limit(limit).offset((page - 1) * limit)
            if includes:
                for include in includes:
                    query = query.options(cls.build_joinedload(include))
            if filter is not None:
                query = query.filter(filter)
            result = await session.execute(query)
            return result.unique().scalars().all()

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
    async def find_one_or_none(cls, filter, includes: List[str] = None):
        async with async_session_maker() as session:
            query = select(cls)
            if includes:
                for include in includes:
                    query = query.options(cls.build_joinedload(include))
            query = query.filter(filter)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()

    @classmethod
    async def find_one_or_fail(cls, filter, includes: List[str] = None):
        async with async_session_maker() as session:
            query = select(cls)
            if includes:
                for include in includes:
                    query = query.options(cls.build_joinedload(include))
            query = query.filter(filter)
            result = await session.execute(query)
            result = result.unique().scalar_one_or_none()
            if result is None:
                raise ModelNotFoundException
            return result

    @classmethod
    async def find_by_id(cls, model_id: int, includes: List[str] = None):
        async with async_session_maker() as session:
            query = select(cls)
            if includes:
                for include in includes:
                    query = query.options(cls.build_joinedload(include))
            query = query.filter_by(id=model_id)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()

    @classmethod
    async def find_by_id_or_fail(cls, model_id: int, includes: List[str] = None):
        async with async_session_maker() as session:
            query = select(cls)
            if includes:
                for include in includes:
                    query = query.options(cls.build_joinedload(include))
            query = query.filter_by(id=model_id)
            result = await session.execute(query)
            result = result.unique().scalar_one_or_none()
            if result is None:
                raise ModelNotFoundException
            return result

    @classmethod
    async def create(cls, includes: List[str] = None, **data):
        async with async_session_maker() as session:
            query = insert(cls).values(**data).returning(cls)
            res = await session.execute(query)
            await session.commit()

            # For Postgres
            res = res.scalar()
            last_id = res.id

            # For MySQL
            # last_id = res.lastrowid
            select_query = select(cls).where(cls.id == last_id)
            if includes:
                for include in includes:
                    select_query = select_query.options(cls.build_joinedload(include))
            result = await session.execute(select_query)
            return result.unique().scalar()

    @classmethod
    async def first_or_create(cls, filter, includes: List[str] = None, **data):
        async with async_session_maker() as session:
            query = select(cls).filter(filter)
            if includes:
                for include in includes:
                    query = query.options(cls.build_joinedload(include))
            result = await session.execute(query)
            result = result.unique().scalar_one_or_none()
            if not result:
                result = await cls.create(includes=includes, **data)
            return result

    @classmethod
    async def update(cls, model_id, **data):
        async with async_session_maker() as session:
            query = select(cls).filter_by(id=model_id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if not result:
                raise ModelNotFoundException
            for key, value in data.items():
                setattr(result, key, value)
            await session.commit()
            return result

    @classmethod
    async def update_by_filter(cls, filter, **data):
        async with async_session_maker() as session:
            query = select(cls).filter(filter)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if not result:
                raise ModelNotFoundException
            for key, value in data.items():
                setattr(result, key, value)
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

    @classmethod
    async def bulk_update_records(cls, records):
        async with async_session_maker() as session:
            # mapper = inspect(cls)
            # update_cases = dict()
            # print(dir(mapper))
            # print(mapper.tables)
            # print(mapper.c)
            # for record in records:
            #     for attr in mapper.c:
            #         # print(attr.name)
            #         # print(dir(attr))
            #         # print(dir(attr.key))
            #         # print(attr.key)
            #         if attr.name != 'id':
            #             if attr.name in record:
            #                 update_cases[attr.name] = case(
            #                     (cls.id == record['id'],
            #                      dict(record[attr.name]) if attr.name in ['texts', 'names', 'options']
            #                                              else record[attr.name])
            #                 )

            ### так не пойдет, т.к. values может обновлять записи только одинаковыми значениями.
            # query = update(cls).values(update_cases).where(cls.id.in_([record['id'] for record in records]))
            # print(query)
            # await session.execute(query)

            await session.execute(update(cls), records)
            await session.commit()


p = inflect.engine()


class Base(DeclarativeBase, BaseRepository):
    id = Column(Integer, primary_key=True, nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:
        return p.plural(cls.__name__.lower())
