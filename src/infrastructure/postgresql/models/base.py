from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import MetaData, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column


class BaseORM(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "pk": "pk_%(table_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "ix": "ix_%(table_name)s_%(column_0_name)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
        }
    )


uuidpk = Annotated[
    UUID, mapped_column(primary_key=True, unique=True, nullable=False, default=uuid4)
]
created_at = Annotated[
    datetime, mapped_column(default=func.now(), server_default=func.now())
]
updated_at = Annotated[
    datetime,
    mapped_column(
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
]
