from dataclasses import dataclass

from src.domain.base.entities import BaseEntity


@dataclass
class User(BaseEntity):
    email: str
    username: str
    password: str
    is_active: bool
