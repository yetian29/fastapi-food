from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import select

from src.infrastructure.postgresql.database import Database
from src.infrastructure.postgresql.models.user import UserORM


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_username_or_email(self, username: str | None = None, email: str | None = None) -> UserORM | None:
        pass

    @abstractmethod
    async def get_by_oid(self, oid: str) -> UserORM | None:
        pass

    @abstractmethod
    async def get_all_user(self) -> :
        pass

    @abstractmethod
    async def create(self, user: UserORM) -> UserORM:
        pass

    @abstractmethod
    async def update(self, user: UserORM) -> UserORM:
        pass

    @abstractmethod
    async def delete(self, oid: str) -> None:
        pass


@dataclass(frozen=True)
class PostgresUserRepository(IUserRepository):
    database: Database

    async def get_by_username_or_email(self, username: str | None = None, email: str | None = None) -> UserORM | None:
        key = username if username else email
        key_orm = UserORM.username if username else UserORM.email
        stmt = select(UserORM).where(key_orm == key).limit(1)
        async with self.database.get_read_only_session() as session:
            return await session.scalar(stmt)

    async def get_by_oid(self, oid: str) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.oid == oid).limit(1)
        async with self.database.get_read_only_session() as session:
            return await session.scalar(stmt)

    async def get_all_user(self):
        pass
            

    async def create(self, user: UserORM) -> UserORM:
        async with self.database.get_write_and_read_session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def update(self, user: UserORM) -> UserORM:
        async with self.database.get_write_and_read_session() as session:
            await session.merge(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def delete(self, oid: str) -> None:
        stmt = delete(UserORM).where(UserORM.oid == oid).limit(1)
        async def with self.databae.get_write_and_read_session() as session:
            await session.execute(stmt)
            await session.commit()
        
