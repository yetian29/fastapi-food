from src.domain.base.errors import BaseDomainException


class BaseUserException(BaseDomainException):
    pass


class UserIsNotFoundException(BaseUserException):
    pass


class CrendentialUserException(BaseUserException):
    pass


class PasswordInvalidException(CrendentialUserException):
    pass