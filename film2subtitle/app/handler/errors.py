__all__ = [
    "Film2SubtitleAPIError",
    "BadRequestError",
    "NotFoundError",
    "UnauthorizedError",
    "InvalidUrlError",
]


class Film2SubtitleAPIError(Exception):
    """Base class for Film2SubtitleAPI errors."""

    # skipcq: PYL-W0231
    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return f"{self.message} [{self.status_code}]"

    __repr__ = __str__


class NotFoundError(Film2SubtitleAPIError):
    """Raised when a resource is not found on the server."""

    def __init__(
        self,
        message: str = "Resource not found",
        status_code: int = 404,
    ) -> None:
        super().__init__(message, status_code)


class BadRequestError(Film2SubtitleAPIError):
    """Raised when a request is malformed or invalid."""

    def __init__(self, message: str = "Bad request", status_code: int = 400) -> None:
        super().__init__(message, status_code)


class UnauthorizedError(Film2SubtitleAPIError):
    """Raised when the user is not authorized to access the resource."""

    def __init__(self, message: str = "Unauthorized", status_code: int = 401) -> None:
        super().__init__(message, status_code)


class InvalidUrlError(Film2SubtitleAPIError):
    """Raised when the URL is not a valid Film2Subtitle URL."""

    def __init__(
        self,
        message: str = "Invalid URL",
        status_code: int = 400,
        url: str = None,
    ) -> None:
        super().__init__(message, status_code)
        self.url = url
