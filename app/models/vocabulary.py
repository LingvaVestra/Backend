import contextlib
import enum
import os
import uuid as uuid_pkg
from datetime import date
from datetime import datetime
from typing import Generator
from typing import List
from typing import Optional
from typing import Union

import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi import File as FormFile
from fastapi import Form
from fastapi import Path
from fastapi import UploadFile
from libcloud.storage.drivers.local import LocalStorageDriver
from libcloud.storage.providers import get_driver
from libcloud.storage.types import ContainerAlreadyExistsError
from libcloud.storage.types import ObjectDoesNotExistError
from libcloud.storage.types import Provider
from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_file import File
from sqlalchemy_file import FileField
from sqlalchemy_file import ImageField
from sqlalchemy_file.exceptions import ValidationError
from sqlalchemy_file.storage import StorageManager
from sqlalchemy_file.validators import SizeValidator
from sqlmodel import Boolean
from sqlmodel import Column
from sqlmodel import create_engine
from sqlmodel import Date
from sqlmodel import DateTime
from sqlmodel import Enum
from sqlmodel import Field
from sqlmodel import func
from sqlmodel import Relationship
from sqlmodel import select
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlmodel import String
from starlette.responses import FileResponse
from starlette.responses import JSONResponse
from starlette.responses import RedirectResponse
from starlette.responses import StreamingResponse

os.makedirs("./upload_dir", 0o777, exist_ok=True)
driver = get_driver(Provider.LOCAL)("./upload_dir")


with contextlib.suppress(ContainerAlreadyExistsError):
    driver.create_container(container_name="category")


container = driver.get_container(container_name="category")

StorageManager.add_storage("category", container)


class CategoryWordLink(SQLModel, table=True):
    category_id: Optional[int] = Field(
        default=None, foreign_key="category.id", primary_key=True
    )
    word_id: Optional[int] = Field(
        default=None, foreign_key="word.id", primary_key=True
    )


class Category(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(nullable=False, index=True)
    image: Optional[str] = Field(nullable=True, index=True)
    feed: bool = Field(default=False, nullable=False)
    words: List["Word"] = Relationship(
        back_populates="category", link_model=CategoryWordLink
    )


class Word(SQLModel, table=True):
    # model_config = {'arbitrary_types_allowed': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(nullable=False, index=True)
    name_eng: Optional[str] = Field(nullable=False, index=True)
    transcription: Optional[str] = Field(nullable=False, index=True)
    audio: Optional[str] = Field(nullable=True, index=True)
    image: Optional[str] = Field(nullable=True, index=True)
    category: List[Category] = Relationship(
        back_populates="words", link_model=CategoryWordLink
    )


# # Configure Storage
# os.makedirs("./upload_dir/attachment", 0o777, exist_ok=True)
# container = LocalStorageDriver("./upload_dir").get_container("attachment")
# StorageManager.add_storage("default", container)
