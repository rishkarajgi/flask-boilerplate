import logging
import os

from elasticapm import set_user_context
from elasticapm.contrib.flask import ElasticAPM
from elasticapm.handlers.logging import LoggingHandler


class CustomElasticAPM(ElasticAPM):

    is_initialized = False

    def init_app(self, app, *args, **kwargs):
        super().init_app(app, service_name=app.config.get('APP_NAME', 'app'),
                         server_url=app.config.get(
                             'APM_SERVER_URL', 'http://apm:8200'
        ), logging=True, debug=True, capture_body='all')
        handler = LoggingHandler(client=self.client)
        handler.setLevel(logging.DEBUG)
        app.logger.addHandler(handler)
        self.is_initialized = True

        @app.before_request
        def apm_user_context():
            # importing over here as it won't work outside request context
            from flask import request
            initiator = request.headers.get('X-Initiator')
            if initiator:
                set_user_context(user_id=initiator)


apm = CustomElasticAPM()
