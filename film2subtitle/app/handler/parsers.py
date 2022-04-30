import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional

from bs4 import BeautifulSoup

from film2subtitle.app.handler.errors import NotFoundError

from film2subtitle.app.handler.types import (  # isort:skip
    DownloadBox,
    DownloadPage,
    LegacySearchResult,
    SubtitleArticle,
    SubtitleMetadata,
)

if TYPE_CHECKING:
    from bs4.element import Tag

    # Since the bs4.element.ResultSet is actually a list of "Tag" objects,
    # we can just use typing.List instead of bs4.element.ResultSet for type annotations.

METADATA_MAP = {
    "نام": "name",
    "زمان": "duration",
    "زبان": "language",
    "کشور": "country",
    "فرمت": "subtitle_file_format",
    "کیفیت": "quality",
    "امتیاز": "imdb_rating",
    "بازیگران": "actors",
    "نویسنده": "writers",
}


def _metadata_mapper(metadata: Dict[str, Any], key: str, value: str) -> None:
    """Map the metadata key to the metadata value based on the mapping table."""
    for k, v in METADATA_MAP.items():
        if k in key:
            if v == "imdb_rating":
                # The IMDb rating can be a float or an integer.
                if match := re.search(r"\d+\.?\d*", value):
                    value = float(match.group())  # type: ignore
                else:
                    # If the rating is not found, set it to 0.0
                    value = 0.0  # type: ignore
            # For actors and writers, we need to split the value by comma to get a list of names.
            if v in ("actors", "writers"):
                # filter out empty strings from the list.
                value = list(filter(None, map(str.strip, value.split(","))))  # type: ignore # noqa: E501
            metadata[v] = value


def _parse_metadata(tag_obj: "Tag") -> Dict[str, Any]:
    """Parse the metadata of a subtitle article."""
    # TODO: Parse metadata in subtitle article header wrapper. (e.g. release date)
    metadata: Dict[str, Any] = {}
    meta_li_tags: List["Tag"] = tag_obj.find_all(class_=re.compile("^sub-meta-*"))
    for li in meta_li_tags:
        left: Optional["Tag"] = li.find(class_="sub-meta-left")
        right: Optional["Tag"] = li.find(class_="sub-meta-right")
        for side in (left, right):
            if not side:
                continue
            key, value = side.get_text(strip=True).split(":", 1)
            # clean up the key and value
            key = key.replace(" ", "").replace("-", "").lower()
            value = value.replace("\n", "").strip()
            # map the key and value to the metadata dict
            _metadata_mapper(metadata, key, value)
    if imdb_url := tag_obj.find(href=re.compile("imdb.com")):
        # IMDb ID pattern: tt\d+
        if match := re.search(r"tt\d+", imdb_url.get("href")):
            metadata["imdb_id"] = match.group()
    return metadata


def _parse_subtitle_article(tag_obj: "Tag") -> Dict[str, Any]:
    """Return parsed subtitle article."""
    return {
        "title": tag_obj.find("h1").get_text(strip=True),
        "url": tag_obj.find_all("a")[0].get("href"),
        "thumbnail": tag_obj.find("img").get("src"),
        "metadata": _parse_metadata(tag_obj),
    }


def _parse_download_box(download_box: "Tag") -> Dict[str, Any]:
    """Return parsed download box from the download page."""
    dl: Dict[str, Any] = {
        "type_": "series" if "فصل" in download_box.text else "movie",
        "links": {},
    }
    for link in download_box.find_all("a"):
        href: str = link.get("href")
        if dl["type_"] == "series":
            if season_match := re.search(r"s\d+", href, re.IGNORECASE):
                season: Dict[str, str] = dl["links"].setdefault(
                    season_match.group(),
                    {},  # if the season is not found, create a new dict for it.
                )
                if episode_match := re.search(r"e\d+", href, re.IGNORECASE):
                    season[episode_match.group()] = href
                else:
                    season["all"] = href
            continue
        if "trailer" in href.lower():
            dl["links"]["trailer"] = href
        else:
            dl["links"]["download"] = href
    return dl


class Parser(ABC):
    """Abstract base class for all parsers."""

    def __init__(self, soup_obj: BeautifulSoup) -> None:
        if not isinstance(soup_obj, BeautifulSoup):
            raise TypeError(
                "Parser requires a BeautifulSoup object as input. "
                f"Got {type(soup_obj)} instead.",
            )
        self._soup = soup_obj

    @abstractmethod
    def parse(self) -> Any:
        """Parse the HTML soup and return the parsed data as a specific dataclass."""
        raise NotImplementedError


class LegacySearchParser(Parser):
    """Parser for the legacy search endpoint."""

    def __init__(self, soup_obj: BeautifulSoup, search_query: str, page: int) -> None:
        super().__init__(soup_obj)
        self._search_query = search_query
        self._page = page

    def iter_results(self) -> Generator[SubtitleArticle, None, None]:
        """A generator that yields all results from the search."""
        articles: List["Tag"] = self._soup.find_all(class_="sub-article-detail")
        for article in articles:
            parsed_dict = _parse_subtitle_article(article)
            metadata = parsed_dict.pop("metadata")
            yield SubtitleArticle(
                **parsed_dict,
                metadata=SubtitleMetadata(**metadata),
            )

    @property
    def total_pages(self) -> int:
        """Return the total number of pages for the search results."""
        if page_numbers := self._soup.find_all("a", class_="page-numbers"):
            nums = [
                int(page_number.text)
                for page_number in page_numbers
                if page_number.text.isdigit()
            ]
            return max(nums)
        return 1

    def parse(self) -> LegacySearchResult:
        """Parse the search results and return a :class:`LegacySearchResult`."""
        return LegacySearchResult(
            query=self._search_query,
            page=self._page,
            total_pages=self.total_pages,
            results=[*self.iter_results()],
        )


class DownloadPageParser(Parser):
    """Parser for the download pages."""

    def __init__(self, soup_obj: BeautifulSoup) -> None:
        super().__init__(soup_obj)
        self._download_box = self._soup.find(class_="sub-download-box")
        if not self._download_box:
            raise NotFoundError("No download box found.")

    @property
    def articles(self) -> List[SubtitleArticle]:
        """Return the list of subtitle articles as :class:`SubtitleArticle` objects."""
        articles: List["Tag"] = self._soup.find_all(class_="sub-article-detail")
        return [
            SubtitleArticle(**_parse_subtitle_article(article))
            for article in articles
            if article and article.find("h1")
        ]

    @property
    def download_box(self) -> DownloadBox:
        """Return the parsed download box object."""
        return DownloadBox(**_parse_download_box(self._download_box))

    def parse(self) -> DownloadPage:
        """Parse the download page and return a :class:`DownloadPage` object."""
        return DownloadPage(articles=self.articles, download_box=self.download_box)
