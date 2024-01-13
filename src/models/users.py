import enum
import uuid as uuid_pkg
from datetime import date, datetime
from typing import List, Optional, Union

from sqlmodel import Boolean, Column, Date, DateTime, Enum, Field, Relationship, SQLModel, String, func
from starlette_admin.contrib.sqla import ModelView


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class UserBase(SQLModel):
    email: str = Field(nullable=True)
    is_active: bool = True
    is_superuser: bool = False
    username: Optional[str] = Field(nullable=True)
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    # gender: Gender = Field(Column(Enum(Gender), default=Gender.MALE))
    date_of_birth: Optional[date] = Field(nullable=True)
    #
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(), onupdate=func.now()))
    avatar: Optional[str] = None
    password: str = Field(max_length=100, nullable=False)
    # device_id: str = Field(max_length=100, nullable=True)
    # is_active: bool = True
    # apple_id


class User(UserBase, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
    )
    user_devices: List["UserDevice"] = Relationship(back_populates="user")


class UserDevice(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
    )
    device_id: str = Field(unique=True, index=True)
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(), onupdate=func.now()))
    user_id: Optional[uuid_pkg.UUID] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="user_devices")
