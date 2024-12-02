from dataclasses import dataclass

from jose import jwt
from passlib.context import CryptContext

from src.core import settings
from src.domain.customer.entities import Customer
from src.domain.customer.errors import CredentailException, CustomerIsNotFoundException
from src.domain.customer.services import (
    IAuthenticateCustomerService,
    ICustomerService,
    ILoginCustomerService,
    IPasswordService,
)
from src.helper.errors import fail
from src.infrastructure.postgresql.repositories.customer import ICustomerRepository

pwd_context = CryptContext(schemes="bcrypt")
SECRET_KEY = settings.api.secret_key
ALGORITHM = "HS256"


class PasswordService(IPasswordService):
    def get_hased_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        verified = pwd_context.verify(plain_password, hashed_password)
        return True if verified else fail(CredentailException)


@dataclass(frozen=True)
class AuthenticateCustomerService(IAuthenticateCustomerService):
    customer_service: ICustomerService
    password_service: IPasswordService

    async def authenticate(self, username: str, password: str):
        customer = await self.customer_service.get_by_username(username)
        if customer:
            self.password_service.verify_password(password, customer.password)
        else:
            fail(CredentailException)


class LoginCustomerService(ILoginCustomerService):
    def generate_token_and_active(self, customer: Customer) -> str:
        customer.token = jwt.encode(customer.oid, SECRET_KEY, algorithm=ALGORITHM)
        customer.is_active = True
        return customer.token


@dataclass(frozen=True)
class CustomerService(ICustomerService):
    repository: ICustomerRepository

    async def get_by_username(self, username: str) -> Customer:
        customer_orm = await self.repository.get_by_username(username)
        if not customer_orm:
            fail(CustomerIsNotFoundException)
        return customer_orm.to_entity()

    async def get_or_create(self, customer: Customer) -> Customer:
        pass

    async def update(self, customer: Customer) -> Customer:
        pass
