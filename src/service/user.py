import re
from dataclasses import dataclass
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from src.core.config.settings import settings
from src.domain.user.entities import User
from src.domain.user.errors import PasswordInvalidException, UserIsNotFoundException, DataVerifyAreNotFoundException, CodeIsNotMatch, CodeHasExpiredException
from src.domain.user.services import ILoginService, IPasswordService, IUserService
from src.helper.errors import fail
from src.infrastructure.postgresql.models.user import UserORM
from src.infrastructure.postgresql.repositories.user import IUserRepository
import random
from datetime import datetime, timedelta
import dataclass, Field
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

pwd_context = CryptContext(schemes=["bcrypt"])

class GoogleAuthentication(IAuthAvailableAreProvided):
    def get_user_by_auth_provider(self, token: str):
        headers = {
           "Authorization": f"Bearer {token}"
        }
        pass

class AppleAuthentication(IAuthAvailableAreProvided):
    pass
    
@dataclass
class CodeService(ICodeService):
    cache: dict = Field(default_factory=dict)
    
    def generate_code(self, email: str | None = None, username: str | None = None, expire_delta: timedeta | None = None) -> str:
        code = str(random.randint(100000, 999999))
        if expire_delta:
            expire = datetime.now() + expire_delta
        else:
            expire = datetime.now() + timedelta(minutes=5)
        data = {
            "code": code,
            "expire": expire
        }
        key = username if username else email
        self.cache[key] = data
        return code

    def validate_code(self, email: str | None = None, username: str | None = None, code: str) -> bool:
        key = username if username else email
        data = self.cache.get(key)
        if not data:
            fail(DataVerifyAreNotFoundException)
        elif code != data.get("code"):
            del self.cache[key]
            fail(CodeIsNotMatch)
        elif datetime.now() > data.get("expire"):
            del self.cache[key]
            fail(CodeHasExpiredException)
        del self.cache[key]
        return True
            
class SendCodeService:
    def send_code(self, email: str, code: str) -> None:
        """Send OTP via email using SendGrid"""
        message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=email,
        subject='Your OTP Verification Code',
        html_content=f'''
            <div style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>OTP Verification</h2>
                <p>Your OTP code is: <strong>{otp}</strong></p>
                <p>This code will expire in 10 minutes.</p>
                <p>If you didn't request this code, please ignore this email.</p>
            </div>
        '''
    ) 
        sg = SendGridAPIClient(
            settings.SENDGRID_KEY
        )
        sg.send(message)
            
        print(f"The code <{code}> has been sent to email <{email}>")
        
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

    def get_hash_password(self, plain_password: str) -> str:
        if self.validate_password_strength(plain_password):
            return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hash_password: str) -> bool:
        if self.validate_password_strength(plain_password):
            return pwd_context.verify(plain_password, hash_password)


@dataclass(frozen=True)
class UserService(IUserService):
    repository: IUserRepositor

    async def get_by_username_or_email(self, username: str | None = None, email: str | None = None) -> User:
        user = await self.repository.get_by_username_or_email(username, email)
        if not user:
            fail(UserIsNotFoundException)
        return user

    async def get_by_oid(self, oid: str) -> User:
        user = await self.repository.get_by_oid(oid)
        if not user:
            fail(UserIsNotFoundException)
        return user

    async def create(self, user: User) -> User:
        user_orm = UserORM.from_entity(user)
        user_orm = await self.repository.create(user_orm)
        return user_orm.to_entity()

    async def update(self, user: User) -> User:
        user_orm = UserORM.from_entity(user)
        user_orm = await self.repository.update(user_orm)
        return user_orm.to_entity()

    async def delete(self, oid: str) -> User:
        user_orm = await self.get_by_oid(oid)
        await self.repository.delete(oid)
        return user_orm.to_entity()
        


@dataclass(frozen=True)
class LoginService(ILoginService):       
    def generate_token_and_is_active(
        self, user: User, expire_delta: timedelta | None = None
    ) -> str:
        if expire_delta:
            expire = datetime.now() + expire_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)

        data = {"sub": user.oid, "exp": expire}
        encoded_jwt = jwt.encode(
            data, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        user.is_active = True
        return encoded_jwt
