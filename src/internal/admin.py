from starlette_admin.contrib.sqla import Admin, ModelView

from src.db.session import engine
from src.models.memes import Meme, MemeCategory, MemeHistory
from src.models.users import User, UserDevice
from src.models.vocabulary import Category, Word

admin = Admin(
    engine,
    title="Vestra admin",
)

admin.add_view(ModelView(User))
admin.add_view(ModelView(UserDevice))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(Word))
admin.add_view(ModelView(Meme))
# admin.add_view(ModelView(MemeCategoryLink))
# admin.add_view(ModelView(MemeHistory))
admin.add_view(ModelView(MemeCategory))
