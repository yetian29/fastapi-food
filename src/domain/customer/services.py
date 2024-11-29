from abc import abstractmethod

from src.domain.customer.entities import Customer


class IPasswordService:
    @abstractmethod
    def get_hased_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass


class IAuthenticateCustomerService:
    @abstractmethod
    async def authenticate(self, username: str, password: str) -> None:
        pass


class ILoginCustomerService:
    @abstractmethod
    def generate_token_and_active(self, customer: Customer) -> str:
        pass


class ICustomerService:
    @abstractmethod
    async def get_by_username(self, username: str) -> Customer:
        pass

    @abstractmethod
    async def get_or_create(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    async def update(self, customer: Customer) -> Customer:
        pass
