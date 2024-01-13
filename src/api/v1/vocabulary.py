from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.session import get_db
from src.models.users import User
from src.models.vocabulary import Category, Word
from src.schemas.users import UserSchema
from src.schemas.vocabulary import CategoryDetailSchema, CategorySchema, WordSchema
from src.services.users import get_current_user
from src.services.vocabulary import CRUDCategory, CRUDWord

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
