# TODOs

I put future plans for this project in this file.

## Completed ✅

- [x] Implement user authentication using OAuth2 password flow.
  - [x] Add settings for database (`Host`, `Port`, ...) and first superuser (`Name`, `email`, ...)
  - [x] Create database utilities (crud operation generic classes) and models (SQLAlchemy ORM)
  - [x] Create schemas for users and security payloads (e.g. access token)
  - [x] Implement security utilities and dependencies for OAuth

## Work in progress ⚒️

## Planned 📝

- [ ] Implement API parsers for movies and series page.
- [ ] Add a new method of searching subtitles that uses `wp-json` endpoint of the film2subtitle website.
  (e.g. for creating tokens and validating them)
- [ ] Add support for adding custom headers/cookies to each request.
- [ ] Add proxy server support to the API handler to prevent the API from being blocked by the website.
