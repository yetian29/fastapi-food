from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseORM(AsyncAttrs, DeclarativeBase):
    pass


class BaseOid:
    oid: Mapped[UUID] = mapped_column(
        default=uuid4, nullable=False, primary_key=True, unique=True
    )
