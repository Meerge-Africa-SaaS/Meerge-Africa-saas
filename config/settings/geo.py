# ruff: noqa: F405
from .base import *  # noqa: F403

INSTALLED_APPS.extend(
    [
        "cities_light",
        "geo",
    ]
)

# CITIES_LIGHT_APP_NAME = "geo"
CITIES_LIGHT_TRANSLATION_LANGUAGES = [
    "en",
]
CITIES_LIGHT_INCLUDE_COUNTRIES = [
    "NG",
]
CITIES_LIGHT_INCLUDE_CITY_TYPES = [
    "PPL",
    "PPLA",
    "PLA2",
    "PPLA3",
    "PPLA4",
    "PPLC",
    "PLF",
    "PPLG",
    "PPLL",
    "PPLR",
    "PPLS",
    "STLMT",
]
