from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Environment settings
    TARGET_ENV: str = "dev"
    LOG_LEVEL: str = "INFO"
    # Backend settings
    BACKEND_URL: str = "http://backend:8000"

    # Database settings
    POSTGRES_DB: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_PORT: str | None = None
    POSTGRES_HOST: str | None = None
    # Langfuse settings
    LANGFUSE_SECRET_KEY: str | None = None
    LANGFUSE_PUBLIC_KEY: str | None = None
    LANGFUSE_HOST: str | None = None

    # General settings
    ARTIFICIAL_DELAY_DURATION: int = 10
    MAX_RECURSION_DEPTH: int = 5
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
