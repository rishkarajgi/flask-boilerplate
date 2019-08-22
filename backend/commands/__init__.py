from .celery import celery
from .clean import clean
from .db import db_cli, drop, fixtures, reset
from .lint import lint
from .shell import shell
from .urls import url, urls

EXISTING_EXTENSION_GROUPS = ['db_cli']

__all__ = [
    'celery',
    'clean',
    'db_cli',
    'drop',
    'fixtures',
    'reset',
    'lint',
    'shell',
    'url',
    'urls'
]
