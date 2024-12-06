from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.postgresql.models.base import BaseOid, BaseORM


class RevokedTokenORM(BaseORM, BaseOid):
    __tablename__ = "revoked_tokens"

    token: Mapped[str] = mapped_column(nullable=False)
    customer_oid: Mapped[UUID] = mapped_column(nullable=False)
    revoked_at: Mapped[datetime] = mapped_column(nullable=False)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
