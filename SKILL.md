---
name: guanyu-html-builder
description: Create GUANYU-branded HTML presentations and responsive web pages using only the GUANYU brand visual guidelines as the primary authority and the calibrated PPT reference files as the secondary layout authority. Use when the user asks for a GUANYU HTML deck, branded landing page, company presentation, product page, data page, or conversion of PPT content into HTML.
---

# GUANYU HTML Builder

## Authority and scope

Follow this authority order without exception:

1. `references/guanyu-brand-rules.md` - derived from the GUANYU VIS Guidelines and the brand's machine-readable PPT rules. It controls fonts, colors, Logo, grid, visual tone, imagery, charts, and prohibitions.
2. `references/guanyu-ppt-layouts.md` - derived from the calibrated PPT reference. It controls page families, page purposes, capacity, calibrated geometry, and presentation rhythm.
3. `references/guanyu-runtime-and-export.md` - derived from approved Frontend Slides runtime mechanics. It controls editing, overview mode, presenter mode, export, print, and QA behavior.
4. The Frontend Slides workflow - use only for content discovery, HTML generation, navigation, animation, conversion, and browser verification.

Do not use Frontend Slides' original visual presets, bold template pack, external template libraries, unapproved fonts, arbitrary colors, or generic AI aesthetics. If a request conflicts with the two GUANYU references, flag the conflict and follow the higher-priority brand rule.

## Required private logo assets

This public skill repository intentionally does not include GUANYU logo PNG files.

Before creating, converting, previewing, QA-ing, or packaging any GUANYU-branded output, verify that the authorized user has placed the approved internal logo files in `assets/logo/` with these exact names:

- `guanyu-standard-black.png`
- `guanyu-standard-white.png`

If either file is missing, stop and ask the user to obtain the approved PNG files from the company's internal brand source and place them in `assets/logo/`. Do not generate a branded deck or substitute the Logo with text, SVG, CSS, screenshots, public web downloads, or recreated artwork.

## Modes

Choose one mode before generating:

- **GUANYU Web Presentation**: fixed 16:9 stage, 1280x720 calibration coordinates, slide navigation, suitable for PPT-like presentations and reports.
- **GUANYU Responsive Web Page**: normal responsive reflow for landing pages, product pages, forms, and websites; preserve GUANYU typography, palette, Logo, grid logic, and visual restraint.

Do not force ordinary websites into a fixed 16:9 stage. Do not make presentations reflow like a dashboard when the user expects slide fidelity.

## Content discovery and delivery workflow

Adopt the Frontend Slides workflow mechanics while keeping all visual decisions inside the GUANYU authority order.

1. Detect the task mode: new presentation, PPT conversion, or enhancement of an existing HTML deck.
2. For a new presentation, collect purpose, audience, approximate length, available text, available images, and density in one concise prompt. Density is mandatory: use **speaker-led** for one claim, large type, and 1–3 short points; use **reading-first** for self-contained tables, notes, diagrams, and 4–8 short points. Split pages instead of shrinking text.
3. When images are supplied, inspect every candidate before outlining: identify what it depicts, whether it is factual and approved, its likely page role, and whether its color/contrast can coexist with GUANYU. Design the outline around approved images; never add generated imagery as evidence. If an image is the evidence or product subject, preserve its full object unless the user approves a crop; adjust text width, title line breaks, and image area before cropping the image.
4. Before generating a new deck, show three one-slide visual previews within the same GUANYU VI: **standard brand** (order and whitespace), **technology/data** (structured lines and evidence), and **narrative/communication** (stronger title plus factual imagery). Do not show internal workflow labels on the preview itself. Use `scripts/create_preview_directions.py` when a quick preview set is sufficient, record the result in `preview-directions.json`, and ask the user to select or mix the directions.
5. For enhancement mode, count existing elements before adding content. If content exceeds the selected density or an image would crowd the stage, split the slide proactively. Recheck full-stage screenshots after every material change.
6. Include inline editing by default for normal HTML delivery. Allow a locked/export-only output only when the user requests it. Persist user edits locally, provide reset, and support edited HTML export with `Ctrl+S` / `Cmd+S`.
7. Include overview mode and print styles in presentations. Add presenter mode only when the user needs rehearsal or delivery support. Offer browser PDF export and deployment only when the user asks to share externally; do not deploy without explicit authorization.

Use `third_party/frontend-slides/viewport-base.css` as the copied fixed-stage, print, and reduced-motion reference. Preserve its MIT notice when copying or distributing substantial portions. Adapt its class names and mechanics to the GUANYU grid; do not import its visual presets or external fonts.

