from datetime import datetime, timedelta
from typing import List, Optional

from pydantic import BaseModel, EmailStr

# from src.models.users import Gender

# from fastapi_jwt_auth import AuthJWT


class WordSchema(BaseModel):
    id: int
    text: str
    text_eng: str
    transcription: Optional[str]
    audio: Optional[str]
    image: Optional[str]


class SearchWordSchema(WordSchema):
    in_vocabulary: bool


class CreateWordSchema(BaseModel):
    text: str
    text_eng: str
    transcription: Optional[str]
    audio: Optional[str]
    image: Optional[str]


class CategorySchema(BaseModel):
    id: int
    name: str
    image: Optional[str]


class CategoryDetailSchema(CategorySchema):
    words: List[WordSchema]
