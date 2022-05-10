import re

HTTP_URL_REGEX = re.compile(
    r"https?://(www\.)?[-a-zA-Z\d@:%._+~#=]{1,256}"
    r"\.[a-zA-Z\d()]{1,6}\b([-a-zA-Z\d()@:%_+.~#?&/=]*)",
)


def valid_film2subtitle_url(url: str) -> bool:
    """Return `True` if the given URL is a valid Film2Subtitle URL."""
    return bool(HTTP_URL_REGEX.match(url) and "film2subtitle.com" in url)
