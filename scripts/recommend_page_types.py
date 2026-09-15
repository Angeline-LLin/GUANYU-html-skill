import argparse
import json
import re
from pathlib import Path
from html.parser import HTMLParser


STANDARD_TYPES = {
    "cover": "Deck identity, opening theme, title/version/presenter.",
    "section": "Chapter break or major narrative transition.",
    "narrative": "One claim plus one short supporting explanation.",
    "columns": "Two to four comparable peer items.",
    "process": "Three to five ordered steps or workflow stages.",
    "metrics": "One evidence-led conclusion with one to three sourced metrics.",
    "image-story": "One factual image paired with one claim.",
    "architecture": "System, layers, nodes, connectors, dependencies.",
    "comparison": "Options compared against shared criteria.",
    "roadmap": "Time, milestones, phases, years, rollout path.",
}

ALIASES = {
    "split": "narrative",
    "image-text": "image-story",
    "image story": "image-story",
    "image-narrative": "image-story",
    "product-spec": "metrics",
    "product": "image-story",
    "system-grid": "architecture",
    "software-stack": "architecture",
    "table": "comparison",
    "timeline": "roadmap",
    "closing": "narrative",
    "cover-image": "cover",
    "three-columns": "columns",
}

EXTENDED_CANDIDATES = {
    "agenda": "Agenda / table of contents. Current workaround: columns or section.",
    "quote": "Executive/customer quote. Current workaround: narrative.",
    "case-study": "Problem-action-result story. Current workaround: narrative + metrics + image-story.",
    "team-profile": "Team or leadership intro. Current workaround: columns with approved portraits.",
    "map-coverage": "Geography/orbit/service coverage. Current workaround: image-story or architecture.",
    "appendix-source": "Dense glossary, assumptions, source notes. Current workaround: comparison or metrics.",
    "quote-proof": "Quote plus metric proof. Current workaround: split into narrative + metrics.",
    "photo-gallery": "Multiple approved images. Current workaround: split into image-story slides.",
}


class SlideHtmlParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_slide = False
        self.depth = 0
        self.slides = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "")
        if tag == "section" and "slide" in classes.split():
            self.in_slide = True
            self.depth = 1
            self.current = {"label": attrs.get("aria-label", ""), "classes": classes, "declared_type": attrs.get("data-page-type", ""), "text": "", "imgs": 0, "tables": 0, "svg": 0}
            return
        if self.in_slide:
            if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
                self.depth += 1
            if tag == "img":
                self.current["imgs"] += 1
            if tag == "table":
                self.current["tables"] += 1
            if tag == "svg":
                self.current["svg"] += 1

    def handle_endtag(self, tag):
        if self.in_slide:
            self.depth -= 1
            if self.depth <= 0:
                self.slides.append(self.current)
                self.current = None
                self.in_slide = False

    def handle_data(self, data):
        if self.in_slide and self.current is not None:
            self.current["text"] += " " + data.strip()


def normalize_type(value):
    value = (value or "").strip().lower().replace("_", "-")
    return ALIASES.get(value, value)


