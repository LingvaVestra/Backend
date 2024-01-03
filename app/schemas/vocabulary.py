from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr

from app.models.users import Gender

# from fastapi_jwt_auth import AuthJWT


class WordSchema(BaseModel):
    id: int
    name: str
    name_eng: str
    transcription: str
    audio: Optional[str]
    image: Optional[str]


class CategorySchema(BaseModel):
    id: int
    name: str
    image: Optional[str]


class CategoryDetailSchema(CategorySchema):
    words: List[WordSchema]
