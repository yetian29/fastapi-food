from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import select

from src.infrastructure.postgresql.database import Database
from src.infrastructure.postgresql.models.customer import CustomerORM


class ICustomerRepository(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> CustomerORM | None:
        pass

    @abstractmethod
    async def create(self, customer_orm: CustomerORM) -> CustomerORM:
        pass

    @abstractmethod
    async def update(self, customer_orm: CustomerORM) -> CustomerORM:
        pass


@dataclass(frozen=True)
class PostgresCustomerRepository(ICustomerRepository):
    database: Database

    async def get_by_username(self, username: str) -> CustomerORM | None:
        stmt = select(CustomerORM).where(CustomerORM.username == username).limit(1)
        async with self.database.get_read_only_session() as session:
            """scalar is used to take single object"""
            customer_orm = await session.scalar(stmt)
            return customer_orm

    """refresh() reloads the object from the database, ensuring you have the most up-to-date version"""

    async def create(self, customer_orm: CustomerORM) -> CustomerORM:
        async with self.database.get_write_and_read_session() as session:
            session.add(customer_orm)
            await session.commit()
            await session.refresh(customer_orm)
            return customer_orm

    async def update(self, customer_orm: CustomerORM) -> CustomerORM:
        async with self.database.get_write_and_read_session() as session:
            dto = await session.merge(customer_orm)
            await session.commit()
            await session.refresh(dto)
            return dto
