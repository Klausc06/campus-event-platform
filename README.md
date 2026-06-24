# Campus Event Platform

> Flask campus event registration & check-in platform — Apple Liquid Glass design system
>
> **Features**: Event CRUD, registration with soft-delete, code-based check-in, **QR code check-in**, admin dashboard with **CSV export**, **pagination**, **category filtering**, bilingual UI (EN/ZH), dark/light theme

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Install

```bash
git clone <repo-url> && cd campus-event-platform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Seed & Run

```bash
python3 seed.py        # creates 6 users + 5 events + sample registrations
python3 run.py         # → http://127.0.0.1:5000
```

### Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123456` |
| Student | `student1` – `student5` | `12345678` |

### Run Tests

```bash
python3 -m pytest tests/ -v
```

## Project Structure

```
campus-event-platform/
├── app/
│   ├── __init__.py          # create_app() factory, blueprint registration
│   ├── extensions.py        # db, login_manager, migrate, csrf instances
│   ├── models.py            # User, Event, Registration models
│   ├── forms.py             # WTForms: LoginForm, RegisterForm, EventForm, CheckinForm
│   ├── decorators.py        # @admin_required decorator
│   ├── auth/
│   │   ├── __init__.py      # auth_bp (url_prefix=/auth)
│   │   └── routes.py        # register, login, logout (POST-only)
│   ├── event/
│   │   ├── __init__.py      # event_bp (url_prefix=/event)
│   │   └── routes.py        # CRUD, search, register, cancel
│   ├── checkin/
│   │   ├── __init__.py      # checkin_bp (url_prefix=/checkin)
│   │   └── routes.py        # check-in with code verification
│   └── admin/
│       ├── __init__.py      # admin_bp (url_prefix=/admin)
│       └── routes.py        # dashboard with stats + per-event rates
├── templates/
│   ├── base.html            # layout: nav, theme/lang toggles, footer
│   ├── _flash.html          # flash message partial (auto-dismiss)
│   ├── auth/                # login.html, register.html
│   ├── event/               # list.html, detail.html, create.html, edit.html
│   ├── checkin/             # checkin.html, qr.html
│   └── admin/               # dashboard.html
├── static/css/
│   └── style.css            # full Liquid Glass design system (659 lines)
├── tests/
│   ├── conftest.py          # fixtures: app, client, auth_client, sample_event
│   ├── test_auth.py         # registration + login tests
│   ├── test_event.py        # event CRUD + registration tests
│   └── test_checkin.py      # check-in flow tests
├── config.py                # Config, TestConfig
├── run.py                   # entry point
├── seed.py                  # demo data seeder
├── requirements.txt         # pinned dependencies
├── DESIGN.md                # design system documentation (Chinese)
├── report.html              # lab report with Mermaid diagrams
├── index.html               # redirects to report.html
├── style-demo.html          # 10 style options demo (design exploration)
├── style-combined.html      # combined Liquid Glass demo (final design)
└── docs/compose/plans/      # implementation plan (10 tasks)
```

## File Guide

### For AI Agents

> This section explains how to modify the project. Each file entry includes:
> - **What it does**: one-paragraph description
> - **How to modify**: specific instructions for common changes
> - **Dependencies**: what it imports, what imports it
> - **Gotchas**: things that will break if you're not careful

---

#### `app/__init__.py` — Application Factory

- **What it does**: Creates the Flask app via `create_app()`. Sets `template_folder` and `static_folder` to the project root (not inside `app/`), loads config, initializes all four extensions (db, login_manager, migrate, csrf), registers four blueprints (auth, event, checkin, admin), and defines the `/` index route that redirects to the event list.
- **How to add a new blueprint**:
  1. Create `app/newmodule/__init__.py` with `newmodule_bp = Blueprint('newmodule', __name__, url_prefix='/newmodule')`
  2. Create `app/newmodule/routes.py` with route functions decorated by `@newmodule_bp.route(...)`
  3. In `app/__init__.py`, add `from app.newmodule import newmodule_bp` and `app.register_blueprint(newmodule_bp)`
