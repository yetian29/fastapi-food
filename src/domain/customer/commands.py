from dataclasses import dataclass

from src.domain.customer.entities import Customer


@dataclass(frozen=True)
class RegisterCustomerCommand:
    customer: Customer


@dataclass(frozen=True)
class LoginCustomerCommand:
    username: str
    password: str
