from dataclasses import dataclass

from src.domain.user.commands import LoginUserCommand, RegisterUserCommand
from src.domain.user.entities import User
from src.domain.user.errors import UserIsExsitedException, PasswordInValidException, OldPasswordIncorrectException
from src.domain.user.services import ILoginService, IUserService
from src.helper.errors import fail


@dataclass(frozen=True)
class RegisterUserUseCase:
    user_service: IUserService

    async def execute(self, command: RegisterUserCommand) -> User:
        if await self.user_service.get_by_username_or_email(command.user.username, command.user.email):
            fail(UserIsExsitedException("The user is exsited. Please login account"))
        return await self.user_service.create(command.user)


@dataclass(frozen=True)
class LoginUserUseCase:
    login_service: ILoginService
    user_service: IUserService
    password_service: IPasswordService

    async def execute(self, command: LoginUserCommand) -> str:
        user = await self.user_service.get_by_username_or_email(command.username, command.email)
        if not self.password_service.verify_password(command.password, user.password):
            fail(
                PasswordInvalidException("Invalid password. The password is incorrect")
            )
        token = await self.login_service.generate_token_and_is_active(user)
        await self.user_service.update(user)
        return token

@dataclass(frozen=True)
class GetUserUseCase: 
    user_service: IUserService
    async def execute(self, command: GetUserCommand) -> User:
        return await self.user_service.get_by_oid(command.oid)

@dataclass(frozen= True)
class GetListUserUseCase:
    user_service: IUserService
    async def execute(self) -> list[User]:
        return await self.user_service.get_list_user()

    
@dataclass(frozen=True)
class ChangePasswordUseCase:
    password_service: IPasswordService
    user_service: IUserService

    async def execute(self, command: ChangePasswordCommand) -> str:
        user = await self.user_service.get_by_username_email(command.username, command.emai)
        if self.password_service.verify_password(command.current_password, user.password):
            hash_password = self.password_service.get_hash_password(command.new_password)
            user.password = hash_password
            await self.user_service.update(user)
            return command.new_password
        fail(OldPasswordIncorrectException)

@dataclass(frozen=True)
class ForgetPasswordUseCase:
    code_service: ICodeService
    send_service: ISendCodeService
    user_service: IUserService
    password_service: IPasswordService

    def execute_one(self, command: ForgetPasswordCommand ) -> str:
        user = await self.user_service.get_by_username_or_email(command.email)
        code = self.code_service.generate_code(user.email)
        self.send_service.send_code(user.email, code)
        return code

    async def execute_two(self, command: VerifyCodeSentToEmailCommand) -> User:
        user = await self.user_service.get_by_username_or_email(command.email)
        self.code_service.validate_code(command.email, command.code)
        return user

    async def execute_three(self, user: User, command: CreateNewPasswordCommand) -> str:
        hash_password = self.password_service.get_hash_password(command.password)
        user.password = hash_password
        await self.user_service.update(user)
        return command.password
        
            
            



