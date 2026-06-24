# Campus Event Platform

A Flask-based web application for campus event management — event creation, registration, and check-in — with an Apple Liquid Glass (WWDC25) inspired design system featuring frosted glass UI, dark/light themes, and bilingual (Chinese/English) support.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask 3.x (app factory + 4 blueprints) |
| ORM | Flask-SQLAlchemy 3.x + SQLite |
| Auth | Flask-Login 0.6 |
| Forms | Flask-WTF + WTForms (CSRF-protected) |
| Migrations | Flask-Migrate (Alembic) |
| Frontend | Jinja2 + custom CSS (Liquid Glass) |
| Fonts | Noto Serif SC (CJK), DM Sans (Latin) |
| Testing | pytest 8.x |
| Extras | qrcode + Pillow (QR generation) |

## Architecture

```
┌─────────────────────────────────────────────┐
│                   Flask App                 │
│              (create_app factory)            │
├──────────┬──────────┬───────────┬───────────┤
│ auth_bp  │event_bp  │checkin_bp │ admin_bp  │
│ /auth    │ /event   │ /checkin  │ /admin    │
├──────────┴──────────┴───────────┴───────────┤
│           Flask-Login + CSRFProtect         │
├─────────────────────────────────────────────┤
│           Flask-SQLAlchemy (SQLite)          │
│        User ← Registration → Event          │
└─────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone <repo-url> && cd campus-event-platform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Seed Demo Data

```bash
python3 seed.py
```

This creates 6 users and 5 sample events with registrations.

### Run

```bash
python3 run.py
# → http://127.0.0.1:5000
```

### Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123456` |
| Student | `student1` – `student5` | `12345678` |

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
│   ├── checkin/             # checkin.html
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
└── requirements.txt         # pinned dependencies
```

## Design System

See **[DESIGN.md](DESIGN.md)** for the complete design specification (Chinese).

### Key CSS Variables

```css
/* Core palette */
--bg: #EDEAE4;           /* page background */
--ink: #1A1A1A;          /* primary text */
--accent: #C45A3A;       /* terracotta accent */
--glass-bg: rgba(255,255,255,0.42);   /* frosted glass */
--glass-blur: 40px;      /* blur radius */
--glass-radius: 20px;    /* unified border radius */

/* Dark theme overrides via [data-theme="dark"] */
--bg: #0E0E12;
--ink: #F0EDE8;
--glass-bg: rgba(255,255,255,0.06);
```

### Theme Toggle

```javascript
setTheme('light' | 'dark')   // sets data-theme on <html>, persists to localStorage
```

### Language Toggle

```javascript
setLang('zh' | 'en')         // swaps textContent from data-zh/data-en attrs
```

## Skills & Tools Used

### Development Skills

| Skill | Purpose |
|-------|---------|
| `frontend-design` | UI component design, Liquid Glass implementation |
| `make-interfaces-feel-better` | Micro-interactions, animations, hover states |
| `compose:plan` | Architecture planning |
| `compose:subagent` | Parallel task execution |
| `docx` | Documentation generation |
| `caveman` | Concise communication mode |

### Design References

- **Apple HIG Liquid Glass** — material spec, light refraction, concentric corners
- **NN/g UX Guidelines** — usability heuristics, accessibility, feedback patterns

### Review Process

```
implement → review → fix → re-review → pass
```

All UI changes went through iterative review cycles focusing on:
- Visual consistency with Liquid Glass spec
- Interaction feedback (hover, active, focus)
- Accessibility (contrast, touch targets, keyboard nav)
- Responsive behavior at 640px breakpoint

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

## API Routes

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | — | Redirects to event list |
| GET/POST | `/auth/register` | — | User registration |
| GET/POST | `/auth/login` | — | User login |
| POST | `/auth/logout` | ✓ | User logout (CSRF) |
| GET | `/event/` | — | Event list + search (`?q=`) |
| GET | `/event/<id>` | — | Event detail |
| GET/POST | `/event/create` | ✓ | Create event |
| GET/POST | `/event/<id>/edit` | ✓ | Edit event (creator/admin) |
| POST | `/event/<id>/delete` | ✓ | Delete event (creator/admin) |
| POST | `/event/<id>/register` | ✓ | Register for event |
| POST | `/event/<id>/cancel` | ✓ | Cancel registration |
| GET/POST | `/checkin/<event_id>` | ✓ | Check-in with code |
| GET | `/admin/` | ✓+admin | Admin dashboard |

## Data Models

```
User (1) ──── (*) Registration (*) ──── (1) Event
  │                                         │
  ├── id                                    ├── id
  ├── username (unique)                     ├── title
  ├── email (unique)                        ├── description
  ├── password_hash                         ├── location
  ├── is_admin                              ├── start_time / end_time
  └── created_at                            ├── max_participants
                                            ├── checkin_code
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

## Testing

### Run Tests

```bash
# Activate venv first
python3 -m pytest tests/ -v
```

### Test Configuration

```python
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
```

### Test Fixtures (conftest.py)

| Fixture | Description |
|---------|-------------|
| `app` | Creates app with TestConfig, in-memory SQLite |
| `client` | Flask test client |
| `auth_client` | Pre-authenticated test client (registers + logs in) |
| `sample_event` | Creates a test event via auth_client |

## Deployment

### Local Development

```bash
python3 run.py
# Debug mode enabled, http://127.0.0.1:5000
```

### Cpolar Tunnel (Optional)

For exposing local dev server to the internet:

```bash
cpolar http 5000
```

### Production Considerations

- Set `SECRET_KEY` environment variable
- Use PostgreSQL instead of SQLite
- Set `WTF_CSRF_ENABLED=True`
- Disable debug mode
- Use Gunicorn/uWSGI as WSGI server

## License

MIT — built as a course project.
