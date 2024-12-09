from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.postgresql.models.base import (
    BaseORM,
    created_at,
    updated_at,
    uuidpk,
)


class User(BaseORM):
    __tablename__ = "user"
    oid: Mapped[uuidpk]
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
