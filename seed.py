import asyncio

from sqlalchemy import and_

from app.users.auth import get_hashed_password
from app.users.models import Role, User


async def seed():
    user_role = await Role.first_or_create(
        filter=and_(Role.name == "user", Role.name_ru == "пользователь"),
        name="user",
        name_ru="пользователь")
    admin_role = await Role.first_or_create(
        filter=and_(Role.name == "admin", Role.name_ru == "администратор"), name="admin",
        name_ru="администратор")
    admin = await User.create(email="admin@admin.com",
                                  hashed_password=get_hashed_password("admin@admin.com"), role_id=admin_role.id)


asyncio.run(seed())
