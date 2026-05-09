---
name: investor-infographic
description: Generate Chinese investor/fund holding-analysis infographics and company operating-analysis infographics using Jiangming's local templates, with optional GPT Image 2 visual asset generation. Use when the user asks for 持仓图, 持仓分析, 投资人/基金经理/基金持仓图片, 13F持仓长图, 手绘信息图, 公司经营全解析, 经营分析图, GPT Image 2 增强, or asks to reuse the orange/hand-drawn templates in ~/templates.
---

# Investor Infographic

Use Jiangming's existing local template system to produce polished Chinese financial-analysis images. The original Claude/Hermes skill is at `/Users/jiangming/.hermes/skills/finance/investor-infographic`; this Codex skill should use the live code in `/Users/jiangming/templates`.

## Quick Paths

- Template root: `/Users/jiangming/templates`
- Output root: `/Users/jiangming/持仓分析`
- Investor orange engine: `/Users/jiangming/templates/investor_infographic.py`
- Company orange engine: `/Users/jiangming/templates/company_infographic.py`
- Investor data template: `/Users/jiangming/templates/data_template.py`
- Existing data modules: `/Users/jiangming/templates/data_*.py`
- Hand-drawn HTML references: `/Users/jiangming/templates/sketch_refs/*_sketch1.html` and `*_sketch2.html`
- Detailed local map: `references/template-system.md`
- GPT Image 2 layer: `references/gpt-image-2-layer.md`
- GPT Image helper script: `scripts/generate_gpt_image.py`

## Decide The Mode

- If the user asks for an investor, fund, fund manager, 13F, portfolio, or "持仓" image, create the investor set: one orange long image plus two hand-drawn landscape images.
- If the user asks for a listed company, business model, operations, moat, financials, or "经营分析", create the company set: one orange operating-analysis image plus three company-style hand-drawn images. The fourth image must cover the company's distinctive management culture / operating culture.
- If the request is ambiguous, infer from the subject. People/funds usually mean investor holdings; companies usually mean operating analysis.

## Workflow

1. Research current data before writing images. For holdings, prefer SEC 13F, fund websites, WhaleWisdom, Nasdaq/official filings, and clearly record the quarter/date. For companies, prefer annual reports, earnings releases, investor relations, and market data with exact dates.
2. Convert all monetary figures to U.S. dollars before writing image text. Clearly label dollar values as `美元`, `USD`, or `$...`; do not leave revenue, profit, market cap, holdings value, cash, CapEx, dividends, buybacks, or debt in local currency as the main displayed value.
3. Separate stable operating data from dynamic market data. Annual/quarterly revenue, profit, cash flow, CapEx, segment revenue, full-year ROI/ROIC, and management commentary must cite the filing or earnings release date. Stock price, market cap, PE, dividend yield, ranking, and analyst target prices must be re-checked at generation time and carry an exact "as of" date.
4. For company operating-analysis images, include a full-year `ROI/投资回报率` profitability metric by default. Prefer the company-level ROIC-style口径: `NOPAT / average invested capital`, where invested capital is `total debt + total equity - cash and equivalents`, averaged across beginning/end fiscal-year balance sheets. If NOPAT is not available, use `net income / average invested capital` and label it `ROI（净利润口径）`. Do not confuse this with stock-price total return. If reliable invested-capital inputs are unavailable, show `ROI口径：资料不足/不可比` rather than inventing a number; ROE/ROA may be shown as secondary context only when clearly labeled.
   Also include a `2026 CapEx/资本开支` item by default in company operating-analysis or operating-panorama images. Use company guidance, annual-report capex plans, earnings-call commentary, or credible analyst/market-data estimates with an exact date. If a company does not disclose a reliable 2026 CapEx figure, write `2026 CapEx：未披露/不可比` or a clearly labeled directional note instead of inventing a number.
