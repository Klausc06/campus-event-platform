# Error Handling & Logging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add comprehensive error handling, structured logging, and visual debugging to the Flask campus event platform for development-stage error tracking.

**Architecture:** Centralized logging config via `dictConfig` in a new `app/logging.py` module. Request-aware log formatter with UUID request IDs. Custom error pages (404/500) with Liquid Glass design showing stack traces in dev. Flask-DebugToolbar for visual debugging. Log viewer route for in-browser log access.

**Tech Stack:** Python logging (dictConfig, RotatingFileHandler), Flask errorhandlers, flask-debugtoolbar, Jinja2 templates

---

## File Map

```
app/
├── logging.py          # NEW — dictConfig, RequestFormatter, request hooks
├── __init__.py         # MODIFY — register error handlers, import logging config
├── extensions.py       # MODIFY — add DebugToolbar init
templates/
├── errors/
│   ├── 404.html        # NEW — Liquid Glass 404 page
│   └── 500.html        # NEW — Liquid Glass 500 page with stack trace
├── admin/
│   └── logs.html       # NEW — log viewer page
├── base.html           # MODIFY — add "Logs" nav link for admin
app/admin/routes.py     # MODIFY — add log viewer route
config.py               # MODIFY — add LOG_LEVEL, SQLALCHEMY_ECHO settings
requirements.txt        # MODIFY — add flask-debugtoolbar
logs/                   # NEW — log directory (gitignored)
.gitignore              # MODIFY — add logs/
tests/test_errors.py    # NEW — error handler tests
```

---

### Task 1: Logging Configuration Module

**Files:**
- Create: `app/logging.py`
- Modify: `app/__init__.py`

- [ ] **Step 1: Create `app/logging.py`**

```python
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
```

- [ ] **Step 2: Modify `app/__init__.py` to import logging**

Add after the existing imports:
```python
from app.logging import setup_logging, register_request_hooks
```

Add inside `create_app()` before blueprint registration:
```python
    setup_logging(app)
    register_request_hooks(app)
```

- [ ] **Step 3: Verify logging works**

Run: `cd /Users/klaus/campus-event-platform && python3 -c "from app import create_app; app = create_app(); app.logger.info('test'); print('OK')"`
Expected: `OK` + log output in console + `logs/app.log` created

- [ ] **Step 4: Commit**

```bash
git add app/logging.py app/__init__.py
git commit -m "feat: add structured logging with request ID tracing"
```

---

### Task 2: Error Handlers + Error Templates

**Files:**
- Create: `templates/errors/404.html`
- Create: `templates/errors/500.html`
- Modify: `app/__init__.py`

- [ ] **Step 1: Create `templates/errors/404.html`**

```html
{% extends "base.html" %}
{% block title %}404 - 页面不存在{% endblock %}
{% block content %}
<div class="error-page">
  <div class="error-code">404</div>
  <h1>页面不存在</h1>
  <p class="error-msg">你访问的页面不存在或已被移除。</p>
  <div class="error-detail glass">
    <div class="detail-label">REQUEST INFO</div>
    <div class="detail-row"><span>URL:</span> <code>{{ request.url }}</code></div>
    <div class="detail-row"><span>Method:</span> <code>{{ request.method }}</code></div>
    <div class="detail-row"><span>Request ID:</span> <code>{{ g.get('request_id', '-') }}</code></div>
  </div>
  <a href="{{ url_for('event.list_events') }}" class="btn btn-primary">返回首页</a>
</div>
{% endblock %}
```

- [ ] **Step 2: Create `templates/errors/500.html`**

