from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_dsn: str
    pg_echo: bool = False

    admin_password_hash: str = ""
    jwt_secret: str

    cors_origins: list[str] = ["http://localhost:3000"]

    show_docs: bool = True
    log_lvl: str = "INFO"

    db_pool_size: int = 10
    db_max_overflow: int = 20


settings = Settings()