5. For company sets, add a dedicated fourth image about `经营管理文化 / 企业文化`. Research and show the company's distinctive hiring and management practices, such as compensation/talent density, engineering bar, technical interview or recruiting requirements, founder/leadership principles, decision-making mechanisms, performance management, internal mobility, research culture, manufacturing discipline, customer obsession, compliance/safety culture, or other company-specific operating norms. Use concrete evidence and avoid generic slogans like `重视创新` unless tied to a specific policy, quote, or source.
6. Create or update a data module in `/Users/jiangming/templates`, named `data_<slug>.py`. Match the relevant schema exactly: investor keys for `investor_infographic.py`, company keys for `company_infographic.py`.
7. Add detailed source metadata to the data module, not just generic labels like "年报" or "彭博". Use `FOOTER_LINES` whenever possible with separate centered lines for:
   - `经营数据：<company annual report / 10-K / annual results / earnings release>，<period/date>`
   - `ROI口径：<NOPAT or net income> / <average invested capital formula and fiscal year>，数据来自 <filing/source/date>` when a company ROI/ROIC metric is shown
   - `管理文化：<company careers / annual report / founder letter / official blog / employee handbook / credible compensation or recruiting source>，截至 <YYYY-MM-DD>` when a company culture image is included
   - `行情数据：<market-data provider such as StockAnalysis / CompaniesMarketCap / Yahoo Finance / Nasdaq / Wind>，截至 <YYYY-MM-DD>`
   - `汇率口径：<provider or filing rate>，截至 <YYYY-MM-DD>` when any non-USD figures were converted
   - `免责声明：本图仅供学习参考，不构成投资建议`
   - `by 江明`
   If a source is unavailable or only approximate, say so explicitly in the footer rather than hiding it.
8. Put generated images under `/Users/jiangming/持仓分析/<number_or_subject_folder>/`. Use existing naming style when a subject folder already exists.
9. Generate the orange long image from `/Users/jiangming/templates`:

```bash
cd /Users/jiangming/templates
python3 investor_infographic.py data_<slug> "/Users/jiangming/持仓分析/<folder>/<name>_橙色长图.png"
python3 company_infographic.py data_<slug> "/Users/jiangming/持仓分析/<folder>/<slug>_经营分析.png"
```

10. For each hand-drawn image, choose the closest references in `/Users/jiangming/templates/sketch_refs`, create a new HTML file, and screenshot it with headless Chrome. Use the HTML template's real CSS canvas size, not a hard-coded viewport. Many company sketches are portrait canvases such as `900x2020` or `900x1980`; using `1200x750` will crop them.

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --screenshot="/Users/jiangming/持仓分析/<folder>/<name>_手绘_投资之道.png" \
  --window-size=<body_css_width>,<body_css_height> \
  --force-device-scale-factor=3 \
  "file:///Users/jiangming/templates/sketch_refs/<slug>_sketch1.html"
