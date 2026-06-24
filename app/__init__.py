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

    with app.app_context():
        if db.engine.url.database and db.engine.url.database != ':memory:':
            from app.models import User
            if not db.engine.dialect.has_table(db.engine.connect(), 'user'):
                db.create_all()
                _seed_demo_data()

    return app


def _seed_demo_data():
    from datetime import datetime, timedelta, timezone
    from app.models import Event, Registration, User

    admin = User(username="admin", email="admin@campus.edu", is_admin=True)
    admin.set_password("admin123456")
    db.session.add(admin)
    students = []
    for i in range(1, 6):
        s = User(username=f"student{i}", email=f"student{i}@campus.edu")
        s.set_password("12345678")
        db.session.add(s)
        students.append(s)
    db.session.flush()
    now = datetime.now(timezone.utc)
    events = [
        Event(title="新学期迎新晚会", description="欢迎新同学加入校园大家庭", location="大礼堂",
              start_time=now + timedelta(days=7), end_time=now + timedelta(days=7, hours=3),
              max_participants=200, checkin_code="WELCOME", creator_id=admin.id, category="社交"),
        Event(title="Python编程工作坊", description="从零开始学习Flask Web开发", location="计算机实验室A301",
              start_time=now + timedelta(days=14), end_time=now + timedelta(days=14, hours=2),
              max_participants=50, checkin_code="PYTHON", creator_id=admin.id, category="学术"),
        Event(title="校园马拉松", description="第五届校园马拉松比赛", location="校田径场",
              start_time=now + timedelta(days=21), end_time=now + timedelta(days=21, hours=4),
              max_participants=500, checkin_code="RUN2024", creator_id=admin.id, category="体育"),
        Event(title="职业规划讲座", description="企业HR分享求职经验", location="学术报告厅",
              start_time=now + timedelta(days=30), end_time=now + timedelta(days=30, hours=2),
              max_participants=100, checkin_code="CAREER", creator_id=admin.id, category="学术"),
        Event(title="电影放映之夜", description="本周放映经典影片", location="多功能厅",
              start_time=now + timedelta(days=3), end_time=now + timedelta(days=3, hours=3),
              max_participants=0, checkin_code="MOVIE", creator_id=admin.id, category="文艺"),
    ]
    for e in events:
        db.session.add(e)
    db.session.flush()
    for s in students[:3]:
        db.session.add(Registration(user_id=s.id, event_id=events[0].id))
    db.session.add(Registration(user_id=students[0].id, event_id=events[1].id,
                                 checked_in=True, checked_in_at=now))
    db.session.commit()
