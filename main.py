from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.urls import router
from app.db.session import init_db
from app.internal.admin import admin

# login_provider = UsernamePasswordProvider(
#     admin_model=Admin,
#     enable_captcha=True,
#     login_logo_url="https://preview.tabler.io/static/logo.svg"
# )


app = FastAPI()

# Create admin

admin.mount_to(app)

app.include_router(router, prefix="/api")
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     # dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.on_event("startup")
async def on_startup():
    await init_db()
    # redis = await aioredis.create_redis_pool("redis://localhost", encoding="utf8")
    # admin_app.configure(
    #     logo_url="https://preview.tabler.io/static/logo-white.svg",
    #     template_folders=[os.path.join(BASE_DIR, "templates")],
    #     providers=[login_provider],
    #     redis=redis,
    # )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/healthchecker")
def root():
    return {"message": "Success"}
