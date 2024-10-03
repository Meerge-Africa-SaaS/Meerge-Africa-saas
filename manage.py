#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    from config.env import env

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{env}")

    execute_from_command_line(sys.argv)
