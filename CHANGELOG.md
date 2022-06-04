# ♻️ Changelog

All notable changes to the _Film2Subtitle API_ will be documented in this file.

The format used in this document is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
- Removed poetry buildpack from Heroku deployement workflow.
