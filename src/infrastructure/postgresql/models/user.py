from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.user.entities import User
from src.infrastructure.postgresql.models.base import (
    BaseORM,
    created_at,
    updated_at,
    uuidpk,
)


class UserORM(BaseORM):
    __tablename__ = "user"
    oid: Mapped[uuidpk]
    email: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @staticmethod
    def from_entity(entity: User) -> "UserORM":
        return UserORM(
            email=entity.email, username=entity.username, password=entity.password
        )

    def to_entity(self) -> User:
        return User(
            oid=self.oid,
            email=self.email,
            username=self.username,
            password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
