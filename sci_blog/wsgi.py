import os
from configurations.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sci_blog.settings")

application = get_wsgi_application()
