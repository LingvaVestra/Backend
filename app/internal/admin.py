from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla import ModelView

from app.db.session import engine
from app.models.users import User


admin = Admin(
    engine,
    title="Vestra admin",
)

admin.add_view(ModelView(User))
