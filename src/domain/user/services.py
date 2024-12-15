from abc import ABC, abstractmethod

from src.domain.user.entities import User

from datetime import timedelta

class ICodeService(ABC):
    @abstractmethod
    def genarate_code(self, email: str, expire_delta: timedelta | None = None) -> str:
        pass

    @abstractmethod
    def validate_code(self, email: str, code: str) -> bool:
        pass

class ISendCodeService(ABC):
    @abstractmethod
    def send_code(self, email: str, code: str) -> None: 
        pass
        
class IPasswordService(ABC):
    @abstractmethod
    def validate_password_strength(self, plain_password: str) -> bool:
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hash_password: str) -> bool:
        pass

    @abstractmethod
    def get_hash_password(self, plain_password: str) -> str:
        pass


class ILoginService(ABC):
    @abstractmethod
    async def authenticate(self, email: str | None = None, username: str | None = None, password: str) -> User:
        pass

    @abstractmethod
    def generate_token_and_is_active(self, user: User, expire_delta: timedelta | None = None) -> str:
        pass


class IUserService(ABC):
    @abstractmethod
    async def get_by_username_or_email(self, username: str | None = None, email: str | None = None) -> User:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, oid: str) -> User:
        pass

    @abstractmethod
    async def change_password(self, username: str | None = None, email: str | None = None, old_password: str) -> str:
        pass

    @abstractmethod
    async def forget_password(self, username: str | None = None, email: str | None  = None) -> str:
        pass