```

11. Verify outputs exist and dimensions are high resolution. Open the images if visual inspection is useful.
12. Before calling any image final, confirm the bottom footer contains a separate centered line exactly reading `by 江明`.
13. Run the image review stage before final delivery. Do not tell the user the images are done until this stage has been completed or any remaining issues have been disclosed.

## Optional GPT Image 2 Layer

Use GPT Image 2 as an optional visual-asset layer, not as the main chart renderer. Keep all data tables, Chinese labels, charts, and final infographic composition in Pillow or HTML/SVG/Chrome, because generated image models can still be imprecise with text placement and layout.

Good uses:

- Generate a hand-drawn portrait, symbolic background, paper texture, scene, or cover-style visual for a sketch.
- Edit an existing sketch visual for mood, color, or illustration richness.
- Produce alternative visual directions before rebuilding the final version in HTML/SVG.

Avoid:

- Asking GPT Image 2 to render final holdings tables, small Chinese text, exact percentages, or complex chart layouts.
- Transparent-background cutouts with `gpt-image-2`; use opaque assets or another model/workflow when transparency is required.

Read `references/gpt-image-2-layer.md` before using the API helper.

## Style Rules

- Orange long image: warm orange system, `#E8883A` as the main accent, generated by Pillow at `SCALE=3` and 2400px width.
- Hand-drawn images: capture the HTML's actual CSS canvas. Landscape sketches may be 1200x750 at 4x; company portrait sketches are often 900x2020 or 900x1980 and should be captured at 3x or higher so the full page and footer are visible.
- Hand-drawn background: light paper `#F7F4ED` with subtle grid lines, inline SVG doodles, rounded hand-drawn strokes, and no stock-looking art.
- Keep information density high but readable: key numbers, top holdings/business segments, distribution chart, changes/actions, philosophy/moat, quotes, and a clear bottom insight.
- Keep colors disciplined: no more than three dominant colors per image unless the existing reference uses a broader palette intentionally.
- When updating existing company hand-drawn templates, treat the old company-specific visual style as the base contract. Preserve the company's palette, logo-like mark, doodle icons, hand-drawn motifs, title hierarchy, and overall layout unless the user explicitly asks for a redesign. New requirements such as ROI/ROIC, 2026 CapEx, source-footers, or management-culture notes should be added as patches to the existing style, not by replacing every company with a unified generic template.
- In company hand-drawn sets, keep `经营之道` and `经营全景` distinct. `经营之道` should explain why the business can compound: moat, flywheel, customer lock-in, technology route, strategic moves, and business logic. `经营全景` should be the data dashboard: revenue/profit, segment mix, ROI/ROIC, 2026 CapEx, risks, and capital allocation. Avoid copying the same metric cards and paragraphs across both images.
- Match every icon or pictogram to the adjacent metric's actual meaning. Use chart/report icons for revenue, gauge/percent/profit icons for margin, chip/factory icons for production or capacity, and portfolio/table icons for holdings. Avoid generic brain, money-bag, or AI symbols unless the adjacent label is specifically about AI capability, cash, or capital allocation.
- Use U.S. dollars as the default monetary display currency. For non-U.S. companies, convert local-currency filings to USD and add the exchange-rate date or conversion basis in the footnote/data source. Main chart labels should read like `$35.7B USD`, `$357亿美元`, or `约 $357 亿美元`, not `₩52.6万亿` as the primary amount.
- Footers must explain data provenance in enough detail for Jiangming to audit the chart later. Avoid vague source-only lines such as `年报 · 彭博`; prefer `经营数据：Alphabet FY2025 Form 10-K / FY2025 earnings release；行情数据：StockAnalysis + CompaniesMarketCap，截至 2026-04-28；汇率口径：...`.
- Company operating-analysis images should reserve one key profitability slot for full-year `ROI/投资回报率` or `ROIC/投资资本回报率`. Label the formula口径 near the metric or in the footer. Use a return/gauge/loop icon for ROI/ROIC, not a cash, revenue, or generic AI icon.
- Company sets should include a fourth image titled around `管理文化`, `经营文化`, `组织文化`, or `人才文化`. This image should explain what makes the company unusual as an organization: hiring bar, compensation/talent density, technical standards, management mechanisms, founder principles, engineering culture, manufacturing discipline, or other company-specific practices. Prefer concrete policies, numbers, and quotes over vague adjectives.
- Include `by 江明` as its own centered footer line in every final image. Use the exact same font, size, and color as the data-source footnote, and place it below the data-source/footer text rather than inline with it. If the footer clips extra lines, adjust the engine or layout height rather than forcing cramped text.

## Image Review Stage

Every completed image batch must be reviewed before delivery. Treat this as a mandatory QA pass, not an optional polish step.

Review at least these items:

