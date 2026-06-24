# Bonus Features: Fix CSV + Add Pagination/Category Filter

> **For agentic workers:** Use compose:subagent to implement.

**Goal:** Fix CSV export issues and add pagination + category filtering to event list.

**Architecture:** Two independent tasks. CSV fix is surgical. Pagination uses Flask-SQLAlchemy `.paginate()` + Jinja2 controls.

---

### Task 1: Fix CSV Export

**Files:**
- Modify: `app/admin/routes.py`

**Issues to fix:**
1. UTF-8 BOM missing — Chinese characters garble in Excel on Windows
2. N+1 query in export_all() — loops events then queries registrations per event
3. Filename encoding — ASCII-only Content-Disposition

**Steps:**

- [ ] Read `app/admin/routes.py`
- [ ] In `export_event()`: prepend BOM `\ufeff` before csv.writer
- [ ] In `export_all()`: replace per-event loop with single joined query:
```python
regs = db.session.query(Registration, Event.title).join(Event).filter(
    Registration.status == 'confirmed'
).all()
```
- [ ] In both routes: use RFC 5987 filename encoding for Chinese filenames
- [ ] Verify syntax
- [ ] Run tests

---

### Task 2: Add Pagination + Category Filter

**Files:**
- Modify: `app/event/routes.py`
- Modify: `templates/event/list.html`
- Modify: `templates/event/create.html`
- Modify: `templates/event/edit.html`
- Modify: `templates/event/detail.html`
- Modify: `app/forms.py`
- Modify: `static/css/style.css`
- Modify: `seed.py`

**Steps:**

- [ ] Read all files listed above
- [ ] In `app/event/routes.py` `list_events()`:
  - Add `page = request.args.get('page', 1, type=int)`
  - Add `category = request.args.get('category', '')`
  - Add category filter: `if category: query = query.filter_by(category=category)`
  - Replace `.all()` with `.paginate(page=page, per_page=12, error_out=False)`
  - Pass `pagination`, `category`, `q` to template
- [ ] In `app/forms.py` EventForm:
  - Add `category` SelectField with choices from models.CATEGORIES
- [ ] In `templates/event/list.html`:
  - Add category filter pills above cards (each links to ?category=X)
  - Active pill highlighted with accent color
  - Add pagination controls below cards (Previous / page numbers / Next)
  - Preserve `q` and `category` in pagination links
- [ ] In `templates/event/create.html` and `edit.html`:
  - Add category select field
- [ ] In `templates/event/detail.html`:
  - Show category badge
- [ ] In `static/css/style.css`:
  - Add `.category-pills`, `.pill`, `.pagination` styles (Liquid Glass variables)
- [ ] In `seed.py`:
  - Add categories to demo events
- [ ] Verify syntax
- [ ] Run tests

---

### Task 3: Verify All + UI Audit

- [ ] Run full test suite: `python3 -m pytest tests/ -v`
- [ ] Run make-interfaces-feel-better review on new/changed templates
- [ ] Fix any issues found
- [ ] Commit
