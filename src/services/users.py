from typing import Annotated, Any, Dict, Optional, Union

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.settings import ALGORITHM, JWT_REFRESH_SECRET_KEY, JWT_SECRET_KEY, oauth2_scheme
from src.db.session import get_db
from src.models.users import Gender, User, UserDevice
from src.schemas.users import SignUpSchema, UserCreate, UserUpdate
from src.services.crud_base import CRUDBase
from src.utils.auth import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, SignUpSchema, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        user = select(User).where(User.email == email)

        result = await db.execute(user)

        return result.scalars().first()

    async def get_or_create_user_by_device_id(self, db: AsyncSession, *, device_id: str) -> Optional[User]:
        user = select(User).select_from(UserDevice).join(UserDevice.user).where(UserDevice.device_id == device_id)

        result = await db.execute(user)
        result = result.scalars().first()
        if result:
            return result
        obj_in = SignUpSchema(email=None, first_name=device_id, password=device_id)
        result = await self.create(db, obj_in=obj_in)
        db_obj = UserDevice(
            user=result,
            device_id=device_id,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return result

    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:

        user = select(User).where(User.username == username)

        result = await db.execute(user)

        return result.scalars().first()

    async def get_by_id(self, db: AsyncSession, *, _uuid: str) -> Optional[User]:

        user = select(User).where(User.id == _uuid)

        result = await db.execute(user)

        return result.scalars().first()

    # async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
    #     return db.query(User).filter(User.username == username).first()

    async def create(self, db: AsyncSession, *, obj_in: SignUpSchema) -> User:
        import datetime

        user = await self.get_by_username(db, username=obj_in.first_name)
        if user:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с такой электронной почтой уже зарегистрирован!",
            )
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            username=obj_in.first_name,
            last_name=None,
            first_name=obj_in.first_name,
            is_active=True,
            is_superuser=False,
            # gender=obj_in.gender,
            date_of_birth=datetime.datetime.now().date(),
            avatar=None,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    async def get_access_from_refresh_token(self, db: AsyncSession, *, refresh_token: str) -> Optional[User]:
        # print('in get access token', refresh_token)

        payload = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        token_user = await self.get_by_email(db, email=payload.get("sub"))

        return token_user


# user = CRUDUser(User)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        _uuid: str = payload.get("sub")
        if _uuid is None:
            raise credentials_exception
        # token_data = SignUpSchema(email=email)
    except JWTError:
        raise credentials_exception
    user = await CRUDUser(User).get_by_id(db, _uuid=_uuid)
    if user is None:
        raise credentials_exception
    return user
