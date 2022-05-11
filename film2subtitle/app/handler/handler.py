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
        page: Optional[int] = None,
    ) -> "LegacySearchResult":
        """
        Search for a Movie or TV show on `film2subtitle.com` website by web scraping the
        search results page (known as the legacy search because it is the old search type
        and in the new version we use JSON API).

        Parameters:
            query (`str`): The query to search for.
            page (`int`, optional): The page number to search for. Defaults to `1`.

        Returns:
            :class:`LegacySearchResult`: The parsed search result object.

        Raises:
            If the requested page for :param:`query` is not found,
            might raise a :class:`NotFoundError`.
        """
        if page and not isinstance(page, int):
            raise TypeError("page number must be an integer")
        _page = abs(page or 1)
        url = f"/page/{_page}/?s={query}" if _page > 1 else f"/?s={query}"
        soup = await self.html(url)
        parser = LegacySearchParser(soup, query, _page)
        return parser.parse()

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
        parser = DownloadPageParser(soup)
        return parser.parse()
