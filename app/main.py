import asyncio
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqladmin import Admin

from app.admin.views import UserAdmin
from app.config import settings
from app.routers import users
from app.utils.admin_auth import AdminAuth
from app.utils.db import sessionmanager
from app.utils.exceptions import register_exception_handlers
from app.utils.shutdown import handle_shutdown


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.remove()
    logger.add(sys.stderr, level=settings.log_lvl)
    logger.info("🚀 Starting application")

    yield

    logger.info("⛔ Stopping application")
    handle_shutdown()
    await asyncio.sleep(3)
    await sessionmanager.close()


app = FastAPI(
    title="base fastapi web application",
    root_path="/api",
    docs_url="/docs" if settings.show_docs else None,
    redoc_url="/redoc" if settings.show_docs else None,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
register_exception_handlers(app)

# Routers
app.include_router(users.router)

admin = Admin(
    app=app,
    engine=sessionmanager.engine,
    authentication_backend=AdminAuth(
        jwt_secret=settings.jwt_secret,
        admin_password_hash=settings.admin_password_hash,
    ),
    templates_dir="static/templates",
)

admin.add_view(UserAdmin)
