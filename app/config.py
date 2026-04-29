from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    app_name: str = "Jade 2D Gateway"
    debug: bool = False

    # Neon (Serverless Postgres)
    database_url: str = ""

    # Xendit
    xendit_secret_key: str = ""
    xendit_public_key: str = ""
    xendit_webhook_token: str = ""

    # Risk engine thresholds
    velocity_max_attempts_per_hour: int = 5
    velocity_max_amount_per_day: float = 50_000.0

    # Set to True to simulate 2D charges without hitting Xendit
    simulate_2d: bool = False


settings = Settings()
