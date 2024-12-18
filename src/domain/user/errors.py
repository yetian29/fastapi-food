from src.domain.base.errors import BaseDomainException


class BaseUserException(BaseDomainException):
    pass

class UserIsNotFoundException(BaseUserException):
    pass

class UserIsExsitedException(BaseUserException):
    pass

class CrendentialUserException(BaseUserException):
    pass

class PasswordInvalidException(CrendentialUserException):
    pass

class OldPasswordInCorrectException(CredentialUserException):
    pass
    
class CodeException(BaseUserException):
    pass
    
class DataVerifyAreNotFoundException(CodeException):
    pass

class CodeIsNotMatchException(CodeException):
    pass

class CodeHasExpiredException(CodeException):
    pass


