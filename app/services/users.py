from typing import Annotated
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from jose import jwt
from jose import JWTError
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import ALGORITHM
from app.core.settings import JWT_REFRESH_SECRET_KEY
from app.core.settings import JWT_SECRET_KEY
from app.core.settings import oauth2_scheme
from app.db.session import get_db
from app.models.users import Gender
from app.models.users import User
from app.schemas.users import SignUpSchema
from app.schemas.users import UserCreate
from app.schemas.users import UserUpdate
from app.services.crud_base import CRUDBase
from app.utils.auth import get_password_hash
from app.utils.auth import verify_password

# from main import oauth2_scheme


class CRUDUser(CRUDBase[User, SignUpSchema, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        user = select(User).where(User.email == email)

        result = await db.execute(user)

        return result.scalars().first()

    async def get_by_uuid(self, db: AsyncSession, *, _uuid: str) -> Optional[User]:
        return db.query(User).filter(User.id == _uuid).first()

    async def get_by_username(
        self, db: AsyncSession, *, username: str
    ) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    async def create(self, db: AsyncSession, *, obj_in: SignUpSchema) -> User:
        import datetime

        user = await self.get_by_email(db, email=obj_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с такой электронной почтой уже зарегистрирован!",
            )
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            username=None,
            last_name=None,
            first_name=obj_in.first_name,
            is_active=True,
            is_superuser=False,
            gender=obj_in.gender,
            date_of_birth=datetime.datetime.now().date(),
            avatar=None,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
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

    async def get_access_from_refresh_token(
        self, db: AsyncSession, *, refresh_token: str
    ) -> Optional[User]:
        # print('in get access token', refresh_token)

        payload = jwt.decode(
            refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_user = await self.get_by_email(db, email=payload.get("sub"))

        return token_user


# user = CRUDUser(User)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # token_data = SignUpSchema(email=email)
    except JWTError:
        raise credentials_exception
    user = await CRUDUser(User).get_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user