- **Dependencies**: Imports `Config` from `config.py`, imports all extension instances from `app/extensions.py`, imports blueprints from `app/auth`, `app/event`, `app/checkin`, `app/admin`.
- **Gotchas**: `template_folder` and `static_folder` use `BASE_DIR` (project root) — don't change these unless you physically move `templates/` and `static/`. The `from app.auth import routes` pattern in blueprint `__init__.py` files causes circular imports if you try to import blueprints at module level outside `create_app()`.

---

#### `app/extensions.py` — Extension Instances

- **What it does**: Creates singleton instances of SQLAlchemy (`db`), LoginManager (`login_manager`), Migrate (`migrate`), and CSRFProtect (`csrf`). Sets `login_manager.login_view = "auth.login"` so unauthenticated users get redirected to the login page.
- **How to add a new extension**: Import the extension class, create an instance, then add `ext.init_app(app)` inside `create_app()` in `app/__init__.py`.
- **Dependencies**: Imported by `app/__init__.py`, `app/models.py`, all route modules.
- **Gotchas**: `login_manager.login_view` must match the `blueprint.endpoint` of your login route — currently `"auth.login"`. If you rename the auth blueprint or its login endpoint, update this string.

---

#### `app/models.py` — Database Models

- **What it does**: Defines three models: `User` (with `UserMixin` for Flask-Login, password hashing via werkzeug), `Event` (with computed properties `registered_count`, `checked_in_count`, `is_full`, plus a `category` field and `CATEGORIES` list), and `Registration` (the many-to-many join table with extra fields). Also defines the `@login_manager.user_loader` callback and a module-level `CATEGORIES = ['Tech', 'Culture', 'Sports', 'Academic', 'Social', 'Other']` list used by forms and templates.
- **How to add a new model**: Create a class inheriting `db.Model`, add `__tablename__`, columns, and relationships. Then run `flask db migrate -m 'add new model'` and `flask db upgrade`.
- **How to add a field to an existing model**: Add a `db.Column(...)` to the class, then run `flask db migrate -m 'add field'` and `flask db upgrade`.
- **How to add event categories**: Already implemented. `Event.category` is a `String(50)` column. The `CATEGORIES` list at module level is imported by `app/forms.py` for the `SelectField` choices and by templates for filter pills.
- **Dependencies**: Imports `db`, `login_manager` from `app/extensions.py`. Imported by all route modules, `seed.py`, test fixtures.
- **Gotchas**:
  - Always use `datetime.now(timezone.utc)` — never `datetime.now()`. Timezone-naive datetimes will cause comparison bugs.
  - Registration uses **soft-delete** (`reg.status = 'cancelled'`) — never `db.session.delete(reg)`.
  - `Event.registrations` has `cascade='all, delete-orphan'` — deleting an Event automatically deletes all its Registrations.
  - `db.get_or_404()` is SQLAlchemy 2.x syntax — don't use the deprecated `query.get_or_404()`.
  - `User.registrations` uses `lazy='dynamic'` — returns a query object, not a list. Use `.filter_by()`, `.count()`, `.all()`.

---

#### `app/forms.py` — WTForms

- **What it does**: Defines four form classes: `LoginForm` (username + password), `RegisterForm` (username + email + password + confirm), `EventForm` (title + description + location + start/end time + max_participants + checkin_code + **category** as a `SelectField`), `CheckinForm` (code only).
- **How to add a new form**: Create a class inheriting `FlaskForm`, add fields with validators. Import it in the relevant route module and template.
- **How to add a field to an existing form**: Add the field to the form class, then update the corresponding template to render it with `{{ form.new_field(class="form-control") }}`.
- **Dependencies**: Imports from `flask_wtf` and `wtforms`. Imported by `app/auth/routes.py`, `app/event/routes.py`, `app/checkin/routes.py`.
- **Gotchas**:
  - `Length(min=8)` means "minimum 8 characters" — `Length(8)` means "exactly 8 characters". Don't confuse them.
  - `Email()` validator requires the `email_validator` package (in requirements.txt).
  - `DateTimeLocalField` uses `format='%Y-%m-%dT%H:%M'` — the HTML datetime-local format. If you change the format, update both the form field and the template input type.

---

#### `app/decorators.py` — Custom Decorators

