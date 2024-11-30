from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class Database:
    def __init__(self, wr_url: str, ro_url: str) -> None:
        self._write_and_read_async_engine = create_async_engine(
            url=wr_url, echo=False, isolation_level="READ COMMITED"
        )
        """expire_on_commit - don't expire objects after transaction commit"""
        self._write_and_read_async_session = async_sessionmaker(
            bind=self._write_and_read_async_engine, expire_on_commit=False
        )

        self._read_only_async_engine = create_async_engine(
            url=ro_url, echo=False, isolation_level="AUTO COMMIT"
        )
        self._read_only_async_session = async_sessionmaker(
            bind=self._read_only_async_engine, expire_on_commit=False
        )

    @asynccontextmanager
    async def get_write_and_read_session(self) -> AsyncGenerator[AsyncSession]:
        session: AsyncSession = self._write_and_read_async_session
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.commit()
            await session.close()

    async def get_read_only_session(self) -> AsyncGenerator[AsyncSession]:
        session: AsyncSession = self._read_only_async_session
        try:
            yield session
        except SQLAlchemyError:
            raise
        finally:
            await session.close()
