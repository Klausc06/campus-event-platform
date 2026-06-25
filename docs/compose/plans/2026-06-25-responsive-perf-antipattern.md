# Responsive + Performance + Anti-Patterns Fix Plan

> Target: 3/5→5/5 responsive, 3/5→5/5 performance, 2/5→5/5 anti-patterns

## Task 1: Clean Duplicate CSS

**What:** Remove duplicate rules introduced by previous fixes.

- [ ] Delete lines 313-318 (first set of category borders — overridden by lines 983-987)
- [ ] Delete lines 974-980 (duplicate `@media (prefers-reduced-motion)` block)

---

## Task 2: Remove Glass from Cards

**What:** Glassmorphism on every card is the #1 AI tell. Nav has its OWN `.nav` rule with backdrop-filter (not `.glass` class). The `.glass::before/::after` pseudo-elements are dead code (no template uses `.nav.glass`/`.stat-card.glass`/`.detail.glass`).

- [ ] In `templates/event/list.html`: remove `glass` class from cards (line 35: `class="card glass"` → `class="card"`)
- [ ] In `static/css/style.css`: add `.card { background: rgba(255,255,255,0.85); }` BEFORE removing glass
- [ ] Delete dead `.glass::before` and `.glass::after` rules (lines 126-147) — no template uses them
- [ ] `.nav` keeps its own `backdrop-filter` at line 188 — NOT affected
- [ ] Also fix `.nav-brand` `letter-spacing: 3px` → `1px` (same anti-pattern as section-tag)

---

## Task 3: Fix Section-Tag Eyebrow

**What:** `font-size: 11px; letter-spacing: 3px; text-transform: uppercase` is the banned eyebrow pattern.

- [ ] Change to: `font-size: 12px; letter-spacing: 1px; text-transform: none`

---

## Task 4: Add Tablet Breakpoint

**What:** Only 640px breakpoint exists. Add 768px for tablet. ORDERING: place 768px block BEFORE 640px block (larger breakpoint first in CSS cascade).

- [ ] Add `@media (max-width: 768px)` BEFORE the existing 640px block with:
  - `.stat-row`: 2x2 grid (`flex-wrap: wrap; .stat-card { flex: 0 0 50% }`)
  - `.admin-table-head`/`.admin-row`: collapse to 2 columns
  - `.hero`: widen max-width to 90%
  - `.cards`, `.detail-wrap`, etc.: widen to 90vw

---

## Task 5: Optimize Performance

- [ ] Add `@media (prefers-reduced-motion: reduce) { .nav { backdrop-filter: none } }` guard
- [ ] Verify no unused CSS rules

---

## Task 6: Verify

- [ ] `python3 -m pytest tests/ -v` — 20/20 pass
- [ ] No `transition: all` in CSS
- [ ] No `border-left` in CSS
- [ ] Only `nav` has `backdrop-filter`
- [ ] No duplicate CSS blocks
- [ ] Tablet breakpoint works at 768px
