from fastapi import APIRouter

from .v1.auth import router as v1_auth_router
from .v1.users import router as v1_user_router

router = APIRouter()

router.include_router(v1_user_router, tags=["Users"], prefix="/v1/users")
router.include_router(v1_auth_router, tags=["Auth"], prefix="/v1/auth")
