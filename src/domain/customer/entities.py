from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Customer:
    oid: UUID
    username: str
    password: str
    access_token: str = ""
    refresh_token: str = ""
    is_active: bool = False
    created_at: datetime
    updated_at: datetime
