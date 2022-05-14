from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    """Settings and configuration for the application."""

    # FastAPI app settings
    API_V1_STR: str = "/api/v1"
    PROJECT_VERSION: str = "1.0.1"
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

    @classmethod
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[str, List[str]]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database settings
    DATABASE_URL: str

    class Config:
        env_file = "film2subtitle/.env"
        case_sensitive = True


settings = Settings()
