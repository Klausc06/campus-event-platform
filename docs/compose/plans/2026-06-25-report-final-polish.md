# Report.html Final Polish Plan

> Based on research findings — 6 actionable items

## Task 1: Remove unused CSS variables

**What:** Remove dead variables that are defined but never used in the `<style>` block.

**Verify:** `grep "glass-bg\|glass-border\|glass-radius" report.html` in `<style>` returns 0 matches.

- [ ] Remove `--glass-bg`, `--glass-border`, `--glass-radius` from `:root`
- [ ] Keep `--glass-blur` (used by nav)
- [ ] Verify

---

## Task 2: Tokenize font-family on body and h1-h6

**What:** Replace raw font stacks with `--font-body` variable.

**Verify:** No raw font stacks in `<style>` block.

- [ ] Add `--font-body: "Noto Serif SC", "Songti SC", "SimSun", serif;` to `:root`
- [ ] Replace `body { font-family: "Noto Serif SC", ... }` with `font-family: var(--font-body)`
- [ ] Replace `h1-h6 { font-family: "Noto Serif SC", ... }` with `font-family: var(--font-body)`
- [ ] Verify

---

## Task 3: Fix hardcoded letter-spacing

**What:** Replace `.cover h1 { letter-spacing: 4px }` with variable.

**Verify:** No hardcoded letter-spacing in `<style>` block.

- [ ] Add `--ls-wider: 4px;` to `:root` (cover title needs wider spacing)
- [ ] Change `.cover h1 { letter-spacing: 4px }` to `var(--ls-wider)`
- [ ] Verify

---

## Task 4: Add .note to copy button selector

**What:** Make `.note` blocks copyable too.

**Verify:** JS selector includes `.note`.

- [ ] Update JS `querySelectorAll` to include `.note`
- [ ] Add `.note .copy-btn` to CSS hover/active/copied selectors
- [ ] Verify

---

## Task 5: Clean up dead glass-radius on cover

**What:** `.cover .project-name` uses `12px` — either make it 6px or document it.

**Verify:** border-radius consistency.

- [ ] Change to 6px for consistency
- [ ] Verify

---

## Task 6: Force fresh deployment

**What:** Ensure GitHub Pages serves the latest version, not a cached one.

**Verify:** Deployed page matches local file.

- [ ] Commit and push
- [ ] Wait for workflow completion
- [ ] Verify deployed content matches local via curl hash comparison
