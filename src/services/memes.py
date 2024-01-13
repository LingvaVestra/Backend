import uuid as uuid_pkg
from typing import Optional

from sqlalchemy import exists, func, not_, select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.paginator import PageParams
from src.models.memes import Meme, MemeHistory


async def get_memes_list(db: AsyncSession, page_params: PageParams, user_id: str) -> Optional[Meme]:
    subq = select(MemeHistory.meme_id).where(MemeHistory.user_id == user_id)
    memes = (
        select(Meme)
        .where(not_(Meme.id.in_(subq)))
        .offset((page_params.page - 1) * page_params.size)
        .limit(page_params.size)
        .options(selectinload(Meme.memecategory))
    )
    result = await db.execute(memes)
    return result.scalars().all()


async def count_memes(db: AsyncSession) -> int:
    count = select(func.count("*")).select_from(Meme)
    result = await db.execute(count)
    return result.scalar()


async def mark_meme_as_read(db: AsyncSession, meme_id: int, user_id: uuid_pkg.UUID):
    exists_qr = select(MemeHistory).where((MemeHistory.user_id == user_id) & (MemeHistory.meme_id == meme_id))
    result = await db.execute(exists(exists_qr).select())
    meme_exists = result.scalar()

    if not meme_exists:
        db_obj = MemeHistory(user_id=user_id, meme_id=meme_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
    return not meme_exists
