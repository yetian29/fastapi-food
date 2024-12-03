from dataclasses import dataclass

from src.domain.customer.commands import LoginCustomerCommand, RegisterCustomerCommand
from src.domain.customer.entities import Customer
from src.domain.customer.services import ICustomerLoginService, ICustomerService


@dataclass(frozen=True)
class RegisterCustomerUseCase:
    customer_service: ICustomerService

    async def execute(self, command: RegisterCustomerCommand) -> Customer:
        return await self.customer_service.create(customer=command.customer)


@dataclass(frozen=True)
class LoginCustomerUseCase:
    customer_login_service: ICustomerLoginService

    async def execute(self, command: LoginCustomerCommand) -> tuple[str, str]:
        customer = await self.customer_login_service.authenticate(
            username=command.username, password=command.password
        )
        return self.customer_login_service.generate_access_token_and_refresh_token_and_is_active(
            customer
        )
