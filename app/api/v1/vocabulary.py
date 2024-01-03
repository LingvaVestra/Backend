from typing import Annotated
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_db
from app.models.users import User
from app.models.vocabulary import Category
from app.models.vocabulary import Word
from app.schemas.users import UserSchema
from app.schemas.vocabulary import CategoryDetailSchema
from app.schemas.vocabulary import CategorySchema
from app.schemas.vocabulary import WordSchema
from app.services.users import get_current_user
from app.services.vocabulary import CRUDCategory
from app.services.vocabulary import CRUDWord


router = APIRouter()


@router.get("/categories/", summary="Categories list", response_model=List[Category])
async def get_categories_list(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> CategorySchema:
    categories = await CRUDCategory(Category).get_list(db)
    print(categories)
    return categories


@router.get(
    "/categories/{category_id}",
    summary="Category detail",
    response_model=CategoryDetailSchema,
)
async def get_category_detail(
    category_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> CategoryDetailSchema:
    category = await CRUDCategory(Category).get_by_id(db, _id=category_id)
    return category
