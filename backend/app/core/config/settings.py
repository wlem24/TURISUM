from decimal import Decimal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    APP_NAME: str = "أثر Athar API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # External APIs
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_MAPS_API_KEY: str = ""
    CLOUDINARY_URL: str = ""
    MOYASAR_SECRET_KEY: str = ""

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"

    # Commission rates
    COMMISSION_GUIDE: Decimal = Decimal("0.20")
    COMMISSION_HOTEL: Decimal = Decimal("0.10")

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    # SMTP
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


settings = Settings()
