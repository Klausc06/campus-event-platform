import os
import traceback as tb

from flask import Flask, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException

from config import Config
from app.extensions import csrf, db, login_manager, migrate, toolbar
from app.logging import setup_logging, register_request_hooks

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static"),
    )
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    if app.debug and toolbar is not None:
        toolbar.init_app(app)

    setup_logging(app)
    register_request_hooks(app)

    from app.auth import auth_bp
    from app.event import event_bp
    from app.checkin import checkin_bp
    from app.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(checkin_bp)
    app.register_blueprint(admin_bp)

    from app.translations import TRANSLATIONS, CATEGORY_MAP

    @app.context_processor
    def inject_translations():
        lang = request.cookies.get('lang', 'zh')
        def t(zh):
            if lang == 'en':
                return TRANSLATIONS.get(zh, zh)
            return zh
        def t_category(zh):
            if lang == 'en':
                return CATEGORY_MAP.get(zh, zh)
            return zh
        return dict(t=t, t_category=t_category)

    @app.errorhandler(404)
    def not_found(e):
        app.logger.warning("404 Not Found: %s", request.url)
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.exception("500 Internal Server Error")
        trace = None
        if app.debug:
            trace = "".join(tb.format_exception(type(e), e, e.__traceback__))
        return render_template("errors/500.html", traceback=trace), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return e
        app.logger.exception("Unhandled exception: %s", str(e))
        trace = None
        if app.debug:
            trace = "".join(tb.format_exception(type(e), e, e.__traceback__))
        return render_template("errors/500.html", traceback=trace), 500

    @app.route('/')
    def index():
        return redirect(url_for('event.list_events'))

    return app
