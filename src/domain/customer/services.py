from abc import abstractmethod
from uuid import UUID

from src.domain.customer.entities import Customer


class IPasswordService:
    @abstractmethod
    def validate_password_strength(self, password: str) -> bool:
        pass

    @abstractmethod
    def get_hahsed_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> True:
        pass


class ITokenService:
    @abstractmethod
    def generate_access_token(self, customer_oid: UUID) -> str:
        pass

    @abstractmethod
    def generate_refresh_token(self, customer_oid: UUID) -> str:
        pass

    @abstractmethod
    def revoke_token(self, token: str):
        pass

    @abstractmethod
    def is_token_valid(self, token: str) -> True:
        pass

    @abstractmethod
    async def refresh_access_token(self, refresh_token: str) -> str:
        pass

    @abstractmethod
    async def refresh_refresh_token(self, refresh_token: str) -> str:
        pass


class ICustomerLoginService:
    @abstractmethod
    async def authenticate(self, username: str, password: str) -> Customer:
        pass

    def generate_access_token_and_refresh_token_and_is_active(
        self, customer: Customer
    ) -> tuple[str, str]:
        pass


class ILoginCustomerService:
    @abstractmethod
    def login(self, customer: Customer) -> str:
        pass


class ICustomerService:
    @abstractmethod
    async def get_by_username(self, username: str) -> Customer:
        pass

    @abstractmethod
    async def get_by_oid(self, oid: UUID) -> Customer:
        pass

    @abstractmethod
    async def create(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    async def update(self, customer: Customer) -> Customer:
        pass
