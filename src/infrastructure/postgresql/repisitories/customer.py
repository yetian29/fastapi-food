from abc import ABC, abstractmethod

from src.infrastructure.postgresql.database import Database
from src.infrastructure.postgresql.models.customer import CustomerORM


class ICustomerRepository(ABC):
    @abstractmethod
    async def get_by_user_name(self, username: str) -> CustomerORM:
        pass

    @abstractmethod
    async def get_or_create(self, customer_orm: CustomerORM) -> CustomerORM:
        pass

    @abstractmethod
    async def update(self, customer_orm: CustomerORM) -> CustomerORM:
        pass


@Database(frozen=True)
class PostgresCustomerRepository(ICustomerRepository):
    database: Database

    async def get_by_user_name(self, username: str) -> CustomerORM:
        pass
