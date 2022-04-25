import uvicorn

from film2subtitle.app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "film2subtitle.app.main:app",
        host="0.0.0.0" if not settings.DEBUG else "127.0.0.1",
        port=8000,
        reload=settings.DEBUG,
    )
