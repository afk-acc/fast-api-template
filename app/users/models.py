from pydantic import create_model

from app.exceptions import ModelNotFoundException
from app.repository.base import Base
from app.database import async_session_maker
from sqlalchemy import Column, String, DateTime, ForeignKey, select, JSON, func, Boolean, UniqueConstraint, insert
from sqlalchemy.orm import joinedload, Mapped

from sqlalchemy.orm import relationship

class Permission(Base):
    names = Column(JSON, nullable=False)
    system_name = Column(String(length=255), nullable=False)
    roles = relationship('Role', secondary='rolepermissions', back_populates='permissions')


class Role(Base):
    names = Column(JSON, nullable=False)
    users = relationship("User", back_populates="role")
    permissions = relationship('Permission', secondary='rolepermissions', back_populates='roles')
    system_role = Column(Boolean, nullable=False, default=False)
    system_name = Column(String(length=255), nullable=True)

    def __str__(self):
        return f"{self.names.get('ru')}"


class RolePermission(Base):
    role_id = Column(ForeignKey("roles.id", ondelete='CASCADE'), nullable=False)
    permission_id = Column(ForeignKey("permissions.id", ondelete='CASCADE'), nullable=False)
    __table_args__ = (UniqueConstraint('role_id', 'permission_id'),)


class User(Base):
    email = Column(String(length=255), nullable=False, unique=True)
    name = Column(String(length=255), nullable=True)
    lastname = Column(String(length=255), nullable=True)
    patronymic = Column(String(length=255), nullable=True)
    photo = Column(String(length=255), nullable=True)
    hashed_password = Column(String(length=255), nullable=False)
    role_id = Column(ForeignKey("roles.id", ondelete="cascade"))
    role = relationship("Role", back_populates="users")
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    def __str__(self):
        return f"{self.email}"


