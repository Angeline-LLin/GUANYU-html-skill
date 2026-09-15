import argparse
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare GUANYU deck source artifacts from a Word document.")
    parser.add_argument("--input", required=True, help="Input .doc or .docx file.")
    parser.add_argument("--out-dir", required=True, help="Output source-artifact directory.")
    parser.add_argument("--density", default="speaker-led", choices=["speaker-led", "reading-first"], help="Deck density mode.")
    parser.add_argument("--direction", default="technology-data", choices=["standard-brand", "technology-data", "narrative-communication"], help="Selected GUANYU preview direction.")
    parser.add_argument("--title", default="", help="Optional deck title for previews and plan.")
    return parser.parse_args()


def convert_doc_to_docx(src, out_dir):
    if src.suffix.lower() == ".docx":
      target = out_dir / src.name
      shutil.copy2(src, target)
      return target
    if src.suffix.lower() != ".doc":
      raise ValueError(f"Unsupported input extension: {src.suffix}")
    target = out_dir / f"{src.stem}.docx"
    try:
        import win32com.client  # type: ignore
    except Exception as exc:
        raise RuntimeError("Converting .doc requires Microsoft Word automation and pywin32. Save the file as .docx or run in a Word-enabled Windows environment.") from exc
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = None
    try:
        doc = word.Documents.Open(str(src))
        doc.SaveAs(str(target), FileFormat=16)
    finally:
        if doc is not None:
            doc.Close(False)
        word.Quit()
    return target


def extract_docx_text(docx_path):
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(docx_path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraphs = []
    for p in root.findall(".//w:p", ns):
        parts = [t.text or "" for t in p.findall(".//w:t", ns)]
        text = "".join(parts).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def extract_docx_images(docx_path, media_dir):
    media_dir.mkdir(parents=True, exist_ok=True)
    records = []
    with zipfile.ZipFile(docx_path) as zf:
        names = [name for name in zf.namelist() if name.startswith("word/media/")]
        for index, name in enumerate(names, 1):
            ext = Path(name).suffix.lower()
            if ext not in IMAGE_EXTS:
                continue
            target = media_dir / f"image{index}{ext}"
            target.write_bytes(zf.read(name))
            records.append({"file": f"media/{target.name}", "source_name": name, "extension": ext})
    return records


def create_image_audit(images):
    audit = []
    for i, image in enumerate(images, 1):
        audit.append({
            "id": f"image-{i:02d}",
            "file": image["file"],
            "depicts": "待人工确认",
            "status": "needs-review",
            "reason": "脚本只能提取素材；是否真实、授权、符合 VI、适合哪一页必须由人工或视觉模型确认。",
            "recommended_slide": None,
            "replacement_required": "若有水印、低清晰度、非授权或非品牌图形，正式交付前必须替换或原生重建。",
            "manual_confirmation": True,
        })
    return audit


def create_slide_plan(input_file, docx_file, paragraphs, images, density, direction, title):
    max_points = 3 if density == "speaker-led" else 6
    summary_points = paragraphs[:max_points]
    return {
        "source": {
            "document": str(input_file),
            "converted_docx": docx_file.name,
            "text_extract": "doc-text.txt",
            "image_audit": "image-audit.json",
            "preview_directions": "preview-directions.json",
        },
        "mode": "GUANYU Web Presentation",
        "density": density,
        "selected_direction": direction,
        "stage": "1920x1080 fixed 16:9",
        "visual_authority": [
            "02 VI手册/GUANYU VIS Guidelines.pdf",
            "PPT相关文件-新版校准副本",
        ],
        "deck_title": title or (paragraphs[0] if paragraphs else input_file.stem),
        "content_inventory": {
            "paragraph_count": len(paragraphs),
            "image_count": len(images),
            "first_points": summary_points,
        },
        "slides": [
            {
                "id": "slide-01",
                "type": "cover",
                "theme": "dark",
                "purpose": "建立主题",
                "primary_claim": title or (paragraphs[0] if paragraphs else input_file.stem),
                "content_source": "Word title / first paragraph",
                "assets": [],
                "manual_confirmation": False,
            },
            {
                "id": "slide-02",
                "type": "narrative",
                "theme": "light",
                "purpose": "承接核心定位或问题",
                "primary_claim": paragraphs[1] if len(paragraphs) > 1 else "待从源文档提炼",
                "content_source": "Word paragraphs",
                "assets": [],
                "manual_confirmation": len(paragraphs) <= 1,
            },
        ],
        "next_step": "由 Codex 根据 text/image audit 选择 10 类 GUANYU 标准页面类型并生成 native HTML；不要把源图当作最终主体页面。",
    }


def run_preview_script(script_dir, out_dir, title, subtitle, direction):
    preview_dir = out_dir / "previews"
    manifest = out_dir / "preview-directions.json"
    cmd = [
        sys.executable,
        str(script_dir / "create_preview_directions.py"),
        "--out-dir",
        str(preview_dir),
        "--manifest",
        str(manifest),
    ]
    if title:
        cmd.extend(["--title", title])
    if subtitle:
        cmd.extend(["--subtitle", subtitle])
    subprocess.run(cmd, check=True)
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["selected_direction"] = direction
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    args = parse_args()
    src = Path(args.input).resolve()
    out_dir = Path(args.out_dir).resolve()
    if not src.is_file():
        raise FileNotFoundError(src)
    out_dir.mkdir(parents=True, exist_ok=True)
    docx = convert_doc_to_docx(src, out_dir)
    paragraphs = extract_docx_text(docx)
    images = extract_docx_images(docx, out_dir / "media")
    (out_dir / "doc-text.txt").write_text("\n\n".join(paragraphs), encoding="utf-8")
    (out_dir / "doc-paragraphs.json").write_text(json.dumps([{"index": i + 1, "text": text} for i, text in enumerate(paragraphs)], ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "image-audit.json").write_text(json.dumps(create_image_audit(images), ensure_ascii=False, indent=2), encoding="utf-8")
    title = args.title or (paragraphs[0] if paragraphs else src.stem)
    subtitle = paragraphs[1] if len(paragraphs) > 1 else ""
    run_preview_script(Path(__file__).resolve().parent, out_dir, title, subtitle, args.direction)
    plan = create_slide_plan(src, docx, paragraphs, images, args.density, args.direction, title)
    (out_dir / "slides-plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "input": str(src),
        "out_dir": str(out_dir),
        "docx": str(docx),
        "paragraphs": len(paragraphs),
        "images": len(images),
        "density": args.density,
        "selected_direction": args.direction,
        "ok": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
