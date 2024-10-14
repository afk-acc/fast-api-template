from sqlalchemy import and_

from app.repository.models import Language
from app.users.auth import get_hashed_password
from app.users.models import Role, User, Permission, RolePermission


class Seeder:
    @staticmethod
    async def run():
        print('users seed start')
        await Language.first_or_create(filter=Language.code == 'ru', code="ru", name="Русский")
        await Language.first_or_create(filter=Language.code == 'en', code="en", name="English")
        await Language.first_or_create(filter=Language.code == 'uz', code="uz", name="Ўзбек")
        await Language.first_or_create(filter=Language.code == 'uz_l', code="uz_l", name="O'zbek")

        admin_role = await Role.first_or_create(
            filter=Role.system_name == 'admin',
            names={
                'ru': "Администратор",
                'en': "Administrator",
                "uz": "Администратор",
                "uz_l": "Administrator"
            }, system_role=True, system_name="admin")
        user_role = await Role.first_or_create(
            filter=Role.system_name == 'user',
            names={
                'ru': "Пользователь",
                "en": "User",
                "uz": "Фойдаланувчи",
                "uz_l": "Foydalanuvchi"
            }, system_role=True, system_name="user")
        permission_all = await Permission.first_or_create(
            filter=Permission.system_name == 'all',
            names={'ru': 'all', 'en': 'all', 'uz': 'all', 'uz_l': 'all'},
            system_name='all'
        )
        
        await RolePermission.first_or_create(filter=and_(
            RolePermission.role_id == admin_role.id,
            RolePermission.permission_id == permission_all.id
        ), role_id=admin_role.id, permission_id=permission_all.id)
        admin = await User.first_or_create(filter=User.email == 'admin@admin.com',
                                           role_id=admin_role.id,
                                           email='admin@admin.com',
                                           hashed_password=get_hashed_password("admin123"))
