"use strict";

const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const { chromium } = require("playwright");

function parseArgs(argv) {
  const args = { html: "", baseUrl: "", outDir: "", chrome: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--html") args.html = argv[++i];
    else if (arg === "--base-url") args.baseUrl = argv[++i];
    else if (arg === "--out-dir") args.outDir = argv[++i];
    else if (arg === "--chrome") args.chrome = argv[++i];
    else if (arg === "--help") {
      console.log("Usage: node scripts/qa_html_deck.js --html demo/deck.html [--base-url http://127.0.0.1:8765] [--out-dir demo/qa]");
      process.exit(0);
    }
  }
  if (!args.html) throw new Error("Missing --html");
  args.html = path.resolve(args.html);
  if (!args.outDir) args.outDir = path.join(path.dirname(args.html), "qa-html-deck");
  args.outDir = path.resolve(args.outDir);
  return args;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function detectTextSymptoms(htmlText) {
  const patterns = [
    { name: "replacement-character", pattern: /�/g },
    { name: "mojibake-candidates", pattern: /(?:瑙傚|鈥|銆|閺|绠|鍦ㄨ|澶)/g },
    { name: "broken-close-tag-candidates", pattern: /\?\/(?:h[1-6]|div|p|span|strong|section)>/g },
  ];
  return patterns.map((item) => {
    const matches = [...htmlText.matchAll(item.pattern)].slice(0, 8).map((m) => m[0]);
    return { name: item.name, count: (htmlText.match(item.pattern) || []).length, samples: matches };
  }).filter((item) => item.count > 0);
}

function writeHtmlReport(report, outDir) {
  const status = report.ok ? "PASS" : "FAIL";
  const rows = report.slideChecks.map((check) => {
    const risk = check.risks?.length ? check.risks.join(", ") : "normal";
    const issues = [
      ...(check.outOfBounds || []).map((item) => `out: ${item.className || item.tag}`),
      ...(check.overlaps || []).map((item) => `overlap: ${item.a} / ${item.b}`),
    ];
    return `<tr>
      <td>${String(check.slide).padStart(2, "0")}</td>
      <td>${escapeHtml(check.label || "")}</td>
      <td>${check.logos}</td>
      <td>${escapeHtml(risk)}</td>
      <td>${issues.length ? escapeHtml(issues.join("; ")) : "OK"}</td>
      <td><img src="slide-${String(check.slide).padStart(2, "0")}.png" alt="Slide ${check.slide} screenshot"></td>
    </tr>`;
  }).join("\n");
  const symptoms = report.textSymptoms.length
    ? report.textSymptoms.map((item) => `<li>${escapeHtml(item.name)}: ${item.count} (${escapeHtml(item.samples.join(", "))})</li>`).join("")
    : "<li>None</li>";
  const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>GUANYU Deck QA Report</title>
  <style>
    body{margin:0;padding:32px;background:#ffffff;color:#000000;font-family:Arial,'Microsoft YaHei',sans-serif}
    h1{font-size:28px;margin:0 0 12px} h2{font-size:18px;margin:28px 0 12px}
    .status{display:inline-block;padding:6px 10px;border:1px solid #000000;font-weight:700}
    table{width:100%;border-collapse:collapse;font-size:13px} th,td{border-top:1px solid #8c8c8c;padding:10px;text-align:left;vertical-align:top}
    img{width:220px;height:auto;border:1px solid #8c8c8c;background:#ffffff}
    code{font-family:Consolas,monospace}
  </style>
</head>
<body>
  <h1>GUANYU Deck QA Report <span class="status">${status}</span></h1>
  <p><code>${escapeHtml(report.html)}</code></p>
  <h2>Summary</h2>
  <ul>
    <li>Slides: ${report.summary.slideCount}</li>
    <li>Broken images: ${report.summary.brokenImages.length}</li>
    <li>Unapproved colors: ${report.summary.unapprovedHexColors.length}</li>
    <li>Reduced motion: ${report.summary.hasReducedMotion ? "yes" : "no"}</li>
    <li>Overview mode: ${report.runtime.hasOverview ? "yes" : "no"}</li>
    <li>Speaker mode: ${report.runtime.hasSpeaker ? "yes" : "no"}</li>
    <li>Overview shortcut: ${report.runtimeInteraction?.overviewOpened ? "yes" : "no"}</li>
    <li>Speaker shortcut: ${report.runtimeInteraction?.speakerOpened ? "yes" : "no"}</li>
    <li>HTML export: ${report.runtime.hasExport ? "yes" : "no"}</li>
    <li>Editable fields: ${report.runtime.editableCount}</li>
  </ul>
  <h2>Text / Encoding Symptoms</h2>
  <ul>${symptoms}</ul>
  <h2>Failures</h2>
  <ul>${report.failures.length ? report.failures.map((item) => `<li>${escapeHtml(item)}</li>`).join("") : "<li>None</li>"}</ul>
  <h2>Slide Screenshots</h2>
  <table><thead><tr><th>#</th><th>Label</th><th>Logo</th><th>Risk</th><th>Issues</th><th>Screenshot</th></tr></thead><tbody>${rows}</tbody></table>
</body>
</html>`;
  fs.writeFileSync(path.join(outDir, "qa-report.html"), html, "utf8");
}

function pageUrl(args, slideNumber) {
  if (args.baseUrl) return `${args.baseUrl.replace(/\/$/, "")}/${path.basename(args.html)}#${slideNumber}`;
  return `${pathToFileURL(args.html).href}#${slideNumber}`;
}

async function main() {
  const args = parseArgs(process.argv);
  fs.mkdirSync(args.outDir, { recursive: true });
  const htmlText = fs.readFileSync(args.html, "utf8");
  const textSymptoms = detectTextSymptoms(htmlText);
  const launchOptions = fs.existsSync(args.chrome) ? { executablePath: args.chrome } : {};
  const browser = await chromium.launch(launchOptions);
  const errors = [];
  const first = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  first.on("pageerror", (err) => errors.push(err.message));
  first.on("requestfailed", (req) => errors.push(`request failed: ${req.url()}`));
  await first.goto(pageUrl(args, 1), { waitUntil: "networkidle" });
  await first.waitForTimeout(1000);

  const summary = await first.evaluate(() => {
    const slides = [...document.querySelectorAll(".slide")];
    return {
      title: document.title,
      slideCount: slides.length,
      activeCount: document.querySelectorAll(".slide.active").length,
      visibleCount: document.querySelectorAll(".slide.visible").length,
      logoCountBySlide: slides.map((slide) => slide.querySelectorAll("img.logo").length),
      logoFilters: [...document.querySelectorAll("img.logo")].map((img) => getComputedStyle(img).filter),
      brokenImages: [...document.images].filter((img) => !img.complete || img.naturalWidth === 0).map((img) => img.getAttribute("src")),
      unapprovedHexColors: [...document.querySelectorAll("style")].flatMap((style) => [...style.textContent.matchAll(/#[0-9a-fA-F]{6}/g)].map((m) => m[0].toLowerCase())).filter((c, i, a) => !["#000000", "#ffffff", "#8c8c8c"].includes(c) && a.indexOf(c) === i),
      hasReducedMotion: [...document.querySelectorAll("style")].some((style) => style.textContent.includes("prefers-reduced-motion")),
    };
  });

  const runtime = await first.evaluate(() => ({
    hasOverview: !!document.querySelector("#overviewOverlay,.overview-overlay,[data-deck-mode='overview']"),
    hasSpeaker: !!document.querySelector("#speakerOverlay,.speaker-overlay,[data-deck-mode='speaker']"),
    hasExport: !!document.querySelector("#exportDeck,[data-action='export-html']"),
    editableCount: document.querySelectorAll("[data-edit-id]").length,
  }));

  const slideChecks = [];
  for (let i = 1; i <= summary.slideCount; i += 1) {
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    page.on("pageerror", (err) => errors.push(err.message));
    page.on("requestfailed", (req) => errors.push(`request failed: ${req.url()}`));
    await page.goto(pageUrl(args, i), { waitUntil: "networkidle" });
    await page.waitForTimeout(1400);
    const check = await page.evaluate((slideNumber) => {
      const stage = document.querySelector("#stage, .deck-stage")?.getBoundingClientRect();
      const slide = document.querySelector(".slide.active");
      if (!stage || !slide) return { slide: slideNumber, missingStageOrSlide: true };
      const targets = [...slide.querySelectorAll("img:not(.logo),.photo,.story-photo,.image-band,.hero-image,.title,.cover-title,.ending h1,.diagram,.timeline,.metrics,.metric-strip,.columns,.steps,.comparison,.architecture,.road,.stack,.layer-map")];
      const outOfBounds = targets.map((el) => {
        const r = el.getBoundingClientRect();
        return {
          tag: el.tagName.toLowerCase(),
          className: typeof el.className === "string" ? el.className : "",
          text: (el.textContent || el.getAttribute("alt") || "").trim().slice(0, 80),
          left: Math.round(r.left - stage.left),
          top: Math.round(r.top - stage.top),
          right: Math.round(r.right - stage.left),
          bottom: Math.round(r.bottom - stage.top),
          out: r.left < stage.left - 1 || r.top < stage.top - 1 || r.right > stage.right + 1 || r.bottom > stage.bottom + 1,
        };
      }).filter((item) => item.out);
      const riskySelectors = [
        ["image", "img:not(.logo),.photo,.story-photo,.image-band,.hero-image"],
        ["data", ".metrics,.metric-strip"],
        ["table-like", ".comparison,.stack,.layer-map,table"],
        ["timeline", ".timeline,.road"],
        ["architecture", ".architecture,.diagram,svg"],
      ];
      const risks = riskySelectors.filter(([, selector]) => slide.querySelector(selector)).map(([name]) => name);
      const boxes = targets.map((el) => {
        const r = el.getBoundingClientRect();
        return { el, name: (el.className || el.tagName || "").toString().slice(0, 50), left: r.left, top: r.top, right: r.right, bottom: r.bottom };
      });
      const overlaps = [];
      for (let a = 0; a < boxes.length; a += 1) {
        for (let b = a + 1; b < boxes.length; b += 1) {
          const A = boxes[a], B = boxes[b];
          if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
          const area = Math.max(0, Math.min(A.right, B.right) - Math.max(A.left, B.left)) * Math.max(0, Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top));
          if (area > 24000 && !A.name.includes("hero-image") && !B.name.includes("hero-image")) overlaps.push({ a: A.name, b: B.name, area: Math.round(area) });
        }
      }
      return {
        slide: slideNumber,
        label: slide.getAttribute("aria-label") || "",
        activeCount: document.querySelectorAll(".slide.active").length,
        visibleCount: document.querySelectorAll(".slide.visible").length,
        logos: slide.querySelectorAll("img.logo").length,
        risks,
        overlaps: overlaps.slice(0, 6),
        outOfBounds,
      };
    }, i);
    await page.screenshot({ path: path.join(args.outDir, `slide-${String(i).padStart(2, "0")}.png`), fullPage: true });
    slideChecks.push(check);
    await page.close();
  }

  await first.keyboard.press("ArrowRight");
  await first.waitForTimeout(100);
  const navigation = await first.evaluate(() => ({ hashAfterArrowRight: location.hash, activeText: document.querySelector(".slide.active .page-foot span:last-child")?.textContent || "" }));

  await first.keyboard.press("KeyO");
  await first.waitForTimeout(100);
  const overviewOpened = await first.evaluate(() => !!document.querySelector("#overviewOverlay.active,.overview-overlay.active,[data-deck-mode='overview'].active"));
  await first.keyboard.press("Escape");
  await first.waitForTimeout(100);
  await first.keyboard.press("KeyS");
  await first.waitForTimeout(100);
  const speakerOpened = await first.evaluate(() => !!document.querySelector("#speakerOverlay.active,.speaker-overlay.active,[data-deck-mode='speaker'].active"));
  await first.keyboard.press("Escape");
  await first.waitForTimeout(100);
  const runtimeInteraction = { overviewOpened, speakerOpened };

  const printPage = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await printPage.goto(pageUrl(args, 1), { waitUntil: "networkidle" });
  await printPage.emulateMedia({ media: "print" });
  const print = await printPage.evaluate(() => ({
    visibleSlides: [...document.querySelectorAll(".slide")].filter((slide) => getComputedStyle(slide).visibility === "visible" && getComputedStyle(slide).opacity === "1").length,
    editorDisplay: getComputedStyle(document.querySelector(".editor-bar"))?.display || "",
  }));

  const viewports = [];
  for (const vp of [{ width: 1920, height: 1080 }, { width: 1440, height: 900 }, { width: 1280, height: 720 }, { width: 768, height: 900 }, { width: 320, height: 700 }]) {
    const page = await browser.newPage({ viewport: vp });
    await page.goto(pageUrl(args, summary.slideCount || 1), { waitUntil: "networkidle" });
    const data = await page.evaluate(() => {
      const stage = document.querySelector("#stage, .deck-stage")?.getBoundingClientRect();
      return {
        docW: document.documentElement.scrollWidth,
        docH: document.documentElement.scrollHeight,
        stageW: Math.round(stage?.width || 0),
        stageH: Math.round(stage?.height || 0),
        activeCount: document.querySelectorAll(".slide.active").length,
      };
    });
    viewports.push({ viewport: `${vp.width}x${vp.height}`, ...data });
    await page.close();
  }

  await browser.close();
  const failures = [];
  if (summary.slideCount < 1) failures.push("No .slide elements found.");
  if (summary.activeCount !== 1 || summary.visibleCount !== 1) failures.push("Initial active/visible state is not exactly one slide.");
  if (summary.logoCountBySlide.some((count) => count !== 1)) failures.push("Every slide must have exactly one logo.");
  if (summary.logoFilters.some((filter) => filter !== "none")) failures.push("Logo CSS filter detected.");
  if (summary.brokenImages.length) failures.push(`Broken images: ${summary.brokenImages.join(", ")}`);
  if (summary.unapprovedHexColors.length) failures.push(`Unapproved hex colors: ${summary.unapprovedHexColors.join(", ")}`);
  if (!summary.hasReducedMotion) failures.push("Missing prefers-reduced-motion.");
  for (const check of slideChecks) {
    if (check.activeCount !== 1 || check.visibleCount !== 1) failures.push(`Slide ${check.slide}: active/visible count is wrong.`);
    if (check.logos !== 1) failures.push(`Slide ${check.slide}: expected one logo.`);
    if (check.outOfBounds?.length) failures.push(`Slide ${check.slide}: ${check.outOfBounds.length} elements out of bounds.`);
  }
  if (navigation.hashAfterArrowRight !== "#2") failures.push("Keyboard navigation did not advance hash to #2.");
  if (print.visibleSlides !== summary.slideCount) failures.push("Print mode does not expose every slide.");
  if (print.editorDisplay !== "none") failures.push("Editor controls are visible in print mode.");
  for (const vp of viewports) {
    const [w, h] = vp.viewport.split("x").map(Number);
    if (vp.docW > w || vp.docH > h) failures.push(`Viewport ${vp.viewport}: document overflows viewport.`);
    if (vp.activeCount !== 1) failures.push(`Viewport ${vp.viewport}: active slide count is wrong.`);
  }

  if (textSymptoms.length) failures.push(`Text/encoding symptoms detected: ${textSymptoms.map((item) => `${item.name}=${item.count}`).join(", ")}`);
  if (!runtime.hasOverview) failures.push("Missing overview mode.");
  if (!runtime.hasExport) failures.push("Missing HTML export action.");
  if (runtime.editableCount < 1) failures.push("No editable fields detected.");
  if (!runtimeInteraction.overviewOpened) failures.push("Overview mode did not open with O key.");
  for (const check of slideChecks) {
    if (check.overlaps?.length) failures.push(`Slide ${check.slide}: possible visual overlap requires screenshot review.`);
  }

  const report = { html: args.html, generatedAt: new Date().toISOString(), summary, runtime, runtimeInteraction, textSymptoms, slideChecks, navigation, print, viewports, errors, failures, ok: failures.length === 0 && errors.length === 0 };
  fs.writeFileSync(path.join(args.outDir, "qa-report.json"), JSON.stringify(report, null, 2), "utf8");
  writeHtmlReport(report, args.outDir);
  console.log(JSON.stringify(report, null, 2));
  if (!report.ok) process.exit(1);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
