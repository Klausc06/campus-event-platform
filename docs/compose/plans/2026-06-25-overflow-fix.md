# Horizontal Overflow Root Cause Fix Plan

## Root Causes
1. `.mermaid` SVG wider than container, no overflow protection
2. `.tree` no overflow/wrap properties
3. `table` uses `table-layout: auto`, expands beyond 100% when cells are wide

## Task 1: Fix Mermaid Overflow

- [ ] Add `overflow-x: auto; max-width: 100%;` to `.mermaid`
- [ ] Add `.mermaid svg { max-width: 100%; height: auto; }`

## Task 2: Fix Tree Overflow

- [ ] Add `overflow-x: auto; max-width: 100%;` to `.tree`

## Task 3: Fix Table Overflow

- [ ] Add `max-width: 100%; overflow-x: auto; display: block;` to `table` (keeps natural column widths, enables internal scroll if needed)
- [ ] Do NOT use `table-layout: fixed` — would break tables with uneven column widths
- [ ] Add `overflow-wrap: break-word; word-break: break-word;` to `th, td`

## Task 4: Verify

- [ ] No horizontal scrollbar on any section
- [ ] Tables render correctly (columns visible)
- [ ] Mermaid diagrams render (may be scrollable if too wide)
- [ ] Commit + push
