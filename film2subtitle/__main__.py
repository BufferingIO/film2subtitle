import uvicorn

from film2subtitle.app.core.config import settings


def run_uvicorn_server() -> None:
    """Run the uvicorn server in development environment."""
    uvicorn.run(
        "film2subtitle.app.main:app",  # path to the FastAPI application
        host="127.0.0.1" if settings.DEBUG else "0.0.0.0",  # skipcq: BAN-B104
        port=8000,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    run_uvicorn_server()