## Native deck architecture

For PPT-to-HTML work, use this four-layer architecture:

1. **Data layer**: read `ppt-content.json`, `ppt-layout.json`, and `ppt-shapes.json`; preserve slide order, original text, facts, units, notes, and source coordinates.
2. **Page-type layer**: classify each page into the GUANYU page families below before rendering: cover, section, narrative, split, columns, process, product structure, architecture, metrics, table, image-text, or closing.
3. **Native rendering layer**: render text and layout with HTML/CSS, and render simple lines, circles, arrows, nodes, and charts with SVG. Do not use rendered PPT pages as final slide bodies.
4. **Interaction layer**: render all slides in the DOM and switch `.active`; keep `.visible` for visited slides when staged reveal is required. Support keyboard, click, wheel, touch, hash navigation, edit mode, and reduced motion.

For a complete deck, the output must contain one native slide node per source slide. A renderer that only creates the current slide is not sufficient for page-count validation, export, or visual QA. Use the source renderings only as comparison references.

## Planning artifacts

For every non-trivial deck, create or update structured planning files beside the source material before final delivery:

- `slides-plan.json`: records source files, mode, density, stage, visual authority, page order, page type, theme, page purpose, primary claim, content source, assets, and manual-confirmation status.
- `image-audit.json`: records every candidate image, dimensions, depicted subject, usability status, reason, recommended slide, replacement requirement, and manual-confirmation status.
- `preview-directions.json`: for new decks, records the three GUANYU-only preview directions, the selected direction, and which slides apply each direction.

Use `references/guanyu-planning-schemas.md` for the planning artifact schemas. Keep these files factual and source-linked; do not use them to invent missing claims, metrics, dates, products, customers, or image provenance.

For Word sources, run `scripts/build_from_doc.py --input <file.docx|file.doc> --out-dir <source-dir> --density <speaker-led|reading-first> --direction <standard-brand|technology-data|narrative-communication>` to create the initial text extraction, image-audit draft, slide-plan starter, and three preview files. If `.doc` conversion fails because Word automation is unavailable, ask the user to provide `.docx`.

Use `scripts/recommend_page_types.py` and `references/guanyu-page-type-selector.md` to choose page types before rendering. If a requested content shape is not covered by the 10 approved standard types, first try splitting or combining existing types. Treat agenda, quote, case-study, team-profile, map-coverage, appendix-source, quote-proof, and photo-gallery as unapproved candidate types until the user approves adding them.

### GUANYU page-type capacity

- `cover`: one oversized title, one metadata line, one information-bearing geometric anchor.
- `section`: section number, short section title, restrained supporting label.
- `narrative` / `split`: one claim and one supporting explanation; do not add a card grid by default.
- `columns`: two to four comparable capabilities, each with a numbered label and short description.
- `process`: three to five ordered steps with a visible sequence line or arrows.
- `product structure` / `architecture`: one central system plus a limited number of labeled relationships; use SVG for connectors.
- `metrics`: one main conclusion plus up to three metrics, each with definition, unit, date, and source when applicable.
- `table`: shared comparison criteria, compact rows, clear header, and no decorative cells.
- `image-text`: use approved or source imagery only when it carries meaning; pair it with a single textual claim.
- `closing`: one final statement and minimal supporting information.

### Approved 10-page template system

Use these as the default GUANYU presentation page types. Start from the closest type; do not invent a new visual system unless the user explicitly asks for one and it can be reconciled with the brand rules.

| Type | Use for | Capacity and grid | Header and motion | Do not use for |
| --- | --- | --- | --- | --- |
| Cover | deck theme or primary statement | one title, one metadata line, one information-bearing anchor | Logo only; stagger title, rule, metadata | dense content |
| Section | a narrative chapter transition | one section number and short chapter title | Logo + section label; number and title reveal separately | body copy or data |
| Narrative | one point of view with explanation | title span 8 columns; one supporting paragraph | Logo + page type; title then supporting text | multi-option comparison |
| Columns | two to four peer capabilities | 3 or 4 equal column groups | Logo + page type; columns stagger | ordered process |
| Process | a three-to-five-step sequence | 3 to 5 ordered steps on a shared line | Logo + page type; steps and directional cues reveal in order | non-sequential categories |
| Metrics | one evidence-led conclusion | up to 3 metrics; every metric requires definition, unit, date, and source | Logo + page type; values precede definitions | unverified numbers |
| Image story | one verified image supporting one claim | default: claim occupies 5 columns and approved image occupies 6 columns; when image detail matters, narrow the text column, manually shorten title line length, enlarge the image area, and use `object-fit: contain`; include image source | Logo + page type; image and caption fade after claim | generated, unapproved, decorative imagery, or forced crops that hide the subject |
| Architecture | system relationships | one center plus 4–5 labeled nodes; SVG connectors only | Logo + page type; center, connectors, then outer nodes | a data table |
| Comparison | options judged against shared criteria | 3 option columns plus criteria column; source and date required | Logo + page type; header then rows | unrelated facts without common criteria |
| Roadmap | phases, milestones, or delivery sequence | 3–5 milestones on one horizontal timeline | Logo + page type; line grows left-to-right then milestones reveal | unordered workstreams |

