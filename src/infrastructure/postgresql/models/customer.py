from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.postgresql.models.base import Base


class CustomerORM(Base):
    __tablename__ = "customer"
    oid: Mapped[UUID] = mapped_column(
        default=uuid4, nullable=False, primary_key=True, unique=True
    )
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(default="", unique=True)
    is_active: Mapped[bool] = mapped_column(default=False)
