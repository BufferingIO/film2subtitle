# ♻️ Changelog

All notable changes to the _Film2Subtitle API_ will be documented in this file.

The format used in this document is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 1.0.3 ()

### Added

- Added a new enum value to `MediaType` to represent `unknown` media type (that the download box is empty).

### Changed

- Changed HTTP method for updating users to `PUT` (`PATCH` is not supported by the API anymore).
- Now creating users from `/api/v1/users` endpoint is only possible for superusers.
- Changed the name for `LegacySearchParser`'s `iter_results` method to `iter_articles`.
- Changed return type hint for `LegacySearchParser.iter_articles` to `Iterator[SubtitleArticle]`.
- Use `list` class on `LegacySearchParser.iter_articles` iterator instead of unpacking it.
- Changed the doc-string for `Film2Subtitle.legacy_search` a little to make it more clear.
- Changed the `type_` attribute of download box to `media_type` and also `SubtitleType` enum class
to `MediaType`.
- Changed the enum value `series` to `tv` in `MediaType` enum class.

### Removed

- Removed FUNDING information.
- Removed unnecessary parameters (`search_query`, `page`) from `LegacySearchParser` initialization process.
- Removed `typing.Optional` from the `page` parameter of `Film2Subtitle.legacy_search` method and gave it a default value of `1`.

## 1.0.2 (2022-06-05)

### Added

- Add FUNDING info to github workflows.
- Add database models, configs, utils, etc.
- Schemas for user and OAuth2 tokens.
- Add more details about response codes in `/api/v1/subs/` endpoint.
- Add new banner for repository.
- Add configs for gitpod.

Below packages are newly added to the project:

- SQLAlchemy (v1.4.36) for database management.
- psycopg2 (v2.9.3) for PostgreSQL support.
- email-validator (v1.2.1) to validate user email address.
- python-jose (v3.3.0) for JWT token generation and verification.
- passlib (v1.7.4) for password hashing.
- python-multipart (v0.0.5) to support `OAuth2PasswordRequestForm` in `/api/v1/login/` endpoint for access token generation.

### Changed

- Bump FastAPI to v0.77.0.
- Bump pyupgrade to v2.32.1 for pre-commit.
- Bump mirros-mypy to v0.960 for pre-commit.

### Removed

- Remove redundant classmethod decorator for validators in project's settings.

## 1.0.1 (2022-5-10)

### Added

- Added changelog file.

### Changed

- Refactored utility function `valid_film2subtitle_url`.
- Changed the documentation of some dataclasses and parser classes.
- Renamed specific variables to a meaningful name.
- Changed the minimum value of `total_pages` parameter in legacy search results to `0`

### Removed

- Removed `query` and `page` parameters from legacy search result.
- Removed poetry buildpack from Heroku deployment workflow.
