from typing import Literal

from config.environ import getenv, loadenv

# load common environment variables
loadenv(".env", skip_missing=True)
loadenv(".env.local", skip_missing=True)

_env = getenv("DJANGO_ENV", "develop")
env: Literal["production", "test", "dev"]

if "prod" in _env:
    loadenv(".env.prod", skip_missing=True)
    loadenv(".env.production", skip_missing=True)
    loadenv(".env.prod.local", skip_missing=True)
    loadenv(".env.production.local", skip_missing=True)
    env = "production"
elif "test" in _env:
    loadenv(".env.test", skip_missing=True)
    loadenv(".env.testing", skip_missing=True)
    loadenv(".env.test.local", skip_missing=True)
    loadenv(".env.testing.local", skip_missing=True)
    env = "test"
else:
    loadenv(".env.dev", skip_missing=True)
    loadenv(".env.develop", skip_missing=True)
    loadenv(".env.dev.local", skip_missing=True)
    loadenv(".env.develop.local", skip_missing=True)
    env = "dev"
