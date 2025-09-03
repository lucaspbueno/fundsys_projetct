from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    POSTGRES_USER    : str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST    : str
    POSTGRES_PORT    : str = "5432"
    POSTGRES_DB      : str
    DEBUG            : bool = False

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",     # caminho
        env_prefix="",       # sem prefixo no nome das variáveis ex: env_prefix="BE" BE_POSTGRES_URL = ....
        case_sensitive=False # case sensitive no nome das variáveis ex: BE_POSTGRES_URL !== be_postgres_url
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
