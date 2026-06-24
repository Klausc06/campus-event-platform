# Report.html 4 Issues Fix Plan

> Based on research findings

## Task 1: Restore Glass Effect (Single Layer)

**What:** Add glass back to containers only, NOT child elements. Single layer, no stacking.

- [ ] Re-add to `:root`: `--glass-bg: rgba(255,255,255,0.42);`, `--glass-border: rgba(255,255,255,0.6);`
- [ ] Apply `backdrop-filter: blur(var(--glass-blur))` + glass bg/border to: `pre`, `.tree`, `.note`, `blockquote`, `.mermaid`
- [ ] Apply glass to `table` wrapper only. `th`, `td` → `background: transparent`
- [ ] Do NOT apply backdrop-filter to `th`, `td`, `code`, `p code` — that causes stacking
- [ ] Add subtle `box-shadow` for depth

---

## Task 2: Fix Scrollbars

**What:** Remove horizontal overflow.

- [ ] Add `overflow-x: hidden` to `.report-body`
- [ ] Remove `white-space: nowrap` from `th`
- [ ] Keep `pre { overflow-x: auto }` (code blocks scroll internally)

---

## Task 3: Fix Copy Button Positioning

**What:** Smaller, hidden by default, shown on hover, no content overlap.

- [ ] Change copy-btn to: `top: 6px; right: 6px; padding: 6px 10px; min-height: 28px; font-size: 11px;`
- [ ] Add `opacity: 0` by default, `opacity: 1` on parent `:hover`
- [ ] Section copy-btn: `top: 4px; right: 4px` (offset from heading)
- [ ] All copy buttons consistent size and behavior

---

## Task 4: Fix Mermaid Diagrams

**What:** Pin CDN version, add error handling, quote labels with special chars.

- [ ] Pin mermaid CDN to `@10.9.0`
- [ ] Wrap `mermaid.initialize()` in `DOMContentLoaded` + `try/catch`
- [ ] Quote node labels containing `/` or special chars in all 3 diagrams
- [ ] Add `console.error` for debugging

---

## Task 5: Verify

- [ ] Open page in browser
- [ ] Check glass effect visible on containers
- [ ] Check no horizontal scrollbar
- [ ] Check copy buttons don't overlap content
- [ ] Check Mermaid diagrams render
- [ ] Commit + push
