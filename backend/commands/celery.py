import subprocess

import click


@click.group()
def celery():
    """Start the celery worker and/or beat."""
    # pylint: disable=W0107
    pass


@celery.command()
def worker():
    """Start the celery worker."""
    subprocess.run('celery worker -A passenger_wsgi.celery -l debug', shell=True)


@celery.command()
def beat():
    """Start the celery beat."""
    subprocess.run('celery beat -A passenger_wsgi.celery -l debug', shell=True)
