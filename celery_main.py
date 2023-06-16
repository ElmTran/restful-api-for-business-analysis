# Standard Library
import os

# Third-Party Libraries
from celery import Celery, platforms

# Project Imports
from settings.base import RabbitMQConfig

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base")
app = Celery(
    "analyzer",
    broker=f"pyamqp://{RabbitMQConfig.user}:{RabbitMQConfig.password}@{RabbitMQConfig.host}:{RabbitMQConfig.port}/",
    result_backend="django-db",
    cache_backend="django-cache",
)
app.config_from_object("django.conf:settings", namespace="CELERY")

platforms.C_FORCE_ROOT = True
if __name__ == "__main__":
    app.worker_main(
        [
            "worker",
            "-l",
            "info",
            "-P",
            "solo",  # solo mode for windows compatibility
        ]
    )
