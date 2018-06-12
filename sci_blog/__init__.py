import os
from configurations import importer

# Add here because some troubles with django-config and pytest:
# https://github.com/jazzband/django-configurations/issues/147
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')
importer.install(check_options=True)
