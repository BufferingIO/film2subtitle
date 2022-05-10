# ♻️ Changelog

All notable changes to the _Film2Subtitle API_ will be documented in this file.

The format used in this document is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
