from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.settings import settings
from src.infrastructure.postgresql.database import Database


class ITokenRepository(ABC):
    @abstractmethod
    async def add_revoked_token(self, token: str) -> None:
        pass

    @abstractmethod
    async def remove_expired_tokens(self) -> None:
        pass


@dataclass(frozen=True)
class PostgresTokenRepository(ITokenRepository):
    database: Database = Database(settings.database.postgres_url)

    async def add_revoked_token(self, token: str):
        async with self.database.get_write_and_read_session() as session:
            session.add(token)
            await session.commit()
