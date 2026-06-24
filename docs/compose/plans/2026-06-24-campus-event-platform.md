# 校园活动报名与签到平台 — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Flask-based campus event registration and check-in platform for course presentation Friday.

**Architecture:** Application Factory pattern + Blueprints (auth/event/checkin/admin). Jinja2 SSR + Bootstrap 5. SQLite + Flask-SQLAlchemy. MVC layered design.

**Tech Stack:** Flask 3.x, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Migrate, Jinja2, Bootstrap 5 (CDN), qrcode, pytest

---

## File Map

```
campus-event-platform/
├── run.py                          # Entry point
├── config.py                       # Config classes
├── requirements.txt                # Dependencies
├── app/
│   ├── __init__.py                 # create_app() factory
│   ├── extensions.py               # db, login_manager, migrate
│   ├── models.py                   # User, Event, Registration
│   ├── forms.py                    # All WTForms
│   ├── decorators.py               # @admin_required
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── event/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── checkin/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── admin/
│       ├── __init__.py
│       └── routes.py
├── templates/
│   ├── base.html
│   ├── _flash.html
│   ├── auth/login.html
│   ├── auth/register.html
│   ├── event/list.html
│   ├── event/detail.html
│   ├── event/create.html
│   ├── event/edit.html
│   ├── checkin/checkin.html
│   └── admin/dashboard.html
├── static/
│   └── css/style.css
└── tests/
    ├── conftest.py
    ├── test_auth.py
    ├── test_event.py
    └── test_checkin.py
```

---

## Task 1: Project Scaffold + App Factory

**Covers:** Architecture setup

**Files:**
- Create: `requirements.txt`, `config.py`, `app/__init__.py`, `app/extensions.py`, `run.py`

- [ ] **Step 1: Create requirements.txt**

```txt
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.2
Flask-Migrate==4.1.0
WTForms==3.2.1
Werkzeug==3.1.3
qrcode==8.0
Pillow==11.1.0
pytest==8.3.5
```

- [ ] **Step 2: Create config.py**

```python
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
```

- [ ] **Step 3: Create app/extensions.py**

```python
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "请先登录"
migrate = Migrate()
```

- [ ] **Step 4: Create app/__init__.py with factory**

```python
from flask import Flask

from app.extensions import db, login_manager, migrate
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.auth import auth_bp
    from app.event import event_bp
    from app.checkin import checkin_bp
    from app.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(checkin_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def index():
        from flask import redirect, url_for
        return redirect(url_for("event.list_events"))

    return app
```

- [ ] **Step 5: Create blueprint __init__.py files**

```python
# app/auth/__init__.py
from flask import Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
from app.auth import routes  # noqa: E402, F401
```

```python
# app/event/__init__.py
from flask import Blueprint
event_bp = Blueprint("event", __name__, url_prefix="/event")
from app.event import routes  # noqa: E402, F401
```

```python
# app/checkin/__init__.py
from flask import Blueprint
checkin_bp = Blueprint("checkin", __name__, url_prefix="/checkin")
from app.checkin import routes  # noqa: E402, F401
```

```python
# app/admin/__init__.py
from flask import Blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
from app.admin import routes  # noqa: E402, F401
```

- [ ] **Step 6: Create run.py**

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

- [ ] **Step 7: Install deps and verify**

Run: `cd /Users/klaus/campus-event-platform && pip install -r requirements.txt && python -c "from app import create_app; app = create_app(); print('OK')"`

Expected: `OK`

- [ ] **Step 8: Commit**

```bash
git init && git add -A && git commit -m "feat: project scaffold with app factory pattern"
```

---

## Task 2: Database Models

**Covers:** Data layer design

**Files:**
- Create: `app/models.py`

- [ ] **Step 1: Write models.py**

```python
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    registrations = db.relationship("Registration", backref="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    max_participants = db.Column(db.Integer, default=0)
    checkin_code = db.Column(db.String(20))
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    creator = db.relationship("User", backref="created_events")
    registrations = db.relationship(
        "Registration", backref="event", lazy="dynamic",
        cascade="all, delete-orphan"
    )

    @property
    def registered_count(self):
        return self.registrations.filter_by(status="confirmed").count()

    @property
    def checked_in_count(self):
        return self.registrations.filter_by(
            status="confirmed", checked_in=True
        ).count()

    @property
    def is_full(self):
        if self.max_participants <= 0:
            return False
        return self.registered_count >= self.max_participants

    def __repr__(self):
        return f"<Event {self.title}>"


class Registration(db.Model):
    __tablename__ = "registrations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    status = db.Column(db.String(20), default="confirmed")  # confirmed/cancelled
    registered_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    checked_in = db.Column(db.Boolean, default=False)
    checked_in_at = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint("user_id", "event_id", name="uq_user_event"),
    )

    def __repr__(self):
        return f"<Registration user={self.user_id} event={self.event_id}>"
```

