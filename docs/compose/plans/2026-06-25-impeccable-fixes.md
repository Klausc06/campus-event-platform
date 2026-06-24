# Impeccable Audit Fix Plan

> Based on impeccable audit (9/20) + critique (22/40). 26 findings. Plan reviewed and corrected.

## Task 1: Fix CSS Syntax Errors

**What:** CSS syntax errors break rule parsing. Fix first.

- [ ] `.auth-wrap`: add missing `;` before `display: flex`
- [ ] `.checkin-wrap`: add missing `;` before `display: flex`
- [ ] Remove empty rule blocks
- [ ] Add `@media (prefers-reduced-motion: reduce)` guard

---

## Task 2: Remove Glass Overuse

**What:** Glass on everything = #1 AI tell. Keep on nav + event cards ONLY.

- [ ] Remove `backdrop-filter` from: `pre`, `.tree`, `.note`, `blockquote`, `.mermaid`, `table`, `.search-box`, `.auth-card`, `.checkin-card`, `.stat-card`, `.admin-table`, `.pagination`
- [ ] Keep glass on: `nav`, `.card` only
- [ ] Replace with solid `rgba(255,255,255,0.85)` or `#f6f8fa`

---

## Task 3: Remove Side-Stripe Borders

**What:** `border-left: 3px solid` banned by impeccable.

- [ ] Remove ALL `border-left` from style.css
- [ ] Alerts: use background tint only (already have --success-soft)
- [ ] Stat cards: replace with `::before` accent dot

---

## Task 4: Fix Accessibility

- [ ] Skip-nav link in base.html
- [ ] `role="group"` + `aria-pressed` on toggle buttons
- [ ] `:focus-visible` outline in CSS
- [ ] Verify `id`/`for` matching on form inputs

---

## Task 5: Fix Touch Targets

- [ ] `.btn`: `min-height: 44px`
- [ ] `.btn-sm`: `min-height: 40px`
- [ ] `.pill`: `padding: 10px 18px`
- [ ] `.page-btn`: `min-height: 40px`

---

## Task 6: Remove Bootstrap

**Dependencies:** Add `.form-control` + utility CSS BEFORE removing.

- [ ] Add `.form-control` rule to style.css
- [ ] Add utility classes: `.d-flex`, `.justify-content-between`, `.align-items-center`, `.mb-4`, `.mt-3`
- [ ] Remove Bootstrap CSS `<link>` from base.html
- [ ] Remove Bootstrap JS `<script>` from base.html

---

## Task 7: Vary Card Layout

- [ ] Add `data-category="{{ event.category }}"` to cards in list.html
- [ ] Add category-specific colored top borders in CSS (6 categories)

---

## Task 8: Update report.html

- [ ] Document impeccable usage in AI辅助 section

---

## Task 9: Verify + Deploy

- [ ] `python3 -m pytest tests/ -v`
- [ ] Verify no broken styles
- [ ] Commit + push
