from abc import ABC, abstractmethod

from sqlalchemy import select

from src.infrastructure.postgresql.database import Database
from src.infrastructure.postgresql.models.customer import CustomerORM


class ICustomerRepository(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> CustomerORM:
        pass

    @abstractmethod
    async def create(self, customer_orm: CustomerORM) -> CustomerORM:
        pass

    @abstractmethod
    async def update(self, customer_orm: CustomerORM) -> CustomerORM:
        pass


@Database(frozen=True)
class PostgresCustomerRepository(ICustomerRepository):
    database: Database

    async def get_by_username(self, username: str) -> CustomerORM | None:
        stmt = select(CustomerORM).where(CustomerORM.username == username).limit(1)
        async with self.database.get_read_only_session() as session:
            """scalar is used to take single object"""
            customer_orm = await session.scalar(stmt)
            return customer_orm
