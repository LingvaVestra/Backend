from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from app.db.session import get_db
from app.models.users import User
from app.schemas.users import UserSchema
from app.services.users import CRUDUser
from app.services.users import get_current_user


router = APIRouter()


@router.get("/me", summary="Info about auth user", response_model=UserSchema)
async def about_me(
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserSchema:
    return current_user
