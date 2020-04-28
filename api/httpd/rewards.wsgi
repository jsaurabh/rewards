"""
WSGI config for drp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drp.settings")

# Set environment variables here since variables set in Apache are global.
os.environ["DATABASE_HOST"] = "db"
os.environ["DATABASE_NAME"] = "rewards"
os.environ["DATABASE_USER"] = "root"
os.environ["DATABASE_PASS"] = "iAmASecret"

application = get_wsgi_application()