Implement all 10 types using the approved 1920×1080 stage, 12-column grid, `72px` outer margin and `18px` gutter established by `demo/guanyu-6-templates.html`. Keep one standard Chinese-English Logo at upper left, begin the header rule after the Logo safety area, and place the page type at upper right. Use black Logo on white pages and white Logo on black pages. Never use CSS filters to change a Logo asset.

Use `demo/guanyu-6-templates.html` as the reviewed visual implementation reference for these 10 types. It is a template system, not factual source material: replace all `待填`, `XX`, dashes, and image placeholders with verified user-provided content before delivery.

Never infer visual quality from page count alone. After rendering, inspect every page at 1920×1080 and at least one scaled viewport; reject any page with overflow, overlap, weak alignment, missing source text, or an unapproved visual treatment.

## Workflow

1. Establish audience, purpose, source materials, language, page count, and delivery status. Separate verified facts from design references. Never invent metrics, customers, products, quotes, or claims.
2. Verify the required private Logo PNG files exist in `assets/logo/`. If they are missing, stop and ask the user to provide the approved internal files before continuing.
3. Read the relevant brand rules. Read the PPT layout reference when the task is a presentation, PPT conversion, or when the user asks to match the calibrated deck.
4. Build `slides-plan.json` before writing HTML. Give each page one narrative job and one primary claim. Select a GUANYU page family and page type; do not silently invent a new brand pattern.
5. For a new presentation, generate three visual previews within the same GUANYU system: standard brand, technology/data, and narrative/communication. These are layout strategies, not different brands. Record them in `preview-directions.json`, then let the user choose one or a deliberate mix before the full deck.
6. If images exist, create `image-audit.json` before finalizing the outline. Use approved factual images in the plan; rebuild off-brand diagrams and watermarked specification boards as native HTML/SVG when possible.
7. Implement the chosen direction with semantic HTML, CSS custom properties, local approved fonts, approved Logo assets, and plain JavaScript. Prefer a self-contained HTML file for presentations unless multiple files materially improve maintainability.
8. Start from `assets/templates/guanyu-deck-runtime.html` for new fixed-stage presentation decks unless a custom architecture is necessary. Implement the runtime from `references/guanyu-runtime-and-export.md`: edit mode, local save, edited HTML export, overview mode, print/PDF mode, keyboard/click/wheel/touch/hash navigation, and reduced-motion support. Presenter mode is optional.
9. Use the calibrated 12-column grid, 1280x720 coordinate system, common header/footer, and page-type capacity from the references. Keep content within the approved geometry.
10. Handle overflow in this order: shorten copy, restructure, split the page, change page type. For image-text pages, first decide whether the image is decorative, contextual, or evidence. If it is evidence, rebalance the layout before cropping: reduce text measure, introduce intentional title breaks, move the image to a fixed grid-aligned region, and use `object-fit: contain` when the full object must be visible. Never solve overflow by silently shrinking below the minimum type sizes.
11. Run `scripts/qa_html_deck.js` on the HTML deck. Inspect the generated screenshots and `qa-report.html`, not just the JSON. Reject any page with overflow, overlap, clipping, Logo misuse, broken images, unapproved colors, broken navigation, broken print/export/runtime mode, missing reduced-motion support, or text/encoding symptoms.
12. Run the GUANYU quality checklist before delivery. For external handoff, run `scripts/package_deck.py` so the HTML, fonts, Logos, images, and selected planning artifacts travel together. Report the files, chosen page types, assumptions, sources, QA result, package path, and any provisional/planned status or font substitution.

## QA and packaging scripts

