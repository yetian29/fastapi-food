from src.domain.base.errors import BaseDomainException


class BaseCustomerException(BaseDomainException):
    pass


class InvalidCredentialException(BaseCustomerException):
    pass


class TokenExpiredException(BaseCustomerException):
    pass


class CustomerIsNotFoundException(BaseCustomerException):
    pass
