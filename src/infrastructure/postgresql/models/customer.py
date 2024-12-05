from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.customer.entities import Customer
from src.infrastructure.postgresql.models.base import Base


class CustomerORM(Base):
    __tablename__ = "customer"
    oid: Mapped[UUID] = mapped_column(
        default=uuid4, nullable=False, primary_key=True, unique=True
    )
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    access_token: Mapped[str] = mapped_column(default="", unique=True)
    refresh_token: Mapped[str] = mapped_column(default="", unique=True)
    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now,
    )

    @staticmethod
    def from_entity(entity: Customer) -> "CustomerORM":
        return CustomerORM(
            username=entity.username,
            password=entity.password,
        )

    def to_entity(self) -> Customer:
        return Customer(
            oid=self.oid,
            username=self.username,
            password=self.password,
            access_token=self.access_token,
            refresh_token=self.refresh_tokne,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
