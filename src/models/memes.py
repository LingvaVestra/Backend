import uuid as uuid_pkg
from datetime import datetime
from typing import List, Optional

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func


class MemeCategoryLink(SQLModel, table=True):
    category_id: Optional[int] = Field(default=None, foreign_key="memecategory.id", primary_key=True)
    meme_id: Optional[int] = Field(default=None, foreign_key="meme.id", primary_key=True)


class MemeCategory(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(nullable=False, index=True)
    image: Optional[str] = Field(nullable=True, index=True)
    # feed: bool = Field(default=False, nullable=False)
    memes: List["Meme"] = Relationship(back_populates="memecategory", link_model=MemeCategoryLink)


class Meme(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: Optional[str] = Field(nullable=False)
    text_eng: Optional[str] = Field(nullable=False, index=True)
    image: Optional[str] = Field(nullable=True, index=True)
    memecategory: List[MemeCategory] = Relationship(back_populates="memes", link_model=MemeCategoryLink)


class MemeHistory(SQLModel, table=True):
    user_id: Optional[uuid_pkg.UUID] = Field(default=None, foreign_key="user.id", primary_key=True, index=True)
    meme_id: Optional[int] = Field(default=None, foreign_key="meme.id", primary_key=True, index=True)
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(), onupdate=func.now()))