- File structure: expected number of folders and images, correct output root, no accidental mixing of company images with fund/investor images.
- Company set count: company operating-analysis requests should normally produce 4 images: the orange operating-analysis image, two business/strategy hand-drawn images, and one management-culture hand-drawn image. If the user asks for fewer or more, follow the request and note the deviation.
- Resolution: orange long images are 2400px wide; hand-drawn images must match the full HTML canvas at high scale, for example 4800x3000 for 1200x750 landscape sketches or 2700x6060 / 2700x5940 for 900px-wide portrait company sketches.
- Text rendering: Chinese fonts render correctly, no tofu boxes/missing glyphs, footer is readable, and the signature line is visible.
- Layout: no obvious overlap, clipping, excessive tilt, cropped footer, off-canvas cards, broken chart bars, or text running outside its container.
- Financial currency: all main monetary figures use USD/美元 by default; local currency appears only in conversion notes or source context.
- Company ROI audit: company operating-analysis images include a full-year ROI/ROIC metric when inputs are available; the formula is labeled; numerator and denominator come from the cited annual filing or earnings release; the metric is not confused with stock-price return, ROE, ROA, or margin.
- 2026 CapEx audit: company operating-analysis or operating-panorama images include a 2026 CapEx item when relevant; the source/date or `未披露/不可比` limitation is visible; local-currency amounts are converted to USD/美元.
- Company sketch separation audit: `经营之道` is business logic/moat/flywheel; `经营全景` is financial dashboard/ROI/2026 CapEx/risk. Reject batches where the two images mostly repeat the same cards or paragraphs.
- Management-culture audit: the dedicated company culture image cites concrete sources for hiring, compensation, technical bar, management mechanisms, founder principles, or operating norms. Reject generic culture claims that could apply to any company, such as `创新文化`, `人才优秀`, or `重视技术`, unless backed by a specific policy, quote, number, or documented practice.
- Source audit: every final image footer separates operating-data sources from market-data sources; includes filing/earnings period, source/provider names, exact market-data "as of" date, and exchange-rate basis/date when relevant. Reject images whose footer only says generic `年报`, `业绩会`, `彭博`, `公开资料`, or `wind` without date/provider context.
- Dynamic market-data audit: stock price, market cap, PE, ranking, and analyst target prices must be freshly checked against current sources during generation and must not be copied from stale templates.
- Footers: data source is present; non-USD source conversion basis is present when needed; `by 江明` appears as a separate centered bottom line in the same font, size, and color as the footnote.
- Icon semantics: metric icons match their meaning, especially revenue, margin/profit, production/capacity, cash/capital allocation, and holdings.
- Existing-style regression: when regenerating an existing company set, compare representative outputs against the previous/reference HTML style and confirm company-specific colors and icons were preserved. Flag any accidental shift to a single shared palette or loss of meaningful icons before delivery.
- Visual consistency: colors, spacing, font hierarchy, and density match the chosen template family and do not look like mixed styles.
- Spot-check visuals: open or render-contact-sheet representative images from the batch, including at least one orange long image and multiple hand-drawn images; inspect the actual pixels, not just file existence.
- Report issues clearly: if any image fails review, fix and regenerate it before final delivery; if a limitation remains, mention it plainly.

## Completion Checklist

- Confirm the data quarter/date in the image text.
- Confirm company sets include the fourth management-culture image unless the user explicitly requested a different count.
- Confirm detailed source provenance is in the footer: operating-data source/date, market-data provider/date, and exchange-rate source/date if used.
- Confirm dynamic market data was freshly verified during the current run and not blindly reused from an older template.
- Confirm company operating-analysis images include full-year ROI/ROIC when reliable inputs exist; confirm the ROI formula, fiscal year, and source are stated; if omitted, confirm the image or footer explicitly says why the ROI口径 is unavailable or not comparable.
- Confirm company operating-analysis or `经营全景` images include 2026 CapEx when relevant; if omitted, confirm the image or footer explicitly says `未披露/不可比` or explains the limitation.
- Confirm company hand-drawn `经营之道` and `经营全景` images have different jobs: one explains business logic/moat/flywheel; the other explains financial dashboard/ROI/2026 CapEx/risk.
- Confirm the management-culture image uses concrete, company-specific evidence and cites sources for claims about compensation, hiring bar, engineering standards, management mechanisms, or culture.
- Confirm all monetary values shown in the image are in USD/美元, with local-currency values omitted or only used as secondary source context.
- Confirm the data source/footer states the exchange-rate date or conversion basis when local-currency data was converted.
- Confirm data source/footer is present.
- Confirm `by 江明` appears as its own centered bottom footer line, with the same style as the data-source footnote.
- Confirm the image review stage was run: file count, resolution, text/font rendering, layout, footer/signature, currency, icon semantics, and representative visual spot-check.
- Confirm the orange image and requested sketch images render without missing fonts/assets.
- If GPT Image 2 was used, confirm generated assets are visually helpful and did not introduce inaccurate text or unsupported financial claims.
- Confirm output paths are under `/Users/jiangming/持仓分析`.
- Tell the user exactly where the images were saved.