- **What it does**: Defines `@admin_required` decorator that checks `current_user.is_admin` and returns 403 if false.
- **How to use**: Apply `@admin_required` on any route function. Must be used **after** `@login_required` (decorator order: outermost first).
- **Dependencies**: Imports `abort` from Flask, `current_user` from Flask-Login. Imported by `app/admin/routes.py`.
- **Gotchas**: Decorator order matters. `@login_required` must be applied before `@admin_required` (i.e., `@login_required` should be the outer decorator). If reversed, `current_user` may be anonymous.

---

#### `app/auth/__init__.py` — Auth Blueprint

- **What it does**: Creates `auth_bp = Blueprint('auth', __name__, url_prefix='/auth')` and imports routes.
- **Dependencies**: Imports routes from `app.auth.routes`.
- **Gotchas**: The `from app.auth import routes` line at the bottom is required — it registers the route functions with the blueprint. Don't remove it.

---

#### `app/auth/routes.py` — Authentication Routes

- **What it does**: Three routes: `register` (GET/POST — creates user, checks uniqueness), `login` (GET/POST — authenticates, sets session, redirects to `next` or event list), `logout` (POST only — clears session).
- **How to add a new auth route**: Add a function with `@auth_bp.route('/path', methods=[...])` decorator.
- **How to change password requirements**: Modify `RegisterForm` in `app/forms.py`.
- **Dependencies**: Imports `auth_bp` from `app.auth`, `db` from `app.extensions`, `User` from `app.models`, forms from `app.forms`.
- **Gotchas**:
  - Logout **must** be POST (CSRF protection) — a GET logout would be vulnerable to CSRF via `<img>` tags.
  - Login redirects to `request.args.get('next')` — validate this in production to prevent open redirect attacks.
  - Registration checks both `username` and `email` uniqueness with separate queries.

---

#### `app/event/__init__.py` — Event Blueprint

- **What it does**: Creates `event_bp = Blueprint('event', __name__, url_prefix='/event')` and imports routes.
- **Dependencies**: Imports routes from `app.event.routes`.
- **Gotchas**: Same pattern as auth — the `from app.event import routes` line is required.

---

#### `app/event/routes.py` — Event Routes

- **What it does**: Seven routes: `list_events` (GET — search by title/location with `?q=`, **category filter with `?cat=`**, **paginated with `?page=`** using `.paginate(page, per_page=12)`), `detail` (GET — shows event + registration status), `create` (GET/POST — logged-in users), `edit` (GET/POST — creator or admin only), `delete` (POST — creator or admin only), `register` (POST — handles re-registration of cancelled registrations), `cancel` (POST — soft-delete via `status='cancelled'`).
- **How to add event filtering**: Add query parameter handling in `list_events()`, update the search form in `templates/event/list.html`.
- **How to add pagination**: Already implemented. Uses Flask-SQLAlchemy's `.paginate(page=page, per_page=12)` on the event query. The pagination object is passed to the template as `pagination`.
- **How to add event categories**: Already implemented. Reads `?cat=` query param, filters with `Event.category == cat` when present.
- **Dependencies**: Imports `event_bp` from `app.event`, `db` from `app.extensions`, `Event`, `Registration` from `app.models`, `EventForm` from `app.forms`.
- **Gotchas**:
  - Cancel uses soft-delete (`reg.status = 'cancelled'`), not `db.session.delete()`.
  - Register handles the case where a cancelled registration exists — it reactivates it instead of creating a new one.
  - Edit/delete check `event.creator_id != current_user.id and not current_user.is_admin` — both creator and admin can edit/delete.
  - `db.get_or_404(Event, id)` is SQLAlchemy 2.x syntax.

---

#### `app/checkin/__init__.py` — Check-in Blueprint

- **What it does**: Creates `checkin_bp = Blueprint('checkin', __name__, url_prefix='/checkin')` and imports routes.
- **Dependencies**: Imports routes from `app.checkin.routes`.

---

#### `app/checkin/routes.py` — Check-in Routes

