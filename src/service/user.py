import re
from dataclasses import dataclass

from passlib.context import CryptContext

from src.domain.user.entities import User
from src.domain.user.errors import PasswordInvalidException, UserIsNotFoundException
from src.domain.user.services import ILoginService, IPasswordService, IUserService
from src.helper.errors import fail
from src.infrastructure.postgresql.models.user import UserORM
from src.infrastructure.postgresql.repositories.user import IUserRepository

pwd_context = CryptContext(schemes=["bcrypt"])


class PasswordService(IPasswordService):
    def validate_password_strength(self, plain_password: str) -> bool:
        if not 8 <= len(plain_password) <= 16:
            fail(
                PasswordInvalidException(
                    "Invalid password. The password has to has length from 8 to 16 character"
                )
            )
        lower_case = any(char.islower() for char in plain_password)
        upper_case = any(char.isupper() for char in plain_password)
        digit_case = any(char.isdigit() for char in plain_password)
        special_case = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", plain_password))
        if not (lower_case and upper_case and digit_case and special_case):
            fail(
                PasswordInvalidException(
                    "Invalid password. The password has to lower case, upper case, digit case and special case"
                )
            )

        return True

    def get_hash_password(self, plain_password: str) -> str:
        if self.validate_password_strength(plain_password):
            return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hash_password: str) -> bool:
        if self.validate_password_strength(plain_password):
            return pwd_context.verify(plain_password, hash_password)


@dataclass(frozen=True)
class UserService(IUserService):
    repostitory: IUserRepository

    async def get_by_username(self, username: str) -> User:
        user = await self.repostitory.get_by_username(username)
        if not user:
            fail(UserIsNotFoundException)
        return user

    async def create(self, user: User) -> User:
        user_orm = UserORM.from_entity(user)
        user_orm = await self.repostitory.create(user_orm)
        return user_orm.to_entity()

    async def update(self, user: User) -> User:
        user = await self.get_by_username(user.username)
        user_orm = UserORM.from_entity(user)
        user_orm = await self.repostitory.update(user_orm)
        return user_orm.to_entity()


@dataclass(frozen=True)
class LoginService(ILoginService):
    user_service: IUserService
    password_service: IPasswordService

    async def authenticate(self, username: str, password: str) -> bool:
        user = await self.user_service.get_by_username(username)
        if not self.password_service.verify_password(password, user.password):
            fail(
                PasswordInvalidException("Invalid password. The password is incorrect")
            )
        return True
