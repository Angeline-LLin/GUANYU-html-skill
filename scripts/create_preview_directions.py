import argparse
import html
import json
from pathlib import Path


DIRECTIONS = [
    {
        "id": "standard-brand",
        "file": "style-a-standard-brand.html",
        "name": "标准品牌",
        "theme": "light",
        "label": "STANDARD BRAND",
        "title": "以秩序和留白建立可信度。",
        "body": "适合正式汇报、公司介绍、投资人或客户材料。强调黑白关系、稳定网格、低装饰密度。",
    },
    {
        "id": "technology-data",
        "file": "style-b-technology-data.html",
        "name": "技术 / 数据",
        "theme": "dark",
        "label": "TECHNOLOGY / DATA",
        "title": "用结构线和指标关系解释系统能力。",
        "body": "适合芯片、架构、路线图、性能指标与研发进展。强调证据、节点、表格和原生 SVG 结构。",
    },
    {
        "id": "narrative-communication",
        "file": "style-c-narrative-communication.html",
        "name": "叙事 / 传播",
        "theme": "dark",
        "label": "NARRATIVE / COMMUNICATION",
        "title": "让一个核心判断成为页面主角。",
        "body": "适合发布会、对外传播、路演开场。强调大标题、真实图片位置和清晰叙事节奏。",
    },
]


REQUIRED_LOGOS = (
    Path(__file__).resolve().parents[1] / "assets" / "logo" / "guanyu-standard-black.png",
    Path(__file__).resolve().parents[1] / "assets" / "logo" / "guanyu-standard-white.png",
)


def parse_args():
    parser = argparse.ArgumentParser(description="Create three GUANYU-only first-slide visual previews.")
    parser.add_argument("--out-dir", required=True, help="Directory for preview HTML files.")
    parser.add_argument("--title", default="", help="Optional real deck title to use in previews.")
    parser.add_argument("--subtitle", default="", help="Optional supporting line.")
    parser.add_argument("--manifest", default="", help="Optional preview-directions JSON path.")
    return parser.parse_args()


