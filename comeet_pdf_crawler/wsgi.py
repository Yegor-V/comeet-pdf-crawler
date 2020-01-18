import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comeet_pdf_crawler.settings")

application = get_wsgi_application()
