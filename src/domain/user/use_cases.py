from dataclasses import dataclass

from src.domain.user.commands import LoginUserCommand, RegisterUserCommand
from src.domain.user.entities import User
from src.domain.user.errors import UserIsExsitedException
from src.domain.user.services import ILoginService, IUserService
from src.helper.errors import fail


@dataclass(frozen=True)
class RegisterUserUseCase:
    user_service: IUserService

    async def execute(self, command: RegisterUserCommand) -> User:
        if await self.user_service.get_by_username(username=command.user.username):
            fail(UserIsExsitedException("The user is exsited. Please login account"))
        return await self.user_service.create(user=command.user)


@dataclass(frozen=True)
class LoginUserUseCase:
    login_service: ILoginService

    async def execute(self, command: LoginUserCommand) -> str:
        user = await self.login_service.authenticate(
            username=command.username, password=command.password
        )
        return await self.login_service.generate_token_and_is_active(user)
