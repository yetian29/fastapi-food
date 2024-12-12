from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import select

from src.infrastructure.postgresql.database import Database
from src.infrastructure.postgresql.models.user import UserORM


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> UserORM | None:
        pass

    @abstractmethod
    async def create(self, user: UserORM) -> UserORM:
        pass

    @abstractmethod
    async def update(self, user: UserORM) -> UserORM:
        pass


@dataclass(frozen=True)
class UserRepository(IUserRepository):
    database: Database

    async def get_by_username(self, username: str) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.username == username).limit(1)
        async with self.database.get_read_only_session() as session:
            return await session.scalar(stmt)

    async def create(self, user: UserORM) -> UserORM:
        async with self.database.get_write_and_read_session() as session:
            session.add(user)
            await session.commit()
            return user

    async def update(self, user: UserORM) -> UserORM:
        async with self.database.get_write_and_read_session() as session:
            await session.merge(user)
            await session.commit()
            await session.refresh(user)
            return user
