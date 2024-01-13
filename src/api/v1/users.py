from typing import Annotated

from fastapi import APIRouter, Depends

from src.db.session import get_db
from src.models.users import User
from src.schemas.users import UserSchema
from src.services.users import CRUDUser, get_current_user

router = APIRouter()


@router.get("/me", summary="Info about auth user", response_model=UserSchema)
async def about_me(current_user: Annotated[User, Depends(get_current_user)]) -> UserSchema:
    return current_user