```html
{% extends "base.html" %}
{% block title %}500 - 服务器错误{% endblock %}
{% block content %}
<div class="error-page">
  <div class="error-code">500</div>
  <h1>服务器内部错误</h1>
  <p class="error-msg">服务器遇到了一个错误。以下是详细信息：</p>

  {% if config.DEBUG %}
  <div class="error-detail glass">
    <div class="detail-label">ERROR TRACEBACK</div>
    <pre class="traceback">{{ traceback }}</pre>
  </div>

  <div class="error-detail glass">
    <div class="detail-label">REQUEST INFO</div>
    <div class="detail-row"><span>URL:</span> <code>{{ request.url }}</code></div>
    <div class="detail-row"><span>Method:</span> <code>{{ request.method }}</code></div>
    <div class="detail-row"><span>Request ID:</span> <code>{{ g.get('request_id', '-') }}</code></div>
    <div class="detail-row"><span>Remote Addr:</span> <code>{{ request.remote_addr }}</code></div>
  </div>

  {% if request.form %}
  <div class="error-detail glass">
    <div class="detail-label">FORM DATA</div>
    <pre>{{ request.form | tojson(indent=2) }}</pre>
  </div>
  {% endif %}

  {% if request.args %}
  <div class="error-detail glass">
    <div class="detail-label">QUERY STRING</div>
    <pre>{{ request.args | tojson(indent=2) }}</pre>
  </div>
  {% endif %}
  {% else %}
  <div class="error-detail glass">
    <div class="detail-label">INFO</div>
    <p>请联系管理员，提供以下 Request ID：</p>
    <code class="request-id">{{ g.get('request_id', '-') }}</code>
  </div>
  {% endif %}

  <a href="{{ url_for('event.list_events') }}" class="btn btn-primary">返回首页</a>
</div>
{% endblock %}
```

- [ ] **Step 3: Register error handlers in `app/__init__.py`**

Add inside `create_app()` after blueprint registration:
```python
    import traceback as tb
    from flask import render_template

    @app.errorhandler(404)
    def not_found(e):
        app.logger.warning("404 Not Found: %s", request.url)
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        trace = "".join(tb.format_exception(type(e), e, e.__traceback__))
        app.logger.exception("500 Internal Server Error")
        return render_template("errors/500.html", traceback=trace), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            return e
        trace = "".join(tb.format_exception(type(e), e, e.__traceback__))
        app.logger.exception("Unhandled exception: %s", str(e))
        return render_template("errors/500.html", traceback=trace), 500
```

- [ ] **Step 4: Add error page CSS to `static/css/style.css`**

Append:
```css
.error-page {
  text-align: center;
  padding: 80px 20px 40px;
  max-width: 600px;
  margin: 0 auto;
}
.error-code {
  font-family: 'DM Sans', sans-serif;
  font-size: 96px;
  font-weight: 300;
  color: var(--accent);
  line-height: 1;
  margin-bottom: 8px;
}
.error-page h1 {
  font-size: 24px;
  font-weight: 300;
  letter-spacing: 3px;
  margin-bottom: 12px;
  text-wrap: balance;
}
.error-msg {
  color: var(--ink-muted);
  margin-bottom: 32px;
}
.error-detail {
  text-align: left;
  padding: 20px 24px;
  margin-bottom: 16px;
}
.detail-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  color: var(--ink-muted);
  letter-spacing: 2px;
  margin-bottom: 12px;
}
.detail-row {
  display: flex;
  gap: 12px;
  padding: 6px 0;
  font-size: 14px;
  border-bottom: 1px solid var(--glass-border-subtle);
}
.detail-row:last-child { border-bottom: none; }
.detail-row span { color: var(--ink-muted); min-width: 100px; }
.detail-row code { color: var(--accent); font-family: 'DM Sans', monospace; font-size: 13px; }
.traceback {
  font-family: 'DM Sans', 'SF Mono', monospace;
  font-size: 12px;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-all;
  color: var(--danger, #A03030);
  background: var(--glass-bg);
  padding: 16px;
  border-radius: 12px;
  border: 1px solid var(--glass-border);
  max-height: 400px;
  overflow-y: auto;
}
.request-id {
  display: inline-block;
  font-family: 'DM Sans', monospace;
  font-size: 18px;
  color: var(--accent);
  padding: 8px 16px;
  background: var(--accent-soft, rgba(196,90,58,0.12));
  border-radius: 8px;
  letter-spacing: 2px;
}
```

