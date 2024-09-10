"""Gunicorn configuration file."""

import os

wsgi_app = os.environ.get("WSGI_APP", "config.wsgi:application")
reload = os.getenv("GUNICORN_RELOAD", "0") == "1"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", "8000")
bind = os.getenv("GUNICORN_BIND", f"{HOST}:{PORT}")
workers = int(os.getenv("GUNICORN_WORKERS", "1"))
threads = int(os.getenv("GUNICORN_THREADS", "1"))

loglevel = os.getenv("GUNICORN_LOG_LEVEL", os.getenv("LOG_LEVEL", "info"))
accesslog = os.getenv("GUNICORN_ACCESS_LOG", "-")
errorlog = os.getenv("GUNICORN_ERROR_LOG", "-")
