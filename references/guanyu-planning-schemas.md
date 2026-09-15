# GUANYU planning artifact schemas

Use these schemas for non-trivial GUANYU presentation builds. Keep every field factual and source-linked.

## `slides-plan.json`

```json
{
  "source": {
    "document": "path-or-name-of-source-file",
    "text_extract": "doc-text.txt",
    "image_audit": "image-audit.json",
    "preview_directions": "preview-directions.json"
  },
  "mode": "GUANYU Web Presentation",
  "density": "speaker-led",
  "selected_direction": "technology-data",
  "stage": "1920x1080 fixed 16:9",
  "visual_authority": [
    "GUANYU VIS Guidelines",
    "calibrated PPT reference"
  ],
  "slides": [
    {
      "id": "slide-01",
      "type": "cover",
      "theme": "dark",
      "purpose": "Establish the topic.",
      "primary_claim": "Verified claim from source content.",
      "content_source": "Source paragraph, slide, table, or image number.",
      "assets": [],
      "manual_confirmation": false
    }
  ]
}
```

## `image-audit.json`

```json
[
  {
    "id": "image-01",
    "file": "media/image1.png",
    "dimensions": "width x height when known",
    "depicts": "What the image factually shows.",
    "status": "approved | use-with-caveat | reference-only | reject | needs-review",
    "reason": "Why it can or cannot be used.",
    "recommended_slide": "slide-03",
    "replacement_required": "none | replace watermark | replace low resolution | rebuild as HTML/SVG",
    "manual_confirmation": true
  }
]
```

## `preview-directions.json`

```json
{
  "directions": [
    {
      "id": "standard-brand",
      "name": "标准品牌",
      "theme": "light",
      "file": "previews/style-a-standard-brand.html"
    },
    {
      "id": "technology-data",
      "name": "技术 / 数据",
      "theme": "dark",
      "file": "previews/style-b-technology-data.html"
    },
    {
      "id": "narrative-communication",
      "name": "叙事 / 传播",
      "theme": "dark",
      "file": "previews/style-c-narrative-communication.html"
    }
  ],
  "selected_direction": "technology-data",
  "rule": "Use only GUANYU VI. These are layout directions, not alternate brands."
}
```
