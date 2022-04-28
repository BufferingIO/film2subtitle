from fastapi import APIRouter, Query, status
from fastapi.exceptions import HTTPException

from film2subtitle.app import schemas
from film2subtitle.app.handler import api_handler
from film2subtitle.app.handler.errors import InvalidUrlError, NotFoundError
from film2subtitle.app.handler.types import DownloadPage, LegacySearchResult

router = APIRouter()


@router.get(
    "/search/legacy",
    response_model=schemas.LegacySearchResult,
    status_code=status.HTTP_200_OK,
    summary="Search for a subtitle using the legacy search API (web scraping).",
    response_description="The subtitle legacy search result.",
)
async def legacy_search(
    query: str = Query(
        ...,
        title="Search query",
        description="The query to search for.",
        example="Avengers",
    ),
    page: int = Query(
        1,
        title="Page number",
        description="The page number to return.",
        gt=0,
    ),
) -> LegacySearchResult:
    """Legacy search endpoint for subtitles."""
    empty_result = LegacySearchResult(
        query=query,
        page=page,
        total_pages=1,
        results=[],
    )

    try:
        return await api_handler.legacy_search(query, page)
    except NotFoundError:
        return empty_result


@router.get(
    "/download",
    response_model=schemas.DownloadPage,
    status_code=status.HTTP_200_OK,
    summary="Download a subtitle by its URL.",
    response_description="The subtitle download page.",
)
async def download_page(
    url: str = Query(
        ...,
        title="Subtitle URL",
        description="The URL of the subtitle to download.",
    ),
) -> DownloadPage:
    """Download page endpoint for subtitles."""
    try:
        return await api_handler.download_page(url)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested download page not found.",
        ) from e
    except InvalidUrlError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The given URL is not a valid Film2Subtitle URL.",
        ) from e
