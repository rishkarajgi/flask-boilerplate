# Flask Base

## [Flask](http://flask.pocoo.org/) Backend

- [SQLAlchemy](http://docs.sqlalchemy.org/en/rel_1_1/) ORM with [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.2/) and migrations provided by [Flask-Alembic](https://flask-alembic.readthedocs.io/en/stable/)
- RESTful APIs provided by a customized integration between [Flask-RESTful](http://flask-restful.readthedocs.io/en/latest/) and [Flask-Marshmallow](http://flask-marshmallow.readthedocs.io/en/latest/)
- [Celery](http://www.celeryproject.org/) for asynchronous tasks, such as sending emails via [Flask-Mail](https://pythonhosted.org/Flask-Mail/)

The backend is structured using the [Application Factory Pattern](http://flask.pocoo.org/docs/0.12/patterns/appfactories/), in conjunction with a little bit of declarative configuration in `backend/config.py` (for ordered registration of extensions, and auto-detection of views, models, serializers, model admins and cli commands). The entry point is the `create_app()` method in `backend/app.py` (`wsgi.py` in production).

## Ansible Production Deployment

- CentOS/RHEL 7.x
- Python 3.6 (provided by the [IUS Project](https://ius.io/))
- PostgreSQL 9.6
- Redis 3.2
- NGINX + uWSGI + supervisord
- Lets Encrypt HTTPS
- Email sending via Postfix with SSL and OpenDKIM

## Local Development QuickStart:

### Using docker-compose

Dependencies:

- `docker` and `docker-compose` (at least docker engine v1.13)

```bash
# install
$ git clone git@github.com:karajrish/flask-boilerplate.git
$ cd base_flask

# configure (the defaults are fine for development)
$ edit `backend/config.example.py` and save as `backend/config.py`

# run it
$ docker-compose up --build  # grab a coffee; bootstrapping takes a while the first time
```

Once it's done building and everything has booted up:

- Access the app at: [http://localhost:8888](http://localhost:8888)
- Access MailHog at: [http://localhost:8025](http://localhost:8025)
- Access the docs at: [http://localhost:5500](http://localhost:5500)
- The API (eg for testing with CURL): [http://localhost:5000](http://localhost:5000)
- And last but not least, the database is exposed on port 5442

### Running locally

This assumes you're on a reasonably standard \*nix system. Windows *might* work if you know what you're doing, but you're on your own there.

Dependencies:

- Python 3.6+
- Your virtualenv tool of choice (strongly recommended)
- PostgreSQL or MariaDB (MySQL)
- Redis (used for sessions persistence and the Celery tasks queue)
- MailHog (not required, but it's awesome for testing email related tasks)

```bash
# install
$ git clone git@github.com:karajrish/flask-boilerplate.git
$ cd base_flask
$ mkvirtualenv -p /path/to/python3 base_flask
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt  # for tests and sphinx docs

# configure
$ edit `backend/config.example.py` and save as `backend/config.py`

# set up database
$ sudo -u postgres -i psql
postgres=# CREATE USER flask_api WITH PASSWORD 'flask_api';
postgres=# CREATE DATABASE flask_api;
postgres=# GRANT ALL PRIVILEGES ON DATABASE flask_api TO flask_api;
postgres=# \q  # (quit)

# run db migrations
$ python manage.py db upgrade

# load db fixtures (optional)
$ python manage.py db fixtures fixtures.json

# backend dev server:
$ python manage.py run

# backend celery workers:
$ python manage.py celery worker
$ python manage.py celery beat
```

## Full Documentation

Run `make docs` and browse to [http://localhost:5500](http://localhost:5500)

Sources are in the `/docs` folder.

FIXME: publish to GitHub Pages.

## License

MIT
