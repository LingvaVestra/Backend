from typing import Annotated, Any, Dict, Optional, Union

import aiohttp
from sqlalchemy import exists, func, not_, select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.paginator import PageParams
from src.core.settings import API_KEY_GOOGLE
from src.models.vocabulary import Category, CategoryWordLink, Vocabulary, Word
from src.schemas.vocabulary import CategorySchema, CreateWordSchema, WordSchema
from src.services.crud_base import CRUDBase


class CRUDWord(CRUDBase[Word, WordSchema, WordSchema]):
    async def get_user_vocabulary(self, db: AsyncSession, *, page_params: PageParams, user_id: str) -> Optional[Word]:
        # words = select(Word).where(Word.users_vocabulary == user_id).options(selectinload(Word.users_vocabulary))
        # result = await db.execute(words)

        subq = select(Vocabulary.word_id).where(Vocabulary.user_id == user_id)
        words = (
            select(Word)
            .where((Word.id.in_(subq)))
            .offset((page_params.page - 1) * page_params.size)
            .limit(page_params.size)
        )
        result = await db.execute(words)
        return result.scalars().all()

    async def vocabulary_count(self, db: AsyncSession, *, user_id: str) -> Optional[Word]:
        words_count = select(func.count("*")).select_from(Vocabulary).where(Vocabulary.user_id == user_id)
        result = await db.execute(words_count)
        return result.scalar()

    async def get_list_by_category(self, db: AsyncSession, *, category_id: int) -> Optional[Word]:
        words = select(Word).where(Word.CategoryWordLink == category_id)
        result = await db.execute(words)
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, *, _id: int) -> Optional[Word]:
        word = select(Word).where(Word.id == _id)

        result = await db.execute(word)

        return result.scalars().first()

    async def get_word_from_vocabulary(self, db: AsyncSession, *, text_eng: str, user_id: str):
        word = select(Word).where((Word.text_eng == text_eng) and (Word.users_vocabulary.user_id == user_id))
        result = await db.execute(word)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateWordSchema, user_id: str) -> Word:

        db_obj = Word(
            text=obj_in.text,
            text_eng=obj_in.text_eng,
            transcription=obj_in.transcription,
            audio=obj_in.audio,
            image=obj_in.image,
        )
        db.add(db_obj)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        db_vocabulary = Vocabulary(user_id=user_id, word_id=db_obj.id)
        db.add(db_vocabulary)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: Word, obj_in: Union[WordSchema, Dict[str, Any]]) -> Word:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        # if update_data["password"]:
        #     hashed_password = get_password_hash(update_data["password"])
        #     del update_data["password"]
        #     update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)


class CRUDCategory(CRUDBase[Category, CategorySchema, CategorySchema]):
    async def get_list(
        self,
        db: AsyncSession,
    ) -> Optional[Category]:
        categories = select(Category)
        result = await db.execute(categories)
        print(result)
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, *, _id: int) -> Optional[Category]:
        category = select(Category).where(Category.id == _id).options(selectinload(Category.words))
        result = await db.execute(category)
        category_result = result.scalar()
        return category_result

    async def create(self, db: AsyncSession, *, obj_in: CategorySchema) -> Category:
        import datetime

        # user = await self.get_by_email(db, email=obj_in.email)
        # if user:
        #     raise HTTPException(
        #         status_code=400,
        #         detail="Пользователь с такой электронной почтой уже зарегистрирован!",
        #     )
        db_obj = Category(
            name=obj_in.name,
            name_eng=obj_in.name_eng,
            transcription=obj_in.transcription,
            audio=obj_in.audio,
            image=obj_in.image,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Category, obj_in: Union[CategorySchema, Dict[str, Any]]
    ) -> Category:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        # if update_data["password"]:
        #     hashed_password = get_password_hash(update_data["password"])
        #     del update_data["password"]
        #     update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)


async def translate_word(
    search_text: str,
):
    url = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY_GOOGLE}&q={search_text}&target=ru&source=en"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
        ) as resp:
            result = await resp.json()
            return Word(
                id=0,
                text=result["data"]["translations"][0]["translatedText"],
                text_eng=search_text,
                transcription=None,
                audio=None,
                image=None,
            )
