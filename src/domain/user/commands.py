from dataclasses import dataclass

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
class ForgetPasswordCommand:
    email: str

