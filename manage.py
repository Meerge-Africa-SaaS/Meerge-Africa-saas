#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

    from django.core.management import execute_from_command_line

    from config.settings import get_settings_module, load_dotenv_files


    os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_settings_module())
    load_dotenv_files()

    execute_from_command_line(sys.argv)
