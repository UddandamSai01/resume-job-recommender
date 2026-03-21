"""
WSGI config for airesume project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""
import sys
import pymysql

pymysql.install_as_MySQLdb()
sys.modules['MySQLdb'] = pymysql

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airesume.settings')

application = get_wsgi_application()
