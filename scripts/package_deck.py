import argparse
import json
import re
import shutil
from pathlib import Path


SKIP_SCHEMES = ("http:", "https:", "data:", "mailto:", "tel:", "#", "javascript:")


def parse_args():
    parser = argparse.ArgumentParser(description="Package a GUANYU HTML deck with its local assets.")
    parser.add_argument("--html", required=True, help="Path to the deck HTML file.")
    parser.add_argument("--out-dir", required=True, help="Output package directory.")
    parser.add_argument("--extra", action="append", default=[], help="Extra file or directory to copy into the package.")
    return parser.parse_args()


def is_local_ref(value):
    value = value.strip().strip("'\"")
    if not value or value.startswith(SKIP_SCHEMES):
        return False
    if re.fullmatch(r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)?", value):
        return False
    return True


def collect_refs(html_text):
    refs = set()
    patterns = [
        r"""(?:src|href)=["']([^"']+)["']""",
        r"""url\(["']?([^)"']+)["']?\)""",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, html_text, flags=re.IGNORECASE):
            ref = match.group(1).split("#", 1)[0].split("?", 1)[0]
            if is_local_ref(ref):
                refs.add(ref.replace("/", "\\"))
    return sorted(refs)


def copy_path(src, dst):
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    else:
        return False
    return True


def main():
    args = parse_args()
    html = Path(args.html).resolve()
    out_dir = Path(args.out_dir).resolve()
    if not html.is_file():
        raise FileNotFoundError(html)
    out_dir.mkdir(parents=True, exist_ok=True)
    html_text = html.read_text(encoding="utf-8")
    copied = []
    missing = []

    target_html = out_dir / "index.html"
    shutil.copy2(html, target_html)
    copied.append({"source": str(html), "target": str(target_html)})

    for ref in collect_refs(html_text):
        src = (html.parent / ref).resolve()
        try:
            relative = src.relative_to(html.parent)
        except ValueError:
            missing.append({"ref": ref, "reason": "outside deck folder"})
            continue
        target = out_dir / relative
        if copy_path(src, target):
            copied.append({"source": str(src), "target": str(target)})
        else:
            missing.append({"ref": ref, "source": str(src), "reason": "not found"})

    for extra in args.extra:
        src = Path(extra).resolve()
        target = out_dir / src.name
        if copy_path(src, target):
            copied.append({"source": str(src), "target": str(target), "extra": True})
        else:
            missing.append({"ref": extra, "source": str(src), "reason": "not found"})

    manifest = {
        "html": str(html),
        "package": str(out_dir),
        "entry": str(target_html),
        "copied": copied,
        "missing": missing,
        "ok": len(missing) == 0,
    }
    (out_dir / "package-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
