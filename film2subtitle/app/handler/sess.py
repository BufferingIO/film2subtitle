from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Set
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from httpx import AsyncClient

from film2subtitle.app.handler.errors import *

if TYPE_CHECKING:
    from httpx import Response


def _validate_response(response: "Response") -> "Response":
    """Validate the response status code and raise appropriate errors."""
    error_map = {
        400: BadRequestError,
        401: UnauthorizedError,
        404: NotFoundError,
    }

    if response.status_code not in (200, 301, 302, 304):
        if err := error_map.get(response.status_code):
            raise err()
        else:
            raise Film2SubtitleAPIError(
                response.reason_phrase,
                response.status_code,
            )  # noqa: E501
    return response


class AsyncSession:
    """An asynchronous session for requesting `film2subtitle.com` endpoints.

    Parameters:
        html_parser (`str`): The HTML parser to use for parsing the responses
        as `bs4.BeautifulSoup` objects.

    Note:
        - The `html_parser` parameter is optional. If not provided, the default
        HTML parser will be used (`lxml`).

        - To request a URL that is not a `film2subtitle.com` endpoint, use the
        `request` method on the :class:`httpx.AsyncClient` object returned by
        :property:`AsyncSession.client` property.
    """

    BASE_URL: ClassVar[str] = "https://film2subtitle.com/"
    DEFAULT_HTML_PARSER: ClassVar[str] = "lxml"
    VALID_HTML_PARSERS: ClassVar[Set[str]] = {
        "lxml",
        "html5lib",
        "html.parser",
    }
    DEFAULT_HEADERS: ClassVar[Dict[str, str]] = {
        "Host": "film2subtitle.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    }

    __slots__ = ("_client", "html_parser")

    def __init__(self, html_parser: Optional[str] = None) -> None:
        self.html_parser = html_parser or self.DEFAULT_HTML_PARSER
        # check if the HTML parser is valid
        if self.html_parser not in self.VALID_HTML_PARSERS:
            raise ValueError(
                f"Invalid HTML parser: {self.html_parser}. "
                f"Valid HTML parsers: {', '.join(self.VALID_HTML_PARSERS)}",
            )
        self._client = AsyncClient(verify=False)

    def __enter__(self) -> "AsyncSession":
        return self

    async def __aenter__(self) -> "AsyncSession":
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    @property
    def client(self) -> AsyncClient:
        """Return the :class:`httpx.AsyncClient` object used for making requests."""
        return self._client

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        allow_redirects: bool = True,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> "Response":
        """Make a request to a URL from the `film2subtitle.com` domain.

        Parameters:
            method (`str`): The HTTP method to use.
            url (`str`): The URL to request (relative to the base URL).
            params (`dict`): The URL parameters to use.
            data (`dict`): The data to send in the request.
            headers (`dict`): The headers to send in the request.
            allow_redirects (`bool`): Whether to allow redirects.
            timeout (`float`): The timeout for the request.
            kwargs: Additional keyword arguments to pass to :meth:`httpx.AsyncClient.request`.

        Returns:
            :class:`httpx.Response`: The response.
        """
        # join the base URL with the URL
        _url = urljoin(self.BASE_URL, url)
        # create the headers
        _headers = self.DEFAULT_HEADERS.copy()
        if headers:
            _headers.update(headers)
        # make the request
        response = await self._client.request(
            method,
            _url,
            params=params,
            data=data,
            headers=_headers,
            follow_redirects=allow_redirects,
            timeout=timeout,
            **kwargs,
        )
        return _validate_response(response)

    async def json(self, url: str, **kwargs) -> Any:
        """Get the JSON response from a URL.

        Parameters:
            url (`str`): The URL to request (relative to the base URL).
            kwargs: Additional keyword arguments to pass to :meth:`AsyncSession.request`.

        Returns:
            `Any`: The JSON response.
        """
        response = await self.request("GET", url, **kwargs)
        return response.json()

    async def html(self, url: str, **kwargs) -> BeautifulSoup:
        """Get the parsed HTML response from a URL as a `bs4.BeautifulSoup` object.

        Parameters:
            url (`str`): The URL to request (relative to the base URL).
            kwargs: Additional keyword arguments to pass to :meth:`AsyncSession.request`.

        Returns:
            :class:`bs4.BeautifulSoup`: The HTML response.
        """
        response = await self.request("GET", url, **kwargs)
        return BeautifulSoup(response.text, self.html_parser)

    async def close(self) -> None:
        """Close the API session."""
        await self._client.aclose()
