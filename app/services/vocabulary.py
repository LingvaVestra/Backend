from typing import Annotated
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from jose import jwt
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import ALGORITHM
from app.core.settings import JWT_REFRESH_SECRET_KEY
from app.core.settings import JWT_SECRET_KEY
from app.core.settings import oauth2_scheme
from app.db.session import get_db
from app.models.vocabulary import Category
from app.models.vocabulary import CategoryWordLink
from app.models.vocabulary import Word
from app.schemas.vocabulary import CategorySchema
from app.schemas.vocabulary import WordSchema
from app.services.crud_base import CRUDBase
from app.utils.auth import get_password_hash
from app.utils.auth import verify_password

# from main import oauth2_scheme


class CRUDWord(CRUDBase[Word, WordSchema, WordSchema]):
    async def get_list_by_category(
        self, db: AsyncSession, *, category_id: int
    ) -> Optional[Word]:
        words = select(Word).where(Word.CategoryWordLink == category_id)
        print(words)
        result = await db.execute(words)
        print(result)
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, *, _id: int) -> Optional[Word]:
        word = select(Word).where(Word.id == _id)

        result = await db.execute(word)

        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: WordSchema) -> Word:
        import datetime

        # user = await self.get_by_email(db, email=obj_in.email)
        # if user:
        #     raise HTTPException(
        #         status_code=400,
        #         detail="Пользователь с такой электронной почтой уже зарегистрирован!",
        #     )
        db_obj = Word(
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
        self,
        db: AsyncSession,
        *,
        db_obj: Word,
        obj_in: Union[WordSchema, Dict[str, Any]]
    ) -> Word:
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
        category = (
            select(Category)
            .where(Category.id == _id)
            .options(selectinload(Category.words))
        )
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
        self,
        db: AsyncSession,
        *,
        db_obj: Category,
        obj_in: Union[CategorySchema, Dict[str, Any]]
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
