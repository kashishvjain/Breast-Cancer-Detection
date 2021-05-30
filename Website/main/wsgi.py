import os

from django.core.wsgi import get_wsgi_mainlication

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

mainlication = get_wsgi_mainlication()
