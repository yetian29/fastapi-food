from dataclasses import dataclass
from uuid import UUID


@dataclass
class Customer:
    oid: UUID
    username: str
    password: str
    token: str = ""
    is_active: bool = False