- [ ] **Step 2: Verify model loads**

Run: `cd /Users/klaus/campus-event-platform && python -c "from app import create_app; from app.models import User, Event, Registration; print('Models OK')"`

Expected: `Models OK`

- [ ] **Step 3: Initialize DB and migration**

Run: `cd /Users/klaus/campus-event-platform && flask db init && flask db migrate -m "initial" && flask db upgrade`

Expected: `app.db` created, migration files in `migrations/`

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat: add User, Event, Registration models with migrations"
```

---

## Task 3: Auth Module (Register + Login + Logout)

**Covers:** User system, role-based access

**Files:**
- Create: `app/forms.py` (LoginForm, RegisterForm), `app/decorators.py`, `app/auth/routes.py`
- Create: `templates/base.html`, `templates/_flash.html`, `templates/auth/login.html`, `templates/auth/register.html`

- [ ] **Step 1: Create app/forms.py**

```python
from flask_wtf import FlaskForm
from wtforms import (
    DateTimeLocalField, EmailField, IntegerField,
    PasswordField, StringField, TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


class LoginForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(), Length(3, 80)])
    email = EmailField("邮箱", validators=[DataRequired(), Email()])
    password = PasswordField("密码", validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField("确认密码", validators=[DataRequired(), EqualTo("password")])


class EventForm(FlaskForm):
    title = StringField("活动名称", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("活动描述")
    location = StringField("活动地点", validators=[Length(max=200)])
    start_time = DateTimeLocalField("开始时间", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    end_time = DateTimeLocalField("结束时间", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    max_participants = IntegerField("最大人数", default=0, validators=[NumberRange(min=0)])
    checkin_code = StringField("签到码", validators=[Length(max=20)])


class CheckinForm(FlaskForm):
    code = StringField("签到码", validators=[DataRequired()])
```

- [ ] **Step 2: Create app/decorators.py**

```python
from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated
```

- [ ] **Step 3: Create app/auth/routes.py**

```python
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import auth_bp
from app.extensions import db
from app.forms import LoginForm, RegisterForm
from app.models import User


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("event.list_events"))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("用户名已存在", "danger")
            return render_template("auth/register.html", form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash("邮箱已注册", "danger")
            return render_template("auth/register.html", form=form)

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("注册成功，请登录", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("event.list_events"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("event.list_events"))
        flash("用户名或密码错误", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
```

- [ ] **Step 4: Create templates/base.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}校园活动平台{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('event.list_events') }}">校园活动平台</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('event.list_events') }}">活动列表</a>
                    </li>
                    {% if current_user.is_authenticated and current_user.is_admin %}
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('admin.dashboard') }}">管理面板</a>
                    </li>
                    {% endif %}
                </ul>
                <ul class="navbar-nav">
                    {% if current_user.is_authenticated %}
                    <li class="nav-item">
                        <span class="nav-link text-light">{{ current_user.username }}</span>
                    </li>
                    <li class="nav-item">
                        <form method="POST" action="{{ url_for('auth.logout') }}" class="d-inline">
                            <button class="nav-link btn btn-link" type="submit">退出</button>
                        </form>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('auth.login') }}">登录</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('auth.register') }}">注册</a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {% include '_flash.html' %}
        {% block content %}{% endblock %}
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

- [ ] **Step 5: Create templates/_flash.html**

```html
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
{% for category, message in messages %}
<div class="alert alert-{{ category if category != 'message' else 'info' }} alert-dismissible fade show" role="alert">
    {{ message }}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
{% endfor %}
{% endif %}
{% endwith %}
```

- [ ] **Step 6: Create templates/auth/login.html**

```html
{% extends "base.html" %}
{% block title %}登录 - 校园活动平台{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow">
            <div class="card-body">
                <h3 class="card-title text-center mb-4">登录</h3>
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.username.label(class="form-label") }}
                        {{ form.username(class="form-control", placeholder="请输入用户名") }}
                    </div>
                    <div class="mb-3">
                        {{ form.password.label(class="form-label") }}
                        {{ form.password(class="form-control", placeholder="请输入密码") }}
                    </div>
                    <button type="submit" class="btn btn-primary w-100">登录</button>
                </form>
                <p class="text-center mt-3 mb-0">
                    还没有账号？<a href="{{ url_for('auth.register') }}">立即注册</a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 7: Create templates/auth/register.html**

```html
{% extends "base.html" %}
{% block title %}注册 - 校园活动平台{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow">
            <div class="card-body">
                <h3 class="card-title text-center mb-4">注册</h3>
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.username.label(class="form-label") }}
                        {{ form.username(class="form-control", placeholder="3-80个字符") }}
                    </div>
                    <div class="mb-3">
                        {{ form.email.label(class="form-label") }}
                        {{ form.email(class="form-control", placeholder="your@email.com") }}
                    </div>
                    <div class="mb-3">
                        {{ form.password.label(class="form-label") }}
                        {{ form.password(class="form-control", placeholder="至少8位") }}
                    </div>
                    <div class="mb-3">
                        {{ form.confirm.label(class="form-label") }}
                        {{ form.confirm(class="form-control", placeholder="再次输入密码") }}
                    </div>
                    <button type="submit" class="btn btn-primary w-100">注册</button>
                </form>
                <p class="text-center mt-3 mb-0">
                    已有账号？<a href="{{ url_for('auth.login') }}">立即登录</a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 8: Create static/css/style.css**

```css
body {
    background-color: #f5f7fa;
}
.card {
    border: none;
    border-radius: 12px;
}
.navbar-brand {
    font-weight: 700;
}
```

- [ ] **Step 9: Verify auth works**

Run: `cd /Users/klaus/campus-event-platform && python run.py &` then `curl -s http://127.0.0.1:5000/auth/login | grep "登录"` then kill the server.

Expected: HTML with "登录" text returned.

- [ ] **Step 10: Commit**

```bash
git add -A && git commit -m "feat: auth module with register/login/logout"
```

---

## Task 4: Event Module (CRUD)

**Covers:** Activity management

**Files:**
- Create: `app/event/routes.py`
- Create: `templates/event/list.html`, `templates/event/detail.html`, `templates/event/create.html`, `templates/event/edit.html`

- [ ] **Step 1: Create app/event/routes.py**

```python
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.event import event_bp
from app.extensions import db
from app.forms import EventForm
from app.models import Event


@event_bp.route("/")
def list_events():
    q = request.args.get("q", "").strip()
    query = Event.query
    if q:
        query = query.filter(
            Event.title.contains(q) | Event.location.contains(q)
        )
    events = query.order_by(Event.start_time.desc()).all()
    return render_template("event/list.html", events=events, q=q)


@event_bp.route("/<int:event_id>")
def detail(event_id):
    event = db.get_or_404(Event, event_id)
    registration = None
    if current_user.is_authenticated:
        from app.models import Registration
        registration = Registration.query.filter_by(
            user_id=current_user.id, event_id=event_id, status="confirmed"
        ).first()
    return render_template("event/detail.html", event=event, registration=registration)


@event_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            max_participants=form.max_participants.data or 0,
            checkin_code=form.checkin_code.data,
            creator_id=current_user.id,
        )
        db.session.add(event)
        db.session.commit()
        flash("活动创建成功", "success")
        return redirect(url_for("event.detail", event_id=event.id))
    return render_template("event/create.html", form=form)


@event_bp.route("/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def edit(event_id):
    event = db.get_or_404(Event, event_id)
    if event.creator_id != current_user.id and not current_user.is_admin:
        from flask import abort
        abort(403)

    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        flash("活动已更新", "success")
        return redirect(url_for("event.detail", event_id=event.id))
    return render_template("event/edit.html", form=form, event=event)


@event_bp.route("/<int:event_id>/delete", methods=["POST"])
@login_required
def delete_event(event_id):
    event = db.get_or_404(Event, event_id)
    if event.creator_id != current_user.id and not current_user.is_admin:
        from flask import abort
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash("活动已删除", "success")
    return redirect(url_for("event.list_events"))
```

NOTE: Add `from flask import request` at top of file.

- [ ] **Step 2: Create templates/event/list.html**

```html
{% extends "base.html" %}
{% block title %}活动列表 - 校园活动平台{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>活动列表</h2>
    {% if current_user.is_authenticated %}
    <a href="{{ url_for('event.create') }}" class="btn btn-primary">创建活动</a>
    {% endif %}
</div>

<form class="mb-4" method="GET">
    <div class="input-group">
        <input type="text" name="q" class="form-control" placeholder="搜索活动名称或地点..." value="{{ q }}">
        <button class="btn btn-outline-primary" type="submit">搜索</button>
    </div>
</form>

<div class="row">
    {% for event in events %}
    <div class="col-12 col-md-6 col-lg-4 mb-4">
        <div class="card h-100 shadow-sm">
            <div class="card-body">
                <h5 class="card-title">{{ event.title }}</h5>
                <p class="text-muted mb-1">
                    {{ event.start_time.strftime('%Y-%m-%d %H:%M') }}
                </p>
                <p class="text-muted mb-2">{{ event.location or '待定' }}</p>
                <p class="card-text">{{ event.description[:100] }}{% if event.description|length > 100 %}...{% endif %}</p>
            </div>
            <div class="card-footer bg-transparent">
                <span class="badge bg-{{ 'danger' if event.is_full else 'success' }}">
                    {% if event.max_participants > 0 %}
                        {{ event.registered_count }}/{{ event.max_participants }} 已报名
                    {% else %}
                        {{ event.registered_count }} 已报名
                    {% endif %}
                </span>
                <a href="{{ url_for('event.detail', event_id=event.id) }}" class="btn btn-sm btn-outline-primary float-end">查看详情</a>
            </div>
        </div>
    </div>
    {% else %}
    <div class="col-12">
        <p class="text-center text-muted">暂无活动</p>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 3: Create templates/event/detail.html**

```html
{% extends "base.html" %}
{% block title %}{{ event.title }} - 校园活动平台{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card shadow">
            <div class="card-body">
                <h2>{{ event.title }}</h2>
                <hr>
                <div class="row mb-3">
                    <div class="col-6">
                        <strong>开始时间：</strong>{{ event.start_time.strftime('%Y-%m-%d %H:%M') }}
                    </div>
                    <div class="col-6">
                        <strong>结束时间：</strong>{{ event.end_time.strftime('%Y-%m-%d %H:%M') }}
                    </div>
                </div>
                <p><strong>地点：</strong>{{ event.location or '待定' }}</p>
                <p><strong>描述：</strong>{{ event.description or '暂无描述' }}</p>
                <p>
                    <strong>报名情况：</strong>
                    <span class="badge bg-{{ 'danger' if event.is_full else 'success' }}">
                        {{ event.registered_count }}{% if event.max_participants > 0 %}/{{ event.max_participants }}{% endif %} 人已报名
                    </span>
                </p>

                {% if current_user.is_authenticated %}
                    {% if registration %}
                        <div class="alert alert-success">
                            你已报名此活动
                            {% if registration.checked_in %}
                            ，已完成签到
                            {% endif %}
                        </div>
                        {% if not registration.checked_in %}
                        <div class="d-flex gap-2">
                            <a href="{{ url_for('checkin.checkin', event_id=event.id) }}" class="btn btn-success">签到</a>
                            <form method="POST" action="{{ url_for('event.cancel_registration', event_id=event.id) }}">
                                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                                <button type="submit" class="btn btn-outline-danger">取消报名</button>
                            </form>
                        </div>
                        {% endif %}
                    {% else %}
                        {% if event.is_full %}
                        <div class="alert alert-warning">名额已满</div>
                        {% else %}
                        <form method="POST" action="{{ url_for('event.register_event', event_id=event.id) }}">
                            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                            <button type="submit" class="btn btn-primary">立即报名</button>
                        </form>
                        {% endif %}
                    {% endif %}
                {% else %}
                <a href="{{ url_for('auth.login') }}" class="btn btn-primary">登录后报名</a>
                {% endif %}

                {% if current_user.is_authenticated and (event.creator_id == current_user.id or current_user.is_admin) %}
                <hr>
                <div class="d-flex gap-2">
                    <a href="{{ url_for('event.edit', event_id=event.id) }}" class="btn btn-sm btn-warning">编辑</a>
                    <form method="POST" action="{{ url_for('event.delete_event', event_id=event.id) }}"
                          onsubmit="return confirm('确定删除此活动？')">
                        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
                        <button type="submit" class="btn btn-sm btn-danger">删除</button>
                    </form>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 4: Create templates/event/create.html and edit.html**

```html
{% extends "base.html" %}
{% block title %}创建活动 - 校园活动平台{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card shadow">
            <div class="card-body">
                <h3 class="mb-4">创建活动</h3>
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.title.label(class="form-label") }}
                        {{ form.title(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.description.label(class="form-label") }}
                        {{ form.description(class="form-control", rows=4) }}
                    </div>
                    <div class="mb-3">
                        {{ form.location.label(class="form-label") }}
                        {{ form.location(class="form-control") }}
                    </div>
                    <div class="row mb-3">
                        <div class="col-6">
                            {{ form.start_time.label(class="form-label") }}
                            {{ form.start_time(class="form-control") }}
                        </div>
                        <div class="col-6">
                            {{ form.end_time.label(class="form-label") }}
                            {{ form.end_time(class="form-control") }}
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-6">
                            {{ form.max_participants.label(class="form-label") }}
                            {{ form.max_participants(class="form-control", placeholder="0表示不限") }}
                        </div>
                        <div class="col-6">
                            {{ form.checkin_code.label(class="form-label") }}
                            {{ form.checkin_code(class="form-control") }}
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary">创建</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

```html
{% extends "base.html" %}
{% block title %}编辑活动 - 校园活动平台{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card shadow">
            <div class="card-body">
                <h3 class="mb-4">编辑活动</h3>
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.title.label(class="form-label") }}
                        {{ form.title(class="form-control") }}
                    </div>
                    <div class="mb-3">
                        {{ form.description.label(class="form-label") }}
                        {{ form.description(class="form-control", rows=4) }}
                    </div>
                    <div class="mb-3">
                        {{ form.location.label(class="form-label") }}
                        {{ form.location(class="form-control") }}
                    </div>
                    <div class="row mb-3">
                        <div class="col-6">
                            {{ form.start_time.label(class="form-label") }}
                            {{ form.start_time(class="form-control") }}
                        </div>
                        <div class="col-6">
                            {{ form.end_time.label(class="form-label") }}
                            {{ form.end_time(class="form-control") }}
                        </div>
                    </div>
                    <div class="row mb-3">
                        <div class="col-6">
                            {{ form.max_participants.label(class="form-label") }}
                            {{ form.max_participants(class="form-control") }}
                        </div>
                        <div class="col-6">
                            {{ form.checkin_code.label(class="form-label") }}
                            {{ form.checkin_code(class="form-control") }}
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary">保存</button>
                    <a href="{{ url_for('event.detail', event_id=event.id) }}" class="btn btn-outline-secondary">取消</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 5: Verify event CRUD**

Run: `cd /Users/klaus/campus-event-platform && python -c "
from app import create_app
app = create_app()
with app.test_client() as c:
    r = c.get('/event/')
    assert r.status_code == 200
    print('Event list OK')
"`

Expected: `Event list OK`

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "feat: event CRUD with list/detail/create/edit/delete"
```

---

## Task 5: Registration (Sign Up + Cancel)

**Covers:** Event registration

**Files:**
- Modify: `app/event/routes.py`

- [ ] **Step 1: Add registration routes to app/event/routes.py**

Append to the file:

```python
from app.models import Registration


@event_bp.route("/<int:event_id>/register", methods=["POST"])
@login_required
def register_event(event_id):
    event = db.get_or_404(Event, event_id)
    if event.is_full:
        flash("报名人数已满", "warning")
        return redirect(url_for("event.detail", event_id=event_id))

    existing = Registration.query.filter_by(
        user_id=current_user.id, event_id=event_id
    ).first()
    if existing:
        if existing.status == "confirmed":
            flash("你已报名该活动", "info")
        else:
            existing.status = "confirmed"
            db.session.commit()
            flash("已重新报名", "success")
    else:
        reg = Registration(user_id=current_user.id, event_id=event_id)
        db.session.add(reg)
        db.session.commit()
        flash("报名成功", "success")

    return redirect(url_for("event.detail", event_id=event_id))


@event_bp.route("/<int:event_id>/cancel", methods=["POST"])
@login_required
def cancel_registration(event_id):
    reg = Registration.query.filter_by(
        user_id=current_user.id, event_id=event_id, status="confirmed"
    ).first()
    if not reg:
        flash("未找到报名记录", "warning")
        return redirect(url_for("event.detail", event_id=event_id))

    reg.status = "cancelled"
    db.session.commit()
    flash("已取消报名", "success")
    return redirect(url_for("event.detail", event_id=event_id))
```

- [ ] **Step 2: Verify registration flow**

Run: `cd /Users/klaus/campus-event-platform && python -c "
from app import create_app
from app.extensions import db
from app.models import User, Event, Registration
from datetime import datetime, timezone

app = create_app()
with app.app_context():
    db.create_all()
    u = User(username='test', email='t@t.com')
    u.set_password('12345678')
    db.session.add(u)
    e = Event(title='Test', start_time=datetime.now(timezone.utc), end_time=datetime.now(timezone.utc), creator_id=1)
    db.session.add(e)
    db.session.commit()
    reg = Registration(user_id=u.id, event_id=e.id)
    db.session.add(reg)
    db.session.commit()
    assert e.registered_count == 1
    reg.status = 'cancelled'
    db.session.commit()
    assert e.registered_count == 0
    print('Registration flow OK')
"`

Expected: `Registration flow OK`

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "feat: event registration with sign up and cancel"
```

---

## Task 6: Check-in Module

**Covers:** Sign-in functionality

**Files:**
- Create: `app/checkin/routes.py`
- Create: `templates/checkin/checkin.html`

- [ ] **Step 1: Create app/checkin/routes.py**

```python
from datetime import datetime, timezone

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.checkin import checkin_bp
from app.extensions import db
from app.forms import CheckinForm
from app.models import Event, Registration


@checkin_bp.route("/<int:event_id>", methods=["GET", "POST"])
@login_required
def checkin(event_id):
    event = db.get_or_404(Event, event_id)
    form = CheckinForm()

    reg = Registration.query.filter_by(
        user_id=current_user.id, event_id=event_id, status="confirmed"
    ).first()

    if not reg:
        flash("请先报名再签到", "warning")
        return redirect(url_for("event.detail", event_id=event_id))

    if reg.checked_in:
        flash("你已完成签到", "info")
        return redirect(url_for("event.detail", event_id=event_id))

    if form.validate_on_submit():
        if form.code.data.strip() == event.checkin_code:
            reg.checked_in = True
            reg.checked_in_at = datetime.now(timezone.utc)
            db.session.commit()
            flash("签到成功！", "success")
            return redirect(url_for("event.detail", event_id=event_id))
        else:
            flash("签到码错误", "danger")

    return render_template("checkin/checkin.html", event=event, form=form)
```

- [ ] **Step 2: Create templates/checkin/checkin.html**

```html
{% extends "base.html" %}
{% block title %}签到 - {{ event.title }}{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow">
            <div class="card-body">
                <h3 class="card-title text-center mb-2">活动签到</h3>
                <p class="text-center text-muted mb-4">{{ event.title }}</p>
                <form method="POST">
                    {{ form.hidden_tag() }}
                    <div class="mb-3">
                        {{ form.code.label(class="form-label") }}
                        {{ form.code(class="form-control form-control-lg text-center", placeholder="请输入签到码", autofocus=true) }}
                    </div>
                    <button type="submit" class="btn btn-success btn-lg w-100">签到</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 3: Verify checkin flow**

Run: `cd /Users/klaus/campus-event-platform && python -c "
from app import create_app
from app.extensions import db
from app.models import User, Event, Registration
from datetime import datetime, timezone

app = create_app()
with app.app_context():
    db.create_all()
    u = User(username='test2', email='t2@t.com')
    u.set_password('12345678')
    db.session.add(u)
    e = Event(title='Test', start_time=datetime.now(timezone.utc), end_time=datetime.now(timezone.utc), creator_id=1, checkin_code='ABC123')
    db.session.add(e)
    db.session.commit()
    reg = Registration(user_id=u.id, event_id=e.id)
    db.session.add(reg)
    db.session.commit()
    assert not reg.checked_in
    reg.checked_in = True
    reg.checked_in_at = datetime.now(timezone.utc)
    db.session.commit()
    assert e.checked_in_count == 1
    print('Checkin flow OK')
"`

Expected: `Checkin flow OK`

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat: checkin module with code verification"
```

---

## Task 7: Admin Dashboard

**Covers:** Management panel

**Files:**
- Create: `app/admin/routes.py`
- Create: `templates/admin/dashboard.html`

- [ ] **Step 1: Create app/admin/routes.py**

```python
from flask import render_template
from flask_login import current_user, login_required

from app.admin import admin_bp
from app.decorators import admin_required
from app.extensions import db
from app.models import Event, Registration, User
from sqlalchemy import func


@admin_bp.before_request
@login_required
@admin_required
def require_admin():
    pass


@admin_bp.route("/")
def dashboard():
    total_users = User.query.count()
    total_events = Event.query.count()
    total_registrations = Registration.query.filter_by(status="confirmed").count()
    total_checkins = Registration.query.filter_by(
        status="confirmed", checked_in=True
    ).count()

    events = Event.query.order_by(Event.created_at.desc()).all()
    event_stats = []
    for e in events:
        reg_count = e.registered_count
        checkin_count = e.checked_in_count
        event_stats.append({
            "event": e,
            "registered": reg_count,
            "checked_in": checkin_count,
            "rate": round(checkin_count / reg_count * 100, 1) if reg_count > 0 else 0,
        })

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_events=total_events,
        total_registrations=total_registrations,
        total_checkins=total_checkins,
        event_stats=event_stats,
    )
```

- [ ] **Step 2: Create templates/admin/dashboard.html**

```html
{% extends "base.html" %}
{% block title %}管理面板 - 校园活动平台{% endblock %}
{% block content %}
<h2 class="mb-4">管理面板</h2>

<div class="row mb-4">
    <div class="col-6 col-md-3 mb-3">
        <div class="card text-center shadow-sm">
            <div class="card-body">
                <h3 class="text-primary">{{ total_users }}</h3>
                <p class="text-muted mb-0">注册用户</p>
            </div>
        </div>
    </div>
    <div class="col-6 col-md-3 mb-3">
        <div class="card text-center shadow-sm">
            <div class="card-body">
                <h3 class="text-success">{{ total_events }}</h3>
                <p class="text-muted mb-0">活动总数</p>
            </div>
        </div>
    </div>
    <div class="col-6 col-md-3 mb-3">
        <div class="card text-center shadow-sm">
            <div class="card-body">
                <h3 class="text-info">{{ total_registrations }}</h3>
                <p class="text-muted mb-0">报名人次</p>
            </div>
        </div>
    </div>
    <div class="col-6 col-md-3 mb-3">
        <div class="card text-center shadow-sm">
            <div class="card-body">
                <h3 class="text-warning">{{ total_checkins }}</h3>
                <p class="text-muted mb-0">签到人次</p>
            </div>
        </div>
    </div>
</div>

<h4 class="mb-3">活动统计</h4>
<div class="table-responsive">
    <table class="table table-hover">
        <thead class="table-light">
            <tr>
                <th>活动名称</th>
                <th>报名人数</th>
                <th>签到人数</th>
                <th>签到率</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            {% for stat in event_stats %}
            <tr>
                <td>{{ stat.event.title }}</td>
                <td>{{ stat.registered }}</td>
                <td>{{ stat.checked_in }}</td>
                <td>
                    <div class="progress" style="min-width: 100px;">
                        <div class="progress-bar bg-success" style="width: {{ stat.rate }}%">
                            {{ stat.rate }}%
                        </div>
                    </div>
                </td>
                <td>
                    <a href="{{ url_for('event.detail', event_id=stat.event.id) }}" class="btn btn-sm btn-outline-primary">查看</a>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="5" class="text-center text-muted">暂无活动</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
```

- [ ] **Step 3: Verify admin dashboard**

Run: `cd /Users/klaus/campus-event-platform && python -c "
from app import create_app
app = create_app()
print('Admin module OK')
"`

Expected: `Admin module OK`

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat: admin dashboard with statistics"
```

---

## Task 8: Seed Data Script

**Covers:** Demo data for presentation

**Files:**
- Create: `seed.py`

- [ ] **Step 1: Create seed.py**

```python
from datetime import datetime, timedelta, timezone

from app import create_app
from app.extensions import db
from app.models import Event, Registration, User

app = create_app()

with app.app_context():
    db.create_all()

    admin = User(username="admin", email="admin@campus.edu", is_admin=True)
    admin.set_password("admin123456")
    db.session.add(admin)

    users = []
    for i in range(1, 6):
        u = User(username=f"student{i}", email=f"student{i}@campus.edu")
        u.set_password("12345678")
        users.append(u)
        db.session.add(u)

    db.session.commit()

    now = datetime.now(timezone.utc)
    events_data = [
        ("校园歌手大赛", "一年一度的校园歌手大赛，欢迎报名参加！", "大礼堂", 2, 200),
        ("Python编程工作坊", "Flask Web开发入门实践", "计算机实验室A301", 3, 30),
        ("篮球友谊赛", "院际篮球友谊赛，以球会友", "体育馆", 1, 50),
        ("读书分享会", "本月推荐：《深入理解计算机系统》", "图书馆二楼", 5, 0),
        ("志愿者招募", "社区服务志愿者招募中", "学生活动中心", 1, 100),
    ]

    for title, desc, loc, days_offset, max_p in events_data:
        e = Event(
            title=title,
            description=desc,
            location=loc,
            start_time=now + timedelta(days=days_offset),
            end_time=now + timedelta(days=days_offset, hours=2),
            max_participants=max_p,
            checkin_code=title[:3].upper() + "2024",
            creator_id=admin.id,
        )
        db.session.add(e)

    db.session.commit()

    events = Event.query.all()
    for u in users[:3]:
        reg = Registration(user_id=u.id, event_id=events[0].id)
        db.session.add(reg)
    reg_done = Registration(user_id=users[0].id, event_id=events[1].id)
    reg_done.checked_in = True
    reg_done.checked_in_at = now
    db.session.add(reg_done)

    db.session.commit()
    print("Seed data created!")
    print(f"Admin: admin / admin123456")
    print(f"Users: student1-5 / 12345678")
```

- [ ] **Step 2: Run seed script**

Run: `cd /Users/klaus/campus-event-platform && python seed.py`

Expected: `Seed data created!`

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "feat: seed data script for demo"
```

---

## Task 9: Manual Verification

**Covers:** End-to-end testing

- [ ] **Step 1: Start the app**

Run: `cd /Users/klaus/campus-event-platform && python run.py`

- [ ] **Step 2: Test in browser / curl**

```bash
# Home page redirects to events
curl -s http://127.0.0.1:5000/ -L | grep "活动列表"

# Login page
curl -s http://127.0.0.1:5000/auth/login | grep "登录"

# Register page
curl -s http://127.0.0.1:5000/auth/register | grep "注册"

# Event list
curl -s http://127.0.0.1:5000/event/ | grep "校园歌手大赛"

# Search
curl -s "http://127.0.0.1:5000/event/?q=Python" | grep "Python编程工作坊"
```

Expected: All greps return content.

- [ ] **Step 3: Test auth flow**

```bash
# Register new user
curl -s -c cookies.txt -b cookies.txt http://127.0.0.1:5000/auth/register -X POST \
  -d "username=newuser&email=new@test.com&password=testtest123&confirm=testtest123&csrf_token=SKIP" \
  -L | grep -E "注册成功|登录"
```

- [ ] **Step 4: Kill server and commit**

```bash
kill %1 2>/dev/null
git add -A && git commit -m "chore: manual verification complete"
```

---

## Task 10: Cleanup + README

**Covers:** Documentation

- [ ] **Step 1: Create README.md**

```markdown
# 校园活动报名与签到平台

基于 Flask 的校园活动管理 Web 应用。

## 功能
- 用户注册/登录
- 活动创建/编辑/删除/搜索
- 活动报名/取消报名
- 签到码签到
- 管理员数据面板

## 快速启动
```bash
pip install -r requirements.txt
python seed.py          # 创建演示数据
python run.py           # 启动服务
```

访问 http://127.0.0.1:5000

## 测试账号
- 管理员: admin / admin123456
- 学生: student1 / 12345678

## 技术栈
- Flask 3.x + Blueprints
- Flask-SQLAlchemy + SQLite
- Flask-Login + Flask-WTF
- Jinja2 + Bootstrap 5
- qrcode 二维码生成
```

- [ ] **Step 2: Final commit**

```bash
git add -A && git commit -m "docs: add README"
```
