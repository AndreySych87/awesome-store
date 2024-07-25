#!/usr/bin/env python

# Copyright 2022 ITCase (info@itcase.pro)

# Django's command-line utility for administrative tasks.
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?") from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    this_file_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(this_file_dir, 'apps'))
    main()
