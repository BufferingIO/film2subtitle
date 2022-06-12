from typing import TYPE_CHECKING, Optional

from film2subtitle.app.handler.errors import InvalidUrlError
from film2subtitle.app.handler.sess import AsyncSession
from film2subtitle.app.handler.utils import valid_film2subtitle_url

from film2subtitle.app.handler.parsers import (  # isort:skip
    DownloadPageParser,
    LegacySearchParser,
)

if TYPE_CHECKING:
    from film2subtitle.app.handler.types import (  # isort:skip
        DownloadPage,
        LegacySearchResult,
    )


class Film2Subtitle(AsyncSession):
    """API handler to interact with main features of `film2subtitle.com` website."""

    async def legacy_search(
        self,
        query: str,
        page: int = 1,
    ) -> "LegacySearchResult":
        """
        Search for a Movie or TV show on `film2subtitle.com` website by parsing
        the html of search results.

        Parameters:
            query (`str`): The query to search for.
            page (`int`): The page number to search for. Defaults to `1`.

        Returns:
            :class:`LegacySearchResult`: The parsed search result object.

        Raises:
            If the requested page for :param:`query` is not found,
            might raise a :class:`NotFoundError`.
        """
        if not isinstance(page, int) and page < 1:
            raise ValueError("Page number must be an integer greater than 0.")
        url = f"/page/{page}/?s={query}" if page > 1 else f"/?s={query}"
        soup = await self.html(url)
        return LegacySearchParser(soup).parse()

    async def download_page(self, url: str) -> "DownloadPage":
        """Get the download page of a subtitle.

        Parameters:
            url (`str`): The URL of the subtitle.

        Returns:
            :class:`DownloadPage`: The parsed download page object.

        Raises:
            :class:`InvalidUrlError`: If the URL is not a valid `film2subtitle.com` URL.
            :class:`NotFoundError`: If the subtitle page is not found.
        """
        if not valid_film2subtitle_url(url):
            raise InvalidUrlError(
                "The provided URL is not a valid film2subtitle.com URL.",
                url=url,
            )
        soup = await self.html(url)
        return DownloadPageParser(soup).parse()
