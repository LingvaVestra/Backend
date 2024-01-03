from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla import ModelView

from app.db.session import engine
from app.models.users import User
from app.models.vocabulary import Category
from app.models.vocabulary import Word

admin = Admin(
    engine,
    title="Vestra admin",
)

admin.add_view(ModelView(User))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(Word))
