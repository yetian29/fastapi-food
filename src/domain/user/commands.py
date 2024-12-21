from dataclasses import dataclass

from sqlalchemy import UUID

from src.domain.user.entities import User


@dataclass(frozen=True)
class RegisterUserCommand:
    user: User


@dataclass(frozen=True)
class LoginUserCommand:
    email: str
    username: str
    password: str


@dataclass(frozen=True)
class ChangePasswordCommand:
    email: str | None = None
    username: str | None = None
    current_password: str
    new_password: str


@dataclass(frozen=True)
class GetUserCommand:
    oid: UUID


@dataclass(frozen=True)
class ForgetPasswordCommand:
    email: str


@dataclass(frozen=True)
class VerifyCodeSentToEmailForForgetPasswordCommand:
    email: str
    code: str


@dataclass(frozen=True)
class CreateNewPasswordCommand:
    user: User
    password: str
