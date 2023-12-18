import uuid
from datetime import datetime
from datetime import timedelta

from pydantic import BaseModel
from pydantic import EmailStr

from app.models.users import Gender

# from fastapi_jwt_auth import AuthJWT


class SignUpSchema(BaseModel):
    # username: str
    first_name: str
    password: str
    email: EmailStr
    gender: Gender


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenScheme(BaseModel):
    access_token: str


class RefreshTokenScheme(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserSchema(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str | None = None
    email: str | None = None
    date_of_birth: datetime | None = None
    avatar: str | None = None
    # full_name: str | None = None
    gender: Gender


class UserInDB(UserSchema):
    hashed_password: str


class UserCreate(BaseModel):
    # username: str
    password: str
    email: str


class UserUpdate(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    gender: str
