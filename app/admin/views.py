from sqladmin import ModelView

from app.models.user import User


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    column_list = [User.id, User.email, User.created_at]
    column_searchable_list = [User.email]
    column_sortable_list = [User.created_at]
    can_delete = False
