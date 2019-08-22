.. _quickstart:

QuickStart
==========

Clone & Configure
-----------------

.. code:: bash

   $ git clone git@github.com:karajrish/flask-boilerplate.git
   $ cd base_flask

* edit :file:`backend/config.example.py` and save as :file:`backend/config.py`

Running with Docker
-------------------

.. code:: bash

   $ docker-compose up --build


Running Locally
---------------

This assumes you're on a reasonably standard \*nix system. Windows *might* work if you know what you're doing, but you're on your own there.

.. code:: bash

   # install dependencies into a virtual environment
   $ mkvirtualenv -p /path/to/python3 base_flask
   $ pip install -r requirements.txt
   $ pip install -r requirements-dev.txt

   # run db migrations
   $ python manage.py db upgrade

   # load db fixtures (optional)
   $ python manage.py db fixtures fixtures.json

   # start backend dev server:
   $ python manage.py run

   # start backend celery worker (currently only required for sending emails):
   $ python manage.py celery worker
