import logging
import time
import uuid
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler

import os
from flask import g, has_request_context, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.method = request.method
            record.remote_addr = request.remote_addr
            record.request_id = getattr(g, "request_id", "no-id")
        else:
            record.url = "-"
            record.method = "-"
            record.remote_addr = "-"
            record.request_id = "-"
        return super().format(record)


def setup_logging(app):
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    log_level = app.config.get("LOG_LEVEL", "DEBUG")

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": RequestFormatter,
                    "format": "[%(asctime)s] %(request_id)s %(remote_addr)s %(method)s %(url)s %(levelname)s %(module)s:%(lineno)d - %(message)s",
                },
                "simple": {
                    "format": "[%(asctime)s] %(levelname)s %(module)s:%(lineno)d - %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                    "level": log_level,
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_file,
                    "maxBytes": 10_000_000,
                    "backupCount": 5,
                    "formatter": "default",
                    "level": "DEBUG",
                },
            },
            "root": {"level": "DEBUG", "handlers": ["console", "file"]},
        }
    )

    app.logger.info("Logging initialized — level=%s file=%s", log_level, log_file)


def register_request_hooks(app):
    @app.before_request
    def log_request_start():
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        g.start_time = time.time()
        app.logger.debug(
            ">>> %s %s [%s]", request.method, request.url, g.request_id
        )

    @app.after_request
    def log_request_end(response):
        duration = time.time() - getattr(g, "start_time", time.time())
        app.logger.info(
            "<<< %s %s %s %.3fs [%s]",
            request.method,
            request.url,
            response.status_code,
            duration,
            getattr(g, "request_id", "no-id"),
        )
        response.headers["X-Request-ID"] = getattr(g, "request_id", "")
        return response
