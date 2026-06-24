# Report.html Visual Overhaul Plan

> **Goal:** Fix 7 visual issues in report.html based on research findings
>
> **Research sources:** Mermaid.js theming docs, GitHub markdown-css patterns, WCAG AA contrast guidelines

---

## Task 1: Remove Red Accent Borders + Unify Border-Radius

**What:** Remove all `border-left: 2px solid var(--accent)` from code blocks, trees, notes, blockquotes. Adopt 4/6/8px border-radius scale.

**Verify:** `grep "border-left.*accent" report.html` returns 0 matches. All border-radius values are 4px, 6px, or 8px.

- [ ] Remove `border-left` from `pre`, `.tree`, `.note`, `blockquote` CSS rules
- [ ] Change all `border-radius: 4px` on code/table to `border-radius: 6px`
- [ ] Change all `border-radius: 8px` on mermaid to `border-radius: 6px`
- [ ] Verify with grep

---

## Task 2: Unify Copy Buttons

**What:** Every `pre`, `.tree`, `blockquote`, `.mermaid`, `table` gets a copy button. Currently only pre/tree/blockquote have them.

**Verify:** JS selector covers all 5 element types. All copy buttons have identical styling.

- [ ] Update JS selector: `document.querySelectorAll('pre, .tree, blockquote, .mermaid, table')`
- [ ] Verify all copy buttons render

---

## Task 3: Fix Glass Effect (Grey/Dusty → Clean)

**What:** Replace `rgba(0,0,0,0.03)` background on code/table/mermaid with clean `#f6f8fa` (GitHub-style light grey). Remove any remaining backdrop-filter on content elements.

**Verify:** No `rgba(0,0,0,0.0` backgrounds on content elements. No `backdrop-filter` except nav.

- [ ] Replace all `background: rgba(0,0,0,0.03)` with `background: #f6f8fa`
- [ ] Replace all `background: rgba(0,0,0,0.02)` with `background: #f8fafb`
- [ ] Verify no backdrop-filter on content elements

---

## Task 4: Improve Text Readability

**What:** Increase text contrast. Cover page text too light.

**Verify:** Cover page meta text uses `--ink-secondary` (#3A3A3A), not `--ink-muted`. All body text ≥ WCAG AA (4.5:1 ratio).

- [ ] Change `.cover .meta-table td:first-child` color from `var(--ink-muted)` to `var(--ink-secondary)`
- [ ] Change `.cover .subtitle` to use `var(--ink-secondary)` not `var(--ink-muted)`
- [ ] Change `.cover .date` to use `var(--ink-secondary)`
- [ ] Ensure `--ink-muted` is only used for truly secondary content (copy buttons, helper text)
- [ ] Verify cover page text is readable

---

## Task 5: Unify Font Sizes and Styles

**What:** Ensure all elements use the CSS variable scale (--text-xs/sm/base/md). Remove any remaining hardcoded font-size/font-family/letter-spacing.

**Verify:** `grep "font-size:" report.html | grep -v "var(--text"` returns 0 matches in the `<style>` block (code examples excluded).

- [ ] Search for hardcoded font-size/font-family/letter-spacing in `<style>` block
- [ ] Replace with CSS variables
- [ ] Verify

---

## Task 6: Redraw Mermaid Diagrams

**What:** Use `mermaid.initialize()` with warm theme variables. Redraw 3 diagrams:
1. System Architecture — cleaner flowchart with `curve: "linear"`
2. Module Relations — simplified, fewer nodes
3. ER Diagram — horizontal layout, fewer fields, clean styling

**Verify:** Mermaid renders with warm cream/terracotta colors. No default blue/green.

- [ ] Add `mermaid.initialize()` with warm theme config in `<script>`
- [ ] Redraw system architecture diagram
- [ ] Redraw module relations diagram
- [ ] Redraw ER diagram with `direction LR`
- [ ] Verify all 3 render correctly

---

## Task 7: Verify + Deploy

- [ ] Open report.html in browser
- [ ] Check all sections visible
- [ ] Check all copy buttons work
- [ ] Check Mermaid diagrams render
- [ ] Check text readability on cover page
- [ ] Check no red accent lines
- [ ] Check consistent border-radius
- [ ] Commit + push
