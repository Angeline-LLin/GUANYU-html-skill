# GUANYU presentation runtime

Use this reference when building or upgrading a GUANYU fixed-stage HTML presentation.

## Required controls

- Keep all slides in the DOM as `.slide` elements inside one 1920×1080 stage.
- Switch the current page with `.active`; retain `.visible` for the current page and visited pages only when staged animation needs that state.
- Support keyboard navigation: ArrowLeft/ArrowRight, PageUp/PageDown, Space.
- Support click navigation by left/right stage halves.
- Support wheel and touch swipe navigation.
- Support URL hash navigation with `#1`, `#2`, etc.
- Include `prefers-reduced-motion: reduce` so all content remains visible without animation.

## Editing

- Include edit mode by default unless the user asks for locked output.
- Trigger edit mode with `E`.
- Add `data-edit-id` to editable content fields only: titles, body copy, table cells, metrics, captions, sources, and speaker notes.
- Do not make Logo, page number, stage geometry, grid, page type, or structural chrome editable.
- Persist edits to `localStorage`.
- Support `Ctrl+S` / `Cmd+S` to export a complete edited HTML file.
- Provide a reset action that clears local saved edits only after user confirmation.

## Overview mode

- Trigger with `O`.
- Show all slide thumbnails or compact title cards.
- Selecting a thumbnail jumps to that slide and closes overview.
- Do not display overview in print mode.

## Optional presenter mode

- Trigger with `S`.
- Show current title, next title, page counter, elapsed time or notes when available.
- Presenter mode is a control surface, not part of the slide stage.
- Do not display presenter mode in print mode.
- Include presenter mode only when the user needs formal rehearsal or delivery support. Do not make it a blocking QA requirement.

## Print and PDF

- Include print CSS that makes every slide visible at 1920×1080 and hides all controls.
- Browser PDF export is the default export path.
- HTML export must bundle current text edits into a downloaded file when possible.

## QA requirements

- Run `scripts/qa_html_deck.js --html <deck.html> --out-dir <qa-dir>`.
- Inspect both `qa-report.json` and `qa-report.html`.
- Treat pages with image/data/table/timeline/architecture risk flags as requiring screenshot review.
- A passing JSON report is necessary but not sufficient when screenshots reveal weak visual hierarchy, cropping, crowding, or Logo misuse.
