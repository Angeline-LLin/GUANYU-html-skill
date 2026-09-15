from pathlib import Path
import json
from pptx import Presentation

root = Path(__file__).resolve().parents[2]
candidates = []
for path in root.rglob('*.pptx'):
    if path.name.startswith('~'):
        continue
    try:
        deck = Presentation(str(path))
        if len(deck.slides) == 27:
            candidates.append((len(path.parts), path, deck))
    except Exception:
        pass
_, source, prs = max(candidates, key=lambda item: item[0])
sw, sh = prs.slide_width, prs.slide_height
slides = []
for index, slide in enumerate(prs.slides, 1):
    items = []
    for shape_index, shape in enumerate(slide.shapes):
        if not hasattr(shape, 'text') or not shape.text.strip():
            continue
        paragraph = shape.text_frame.paragraphs[0] if shape.text_frame.paragraphs else None
        run = paragraph.runs[0] if paragraph and paragraph.runs else None
        font = run.font if run else None
        color = '#000000'
        try:
            if font and font.color and font.color.type and font.color.rgb:
                color = '#' + str(font.color.rgb)
        except Exception:
            pass
        size = round((font.size.pt if font and font.size else 14) * 1280 / 96, 1)
        items.append({'id': f'{index}-{shape_index}', 'text': ' '.join(x.strip() for x in shape.text.splitlines() if x.strip()), 'x': round(shape.left / sw * 1280, 1), 'y': round(shape.top / sh * 720, 1), 'w': round(shape.width / sw * 1280, 1), 'h': round(shape.height / sh * 720, 1), 'font': font.name if font and font.name else 'MiSans', 'size': size, 'color': color})
    slides.append({'slide': index, 'items': items})
(root / 'guanyu-html-builder' / 'demo' / 'ppt-layout.json').write_text(json.dumps({'source': str(source), 'slides': slides}, ensure_ascii=False, indent=2), encoding='utf-8')
print('extracted', len(slides), 'slides')
