from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.paginator import PagedResponseSchema, PageParams, paginate
from src.db.session import get_db
from src.models.users import User
from src.models.vocabulary import Category, Word
from src.schemas.users import UserSchema
from src.schemas.vocabulary import CategoryDetailSchema, CategorySchema, CreateWordSchema, SearchWordSchema, WordSchema
from src.services.users import get_current_user
from src.services.vocabulary import CRUDCategory, CRUDWord, translate_word

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


@router.get("/me", summary="User vocabulary", response_model=PagedResponseSchema[WordSchema])
async def get_me_vocabulary(
    current_user: Annotated[User, Depends(get_current_user)],
    page_params: PageParams = Depends(PageParams),
    db: AsyncSession = Depends(get_db),
) -> WordSchema:
    words = await CRUDWord(Word).get_user_vocabulary(db, page_params=page_params, user_id=str(current_user.id))
    count = await CRUDWord(Word).vocabulary_count(db, user_id=str(current_user.id))
    return paginate(page_params, count, words)


@router.post("/me", summary="Add new word in user vocabulary", response_model=WordSchema)
async def add_new_word(
    payload: CreateWordSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> WordSchema:
    word = await CRUDWord(Word).create(db, obj_in=payload, user_id=str(current_user.id))
    return word


@router.get("/", summary="Search word", response_model=SearchWordSchema)
async def search_word(
    search,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
) -> SearchWordSchema:
    word = await CRUDWord(Word).get_word_from_vocabulary(db, text_eng=search, user_id=str(current_user.id))
    if word:
        word = word[0].model_dump()
        word["in_vocabulary"] = True

        return word
    new_word = await translate_word(search)
    new_word = new_word.model_dump(exclude_unset=True, exclude_none=False)

    new_word["in_vocabulary"] = False
    return new_word