- [ ] **Step 5: Verify error pages work**

Run: `cd /Users/klaus/campus-event-platform && python3 -c "
from app import create_app
app = create_app()
with app.test_client() as c:
    r = c.get('/nonexistent-page')
    assert r.status_code == 404
    assert '404' in r.data.decode()
    print('404 page OK')
"`
Expected: `404 page OK`

- [ ] **Step 6: Commit**

```bash
git add templates/errors/ static/css/style.css app/__init__.py
git commit -m "feat: custom error pages with stack traces (404/500)"
```

---

### Task 3: Flask-DebugToolbar Integration

**Files:**
- Modify: `requirements.txt`
- Modify: `app/extensions.py`
- Modify: `app/__init__.py`

- [ ] **Step 1: Add to `requirements.txt`**

Append: `flask-debugtoolbar==0.16.0`

- [ ] **Step 2: Add toolbar to `app/extensions.py`**

Append:
```python
from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension()
```

- [ ] **Step 3: Initialize in `app/__init__.py`**

Import toolbar:
```python
from app.extensions import csrf, db, login_manager, migrate, toolbar
```

Add after `csrf.init_app(app)`:
```python
    if app.debug:
        toolbar.init_app(app)
```

- [ ] **Step 4: Add config in `config.py`**

Add to `Config` class:
```python
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_ECHO = False
```

Add to `TestConfig`:
```python
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_ECHO = False
```

- [ ] **Step 5: Verify toolbar appears**

Run: `cd /Users/klaus/campus-event-platform && pip install flask-debugtoolbar && python3 run.py &`
Then: `curl -s http://127.0.0.1:5000/event/ | grep -c "debugtoolbar"`
Expected: > 0

- [ ] **Step 6: Commit**

```bash
git add requirements.txt app/extensions.py app/__init__.py config.py
git commit -m "feat: integrate flask-debugtoolbar for visual debugging"
```

---

### Task 4: Admin Log Viewer Route

**Files:**
- Create: `templates/admin/logs.html`
- Modify: `app/admin/routes.py`
- Modify: `templates/base.html`

- [ ] **Step 1: Create `templates/admin/logs.html`**

```html
{% extends "base.html" %}
{% block title %}日志 - 管理面板{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2>系统日志</h2>
  <div>
    <a href="{{ url_for('admin.dashboard') }}" class="btn btn-glass btn-sm">返回面板</a>
  </div>
</div>

<div class="log-viewer glass">
  <div class="log-header">
    <span class="log-filename">logs/app.log</span>
    <span class="log-lines">{{ total_lines }} lines</span>
  </div>
  <pre class="log-content">{{ log_content }}</pre>
</div>

<div class="log-viewer glass mt-3">
  <div class="log-header">
    <span class="log-filename">Recent Errors (last 50)</span>
  </div>
  <pre class="log-content log-errors">{{ error_lines }}</pre>
</div>
{% endblock %}
```

- [ ] **Step 2: Add log viewer route to `app/admin/routes.py`**

Append:
```python
import os


@admin_bp.route("/logs")
def logs():
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    log_file = os.path.join(log_dir, "app.log")

    log_content = ""
    error_lines = ""
    total_lines = 0

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            lines = f.readlines()
            total_lines = len(lines)
            log_content = "".join(lines[-200:])
            error_lines = "".join(
                l for l in lines if "ERROR" in l or "CRITICAL" in l or "Traceback" in l
            )[-3000:]

    return render_template(
        "admin/logs.html",
        log_content=log_content,
        error_lines=error_lines,
        total_lines=total_lines,
    )
```

- [ ] **Step 3: Add "日志" nav link in `templates/base.html`**

