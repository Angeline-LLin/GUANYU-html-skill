# GUANYU HTML Builder

为 GUANYU（观宇芯算）创建符合品牌规范的 HTML 演示文稿与响应式网页。

本项目将 GUANYU 的视觉规范、PPT 页面布局和 HTML 演示运行时整合为一个 Codex Skill，适用于品牌介绍、产品页面、数据报告，以及 PPT 到可编辑 HTML 演示文稿的转换。

## 功能

- 创建 GUANYU 品牌 HTML 演示文稿：固定 16:9 画布，支持翻页、概览、打印与 PDF 导出。
- 创建 GUANYU 品牌响应式网页：适用于落地页、产品页和数据页等正常网页场景。
- 将 PPT/PPTX 内容转换为可编辑的 HTML、CSS 与 SVG 页面。
- 提供三种品牌内视觉方向：标准品牌、科技数据、叙事传播。
- 支持键盘、点击、滚轮、触摸和 URL Hash 导航，以及减少动态效果的无障碍偏好。
- 包含视觉预览、页面类型推荐、HTML 质量检查与交付打包脚本。

## 品牌原则

- 仅使用 GUANYU 批准的字体、Logo、颜色和网格系统。
- 默认 UI 色彩仅使用黑 `#000000`、白 `#FFFFFF` 与银灰 `#8C8C8C`。
- 中文使用 MiSans；英文、数字、符号与英文标点使用 Switzer。
- 不使用霓虹、彩虹图表、大面积渐变或通用 AI 风格。
- 不虚构客户、指标、日期、图片来源或业务事实。
- 图片是事实证据时，优先保留完整主体，而不是为版面强行裁切。

详细规范请见 [`references/guanyu-brand-rules.md`](references/guanyu-brand-rules.md)。

## 安装

将仓库克隆到你本机的 Codex Skills 目录，并保持根目录中的 `SKILL.md` 文件不变：

```powershell
git clone https://github.com/Aneline-lin/GUANYU-html-skill.git <你的-Codex-Skills-目录>/guanyu-html-builder
```

重新打开 Codex 后，即可直接描述需求，例如：

```text
用 GUANYU 品牌制作一份 8 页的产品介绍 HTML 演示文稿。
受众是潜在客户，语言为中英双语，内容密度为 speaker-led。
```

> Codex Skills 的安装目录会随安装方式和运行环境而不同；请使用你的实际 Skills 目录替换示例中的路径。

## 使用示例

### 新建 HTML 演示文稿

```text
创建一份 GUANYU 品牌 HTML 演示文稿：
- 主题：XXX
- 受众：XXX
- 页数：8 页
- 语言：中文
- 内容密度：speaker-led
- 已提供素材：产品图、客户案例、数据表
```

### PPT 转 HTML

```text
将这个 PPTX 转为可编辑的 GUANYU HTML 演示文稿。
保留原始页序、文字、数据与图片；输出视觉保真度说明和 QA 结果。
```

### 创建响应式网页

```text
创建一个 GUANYU 品牌响应式产品落地页。
不要使用固定 16:9 演示画布；使用正常网页布局。
```

## 工作流

1. 明确受众、目标、语言、页数、内容密度和素材来源。
2. 选择输出模式：`GUANYU Web Presentation` 或 `GUANYU Responsive Web Page`。
3. 为非简单演示创建页面计划与图片审计。
4. 先生成三种品牌内视觉方向供选择。
5. 用原生 HTML、CSS 与 SVG 实现页面和交互。
6. 运行 QA，检查溢出、对齐、图片、Logo、导航、打印和无障碍动画。
7. 为外部交付打包 HTML、字体、Logo、图片与计划文件。

## 目录结构

```text
.
├── SKILL.md                 # Codex Skill 主指令
├── agents/                  # 子任务与工作流提示
├── assets/                  # Logo、字体、模板等品牌资产
├── demo/                    # 页面类型与实现示例
├── references/              # 品牌规范、布局规范、运行时与 QA 规则
├── scripts/                 # 转换、预览、QA、打包与页面推荐工具
└── third_party/             # 第三方运行时与许可证文件
```

## 常用脚本

```powershell
# 生成三种首页视觉方向
python scripts/create_preview_directions.py --out-dir output

# 从 Word 文档建立演示初始规划文件
python scripts/build_from_doc.py --input source.docx --out-dir output

# 推荐页面类型
python scripts/recommend_page_types.py --text "你的内容"

# 检查 HTML 演示文稿
node scripts/qa_html_deck.js --html output/index.html

# 打包交付文件
python scripts/package_deck.py --html output/index.html --out-dir package
```

## 第三方依赖

本项目包含第三方 `frontend-slides` 运行时参考。复制或分发其重要代码时，请保留原始 MIT 许可证声明。

## 状态与反馈

当前项目是 GUANYU 内部品牌技能与模板库。欢迎通过 Issue 提交问题、改进建议或新增页面类型需求。
