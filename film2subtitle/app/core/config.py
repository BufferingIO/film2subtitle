import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator


class Settings(BaseSettings):
    """Settings and configuration for the application."""

    # FastAPI app settings
    API_V1_STR: str = "v1"
    PROJECT_VERSION: str = "1.0.4"
    PROJECT_NAME: str = "Film2Subtitle API"
    PROJECT_DESCRIPTION: str = (
        "A REST API for the film2subtitle.com website that allows you to "
        "search and download subtitles for movies and TV shows.\n\n"
        "This API is open source and is available on "
        "[GitHub](https://github.com/IHosseini083/film2subtitle)!\n\nMake sure to "
        "star the repository if you like it and contribute to it if you're "
        "willing to extend the functionality or improve the current features."
    )
    DOCS_FAVICON_PATH: str = "/static/img/favicon.png"
    DEBUG: bool = True
    CORS_ORIGINS: List[AnyHttpUrl] = []
    # # 60 minutes * 24 hours * 1 days = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    SECRET_KEY: str = secrets.token_urlsafe(32)

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls,  # noqa
        v: Union[str, List[str]],
    ) -> Union[str, List[str]]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database settings
    DATABASE_URL: str

    @validator("DATABASE_URL", pre=True)
    def fix_database_url(cls, v: str) -> str:  # noqa
        return v.replace("postgres://", "postgresql://", 1)

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        env_file = "film2subtitle/.env"
        case_sensitive = True


settings = Settings()
