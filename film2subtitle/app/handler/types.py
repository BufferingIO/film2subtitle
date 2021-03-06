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
from film2subtitle.app.schemas.subtitles import MediaType


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
    """A dataclass containing the results for a legacy search and the number of total pages."""

    total_pages: int
    results: List[SubtitleArticle]


@dataclass
class DownloadBox:
    """A download box containing links to download a subtitle."""

    media_type: MediaType
    links: dict


@dataclass
class DownloadPage:
    """Represents download page of a subtitle."""

    articles: List[SubtitleArticle]
    download_box: DownloadBox
