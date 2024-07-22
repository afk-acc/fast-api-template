from pydantic import create_model

from app.exceptions import ModelNotFoundException
from app.repository.base import Base
from app.database import async_session_maker
from sqlalchemy import Column, String, DateTime, ForeignKey, select, JSON, func, Boolean, UniqueConstraint, insert
from sqlalchemy.orm import joinedload, Mapped

from sqlalchemy.orm import relationship




class Permission(Base):
    names = Column(JSON, nullable=False)
    system_name = Column(String, nullable=False)
    roles = relationship('Role', secondary='rolepermissions', back_populates='permissions')


class Role(Base):
    names = Column(JSON, nullable=False)
    users = relationship("User", back_populates="role")
    permissions = relationship('Permission', secondary='rolepermissions', back_populates='roles')
    system_role = Column(Boolean, nullable=False, default=False)
    system_name = Column(String, nullable=True)
    @classmethod
    async def find_by_id_or_fail(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls).filter_by(id=model_id).options(joinedload(cls.permissions))
            result = await session.execute(query)
            result = result.unique().scalar_one_or_none()
            if result is None:
                raise ModelNotFoundException
            return result
    @classmethod
    async def paginate(cls, page: int, limit: int, filter=None):
        async with async_session_maker() as session:
            if filter is not None:
                query = select(cls).filter(filter).limit(limit).offset((page - 1) * limit).options(joinedload(
                    cls.permissions))
            else:
                query = select(cls).limit(limit).offset((page - 1) * limit).options(joinedload(
                    cls.permissions))
            result = await session.execute(query)
            return result.unique().scalars().all()
    @classmethod
    async def get_all(cls, filter=None):
        async with async_session_maker() as session:
            if filter is not None:
                query = select(cls).filter(filter).options(joinedload(cls.permissions))
            else:
                query = select(cls).options(joinedload(cls.permissions))
            result = await session.execute(query)
            return result.scalars().all()

    def __str__(self):
        return f"{self.names.get('ru')}"


class RolePermission(Base):
    role_id = Column(ForeignKey("roles.id"), nullable=False)
    permission_id = Column(ForeignKey("permissions.id"), nullable=False)
    __table_args__ = (UniqueConstraint('role_id', 'permission_id'),)


class User(Base):
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    patronymic = Column(String, nullable=True)
    photo = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role_id = Column(ForeignKey("roles.id", ondelete="cascade"))
    role = relationship("Role", back_populates="users")
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    def __str__(self):
        return f"{self.email}"

    @classmethod
    async def find_by_id_or_fail(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls).filter_by(id=model_id).options(joinedload(cls.role).options(joinedload(Role.permissions)))
            result = await session.execute(query)
            result = result.unique().scalar_one_or_none()
            if result is None:
                raise ModelNotFoundException
            return result
    @classmethod
    async def find_one_or_none(cls, filter):
        async with async_session_maker() as session:
            query = select(cls).options(joinedload(cls.role).options(joinedload(Role.permissions))).filter(filter)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()

    @classmethod
    async def get_all(cls, filter=None):
        async with async_session_maker() as session:
            if filter is not None:
                query = select(cls).filter(filter).options(joinedload(cls.role))
            else:
                query = select(cls).options(joinedload(cls.role))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def paginate(cls, page: int, limit: int, filter=None):
        async with async_session_maker() as session:
            if filter is not None:
                query = select(cls).filter(filter).limit(limit).offset((page - 1) * limit).options(joinedload(
                    cls.role).joinedload(Role.permissions))
            else:
                query = select(cls).limit(limit).offset((page - 1) * limit).options(joinedload(
                    cls.role).joinedload(Role.permissions))
            result = await session.execute(query)
            return result.unique().scalars().all()

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with (async_session_maker() as session):
            query = select(cls).filter_by(id=model_id).options(joinedload(cls.role).options(joinedload(Role.permissions)))
            result = await session.execute(query)
            result = result.unique().scalar()
            return result
