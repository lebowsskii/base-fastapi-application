import contextlib
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings
from app.utils.serialize import json_serializer


class DatabaseSessionManager:
    def __init__(self, dsn: str, engine_kwargs: dict[str, Any] | None = None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine = create_async_engine(dsn, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False,
            expire_on_commit=False,
            bind=self._engine,
        )

    def has_engine(self) -> bool:
        return self._engine is not None

    @property
    def engine(self) -> Any:
        return self._engine

    async def close(self):
        if self._engine is None:
            raise RuntimeError("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncGenerator[AsyncConnection, None]:
        if self._engine is None:
            raise RuntimeError("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            yield connection

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._sessionmaker is None:
            raise RuntimeError("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(
    settings.pg_dsn,
    {
        "echo": settings.pg_echo,
        "json_serializer": json_serializer,
        "pool_size": settings.db_pool_size,
        "max_overflow": settings.db_max_overflow,
        "pool_pre_ping": True,
    },
)
