import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()


DATABASE_URL = os.environ.get("DATABASE_URL")

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_MINUTES = os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES")
ALGORITHM = os.environ.get("ALGORITHM")
REDIS_URL = os.environ.get("REDIS_URL")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/v1/login")