def render_preview(direction, title, subtitle):
    is_dark = direction["theme"] == "dark"
    bg = "#000000" if is_dark else "#ffffff"
    fg = "#ffffff" if is_dark else "#000000"
    logo = "guanyu-standard-white.png" if is_dark else "guanyu-standard-black.png"
    title_text = title or direction["title"]
    body_text = subtitle or direction["body"]
    structural = ""
    if direction["id"] == "technology-data":
        structural = """
        <svg class="diagram" viewBox="0 0 620 360" aria-hidden="true">
          <line x1="310" y1="70" x2="140" y2="260"/><line x1="310" y1="70" x2="310" y2="260"/><line x1="310" y1="70" x2="480" y2="260"/>
          <circle cx="310" cy="70" r="54"/><circle cx="140" cy="260" r="42"/><circle cx="310" cy="260" r="42"/><circle cx="480" cy="260" r="42"/>
        </svg>"""
    elif direction["id"] == "narrative-communication":
        structural = '<div class="image-slot">真实图片 / 来源待填</div>'
    else:
        structural = '<div class="rules"><span></span><span></span><span></span></div>'
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GUANYU {html.escape(direction["name"])} preview</title>
  <style>
    @font-face{{font-family:MiSans;src:url('../assets/fonts/MiSans-Regular.otf');font-weight:400}}
    @font-face{{font-family:MiSans;src:url('../assets/fonts/MiSans-Semibold.otf');font-weight:600}}
    @font-face{{font-family:Switzer;src:url('../assets/fonts/Switzer-Medium.otf');font-weight:500}}
    :root{{--black:#000000;--white:#ffffff;--silver:#8c8c8c;--ease:cubic-bezier(.16,1,.3,1)}}
    *{{box-sizing:border-box}} html,body{{width:100%;height:100%;margin:0;overflow:hidden;background:#000000}}
    .stage{{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform:translate(-50%,-50%) scale(var(--scale,1));transform-origin:center;background:{bg};color:{fg};font-family:MiSans,sans-serif;padding:72px;overflow:hidden}}
    .frame{{position:absolute;inset:32px;border:1px solid {"rgba(255,255,255,.16)" if is_dark else "rgba(0,0,0,.12)"}}}
    .logo{{position:absolute;left:72px;top:60px;width:108px;height:44px;object-fit:contain;object-position:left center}}
    .head{{position:absolute;left:234px;right:72px;top:72px;display:grid;grid-template-columns:1fr auto;align-items:center;color:#8c8c8c;font:500 15px/1 Switzer,sans-serif;text-transform:uppercase}} .head:before{{content:"";height:1px;background:currentColor}}
    .eyebrow{{margin-top:160px;color:#8c8c8c;font:500 18px/1 Switzer,sans-serif;text-transform:uppercase}}
    h1{{width:1180px;margin:30px 0 0;font:600 112px/1.05 MiSans,sans-serif;letter-spacing:0}}
    p{{width:720px;margin:42px 0 0;color:#8c8c8c;font:400 26px/1.55 MiSans,sans-serif}}
    .visual{{position:absolute;right:72px;bottom:120px;width:620px;height:360px}}
    .rules{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;height:100%;align-items:end}} .rules span{{display:block;border-top:2px solid currentColor;height:88px}}
    .diagram{{width:100%;height:100%;stroke:currentColor;fill:none;stroke-width:2}} .diagram circle{{fill:{bg}}}
    .image-slot{{width:100%;height:100%;border:1px solid #8c8c8c;display:flex;align-items:center;justify-content:center;color:#8c8c8c;font:500 22px/1 MiSans,sans-serif}}
    .foot{{position:absolute;left:72px;right:72px;bottom:52px;display:flex;justify-content:space-between;color:#8c8c8c;font:500 14px/1 Switzer,sans-serif}}
    .reveal{{opacity:0;transform:translateY(24px);animation:in .7s var(--ease) forwards}} .reveal:nth-child(2){{animation-delay:.08s}} .reveal:nth-child(3){{animation-delay:.16s}} @keyframes in{{to{{opacity:1;transform:none}}}}
    @media (prefers-reduced-motion:reduce){{.reveal{{animation:none;opacity:1;transform:none}}}}
  </style>
</head>
<body>
  <main class="stage" id="stage">
    <div class="frame"></div><img class="logo" src="../assets/logo/{logo}" alt="观宇芯算 GUANYU"><div class="head"><span>{html.escape(direction["label"])}</span></div>
    <div class="eyebrow reveal">GUANYU / VISUAL DIRECTION</div><h1 class="reveal">{html.escape(title_text)}</h1><p class="reveal">{html.escape(body_text)}</p><div class="visual reveal">{structural}</div>
    <div class="foot"><span>GUANYU / PREVIEW</span><span>01 / 01</span></div>
  </main>
  <script>function scale(){{document.querySelector('#stage').style.setProperty('--scale',Math.min(innerWidth/1920,innerHeight/1080));}}addEventListener('resize',scale);scale();</script>
</body>
</html>"""


def main():
    args = parse_args()
    missing_logos = [str(path) for path in REQUIRED_LOGOS if not path.is_file()]
    if missing_logos:
        raise SystemExit(
            "Missing required internal GUANYU logo PNG files. "
            "Place guanyu-standard-black.png and guanyu-standard-white.png in assets/logo/ before generating previews. "
            f"Missing: {', '.join(missing_logos)}"
        )
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for direction in DIRECTIONS:
        target = out_dir / direction["file"]
        target.write_text(render_preview(direction, args.title, args.subtitle), encoding="utf-8")
        records.append({k: direction[k] for k in ("id", "name", "theme", "file")})
    manifest = {
        "directions": records,
        "selected_direction": None,
        "rule": "Use only GUANYU VI. These are layout directions, not alternate brands.",
    }
    manifest_path = Path(args.manifest).resolve() if args.manifest else out_dir / "preview-directions.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"out_dir": str(out_dir), "manifest": str(manifest_path), "count": len(records), "ok": True}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
