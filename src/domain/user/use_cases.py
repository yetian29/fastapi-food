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
        if await self.user_service.get_by_username_or_email(username=command.user.username, email=command.user.email):
            fail(UserIsExsitedException("The user is exsited. Please login account"))
        return await self.user_service.create(user=command.user)


@dataclass(frozen=True)
class LoginUserUseCase:
    login_service: ILoginService
    user_service: IUserService

    async def execute(self, command: LoginUserCommand) -> str:
        user = await self.login_service.authenticate(
            email=command.email,
            username=command.username, password=command.password
        )
        token = await self.login_service.generate_token_and_is_active(user)
        await self.user_service.update(user)
        return token
        

@dataclass(frozen=True)
class ChangePasswordUseCase:
    password_service: IPasswordService
    user_service: IUserService

    async def execute(self, command: ChangePasswordCommand) -> str:
        user = await self.user_service.get_by_username_email(username=command.username, email=command.emai)
        if self.password_service.verify_password(password, user.password):
            hash_password = self.password_service.get_hash_password(command.new_password)
            user.password = hash_password
            await self.user_service.update(user)
            return command.new_password
        fail(OldPasswordIncorrectException)

