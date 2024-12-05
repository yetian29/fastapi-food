from dataclasses import dataclass, field
from datetime import datetime, timedelta
from uuid import UUID

from jose import jwt
from passlib.context import CryptContext

from src.domain.customer.entities import Customer
from src.domain.customer.errors import (
    CustomerIsNotFoundException,
    InvalidCredentialException,
    JWTException,
    TokenExpiredException,
    TokenInvalidException,
    TokenTypeInvalidException,
)
from src.domain.customer.services import (
    ICustomerLoginService,
    ICustomerService,
    IPasswordService,
    ITokenService,
)
from src.helper.errors import fail
from src.infrastructure.postgresql.models.customer import CustomerORM
from src.infrastructure.postgresql.repositories.customer import ICustomerRepository


@dataclass
class PasswordService(IPasswordService):
    _min_password_strength: int = 8
    _max_password_strength: int = 64
    _pwd_context: CryptContext = CryptContext(schemes="bcrypt")

    def validate_password_strength(self, password: str) -> bool:
        if (
            not self._min_password_strength
            <= len(password)
            <= self._max_password_strength
        ):
            return False
        return True

    def get_hashed_password(self, plain_password: str) -> str:
        if not self.validate_password_strength(plain_password):
            fail(
                InvalidCredentialException(
                    "Password does not meet strength requirement"
                )
            )
        return self._pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> True:
        verified = self._pwd_context.verify(plain_password, hashed_password)
        return (
            True
            if verified
            else fail(InvalidCredentialException("Password is incorrect"))
        )


@dataclass
class TokenService(ITokenService):
    _secret_key: str
    _access_token_expire_minutes: int = 15
    _refresh_token_expire_days: int = 7
    _algorithm: str = "HS256"
    _revoke_token: set[str] = field(default_factory=set)

    customer_service: ICustomerService

    def generate_access_token(self, customer_oid: UUID) -> str:
        expire = datetime.now() + timedelta(minutes=self._access_token_expire_minutes)
        payload = {"sub": str(customer_oid), "type": "access", "exp": expire}
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def generate_refresh_token(self, customer_oid: UUID) -> str:
        expire = datetime.now() + timedelta(days=self._refresh_token_expire_days)
        payload = {"sub": str(customer_oid), "type": "refresh", "exp": expire}
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def revoke_token(self, token: str):
        self._revoke_token.add(token)

    def is_token_valid(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=self._algorithm)
        except jwt.ExpiredSignatureError:
            fail(TokenExpiredException("Token has expired"))
        except jwt.JWTError:
            fail(JWTException)
        else:
            if payload.get("type") not in ["access", "refresh"]:
                fail(TokenTypeInvalidException)

            elif token in self.revoke_token:
                fail(TokenInvalidException)
            return payload

    async def refresh_access_token(self, refresh_token: str) -> str:
        payload = self.is_token_valid(refresh_token)
        customer_oid = UUID(payload.get("sub"))
        customer = await self.customer_service.get_by_oid(oid=customer_oid)
        self.revoke_token(customer.access_token)
        new_access_token = self.generate_access_token(customer.oid)
        return new_access_token

    async def refresh_refresh_token(self, refresh_token: str) -> str:
        payload = self.is_token_valid(refresh_token)
        customer_oid = UUID(payload.get("sub"))
        customer = await self.customer_service.get_by_oid(oid=customer_oid)
        self.revoke_token(customer.refresh_token)
        new_refresh_token = self.generate_refresh_token(customer.oid)
        return new_refresh_token


@dataclass(frozen=True)
class CustomerService(ICustomerService):
    repository: ICustomerRepository

    async def get_by_username(self, username: str) -> Customer:
        dto = await self.repository.get_by_username(username)
        if not dto:
            fail(CustomerIsNotFoundException)
        return dto.to_entity()

    async def get_by_oid(self, oid: UUID) -> Customer:
        dto = await self.repository.get_by_oid(oid)
        if not dto:
            fail(CustomerIsNotFoundException)
        return dto.to_entity()

    async def create(self, customer: Customer) -> Customer:
        dto = CustomerORM.from_entity(customer)
        dto = await self.repository.create(dto)
        return dto.to_entity()

    async def update(self, customer: Customer) -> Customer:
        dto = CustomerORM.from_entity(customer)
        dto = await self.repository.update(dto)
        return dto.to_entity()


@dataclass(frozen=True)
class CustomerLoginService(ICustomerLoginService):
    customer_service: ICustomerService
    password_service: IPasswordService
    token_service: ITokenService

    async def authenticate(self, username: str, password: str) -> Customer:
        customer = await self.customer_service.get_by_username(username)
        self.password_service.verify_password(password, customer.password)
        return customer

    def generate_access_token_and_refresh_token_and_is_active(
        self, customer: Customer
    ) -> tuple[str, str]:
        access_token = self.token_service.generate_access_token(
            customer_oid=customer.oid
        )
        refresh_token = self.token_service.generate_refresh_token(
            customer_oid=customer.oid
        )
        customer.is_active = True
        return access_token, refresh_token
