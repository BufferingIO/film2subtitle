from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from httpx import RequestError

from film2subtitle.app import schemas
from film2subtitle.app.api.v1 import api_router as api_v1_router
from film2subtitle.app.core.config import settings
from film2subtitle.app.handler import api_handler

openapi_tags = [
    {
        "name": "Subtitles",
        "description": "Endpoints related to subtitles search and download.",
    },
    {
        "name": "Health",
        "description": "Endpoints related to health check and status of the service.",
    },
]

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=openapi_tags,
    docs_url=None,  # Set this to None to serve the Swagger UI at another URL
)

# Mount the static files
app.mount("/static", StaticFiles(directory="film2subtitle/app/static"), name="static")

# add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add the version 1 API router to the app
app.include_router(api_v1_router, prefix=settings.API_V1_STR)


# add a custom error handler for 'HTTPException's
@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException) -> JSONResponse:
    """:class:`HTTPException` error handler."""
    ecode_mapping = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        406: "NOT_ACCEPTABLE",
        409: "CONFLICT",
        500: "INTERNAL_SERVER_ERROR",
    }
    content = {
        "error": ecode_mapping.get(exc.status_code, "UNKNOWN_ERROR"),
        "message": exc.detail,
    }
    return JSONResponse(
        content=content,
        status_code=exc.status_code,
        headers=exc.headers,
    )


@app.exception_handler(RequestError)
async def api_client_error_handler(_, __) -> JSONResponse:
    """Client connection error handler."""
    return JSONResponse(
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": (
                "The server encountered an internal error and was unable to "
                "connect to the API. Please try again later."
            ),
        },
        status_code=500,
    )


@app.on_event("shutdown")
async def clean_up_on_shutdown() -> None:
    """Clean up the resources before shutdown."""
    # close the api handler session
    await api_handler.close()


# Override the documentation endpoint to serve a customized version
@app.get(f"{settings.API_V1_STR}/docs", include_in_schema=False)
async def get_docs_v1() -> HTMLResponse:
    """A custom route to override the default swagger UI for the v1 API."""
    return get_swagger_ui_html(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        title=f"{settings.PROJECT_NAME} | Documentation",
        swagger_favicon_url=settings.DOCS_FAVICON_PATH,
    )


# A simple health check endpoint that always returns 200
@app.get(
    f"{settings.API_V1_STR}/health",
    tags=["Health"],
    response_model=schemas.HealthCheck,
    response_description="Health check response.",
)
async def health_check() -> JSONResponse:
    """A simple health check endpoint to check the service status."""
    return JSONResponse(
        content={"status": "OK"},
    )
