from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str
    user: str
    password: str
    port: str
    database: str

    @property
    def async_postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class ApiSettings(BaseModel):
    secret_key: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow",
    )

    # Define environment variables directly
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    SECRET_KEY: str

    @property
    def database(self) -> DatabaseSettings:
        return DatabaseSettings(
            host=self.POSTGRES_HOST,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )

    @property
    def api(self) -> ApiSettings:
        return ApiSettings(secret_key=self.SECRET_KEY)


settings = Settings()
