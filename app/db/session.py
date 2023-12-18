import asyncio
import os

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import DATABASE_URL


engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db() -> AsyncSession:
    try:
        session: AsyncSession = async_session()
        yield session
    except:
        await asyncio.sleep(1)

    finally:
        await session.close()
