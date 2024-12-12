from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config.settings import settings


class Database:
    def __init__(self, url: str = settings.POSTGRES_URL) -> None:
        self._write_and_read_async_engine = create_async_engine(
            url=url, echo=False, isolation_level="READ COMMITTED"
        )
        """expire_on_commit - don't expire objects after transaction commit"""
        self._write_and_read_async_session = async_sessionmaker(
            bind=self._write_and_read_async_engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

        self._read_only_async_engine = create_async_engine(
            url=url, echo=False, isolation_level="AUTOCOMMIT"
        )
        """autocommit=True: Read-only session should be autocommit"""
        """autoflush=False: disable autoflush for more control"""
        self._read_only_async_session = async_sessionmaker(
            bind=self._read_only_async_engine,
            expire_on_commit=False,
            autocommit=True,
            autoflush=False,
        )

    @asynccontextmanager
    async def get_write_and_read_session(self) -> AsyncGenerator[AsyncSession, Any]:
        session: AsyncSession = self._write_and_read_async_session()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()

    @asynccontextmanager
    async def get_read_only_session(self) -> AsyncGenerator[AsyncSession, Any]:
        session: AsyncSession = self._read_only_async_session()
        try:
            yield session
        except SQLAlchemyError:
            raise
        finally:
            await session.close()
