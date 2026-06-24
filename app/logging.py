import logging
import time
import uuid
from logging.config import dictConfig

import os
from flask import g, has_request_context, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.method = request.method
            record.remote_addr = request.remote_addr
            record.request_id = getattr(g, "request_id", "")
        else:
            record.url = "-"
            record.method = "-"
            record.remote_addr = "-"
            record.request_id = ""
        return super().format(record)


def setup_logging(app):
    log_file = app.config.get('LOG_FILE') or os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "app.log")
    log_dir = os.path.dirname(log_file)

    log_level = app.config.get("LOG_LEVEL", "DEBUG")

    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": log_level,
        },
    }

    try:
        os.makedirs(log_dir, exist_ok=True)
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_file,
            "maxBytes": 10_000_000,
            "backupCount": 5,
            "formatter": "default",
            "level": "DEBUG",
        }
        handler_list = ["console", "file"]
    except OSError:
        handler_list = ["console"]

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
            "handlers": handlers,
            "root": {"level": "DEBUG", "handlers": handler_list},
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
            getattr(g, "request_id", ""),
        )
        response.headers["X-Request-ID"] = getattr(g, "request_id", "")
        return response
