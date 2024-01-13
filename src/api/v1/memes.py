from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.paginator import PagedResponseSchema, PageParams, paginate
from src.db.session import get_db
from src.models.users import User
from src.schemas.memes import MemeReadSchema, MemeSchema
from src.services.memes import count_memes, get_memes_list, mark_meme_as_read
from src.services.users import get_current_user

router = APIRouter()


@router.get("", summary="Memes list", response_model=PagedResponseSchema[MemeSchema])
async def memes_list(
    current_user: Annotated[User, Depends(get_current_user)],
    page_params: PageParams = Depends(PageParams),
    db: AsyncSession = Depends(get_db),
) -> MemeSchema:
    memes = await get_memes_list(db, page_params, user_id=current_user.id)
    count = await count_memes(db)

    return paginate(page_params, count, memes)


@router.post("", summary="Mark meme as read", response_model=None)
async def _mark_meme_as_read(
    current_user: Annotated[User, Depends(get_current_user)],
    payload: MemeReadSchema = Body(),
    db: AsyncSession = Depends(get_db),
):

    status = await mark_meme_as_read(db, meme_id=payload.meme_id, user_id=current_user.id)

    if status:
        return {"success": "ok"}
    # raise HTTPException(detail="Уже просмотрено!", status_code=400)
    return JSONResponse(content={"detail": "Уже просмотрено!"}, status_code=400)
