# GUANYU page type selector

Use this reference before rendering a GUANYU presentation. Select page type from content purpose, not from visual preference.

## Standard page types

| Type | Primary signal | Use when | Split when |
| --- | --- | --- | --- |
| `cover` | deck identity | one overall topic, title, date/version, presenter, or client | there are claims, data, or diagrams |
| `section` | chapter break | a new narrative chapter starts | body text exceeds one short phrase |
| `narrative` | one claim | one viewpoint plus one paragraph or 1-3 bullets | there are multiple peer items or a sequence |
| `columns` | peer set | 2-4 comparable capabilities, audiences, benefits, or modules | items are ordered or have dependencies |
| `process` | sequence | 3-5 ordered actions, workflow stages, conversion steps, or operational loops | sequence has dates; use roadmap |
| `metrics` | evidence number | 1-3 numbers with unit, definition, date, and source | more than 3 metrics or no source |
| `image-story` | factual image | one approved product/photo/scene image supports one claim | image is decorative or unapproved |
| `architecture` | relationships | one center/system plus 4-6 nodes, layers, connectors, or dependencies | content is a table or timeline |
| `comparison` | shared criteria | options are compared against the same criteria | rows do not share criteria |
| `roadmap` | time | milestones, years, phases, rollout path, or version plan | items are not chronological |

## Content cues

- Contains years, quarters, phases, `2026`, `2030`, `V1`, `Phase`: prefer `roadmap`.
- Contains numbers with units such as `W`, `GB`, `TB/s`, `PFLOPS`, `%`: prefer `metrics` or `comparison`.
- Contains words like architecture, system, stack, layer, node, connector, deploy: prefer `architecture`.
- Contains workflow verbs such as collect, process, validate, deploy, export: prefer `process`.
- Contains `vs`, compare, option, before/after, solution A/B: prefer `comparison`.
- Contains a single image that must remain complete: prefer `image-story`.
- Contains 2-4 parallel terms separated by commas or bullets: prefer `columns`.
- Contains a strong sentence without evidence objects: prefer `narrative`.

## Currently approved visual coverage

The reviewed `demo/guanyu-6-templates.html` covers these 10 standard page types: `cover`, `section`, `narrative`, `columns`, `process`, `metrics`, `image-story`, `architecture`, `comparison`, `roadmap`.

## Known uncovered candidates

These are not yet approved standard page types. Use existing standard types first. Add a new type only when real source material repeatedly needs it.

- `agenda`: meeting agenda or table of contents. Current workaround: `columns` or `section`.
- `quote`: customer/executive quote. Current workaround: `narrative`.
- `case-study`: problem/action/result story. Current workaround: 2-3 slides using `narrative`, `metrics`, and `image-story`.
- `team-profile`: leadership or team introduction. Current workaround: `columns` with approved portraits.
- `map-coverage`: geography, orbit coverage, service coverage. Current workaround: `image-story` if using a real map image, or `architecture` if using schematic nodes.
- `appendix-source`: dense source notes, glossary, appendix. Current workaround: `comparison` or `metrics` with reduced hierarchy.
- `quote-proof`: quote plus evidence number. Current workaround: split into `narrative` + `metrics`.
- `photo-gallery`: multiple images. Current workaround: split into multiple `image-story` slides.

Do not design these candidates until a real deck needs them and the user approves adding them to the standard system.
