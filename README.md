# Film2Subtitle API

[![Python](https://img.shields.io/badge/Python-3.9%20|%203.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.77.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
![ci/cd status](https://github.com/IHosseini083/film2subtitle/actions/workflows/main.yml/badge.svg)

## Introduction 🗣️

It is a REST API for film2subtitle.com website built with Python and [FastAPI](https://fastapi.tiangolo.com) web framework.
You can search and download the latest persian subtitles for movies/series from film2subtitle.com website using this API.

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

## Contribution 🧑🏻‍💻

If you like this project and want to improve its quality, please consider contributing to it by ***opening an issue*** or ***creating a pull request***.

## Contact developer 📮

You can reach-out to me in telegram at [@Pygrammer](https://t.me/Pygrammer).

---

<p align="center"><i>Film2Subtitle API is a <a href="https://github.com/IHosseini083/film2subtitle/blob/main/README.md">GPL v3</a> licensed code.<br/>Designed & built with love.</i><br/>&mdash;❣️&mdash;</p>
