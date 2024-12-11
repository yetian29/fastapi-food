import re

from src.domain.user.errors import PasswordInvalidException
from src.domain.user.services import IPasswordService
from src.helper.errors import fail


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
