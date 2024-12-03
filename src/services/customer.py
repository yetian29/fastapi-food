from dataclasses import dataclass
from datetime import datetime, timedelta

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
from src.infrastructure.postgresql.models.customer import CustomerORM
from src.infrastructure.postgresql.repositories.customer import ICustomerRepository

pwd_context = CryptContext(schemes="bcrypt")
SECRET_KEY = settings.api.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


class PasswordService(IPasswordService):
    def get_hased_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> True:
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
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {"oid": customer.oid, "exp": expire}
        customer.token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        customer.is_active = True
        return customer.token


@dataclass(frozen=True)
class CustomerService(ICustomerService):
    repository: ICustomerRepository

    async def get_by_username(self, username: str) -> Customer:
        dto = await self.repository.get_by_username(username)
        if not dto:
            fail(CustomerIsNotFoundException)
        return dto.to_entity()

    async def get_or_create(self, customer: Customer) -> Customer:
        try:
            customer = await self.get_by_username(username=customer.username)
        except CustomerIsNotFoundException:
            dto = CustomerORM.from_entity(customer)
            dto = await self.repository.create(dto)
        return dto.to_entity()

    async def update(self, customer: Customer) -> Customer:
        dto = CustomerORM.from_entity(customer)
        dto = await self.repository.update(dto)
        return dto.to_entity()
