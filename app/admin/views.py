from sqladmin import ModelView

from app.users.models import User


# class UserAdmin(ModelView, model=User):
#     column_list = [User.id, User.email, User.role]
#     column_labels = {'id': 'ID', 'email': "EMAIL", 'role': "Роль"}
#     name = "Пользователь"
#     name_plural = "Пользователи"
#     icon = "fa-solid fa-user"
#     column_details_exclude_list = [User.hashed_password]
#     column_sortable_list = [User.id, User.email]
#     column_searchable_list = [User.email, User.id]
#


