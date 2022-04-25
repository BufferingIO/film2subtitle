# Film2Subtitle API

[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)](https://fastapi.tiangolo.com)

## Introduction 🗣️

It is a REST API for film2subtitle.com website built with Python and [FastAPI](https://fastapi.tiangolo.com) web framework.
You can search and download the latest persian subtitles for movies/series from film2subtitle.com website by using this API.

Please note that this is not an official API from developers of the film2subtitle.com website! It is for educational purposes
and personal use only (you can extend it to your own needs) and was built using the FastAPI framework to give you the best performance
and experience of using an API.

The BeautifulSoup parser classes used in this API are exclusively programmed, and you'll not find any similar code in other APIs.

## Documentation 📖

Coming soon...

## TODOs 📝

- [ ] Implement API parsers for movies and series page.
- [ ] Add a new method of searching subtitles that uses `wp-json` endpoint of the film2subtitle website.
- [ ] Implement user authentication using OAuth2 password flow.
  - [ ] Add settings for database (`Host`, `Port`, ...) and first superuser (`Name`, `email`, ...)
  - [ ] Create database utilities (crud operation generic classes) and models (SQLAlchemy ORM)
  - [ ] Create schemas for users and security payloads (e.g. access token)
  - [ ] Implement security utilities and dependencies for OAuth (e.g. for creating tokens and validating them)
- [ ] Add support for adding custom headers/cookies to each request.
- [ ] Add proxy server support to the API handler to prevent the API from being blocked by the website.

## License ©️

This project is licensed under the GNU General Public License v3.0.
You can find the full license text in [here](LICENSE).

[![License: GPL v3.0](https://img.shields.io/badge/License-GPL%20v3.0-red.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Contribution 🧑🏻‍💻

If you like this project and want to improve its quality, please consider contributing to it by ***opening an issue*** or ***creating a pull request***.

## Contact developer 📮

You can reach-out to me in telegram at [@Pygrammer](https://t.me/Pygrammer).
