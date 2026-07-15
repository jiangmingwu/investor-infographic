# Local Template System

## What Exists

- `/Users/jiangming/templates/investor_infographic.py` creates the orange investor/fund holding-analysis long image.
- `/Users/jiangming/templates/company_infographic.py` is the legacy orange company operating-analysis renderer and is opt-in for current work.
- `/Users/jiangming/templates/company_visual_standard_v2.py` contains the current shared `经营之道` and `经营全景` visual contract.
- `/Users/jiangming/templates/company_logo_assets.py` validates registered official Logo assets and hashes.
- `/Users/jiangming/templates/data_template.py` is the investor/fund data skeleton.
- `/Users/jiangming/templates/data_*.py` contains the live investor and company data modules.
- `/Users/jiangming/templates/data/market_history/` contains audited company-profile price snapshots.
- `/Users/jiangming/templates/assets/company_logos/` contains official Logo source assets and visibility-normalized derivatives.
- `/Users/jiangming/templates/sketch_refs/` contains the live hand-drawn HTML/CSS references.
- `/Users/jiangming/持仓分析/` contains previous finished images and should be the default output root.
- The GitHub mirror mentioned by the user is `https://github.com/jiangmingwu/investor-infographic`, but the local `/Users/jiangming/templates` copy is the active working source unless the user asks to sync from GitHub.

## Investor Data Schema

Use `/Users/jiangming/templates/data_template.py` as the live source of truth. Required shape:

- `TITLE`, `SUBTITLE`, `UPDATE_DATE`
- `BASIC_INFO`: ordered key/value map for person and firm profile
- `PORTFOLIO_SUMMARY`: ordered key/value map for total market value, position count, concentration, largest holding, cash if useful
- `HOLDINGS_LABEL`
- `TOP_HOLDINGS`: tuples `(rank, company_name, ticker, percent, market_value, shares, sector)`
- `SECTOR_DISTRIBUTION`: tuples `(sector, percent)`
- `CHANGES_LABEL`
- `RECENT_CHANGES`: tuples `(action, target, detail, color)` using `GREEN`, `RED`, or `ORANGE`
- `INVESTMENT_PHILOSOPHY`: tuples `(title, description)`
- `KEY_METRICS`: tuples `(metric, value)`
- `FAMOUS_QUOTES`: list of short quotes
- `DATA_SOURCE` or `FOOTER_LINES`

Investor command:

```bash
cd /Users/jiangming/templates
python3 investor_infographic.py data_<slug> "/Users/jiangming/持仓分析/<folder>/<name>_橙色长图.png"
```

## Current Company Four-Page Contract

Listed-company work defaults to four hand-drawn pages from one approved company packet and one company-specific visual configuration:

1. `公司档案`: eight required identity fields, business scope, a hand-drawn `上市以来股价走势`, industry position, and milestones.
2. `经营之道`: long-term positioning, 3-5 real core drivers, hard evidence plus industry meaning, recent actions, and a verified quote when useful.
3. `经营全景`: the fixed six-card financial/valuation snapshot, segment mix, ROI/ROIC, 2026 CapEx, shareholder return, highlights/risks, and important institutions/shareholders.
4. `管理文化`: 1-3 documented people/organization principles, each with a practice and a case or number.

The company-profile stock chart sits immediately after `业务范围`. It uses split-adjusted closing prices, excludes cash-dividend reinvestment, displays USD, and states the security, period, provider, retrieval date, and dated FX method in the footer. If listing history and comparable price history start at different times, state both instead of inventing earlier prices.

## Legacy Company Data Schema

Use existing company modules such as `data_nvidia.py`, `data_pdd.py`, `data_tencent.py`, or `data_apple.py` as examples. Required shape:

