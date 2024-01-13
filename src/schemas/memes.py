from typing import List

from pydantic import BaseModel


class MemeCategorySchema(BaseModel):
    id: int
    name: str


class MemeSchema(BaseModel):
    id: int
    text: str
    text_eng: str
    image: str
    memecategory: List[MemeCategorySchema]