- **What it does**: Single route `checkin` (GET/POST) — verifies that the user is registered and not already checked in, then compares the submitted code against `event.checkin_code`. On success, sets `checked_in=True` and records `checked_in_at` timestamp.
- **How to add QR code check-in**: Already implemented. The `qr` route at `/checkin/<event_id>/qr` generates a QR code PNG (via the `qrcode` library) encoding the check-in URL with the code as a query parameter. Displayed on the event detail page.
- **How to change check-in method**: Modify the comparison `form.code.data.strip() == event.checkin_code` at line 36.
- **Dependencies**: Imports `checkin_bp` from `app.checkin`, `db` from `app.extensions`, `Event`, `Registration` from `app.models`, `CheckinForm` from `app/forms`.
- **Gotchas**:
  - Code comparison uses `.strip()` to handle accidental whitespace.
  - `checked_in_at` uses `datetime.now(timezone.utc)` — not `datetime.now()`.
  - Uses `db.session.get(Event, event_id)` instead of `db.get_or_404()` — returns `None` if not found, then manually redirects with flash message.

---

#### `app/admin/__init__.py` — Admin Blueprint

- **What it does**: Creates `admin_bp = Blueprint('admin', __name__, url_prefix='/admin')` and imports routes.
- **Dependencies**: Imports routes from `app.admin.routes`.

---

#### `app/admin/routes.py` — Admin Dashboard

- **What it does**: Uses `@admin_bp.before_request` to enforce `@login_required` + `@admin_required` on ALL admin routes. The `dashboard` route queries global stats (total users, events, registrations, check-ins) and per-event stats (registered count, checked-in count, check-in rate). **CSV export** routes: `/admin/export/all` (all registrations) and `/admin/export/<event_id>` (single event). Both return `text/csv` with UTF-8 BOM encoding for Excel compatibility.
- **How to add new stats**: Add a query in `dashboard()`, pass the result to the template context.
- **How to add CSV export**: Already implemented. Two routes generate CSV responses using Python's `csv.writer` with `utf-8-sig` encoding (BOM). The dashboard template has export buttons.
- **Dependencies**: Imports `admin_bp` from `app.admin`, `admin_required` from `app.decorators`, `db` from `app.extensions`, `User`, `Event`, `Registration` from `app.models`.
- **Gotchas**: The `before_request` hook applies authentication to ALL admin routes — you don't need `@login_required` on individual routes. If you add a public admin route, you'll need to exempt it.

---

#### `templates/base.html` — Base Template

