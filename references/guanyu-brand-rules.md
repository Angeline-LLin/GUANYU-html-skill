# GUANYU Brand Rules

## Authority

Primary source: `02 VI閹靛鍞?GUANYU VIS Guidelines.pdf`.
Secondary machine-readable source: `PPT閻╃鍙ч弬鍥︽-閺傛壆澧楅弽鈥冲櫙閸擃垱婀?04 PPT濡剝婢?PPT SKILL/GUANYU-PPT-SKILL-鐟欏棜顫庣憴鍕灟閹靛鍞?v1.0.1-閸樺棗褰堕崺铏瑰殠.pdf`.

When a page-level example conflicts with the brand manual, follow the brand manual.

## Palette

- Space Black: `#000000`
- Essential White: `#FFFFFF`
- Matrix Silver: `#8C8C8C`
- Use black or white as the main canvas.
- Use silver and transparent gray only for secondary information, thin rules, axes, reference values, and small material cues.
- Keep gradients local, named, grayscale, and collectively below 8% of page area.
- Do not use blue, cyan, orange, or other generic technology accents in text, charts, shapes, or Logo.

## Typography

- Chinese: MiSans.
- Latin letters, numbers, symbols, and Latin punctuation: Switzer.
- Use the local files in `assets/fonts/` with `@font-face`.
- Suggested presentation roles on a 1280x720 calibration stage:
  - Main title: Chinese 52px equivalent, Latin 55px minimum.
  - Cover title: Chinese 40px, Latin 44px minimum.
  - Page title: Chinese 36px, Latin 40px minimum.
  - Subtitle: Chinese 22px, Latin 24px minimum.
  - Body: Chinese 17px, Latin 18px minimum.
  - Label: Chinese 12px, Latin 13px minimum.
  - Caption: Chinese 10px, Latin 11px minimum.
  - KPI: 54px, with Switzer Bold reserved for large KPI numbers.
- If content does not fit, shorten, split, or change the layout. Do not silently shrink below role minimums.

## Logo

- This public repository intentionally does not include GUANYU logo PNG files.
- Authorized internal users must obtain the approved black and white transparent PNG files from the company's internal brand source and place them in `assets/logo/` before using this skill.
- Required file names: `guanyu-standard-black.png` and `guanyu-standard-white.png`.
- If either required PNG is missing, stop and ask the user to provide the approved internal files. Do not substitute text, SVG, CSS, public web downloads, screenshots, or recreated artwork.
- Prefer the Chinese-English combination Logo.
- Use black on light backgrounds and white on dark or image backgrounds.
- Use one Logo instance on ordinary cover and content pages.
- Never stretch, compress, rotate, redraw, outline, recolor, blur, shadow, or recombine it.
- Do not use EMF or WMF Logo assets.

## Visual language

- High contrast, restrained, precise, and technology-oriented without generic blue technology styling.
- Establish hierarchy with position, whitespace, size, and grayscale before adding lines or fills.
- Use one strong visual when imagery is needed. Keep product, facility, customer, identity, test, and evidence images factual; never regenerate them automatically.
- Use neutral black overlays only when needed to protect text readability over imagery.
- Do not add third-party Logo or reference copy to the output.

## Geometry and grid

- Presentation canvas: 16:9; calibrate at 1280x720.
- Use a 12-column grid, consistent outer margins, and consistent gutters.
- Content page Logo reference position: about x=48, y=48.
- Content starts at approximately y=229; ordinary title begins around y=127.
- Footer source begins around x=48, y=653; page number is right-aligned near x=1172, y=653.
- Content pages use a common header/footer. Covers and section pages may omit them only when the selected page type declares that exception.


## Native HTML slide system

Use a 1920x1080 fixed stage scaled as a whole. Build slide content with native HTML, CSS, SVG, and JavaScript. Use PNG/PDF renders only for visual comparison and QA, never as the primary slide content in the final GUANYU HTML presentation.

