import contextlib
import os
from typing import List, Optional

from libcloud.storage.providers import get_driver
from libcloud.storage.types import ContainerAlreadyExistsError, Provider
from sqlalchemy_file.storage import StorageManager
from sqlmodel import Field, Relationship, SQLModel

os.makedirs("./upload_dir", 0o777, exist_ok=True)
driver = get_driver(Provider.LOCAL)("./upload_dir")


with contextlib.suppress(ContainerAlreadyExistsError):
    driver.create_container(container_name="category")


container = driver.get_container(container_name="category")

StorageManager.add_storage("category", container)


class CategoryWordLink(SQLModel, table=True):
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", primary_key=True)
    word_id: Optional[int] = Field(default=None, foreign_key="word.id", primary_key=True)


class Category(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(nullable=False, index=True)
    image: Optional[str] = Field(nullable=True, index=True)
    feed: bool = Field(default=False, nullable=False)
    words: List["Word"] = Relationship(back_populates="category", link_model=CategoryWordLink)


class Word(SQLModel, table=True):
    # model_config = {'arbitrary_types_allowed': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    text: Optional[str] = Field(nullable=False, index=True)
    text_eng: Optional[str] = Field(nullable=False, index=True)
    transcription: Optional[str] = Field(nullable=False, index=True)
    audio: Optional[str] = Field(nullable=True, index=True)
    image: Optional[str] = Field(nullable=True, index=True)
    category: List[Category] = Relationship(back_populates="words", link_model=CategoryWordLink)


# # Configure Storage
# os.makedirs("./upload_dir/attachment", 0o777, exist_ok=True)
# container = LocalStorageDriver("./upload_dir").get_container("attachment")
# StorageManager.add_storage("default", container)
