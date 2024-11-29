from pydantic import BaseModel


class ApiSettings(BaseModel):
    """api jwt secret key"""

    secret_key: str


class Settings:
    api: ApiSettings


settings = Settings()
