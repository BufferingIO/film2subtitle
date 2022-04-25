from enum import Enum
from typing import List

from pydantic import BaseModel, Field, HttpUrl


class SubtitleType(str, Enum):
    """The type of subtitle."""

    SERIES = "series"
    MOVIE = "movie"


class SubtitleMetadata(BaseModel):
    """Schema for subtitle metadata extracted from the subtitle article."""

    name: str
    duration: str
    language: str
    country: str
    subtitle_file_format: str
    quality: str
    imdb_id: str
    imdb_rating: float
    actors: List[str]
    writers: List[str]


class SubtitleArticle(BaseModel):
    """Represents a subtitle article."""

    title: str = Field(
        ...,
        title="Article title",
        description="The title of the subtitle article.",
        example="دانلود زیرنویس فارسی سریال Ozark",
    )
    url: HttpUrl = Field(
        ...,
        title="Article URL",
        description="The URL of the subtitle article on the film2subtitle website.",
    )
    thumbnail: str = Field(
        ...,
        title="Article thumbnail",
        description="The URL of the thumbnail of the subtitle article.",
        example="https://film2subtitle.com/wp-content/uploads/2021/10/دانلود-زیرنویس-فارسی-سریال-Ozark.jpg",
    )
    metadata: SubtitleMetadata = Field(
        ...,
        title="Article metadata",
        description="The metadata of the subtitle article.",
        example=SubtitleMetadata(
            name="Fantastic Beasts: The Secrets of Dumbledore",
            duration="2h 22mins",
            language="انگلیسی",
            country="انگلیس",
            subtitle_file_format="srt",
            quality="Blueray",
            imdb_id="tt4123432",
            imdb_rating=6.7,
            actors=[
                "Mads Mikkelsen",
                "Ezra Miller",
                "Katherine Waterston",
            ],
            writers=[
                "J.K. Rowling",
                "Steve Kloves",
            ],
        ),
    )


class LegacySearchResult(BaseModel):
    """Represents a legacy search result."""

    query: str = Field(
        ...,
        title="Search query",
        description="The query that was used to search for the subtitle article.",
    )
    page: int = Field(
        ...,
        title="Search page",
        description="The page of the search result.",
        ge=1,
    )
    total_pages: int = Field(
        ...,
        title="Total search pages",
        description="The total number of pages available for the search query.",
        ge=1,
    )
    results: List[SubtitleArticle] = Field(
        ...,
        title="Search results",
        description="A list of subtitle articles that match the search query.",
    )


class DownloadBox(BaseModel):
    """Represents a download box returned by the downloader API."""

    type_: SubtitleType = Field(
        ...,
        title="Subtitle type",
        description="The type of the subtitle (series or movie).",
    )
    links: dict = Field(
        ...,
        title="Subtitle download links",
        description="A dictionary of subtitle download links.",
    )


class DownloadPage(BaseModel):
    """Represents a download page returned by the downloader API."""

    articles: List[SubtitleArticle] = Field(
        ...,
        title="Subtitle articles",
        description="A list of subtitle articles available in the download page.",
    )
    download_box: DownloadBox = Field(
        ...,
        title="Download box",
        description="The download box of the download page containing the subtitle download links.",
    )