def score_text(text, imgs=0, tables=0, svg=0):
    t = text.lower()
    scores = {name: 0 for name in STANDARD_TYPES}
    reasons = {name: [] for name in STANDARD_TYPES}

    def add(name, points, reason):
        scores[name] += points
        reasons[name].append(reason)

    if re.search(r"\b(agenda|contents|目录|议程)\b", t):
        add("columns", 2, "agenda-like content; use columns/section unless agenda is approved")
    if re.search(r"(cover|封面|主题|title)", t):
        add("cover", 2, "title/cover cue")
    if re.search(r"(chapter|section|章节|部分)", t):
        add("section", 2, "section cue")
    if re.search(r"(第一|第二|第三|01|02|03|1\.|2\.|3\.)", text) and len(re.findall(r"(01|02|03|04|05|\d\.)", text)) >= 3:
        add("process", 2, "ordered labels")
    if re.search(r"(20\d{2}|phase|阶段|路线|roadmap|里程碑|计划)", text, re.I):
        add("roadmap", 4, "time/milestone cue")
    if re.search(r"(\d+\s?(w|kw|gb|tb/s|gb/s|pfLOPS|eflops|%|颗|nm)|<\s?\d+|>\s?\d+)", text, re.I):
        add("metrics", 4, "number/unit cue")
    if re.search(r"(架构|系统|stack|layer|node|节点|部署|连接|依赖|平台|orbitinfer)", t):
        add("architecture", 3, "system relationship cue")
    if re.search(r"(compare|comparison|vs|对比|比较|方案|优劣|差异)", t):
        add("comparison", 4, "comparison cue")
    if re.search(r"(流程|步骤|工作流|process|转化|验证|导出|部署)", t):
        add("process", 3, "workflow cue")
    if imgs > 1:
        add("image-story", 2, "image assets present")
    if tables:
        add("comparison", 3, "table element present")
    if svg:
        add("architecture", 2, "svg relationship/diagram element present")
    if len(re.findall(r"[，,、;；]", text)) >= 3:
        add("columns", 1, "parallel-item punctuation")
    if max(scores.values()) == 0:
        add("narrative", 1, "default one-claim page")

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    best, score = ranked[0]
    return {
        "recommended_type": best,
        "score": score,
        "alternatives": [{"type": name, "score": s} for name, s in ranked[1:4] if s > 0],
        "reasons": reasons[best],
    }


def load_plan(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        {
            "id": slide.get("id") or f"slide-{i+1:02d}",
            "declared_type": normalize_type(slide.get("type", "")),
            "text": " ".join(str(slide.get(k, "")) for k in ("purpose", "primary_claim", "content_source")),
        }
        for i, slide in enumerate(data.get("slides", []))
    ]


def load_html(path):
    parser = SlideHtmlParser()
    parser.feed(Path(path).read_text(encoding="utf-8"))
    result = []
    for i, slide in enumerate(parser.slides):
        result.append({
            "id": f"slide-{i+1:02d}",
            "declared_type": normalize_type(slide.get("declared_type", "")),
            "text": f"{slide['label']} {slide['classes']} {slide['text']}",
            "imgs": slide["imgs"],
            "tables": slide["tables"],
            "svg": slide["svg"],
        })
    return result


def parse_args():
    parser = argparse.ArgumentParser(description="Recommend GUANYU page types and report coverage gaps.")
    parser.add_argument("--plan", action="append", default=[], help="slides-plan JSON file. Can repeat.")
    parser.add_argument("--html", action="append", default=[], help="HTML deck/template file. Can repeat.")
    parser.add_argument("--text", default="", help="Raw text to classify.")
    parser.add_argument("--out", default="", help="Optional JSON report path.")
    return parser.parse_args()


def main():
    args = parse_args()
    items = []
    for plan in args.plan:
        for item in load_plan(plan):
            item["source"] = plan
            items.append(item)
    for html in args.html:
        for item in load_html(html):
            item["source"] = html
            items.append(item)
    if args.text:
        items.append({"id": "input-text", "declared_type": "", "text": args.text, "source": "arg:text"})

    recommendations = []
    covered = set()
    declared = set()
    for item in items:
        recommendation = score_text(item["text"], item.get("imgs", 0), item.get("tables", 0), item.get("svg", 0))
        declared_type = normalize_type(item.get("declared_type", ""))
        if declared_type in STANDARD_TYPES:
            declared.add(declared_type)
        covered.add(declared_type if declared_type in STANDARD_TYPES else recommendation["recommended_type"])
        recommendations.append({
            "source": item["source"],
            "id": item["id"],
            "declared_type": declared_type or None,
            **recommendation,
        })

    missing_standard = [name for name in STANDARD_TYPES if name not in covered]
    report = {
        "standard_types": STANDARD_TYPES,
        "declared_coverage": sorted(declared),
        "effective_coverage": sorted(covered),
        "missing_standard_types": missing_standard,
        "unapproved_candidate_types": EXTENDED_CANDIDATES,
        "recommendations": recommendations,
        "ok": True,
    }
    if args.out:
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
