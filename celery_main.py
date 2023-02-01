import os
from celery import Celery, platforms
from settings.base import RabbitMQConfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')
rabbitmq = RabbitMQConfig()
app = Celery(
    'analyzer',
    broker=f'pyamqp://{rabbitmq.user}:{rabbitmq.password}@{rabbitmq.host}:{rabbitmq.port}/',
    result_backend='django-db',
    cache_backend='django-cache',
)
app.config_from_object('django.conf:settings', namespace='CELERY')

platforms.C_FORCE_ROOT = True
if __name__ == '__main__':

    app.worker_main([
        'worker', '-l', 'info', '-P', 'solo'    # solo mode for windows compatibility
    ])
