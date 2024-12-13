from functools import lru_cache

import punq

from src.domain.user.services import ILoginService, IPasswordService, IUserService
from src.domain.user.use_cases import LoginUserUseCase, RegisterUserUseCase
from src.infrastructure.postgresql.database import Database
from src.infrastructure.postgresql.repositories.user import (
    IUserRepository,
    PostgresUserRepository,
)
from src.service.user import LoginService, PasswordService, UserService


@lru_cache(1)
def get_container() -> punq.Container:
    return init_container()


def init_container() -> punq.Container:
    container = punq.Container()
    container.register(Database, scope=punq.Scope.singleton)

    container.register(IUserRepository, PostgresUserRepository)
    container.register(IUserService, UserService)
    container.register(ILoginService, LoginService)
    container.register(IPasswordService, PasswordService)
    container.register(RegisterUserUseCase)
    container.register(LoginUserUseCase)
    return container
