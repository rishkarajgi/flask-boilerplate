from backend.app import create_app
# we import this here so celery can access it for its startup
from backend.extensions.celery import celery

# pylint: disable=invalid-name
application = create_app()


__all__ = [
    'celery',
    'application'
]