- `TITLE`, `SUBTITLE`, `UPDATE_DATE`
- `COMPANY_PROFILE`
- `FINANCIAL_SUMMARY`
- `SEGMENTS_LABEL`
- `BUSINESS_SEGMENTS`: tuples `(rank, segment, percent, revenue, yoy, trend, note)`
- `REVENUE_MIX`: tuples `(segment, percent)`
- `MOVES_LABEL`
- `STRATEGIC_MOVES`: tuples `(action_type, target, detail, color)`
- `MOAT`: tuples `(title, description)`
- `KEY_METRICS`
- `RISKS_HIGHLIGHTS`: tuples `(kind, title, description)` where `kind` is usually `亮点` or `风险`
- `QUOTES_LABEL`
- `QUOTES`
- `DATA_SOURCE` or `FOOTER_LINES`

Legacy orange company command, only when explicitly requested or preserving an old batch:

```bash
cd /Users/jiangming/templates
python3 company_infographic.py data_<slug> "/Users/jiangming/持仓分析/<folder>/<slug>_经营分析.png"
```

## Hand-Drawn Sketches

Create two landscape PNGs for investor holding requests unless the user asks otherwise:

- `*_sketch1.html`: "投资之道" style, usually a portrait or symbolic figure, core principles, arrows/process, and quotes.
- `*_sketch2.html`: "持仓全景" style, usually key figures, top holdings bars, sector pie/donut, recent changes, and bottom insight.

For current company analysis, render the four-page contract above rather than adapting only two generic sketches. Preserve each company's palette, official Logo, semantic icon family, and narration style.

Screenshot command:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --screenshot="/Users/jiangming/持仓分析/<folder>/<output>.png" \
  --window-size=<body_css_width>,<body_css_height> \
  --force-device-scale-factor=4 \
  "file:///Users/jiangming/templates/sketch_refs/<slug>_sketch1.html"
```

Use the HTML's real CSS canvas and a 3x or 4x scale. Reject any output whose footer, signature, chart endpoint, text, or card falls outside the canvas.

## Required Signature

Every generated final image must include Jiangming's signature:

```text
by 江明
```

Rules:

- Place it as a separate centered footer line at the bottom of the image.
- Use the same font family, font size, and color as the data-source footnote.
- Do not merge it inline with the data-source text.
- If adding the signature causes clipping, increase the footer or screenshot height and regenerate.
- For Pillow orange long images, the engines append this line automatically unless `FOOTER_LINES` already contains an exact `by 江明` line.

## Required Money Currency

Display every monetary amount in U.S. dollars by default.

Scope:

- Revenue, profit, net income, operating profit, EBITDA, free cash flow
- Market cap, enterprise value, valuation multiples with money numerators
- Holdings value, position value, cash, AUM, portfolio market value
- CapEx, R&D spend, dividends, buybacks, debt, net cash, investments
- Any other explicitly monetary number

Rules:

- Convert local-currency reported figures to USD before placing them in image text.
- Label USD clearly using `美元`, `USD`, or `$` plus a clear unit such as `$35.7B USD` or `约 $357 亿美元`.
- Do not use local-currency symbols such as `₩`, `¥`, `€`, `£`, or `NT$` as the primary displayed amount in final images.
- Record the exchange-rate date or conversion basis in the data source/footer, for example `金额按 2026-04-23 KRW/USD 汇率折算为美元`.
- Use the latest reliable exchange rate when generating current images; if the figure is tied to a historical filing date, use a date-appropriate rate and label it.
- Local currency may be kept in internal notes or source citations, but final image labels should prioritize USD.

## Research Notes

- Holdings are time-sensitive. Always verify the latest quarter and filing date before claiming "latest".
- For US institutional holdings, use SEC 13F as the anchor. Cross-check with WhaleWisdom or the manager's official site when useful.
- For ETF-style public holdings such as ARK, use the issuer's daily holdings when available instead of only quarterly 13F data.
- For company images, use official annual reports, quarterly earnings releases, investor relations, official Careers/culture pages, Proxy filings, and official brand assets as anchors. Market cap, stock price, valuation multiples, holders, and price-history endpoints need dated sources.
- Use the footer as the audit layer: compact fiscal period, market-data date, ROI formula, CapEx source/limitation, shareholder-return source, culture source, exchange-rate basis, disclaimer, and a separate centered `by 江明` line.
