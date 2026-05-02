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
- If the user asks for a listed company, business model, operations, moat, financials, or "经营分析", use the company orange engine and the company-style sketch references.
- If the request is ambiguous, infer from the subject. People/funds usually mean investor holdings; companies usually mean operating analysis.

## Workflow

1. Research current data before writing images. For holdings, prefer SEC 13F, fund websites, WhaleWisdom, Nasdaq/official filings, and clearly record the quarter/date. For companies, prefer annual reports, earnings releases, investor relations, and market data with exact dates.
2. Convert all monetary figures to U.S. dollars before writing image text. Clearly label dollar values as `美元`, `USD`, or `$...`; do not leave revenue, profit, market cap, holdings value, cash, CapEx, dividends, buybacks, or debt in local currency as the main displayed value.
3. Separate stable operating data from dynamic market data. Annual/quarterly revenue, profit, cash flow, CapEx, segment revenue, and management commentary must cite the filing or earnings release date. Stock price, market cap, PE, dividend yield, ranking, and analyst target prices must be re-checked at generation time and carry an exact "as of" date.
4. Create or update a data module in `/Users/jiangming/templates`, named `data_<slug>.py`. Match the relevant schema exactly: investor keys for `investor_infographic.py`, company keys for `company_infographic.py`.
5. Add detailed source metadata to the data module, not just generic labels like "年报" or "彭博". Use `FOOTER_LINES` whenever possible with separate centered lines for:
   - `经营数据：<company annual report / 10-K / annual results / earnings release>，<period/date>`
   - `行情数据：<market-data provider such as StockAnalysis / CompaniesMarketCap / Yahoo Finance / Nasdaq / Wind>，截至 <YYYY-MM-DD>`
   - `汇率口径：<provider or filing rate>，截至 <YYYY-MM-DD>` when any non-USD figures were converted
   - `免责声明：本图仅供学习参考，不构成投资建议`
   - `by 江明`
   If a source is unavailable or only approximate, say so explicitly in the footer rather than hiding it.
6. Put generated images under `/Users/jiangming/持仓分析/<number_or_subject_folder>/`. Use existing naming style when a subject folder already exists.
7. Generate the orange long image from `/Users/jiangming/templates`:

```bash
cd /Users/jiangming/templates
python3 investor_infographic.py data_<slug> "/Users/jiangming/持仓分析/<folder>/<name>_橙色长图.png"
python3 company_infographic.py data_<slug> "/Users/jiangming/持仓分析/<folder>/<slug>_经营分析.png"
```

8. For each hand-drawn image, choose the closest references in `/Users/jiangming/templates/sketch_refs`, create a new HTML file, and screenshot it with headless Chrome. Use the HTML template's real CSS canvas size, not a hard-coded viewport. Many company sketches are portrait canvases such as `900x2020` or `900x1980`; using `1200x750` will crop them.

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --screenshot="/Users/jiangming/持仓分析/<folder>/<name>_手绘_投资之道.png" \
  --window-size=<body_css_width>,<body_css_height> \
  --force-device-scale-factor=3 \
  "file:///Users/jiangming/templates/sketch_refs/<slug>_sketch1.html"
```

9. Verify outputs exist and dimensions are high resolution. Open the images if visual inspection is useful.
10. Before calling any image final, confirm the bottom footer contains a separate centered line exactly reading `by 江明`.
11. Run the image review stage before final delivery. Do not tell the user the images are done until this stage has been completed or any remaining issues have been disclosed.

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
- Match every icon or pictogram to the adjacent metric's actual meaning. Use chart/report icons for revenue, gauge/percent/profit icons for margin, chip/factory icons for production or capacity, and portfolio/table icons for holdings. Avoid generic brain, money-bag, or AI symbols unless the adjacent label is specifically about AI capability, cash, or capital allocation.
- Use U.S. dollars as the default monetary display currency. For non-U.S. companies, convert local-currency filings to USD and add the exchange-rate date or conversion basis in the footnote/data source. Main chart labels should read like `$35.7B USD`, `$357亿美元`, or `约 $357 亿美元`, not `₩52.6万亿` as the primary amount.
- Footers must explain data provenance in enough detail for Jiangming to audit the chart later. Avoid vague source-only lines such as `年报 · 彭博`; prefer `经营数据：Alphabet FY2025 Form 10-K / FY2025 earnings release；行情数据：StockAnalysis + CompaniesMarketCap，截至 2026-04-28；汇率口径：...`.
- Include `by 江明` as its own centered footer line in every final image. Use the exact same font, size, and color as the data-source footnote, and place it below the data-source/footer text rather than inline with it. If the footer clips extra lines, adjust the engine or layout height rather than forcing cramped text.

## Image Review Stage

Every completed image batch must be reviewed before delivery. Treat this as a mandatory QA pass, not an optional polish step.

Review at least these items:

- File structure: expected number of folders and images, correct output root, no accidental mixing of company images with fund/investor images.
- Resolution: orange long images are 2400px wide; hand-drawn images must match the full HTML canvas at high scale, for example 4800x3000 for 1200x750 landscape sketches or 2700x6060 / 2700x5940 for 900px-wide portrait company sketches.
- Text rendering: Chinese fonts render correctly, no tofu boxes/missing glyphs, footer is readable, and the signature line is visible.
- Layout: no obvious overlap, clipping, excessive tilt, cropped footer, off-canvas cards, broken chart bars, or text running outside its container.
- Financial currency: all main monetary figures use USD/美元 by default; local currency appears only in conversion notes or source context.
- Source audit: every final image footer separates operating-data sources from market-data sources; includes filing/earnings period, source/provider names, exact market-data "as of" date, and exchange-rate basis/date when relevant. Reject images whose footer only says generic `年报`, `业绩会`, `彭博`, `公开资料`, or `wind` without date/provider context.
- Dynamic market-data audit: stock price, market cap, PE, ranking, and analyst target prices must be freshly checked against current sources during generation and must not be copied from stale templates.
- Footers: data source is present; non-USD source conversion basis is present when needed; `by 江明` appears as a separate centered bottom line in the same font, size, and color as the footnote.
- Icon semantics: metric icons match their meaning, especially revenue, margin/profit, production/capacity, cash/capital allocation, and holdings.
- Visual consistency: colors, spacing, font hierarchy, and density match the chosen template family and do not look like mixed styles.
- Spot-check visuals: open or render-contact-sheet representative images from the batch, including at least one orange long image and multiple hand-drawn images; inspect the actual pixels, not just file existence.
- Report issues clearly: if any image fails review, fix and regenerate it before final delivery; if a limitation remains, mention it plainly.

## Completion Checklist

- Confirm the data quarter/date in the image text.
- Confirm detailed source provenance is in the footer: operating-data source/date, market-data provider/date, and exchange-rate source/date if used.
- Confirm dynamic market data was freshly verified during the current run and not blindly reused from an older template.
- Confirm all monetary values shown in the image are in USD/美元, with local-currency values omitted or only used as secondary source context.
- Confirm the data source/footer states the exchange-rate date or conversion basis when local-currency data was converted.
- Confirm data source/footer is present.
- Confirm `by 江明` appears as its own centered bottom footer line, with the same style as the data-source footnote.
- Confirm the image review stage was run: file count, resolution, text/font rendering, layout, footer/signature, currency, icon semantics, and representative visual spot-check.
- Confirm the orange image and requested sketch images render without missing fonts/assets.
- If GPT Image 2 was used, confirm generated assets are visually helpful and did not introduce inaccurate text or unsupported financial claims.
- Confirm output paths are under `/Users/jiangming/持仓分析`.
- Tell the user exactly where the images were saved.
