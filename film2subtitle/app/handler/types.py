from dataclasses import dataclass, field
from typing import List

__all__ = [
    "SubtitleArticle",
    "SubtitleMetadata",
    "LegacySearchResult",
    "DownloadBox",
    "DownloadPage",
]


# Common types used in the API (e.g. legacy search and download page).
@dataclass
class SubtitleMetadata:
    """The metadata parsed from a subtitle article.
    This metadata can be retrieved from a legacy search result or
    from the download page of a subtitle.
    """

    name: str
    duration: str
    language: str
    country: str
    subtitle_file_format: str
    quality: str
    imdb_id: str = field(default_factory=str)
    imdb_rating: float = field(default_factory=float)
    actors: List[str] = field(default_factory=list)
    writers: List[str] = field(default_factory=list)


@dataclass
class SubtitleArticle:
    """
    Represents a parsed subtitle article from a `div` tag with class `sub-article-detail`.
    """

    title: str
    url: str
    thumbnail: str
    metadata: SubtitleMetadata


# Types used in the legacy search API.
@dataclass
class LegacySearchResult:
    """A list of search results returned by the legacy search endpoint."""

    query: str
    page: int
    next_page: int = field(init=False)
    total_pages: int
    results: List[SubtitleArticle]

    def __post_init__(self) -> None:
        self.next_page = self.page + 1 if self.page < self.total_pages else 1


@dataclass
class DownloadBox:
    """A download box containing links to download a subtitle."""

    type_: str
    links: dict


@dataclass
class DownloadPage:
    """Represents download page of a subtitle."""

    articles: List[SubtitleArticle]
    download_box: DownloadBox
