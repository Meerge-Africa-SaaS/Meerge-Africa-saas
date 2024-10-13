"""Utility functions for application."""

import os
from typing import (
    Any,
    ParamSpec,
    TypeVar,
    overload,
)

T = TypeVar("T", bound=Any)
P = ParamSpec("P")
R = TypeVar("R")
MISSING = object()


def _extract_env_vars(text: str) -> dict[str, str]:
    """Extract environment variables from a string."""
    env_vars = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, value = line.split("=", 1)
        env_vars[name.strip()] = value.strip()
    return env_vars


def loadenv(
    env_file: str = ".env",
    override: bool = False,
    force_reload: bool = False,
    skip_missing: bool = False,
):
    """Load the environment variables from the env file."""
    # Load environment variables only once
    loaded_envs = getlistenv("ENVS_LOADED", [])
    if env_file in loaded_envs:
        if not force_reload:
            return
    else:
        loaded_envs.append(env_file)

    if not (env_file and os.path.exists(env_file)):
        if skip_missing:
            return
        raise RuntimeError(f"Environment file {env_file!r} does not exist.")
    try:
        with open(env_file) as f:
            env_vars = _extract_env_vars(f.read())
    except Exception as e:
        raise RuntimeError(
            f"Failed to load environment variables from {env_file!r}"
        ) from e

    for name, value in env_vars.items():
        if override or name not in os.environ:
            os.environ[name] = value
        else:
            os.environ.setdefault(name, value)
    setlistenv("ENVS_LOADED", loaded_envs)


@overload
def getenv(name: str) -> str: ...


@overload
def getenv(name: str, default: T) -> str | T: ...


def getenv(name: str, default: str | T = MISSING) -> str | T:  # type: ignore[assignment]
    """Get environment variable or return default value."""
    try:
        return os.environ[name]
    except KeyError:
        if default is MISSING:
            raise RuntimeError(
                f"Environment variable {name!r} is not set."
            ) from None
        return default


@overload
def getlistenv(name: str) -> list[str]: ...


@overload
def getlistenv(name: str, default: T) -> list[str] | T: ...


def getlistenv(name: str, default: list[str] | T = MISSING) -> list[str] | T:  # type: ignore[assignment]
    """Get environment variable or return default value."""
    try:
        return os.environ[name].split(",")
    except KeyError:
        if default is MISSING:
            raise RuntimeError(
                f"Environment variable {name!r} is not set."
            ) from None
        return default


@overload
def getintenv(name: str) -> int: ...


@overload
def getintenv(name: str, default: T) -> int | T: ...


def getintenv(name: str, default: int | T = MISSING) -> int | T:  # type: ignore[assignment]
    """Get environment variable or return default value."""
    try:
        return int(os.environ[name])
    except KeyError:
        if default is MISSING:
            raise RuntimeError(
                f"Environment variable {name!r} is not set."
            ) from None
        return default


@overload
def getfloatenv(name: str) -> float: ...


@overload
def getfloatenv(name: str, default: T) -> float | T: ...


def getfloatenv(name: str, default: float | T = MISSING) -> float | T:  # type: ignore[assignment]
    """Get environment variable or return default value."""
    try:
        return float(os.environ[name])
    except KeyError:
        if default is MISSING:
            raise RuntimeError(
                f"Environment variable {name!r} is not set."
            ) from None
        return default


@overload
def getboolenv(name: str) -> bool: ...


@overload
def getboolenv(name: str, default: T) -> bool | T: ...


def getboolenv(name: str, default: bool | T = MISSING) -> bool | T:  # type: ignore[assignment]
    """Get environment variable or return default value."""
    try:
        return os.environ[name].lower() in ["true", "1", "yes"]
    except KeyError:
        if default is MISSING:
            raise RuntimeError(
                f"Environment variable {name!r} is not set."
            ) from None
        return default


def setenv(name: str, value: Any) -> None:
    """Set an environment variable."""
    os.environ[name] = str(value)


def setlistenv(name: str, value: list[Any]) -> None:
    """Set a list environment variable."""
    os.environ[name] = ",".join(map(str, value))


def getenvs(prefix: str) -> dict[str, str]:
    """Get all environment variables with a prefix."""
    return {
        name: value
        for name, value in os.environ.items()
        if name.startswith(prefix)
    }