Add the logs link next to the admin link in the `.nav-links` div (matching existing `<a>` tag pattern, not `<li>`):
```html
{% if current_user.is_authenticated and current_user.is_admin %}
<a href="{{ url_for('admin.dashboard') }}" class="{% if request.endpoint == 'admin.dashboard' %}active{% endif %}" data-zh="管理" data-en="Admin">管理</a>
<a href="{{ url_for('admin.logs') }}" class="{% if request.endpoint == 'admin.logs' %}active{% endif %}" data-zh="日志" data-en="Logs">日志</a>
{% endif %}
```

- [ ] **Step 4: Add log viewer CSS to `static/css/style.css`**

Append:
```css
.log-viewer {
  padding: 20px 24px;
}
.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--glass-border-subtle);
}
.log-filename {
  font-family: 'DM Sans', monospace;
  font-size: 12px;
  color: var(--ink-muted);
  letter-spacing: 1px;
}
.log-lines {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  color: var(--ink-muted);
  font-variant-numeric: tabular-nums;
}
.log-content {
  font-family: 'DM Sans', 'SF Mono', monospace;
  font-size: 11px;
  line-height: 1.6;
  max-height: 500px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
  color: var(--ink-secondary);
}
.log-errors {
  color: var(--danger, #A03030);
}

```

- [ ] **Step 5: Verify log viewer works**

Run: `cd /Users/klaus/campus-event-platform && python3 -c "
from app import create_app
app = create_app()
with app.test_client() as c:
    r = c.get('/admin/logs')
    print(f'Status: {r.status_code}')
"`
Expected: Status: 302 (redirect to login, because not authenticated)

- [ ] **Step 6: Commit**

```bash
git add templates/admin/logs.html templates/base.html app/admin/routes.py static/css/style.css
git commit -m "feat: admin log viewer route with error filtering"
```

---

### Task 5: Update .gitignore + Tests

**Files:**
- Modify: `.gitignore`
- Create: `tests/test_errors.py`

- [ ] **Step 1: Add `logs/` to `.gitignore`**

Append: `logs/`

- [ ] **Step 2: Create `tests/test_errors.py`**

```python
class TestErrorPages:
    def test_404_page(self, client):
        r = client.get("/nonexistent")
        assert r.status_code == 404
        assert "404" in r.data.decode()

    def test_500_page(self, app, client):
        @app.route("/test-error")
        def test_error():
            raise RuntimeError("Test error")

        r = client.get("/test-error")
        assert r.status_code == 500
        page = r.data.decode()
        assert "500" in page

    def test_request_id_in_response(self, client):
        r = client.get("/event/")
        assert "X-Request-ID" in r.headers

    def test_log_file_created(self, app):
        import os
        log_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "logs", "app.log"
        )
        with app.app_context():
            app.logger.info("test log entry")
        assert os.path.exists(log_file)
```

- [ ] **Step 3: Run tests**

Run: `cd /Users/klaus/campus-event-platform && source venv/bin/activate && python3 -m pytest tests/test_errors.py -v`
Expected: 4 passed

- [ ] **Step 4: Commit**

```bash
git add .gitignore tests/test_errors.py
git commit -m "feat: error handling tests + gitignore logs/"
```

---

### Task 6: Verification + Cleanup

- [ ] **Step 1: Run full test suite**

Run: `cd /Users/klaus/campus-event-platform && source venv/bin/activate && python3 -m pytest tests/ -v`
Expected: all tests pass (16 existing + 4 new = 20)

- [ ] **Step 2: Run UI audit with make-interfaces-feel-better**

Dispatch review subagent to check:
- Error page templates use Liquid Glass variables
- Log viewer uses glass styling
- No transition: all
- Hit areas ≥ 40px on all buttons
- tabular-nums on numbers

- [ ] **Step 3: Fix any issues found**

- [ ] **Step 4: Final commit**

```bash
git add -A && git commit -m "fix: address UI audit findings on error pages"
```
