"""
WSGI config for secure_case_connect project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_case_connect.settings')

application = get_wsgi_application()