- **What it does**: HTML skeleton with: Google Fonts (Noto Serif SC + DM Sans), Bootstrap 5.3 CSS, custom `style.css`, sticky nav bar (brand, nav links, lang/theme toggles, logout/login buttons), main content area with flash messages, footer, Bootstrap JS, and inline JavaScript for theme/language switching with localStorage persistence.
- **How to add a new nav link**: Add `<a>` inside `.nav-links` div, with `data-zh` and `data-en` attributes for bilingual support.
- **How to add a new page**: Create a template extending `base.html` with `{% extends "base.html" %}` and `{% block content %}...{% endblock %}`.
- **How to add a new language**: Add `data-ja="..."` attributes to elements, add a toggle button calling `setLang('ja')`, update the `setLang()` function.
- **Dependencies**: Extends nothing (it's the root template). All other templates extend this.
- **Gotchas**:
  - Logout is a POST form with CSRF token — never make it a GET link.
  - `form.hidden_tag()` or `{{ csrf_token() }}` must be in every POST form.
  - The `setTheme()` and `setLang()` functions are inline — changes affect all pages.
  - Bootstrap is loaded from CDN — no local fallback.

---

#### `templates/_flash.html` — Flash Messages Partial

- **What it does**: Renders Flask flash messages with category-based styling (success/danger/warning/info). Auto-dismisses after ~5 seconds via CSS animation.
- **Dependencies**: Included by `base.html` via `{% include '_flash.html' %}`.
- **Gotchas**: The `flash-auto-dismiss` CSS class drives the auto-fade. Changing the animation duration requires updating both `@keyframes fadeOut` and the `animation` property in `style.css`.

---

#### `templates/event/list.html` — Event List

- **What it does**: Hero section with title, search bar (GET form with `?q=`), "Create Event" button (authenticated users only), **category filter pills** (horizontal pill buttons linking to `?cat=...`), card grid with stagger animation, **pagination controls** (prev/next + page numbers), and empty state.
- **How to add filtering**: Already implemented. Category pills filter by `?cat=` query param, rendered from the `CATEGORIES` list.
- **How to change card layout**: Modify `.card` CSS in `static/css/style.css`.
- **Dependencies**: Extends `base.html`. Uses `events`, `q`, `active_cat`, and `pagination` from route context.
- **Gotchas**: Stagger animation uses `{{ loop.index0 * 80 }}ms` delay — change `80` to adjust the speed of the cascade effect.

---

#### `templates/event/detail.html` — Event Detail

- **What it does**: Shows event info (title, time, location, capacity, creator, **category badge**), description, **QR code button** (links to `/checkin/<id>/qr`), and action buttons that change based on state: not logged in → "Login to Register"; registered + not checked in → "Check In" + "Cancel"; already checked in → status box; event full → "Full" box. Creator/admin sees edit/delete tools.
- **How to add new event fields**: Add to the `.info-grid` section, update `Event` model and `EventForm`.
- **Dependencies**: Extends `base.html`. Uses `event` and `registration` from route context.
- **Gotchas**: Registration status checks (`registration`, `registration.checked_in`, `event.is_full`) control which buttons are displayed. The logic is in the template — be careful with Jinja2 conditionals.

---

#### `templates/event/create.html` — Create Event Form

- **What it does**: Centered glass card form with all `EventForm` fields including **category select dropdown**. Includes bilingual placeholders and helper text.
- **Dependencies**: Extends `base.html`. Uses `form` (EventForm) from route context.
- **Gotchas**: `form.hidden_tag()` includes the CSRF token — never remove it. The `form-row` class creates a 2-column grid for start/end time.

---

#### `templates/event/edit.html` — Edit Event Form

- **What it does**: Same layout as create form, pre-populated with existing event data. Adds a "Cancel" link back to event detail.
- **Dependencies**: Extends `base.html`. Uses `form` (EventForm) and `event` from route context.
- **Gotchas**: The form uses `obj=event` in the route to pre-populate — if you add new fields, they must be on the Event model for auto-population to work.

---

#### `templates/auth/login.html` — Login Page

- **What it does**: Centered glass card with username/password form and "Register" link.
- **Dependencies**: Extends `base.html`. Uses `form` (LoginForm) from route context.
- **Gotchas**: `form.hidden_tag()` includes CSRF token — never remove it.

---

#### `templates/auth/register.html` — Registration Page

- **What it does**: Centered glass card with username/email/password/confirm form and "Login" link.
- **Dependencies**: Extends `base.html`. Uses `form` (RegisterForm) from route context.
- **Gotchas**: Password confirm field uses `EqualTo('password')` validator — the field name must match exactly.

---

#### `templates/checkin/checkin.html` — Check-in Page

- **What it does**: Centered glass card with event title, large code input field, and submit button.
- **Dependencies**: Extends `base.html`. Uses `form` (CheckinForm) and `event` from route context.
- **Gotchas**: The code input uses `letter-spacing: 8px` for spaced-out display and `font-size: 22px` — changing these affects readability.

---

#### `templates/checkin/qr.html` — QR Code Display Page

- **What it does**: Displays a QR code image (base64-embedded PNG) for an event's check-in URL. The QR code encodes `/checkin/<event_id>?code=<checkin_code>` so scanning it opens the check-in page directly. Includes event title and a back link.
- **Dependencies**: Extends `base.html`. Uses `qr_img` (base64 data URI) and `event` from route context.
- **Gotchas**: The QR code is generated server-side by the `qrcode` library and passed as a base64 data URI — no external image hosting needed.

---

#### `templates/admin/dashboard.html` — Admin Dashboard

- **What it does**: Stat cards row (users, events, registrations, check-ins) + event stats table with progress bars showing check-in rates + **CSV export buttons** (per-event and all-registrations).
- **How to add new metrics**: Add a `.stat-card` div in `.stat-row`, add the query in `app/admin/routes.py:dashboard()`.
- **How to add export button**: Already implemented. Per-event export buttons (`.btn-sm`) link to `/admin/export/<event_id>`, and an "Export All" button links to `/admin/export/all`.
- **Dependencies**: Extends `base.html`. Uses `total_users`, `total_events`, `total_registrations`, `total_checkins`, `event_stats` from route context.
- **Gotchas**: The `.admin-table` class uses glass styling with `backdrop-filter`. Progress bar width is set via inline `style="width:{{ stat.rate }}%"`.

---

#### `static/css/style.css` — Design System

- **What it does**: 659-line CSS file implementing the complete Apple Liquid Glass design system. Includes: CSS custom properties for light/dark themes (lines 1-75), reset (line 77), `.glass` component with `::before` highlight and `::after` refraction (lines 88-127), navigation (128-201), hero section (203-223), search box (225-255), cards with stagger animation (257-336), detail page (338-350), buttons (354-413), auth/checkin forms (415-496), admin dashboard (498-558), flash messages (593-630), footer (632-641), and responsive breakpoint at 640px (647-659).
- **How to change colors**: Modify CSS variables in `:root`/`[data-theme="light"]` (lines 1-38) and `[data-theme="dark"]` (lines 40-75).
- **How to change fonts**: Update the Google Fonts `<link>` in `templates/base.html` and the `font-family` declarations in CSS.
- **How to add a new component**: Follow the `.glass` pattern: `background` (semi-transparent), `backdrop-filter` (blur), `border` (1px solid), `border-radius` (--glass-radius), `box-shadow`, `::before` (highlight), `::after` (refraction).
- **Dependencies**: Loaded by `templates/base.html`. Referenced by `DESIGN.md`.
- **Gotchas**:
  - **Never** use `transition: all` — always specify exact properties (performance).
  - `--glass-radius: 20px` controls concentric rounding — override on nested elements (e.g., `--glass-radius: 16px` on `.stat-card`).
  - The responsive breakpoint is 640px — single breakpoint, no intermediate sizes.
  - `.glass > * { position: relative; z-index: 2; }` ensures content stays above the `::before`/`::after` pseudo-elements.

---

#### `config.py` — Configuration

- **What it does**: Defines `Config` class (dev config with SQLite, CSRF enabled, secret key from env) and `TestConfig` (in-memory SQLite, CSRF disabled, testing mode).
- **How to add new config**: Add to `Config` class, override in `TestConfig` if needed for testing.
- **Dependencies**: Imported by `app/__init__.py`, `tests/conftest.py`.
- **Gotchas**: `SECRET_KEY` defaults to `'dev-secret-key'` — **must** be changed in production via the `SECRET_KEY` environment variable.

---

#### `run.py` — Entry Point

- **What it does**: Imports `create_app`, creates the app, runs it with `debug=True`.
- **How to change port**: `app.run(debug=True, port=8080)`.
- **Dependencies**: Imports `create_app` from `app`.
- **Gotchas**: `debug=True` only for development. Never deploy with debug mode enabled.

---

#### `seed.py` — Demo Data

- **What it does**: Creates 1 admin (`admin`/`admin123456`), 5 students (`student1`-`student5`/`12345678`), 5 sample events with different time offsets and capacities, and sample registrations (3 students registered for the welcome event, student1 registered and checked in for the Python workshop).
- **How to add more demo data**: Add `User`, `Event`, or `Registration` objects before `db.session.commit()`.
- **Dependencies**: Imports `create_app` from `app`, `db` from `app.extensions`, models from `app.models`.
- **Gotchas**: Must run with an empty database — delete `instance/app.db` first if it exists. Uses `db.session.flush()` to get auto-generated IDs before creating dependent records.

---

#### `tests/conftest.py` — Test Fixtures

- **What it does**: Provides four pytest fixtures: `app` (creates app with TestConfig, in-memory SQLite, creates/drops all tables), `client` (Flask test client), `auth_client` (registers and logs in a test user), `sample_event` (creates a test event via auth_client).
- **How to add new fixtures**: Add `@pytest.fixture` functions. Use `auth_client` for routes that require authentication.
- **Dependencies**: Imports `create_app` from `app`, `db` from `app.extensions`, `TestConfig` from `config`.
- **Gotchas**: `TestConfig` disables CSRF — don't test CSRF behavior with these fixtures. The `sample_event` fixture depends on `auth_client` (the event creator is user ID 1).

---

#### `tests/test_auth.py` — Auth Tests

- **What it does**: 5 tests covering: successful registration (302 redirect to login), duplicate username detection, successful login (302 redirect), wrong password (flash message), and logout (302 redirect to login).
- **Dependencies**: Uses `client` and `auth_client` fixtures from `conftest.py`.
- **Gotchas**: Tests assert on Chinese flash messages (e.g., `'用户名已存在'`) — if you change message text, update tests.

---

#### `tests/test_event.py` — Event Tests

- **What it does**: 6 tests covering: empty event list (200), create event while logged in (302), create event while logged out (302 to login), event detail page (200 + content check), edit event (302), delete event (302 redirect to list).
- **Dependencies**: Uses `client`, `auth_client`, `sample_event` fixtures. Uses `EVENT_DATA` dict for form data.
- **Gotchas**: `EVENT_DATA` datetime strings use `%Y-%m-%dT%H:%M` format — must match `DateTimeLocalField` format in `EventForm`.

---

#### `tests/test_checkin.py` — Check-in Tests

- **What it does**: 5 tests covering: register for event (302), check-in with correct code (flash '签到成功'), check-in with wrong code (flash '签到码错误'), check-in without registration (flash '尚未报名'), double check-in prevention (flash '已经签到过了').
- **Dependencies**: Uses `auth_client` and `sample_event` fixtures.
- **Gotchas**: Tests depend on the `sample_event` fixture's `checkin_code='ABC123'`. The order of operations matters — register before check-in.

---

#### `requirements.txt` — Dependencies

- **What it does**: Pins all Python dependencies with exact versions.
- **Dependencies**: Used by `pip install -r requirements.txt`.
- **Gotchas**: Flask 3.1.1, Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.x — don't downgrade to SQLAlchemy 1.x (incompatible `db.get_or_404()` syntax).

---

#### `report.html` — Lab Report

- **What it does**: Self-contained 12-section HTML report with Mermaid diagrams, copy buttons, scroll animations, and responsive layout. Demonstrates the project's technical architecture visually.
- **How to edit content**: Modify HTML directly — all sections have `id` attributes (`s1` through `s12`).
- **How to add a new section**: Add `<h2 id='sN'>` heading + `<div class='section'>` with content.
- **Gotchas**: Mermaid diagrams render client-side — the CDN script must load. Copy buttons are auto-generated by JavaScript on page load.

---

#### `index.html` — Redirect Page

- **What it does**: Simple HTML page that redirects to `report.html` via `<meta http-equiv="refresh">`.
- **Gotchas**: This is NOT part of the Flask app — it's a static file for GitHub Pages or direct file access.

---

#### `DESIGN.md` — Design System Documentation

- **What it does**: Chinese-language design system specification covering: color system (light/dark themes with all CSS variable values), typography (font families, sizes, weights, spacing), Liquid Glass implementation (glass component, pseudo-elements, concentric corners), component specs (nav, cards, buttons, forms, badges, tables, flash messages), interaction patterns (transitions, click feedback, touch targets), theme switching, i18n, and responsive design.
- **How to use**: Reference when modifying any visual aspect of the project.
- **Dependencies**: References CSS variables and class names from `static/css/style.css`.
- **Gotchas**: CSS variable names in DESIGN.md must match `style.css` — update both when changing. The color contrast ratios cited assume the specified background colors.

---

## API Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | — | Redirects to event list |
| GET/POST | `/auth/register` | — | User registration |
| GET/POST | `/auth/login` | — | User login |
| POST | `/auth/logout` | ✓ | User logout (CSRF) |
| GET | `/event/` | — | Event list + search (`?q=`) + category filter (`?cat=`) + pagination (`?page=`) |
| GET | `/event/<id>` | — | Event detail |
| GET/POST | `/event/create` | ✓ | Create event |
| GET/POST | `/event/<id>/edit` | ✓ | Edit event (creator/admin) |
| POST | `/event/<id>/delete` | ✓ | Delete event (creator/admin) |
| POST | `/event/<id>/register` | ✓ | Register for event |
| POST | `/event/<id>/cancel` | ✓ | Cancel registration (soft-delete) |
| GET/POST | `/checkin/<event_id>` | ✓ | Check-in with code |
| GET | `/checkin/<event_id>/qr` | ✓ | QR code PNG for check-in URL |
| GET | `/admin/` | ✓+admin | Admin dashboard |
| GET | `/admin/export/<event_id>` | ✓+admin | CSV export for single event |
| GET | `/admin/export/all` | ✓+admin | CSV export for all registrations |

## Data Models

```
User (1) ──── (*) Registration (*) ──── (1) Event
  │                                         │
  ├── id                                    ├── id
  ├── username (unique)                     ├── title
  ├── email (unique)                        ├── description
  ├── password_hash                         ├── location
  ├── is_admin                              ├── start_time / end_time
  └── created_at                                                                        ├── max_participants
                                            ├── checkin_code
                                            ├── category (enum: Tech/Culture/Sports/Academic/Social/Other)
                                            ├── creator_id → User
                                            └── created_at

Registration
  ├── user_id → User
  ├── event_id → Event
  ├── status ('confirmed' | 'cancelled')
  ├── registered_at
  ├── checked_in (bool)
  └── checked_in_at
```

## Skills & Tools Used

| Skill | Purpose |
|-------|---------|
| `frontend-design` | UI component design, Liquid Glass implementation |
| `make-interfaces-feel-better` | 14-principle UI audit (hit areas, transitions, tabular-nums, etc.) |
| `docx` | Read course manual .docx for requirements extraction |
| `caveman` | Concise communication mode for reduced token usage |

### Design References

- **Apple HIG Liquid Glass** — material spec, light refraction, concentric corners
- **NN/g UX Guidelines** — usability heuristics, accessibility, feedback patterns

## Architecture Decisions

### App Factory Pattern

```python
def create_app(config_class=Config):
    app = Flask(__name__, template_folder=..., static_folder=...)
    # init extensions, register blueprints
    return app
```

**Why**: Avoids circular imports, enables testing with `TestConfig`, supports multiple instances.

### Soft-Delete for Registration

```python
reg.status = 'cancelled'  # instead of db.session.delete(reg)
```

**Why**: Preserves registration history, enables waitlist re-activation, maintains referential integrity.

### POST-Only Logout

```python
@auth_bp.route('/logout', methods=['POST'])
```

**Why**: CSRF protection — GET logout would be vulnerable to CSRF via `<img>` tags or link injection.

### UTC Datetimes

```python
created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
```

**Why**: Timezone consistency — all timestamps stored in UTC, displayed with local conversion.

### Flask-WTF CSRFProtect

```python
csrf = CSRFProtect()  # global CSRF protection
```

**Why**: Protects all POST forms by default; logout form explicitly includes `csrf_token()`.

### db.get_or_404()

```python
event = db.get_or_404(Event, id)
```

**Why**: SQLAlchemy 2.x compatible — replaces deprecated `query.get_or_404()`, returns 404 on missing records.

### Pagination via Flask-SQLAlchemy `.paginate()`

```python
page = request.args.get('page', 1, type=int)
pagination = query.paginate(page=page, per_page=12, error_out=False)
```

**Why**: `.paginate()` returns a `Pagination` object with built-in `has_prev`/`has_next`/`iter_pages()` — simpler and less error-prone than manual cursor/offset pagination. The `per_page=12` aligns with the 3-column card grid. Cursor-based pagination was considered but adds complexity for minimal benefit at this scale.

### Server-Side QR Code Generation

```python
import qrcode, io, base64
img = qrcode.make(checkin_url)
buf = io.BytesIO()
img.save(buf, format='PNG')
qr_b64 = base64.b64encode(buf.getvalue()).decode()
```

**Why**: Generating QR codes server-side with the `qrcode` library avoids client-side JS dependencies and works without JavaScript. The image is embedded as a base64 data URI — no external hosting or static file management needed.

### CSV Export with UTF-8 BOM

```python
response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
```

**Why**: Using `utf-8-sig` (UTF-8 with BOM) ensures Excel on Windows correctly detects the encoding and displays CJK characters. Plain UTF-8 CSVs open with garbled Chinese text in Excel by default.

## License

MIT — built as a course project.
