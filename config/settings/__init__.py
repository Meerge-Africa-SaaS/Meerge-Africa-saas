from os import getenv
import os
from pathlib import Path
from typing import Literal, cast
import dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if (env_file := BASE_DIR / ".env").exists():
    print(f"loading: {os.path.basename(env_file)}")
    dotenv.load_dotenv(
        dotenv_path=env_file,
        verbose=True,
        override=False,
    )
if (env_file := BASE_DIR / ".env.local").exists():
    print(f"loading: {os.path.basename(env_file)}")
    dotenv.load_dotenv(
        dotenv_path=env_file,
        verbose=True,
        override=False,
    )

EnvT = Literal["production", "test", "development"]
DJANGO_ENV: EnvT = cast(
    EnvT, getenv("DJANGO_ENV", getenv("PYTHON_ENV", "development"))
)

assert DJANGO_ENV in (
    "production",
    "test",
    "development",
), f"Invalid environment: {DJANGO_ENV}"


def _dotenv_files_for(envs: list[str]):
    """get the dotenv files for the given environments."""
    for name in envs:
        yield f".env.{name}"
        yield f".env.{name}.local"


def load_dotenv_files(env: EnvT = DJANGO_ENV):
    """load the dotenv files for an environment."""
    dotenv_files = []
    if env == "production":
        dotenv_files.extend(_dotenv_files_for(["prod", "production"]))
    elif env == "test":
        dotenv_files.extend(_dotenv_files_for(["test", "testing"]))
    else:
        dotenv_files.extend(_dotenv_files_for(["dev", "development"]))

    for dotenv_file in dotenv_files:
        if (env_file := BASE_DIR / dotenv_file).exists():
            print(f"loading: {os.path.basename(dotenv_file)}")
            dotenv.load_dotenv(
                dotenv_path=env_file,
                verbose=True,
                override=True,
            )


def get_settings_module(env: EnvT = DJANGO_ENV) -> str:
    """Get the settings file for an environment."""
    filename: str = env
    if env == "development":
        filename = "dev"
    return f"config.settings.{filename}"
