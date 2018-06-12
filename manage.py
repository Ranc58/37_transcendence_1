#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sci_blog.settings")

if __name__ == "__main__":
    from configurations.management import execute_from_command_line
    execute_from_command_line(sys.argv)
