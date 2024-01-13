from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.session import get_db
from src.models.users import User
from src.schemas.users import AccessTokenScheme, LoginAnon, RefreshTokenScheme, SignUpSchema, TokenSchema, UserSchema
from src.services.users import CRUDUser
from src.utils.auth import create_access_token, create_refresh_token

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30


router = APIRouter()


@router.post("/signup", summary="User Sign-up", response_model=UserSchema)
async def signup(payload: SignUpSchema = Body(), session: AsyncSession = Depends(get_db)):
    """Processes request to register user account."""
    return await CRUDUser(User).create(session, obj_in=payload)


@router.post("/login", summary="User Login", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await CRUDUser(User).authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        # return JSONResponse
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


@router.post("/refresh", summary="Refresh access token", response_model=AccessTokenScheme)
async def refresh_token(form_data: RefreshTokenScheme, db: AsyncSession = Depends(get_db)):
    user = await CRUDUser(User).get_access_from_refresh_token(db, refresh_token=form_data.refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_access_token(user.email),
        # "refresh_token": create_refresh_token(user.email),
    }


@router.post("/login-anonim", summary="Anonim User Login", response_model=TokenSchema)
async def login(payload: LoginAnon = Body(), db: AsyncSession = Depends(get_db)):
    user = await CRUDUser(User).get_or_create_user_by_device_id(db, device_id=payload.device_id)
    if not user:
        # return JSONResponse
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }
