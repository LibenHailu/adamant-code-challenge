import os
from typing import ClassVar, List, Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

ENV: str = ""


class Configs(BaseSettings):
    ENV: str = os.getenv("ENV", "dev")

    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    APP_VERSION: str = "0.0.1"
    PROJECT_TITLE: str = "Adamant Challenge Backend Application"

    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    ENV_DATABASE_MAP: dict = {
        "prod": "adamant-prod-db",
        "dev": "verceldb",  # free neon dev db - change later
        "test": "adamant-test-db",
    }

    DB: str = os.getenv("DB", "postgresql")
    DB_USER: Optional[str] = os.getenv("DB_USER", "default")
    DB_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD", "secret")
    DB_HOST: Optional[str] = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_ENGINE: str = "postgresql"

    DATABASE_URI_FORMAT: str = (
        "{db_engine}://{user}:{password}@{host}:{port}/{database}"
    )

    # DATABASE_URI: ClassVar[str] = (
    #     "{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
    #         db_engine=DB_ENGINE,
    #         user=DB_USER,
    #         password=DB_PASSWORD,
    #         host=DB_HOST,
    #         port=DB_PORT,
    #         database=ENV_DATABASE_MAP[ENV],
    #     )
    # )
    DATABASE_URI: str = os.getenv("DATABASE_URL", "")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")


configs = Configs()
