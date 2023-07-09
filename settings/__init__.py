# Standard Library
import mimetypes

# Third-Party Libraries
import pymysql

# Project Imports
from celery_main import app as celery_app

__all__ = "celery_app"

pymysql.install_as_MySQLdb()
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/javascript", ".js", True)
mimetypes.add_type("text/html", ".html", True)