- `scripts/qa_html_deck.js`: use Node with Playwright. Required inputs: `--html`. Optional inputs: `--base-url`, `--out-dir`, `--chrome`. It writes `qa-report.json`, `qa-report.html`, and one screenshot per slide. A passing JSON report must have `ok: true`, and the HTML report must be visually reviewed for flagged image/data/table/timeline/architecture pages.
- `scripts/package_deck.py`: use Python. Required inputs: `--html` and `--out-dir`. Optional repeated `--extra` copies planning or source-audit files. It writes `package-manifest.json`; a passing package must have `ok: true`.
- `scripts/create_preview_directions.py`: use Python. Required input: `--out-dir`. Optional `--title`, `--subtitle`, and `--manifest`. It writes three GUANYU-only first-slide previews and a preview manifest.
- `scripts/build_from_doc.py`: use Python. Required inputs: `--input` and `--out-dir`. Optional `--density`, `--direction`, and `--title`. It prepares Word-derived source artifacts and preview files for a later native HTML build.
- `scripts/recommend_page_types.py`: use Python. Inputs can include repeated `--plan`, repeated `--html`, or `--text`. Optional `--out` writes a JSON report. It recommends approved page types and reports standard-type coverage gaps plus unapproved candidate types.

Use the bundled Codex Node/Python runtimes when available. Do not rely on system runtimes if the workspace dependency loader provides local paths.

## PPT to HTML conversion

When a PPTX is provided or exists in the workspace, do not invent replacement copy or create a generic sample deck. Use the conversion path:

1. Extract slide text with `scripts/extract_ppt_text.py`.
2. Extract text-box geometry and basic typography with `scripts/extract_ppt_layout.py`.
3. Preserve source slide order and rendered pages as visual references under `ppt-slides/`.
4. Build a fixed 16:9 HTML stage with keyboard, click, touch, URL-hash navigation, and reduced-motion support.
5. Add optional edit mode with visible HTML text overlays and a side-panel editor. Keep overlays hidden during normal playback so they cannot create duplicate text over the visual reference.
6. Keep extracted JSON beside the HTML output and disclose whether the result is visual-fidelity, hybrid-editable, or fully rebuilt.
7. Do not claim a fully editable conversion until text, images, shapes, charts, and tables have been rebuilt as HTML/SVG elements and checked against rendered source slides.

Use [guanyu-viewport-base.css](references/guanyu-viewport-base.css) as the base for native GUANYU presentations. Keep slide content at 1920x1080, scale the whole stage once, toggle `active`/`visible` for slide state, use `reveal` for staged animation, and keep controls outside the stage.

For the next reconstruction stage, use `scripts/extract_ppt_shapes.py` to inventory non-text shapes, lines, images, tables, charts, geometry, and basic fills/lines. Store the result as `ppt-shapes.json` and use it to prioritize SVG/HTML reconstruction of simple geometry before attempting complex charts or tables.

## Mandatory implementation rules

- Use local `MiSans` for Chinese and `Switzer` for Latin letters, numbers, symbols, and Latin punctuation. Use the approved files in `assets/fonts/`.
- Require the approved internal Logo PNG files in `assets/logo/` before any branded output is generated. Missing Logo files are a blocking condition, not a reason to recreate or download substitutes.
- Use only `Space Black #000000`, `Essential White #FFFFFF`, and `Matrix Silver #8C8C8C` for the UI system unless the brand reference explicitly allows otherwise. Natural image colors may remain inside images but must not become system accent colors.
- Never introduce blue, cyan, orange, rainbow chart palettes, large gradients, neon cyberpunk styling, or decorative slanted separators.
- Use one approved Logo instance per ordinary page unless the page type explicitly permits omission. Never redraw, distort, rotate, recolor, shadow, blur, or recombine the Logo.
- Use the black Logo on light backgrounds and the white Logo on dark or image backgrounds. Do not use EMF/WMF Logo files.
- Use a 12-column grid with consistent margins and alignment. Keep one primary alignment axis and no more than four visible hierarchy levels per page.
- Use information-bearing lines, circles, pills, and arrows only. A pill must carry a short label or process step; it is not decorative UI chrome.
- For data pages, show the conclusion, definition, date, unit, and source. Prefer one main data conclusion per page. Avoid 3D charts and decorative dashboards.
- Include `prefers-reduced-motion: reduce` and keep animations short, purposeful, and subordinate to content.
- Keep all local asset references relative and never expose secrets or private data in client-side code.

## Delivery

Report:

- What was created or changed and the exact file path.
- Whether the output is presentation mode or responsive web mode.
- The selected GUANYU page types or layout direction.
- The facts and visual assets used as sources.
- What was verified and any remaining limitations.

Use [guanyu-brand-rules.md](references/guanyu-brand-rules.md), [guanyu-ppt-layouts.md](references/guanyu-ppt-layouts.md), and [guanyu-quality-checklist.md](references/guanyu-quality-checklist.md) as the only design references.

