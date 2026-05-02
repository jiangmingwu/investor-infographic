# Local Template System

## What Exists

- `/Users/jiangming/templates/investor_infographic.py` creates the orange investor/fund holding-analysis long image.
- `/Users/jiangming/templates/company_infographic.py` creates the orange company operating-analysis long image.
- `/Users/jiangming/templates/data_template.py` is the investor/fund data skeleton.
- `/Users/jiangming/templates/data_*.py` contains existing examples. At installation time there were 34 data files.
- `/Users/jiangming/templates/sketch_refs/` contains hand-drawn HTML references. At installation time there were 58 HTML files.
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

## Company Data Schema

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

Company command:

```bash
cd /Users/jiangming/templates
python3 company_infographic.py data_<slug> "/Users/jiangming/持仓分析/<folder>/<slug>_经营分析.png"
```

## Hand-Drawn Sketches

Create two landscape PNGs for investor holding requests unless the user asks otherwise:

- `*_sketch1.html`: "投资之道" style, usually a portrait or symbolic figure, core principles, arrows/process, and quotes.
- `*_sketch2.html`: "持仓全景" style, usually key figures, top holdings bars, sector pie/donut, recent changes, and bottom insight.

For company analysis, adapt the same two-sketch idea to "商业模式/护城河" and "经营全景/财务结构".

Screenshot command:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --screenshot="/Users/jiangming/持仓分析/<folder>/<output>.png" \
  --window-size=1200,750 \
  --force-device-scale-factor=4 \
  "file:///Users/jiangming/templates/sketch_refs/<slug>_sketch1.html"
```

Expected screenshot size: 4800x3000px.

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
- For company images, use official annual reports, quarterly earnings releases, and investor relations as anchors. Market cap, stock price, and valuation multiples need date labels.
- Keep source labels concise in `DATA_SOURCE`; detailed citations can be provided in the chat response if the user asks for sources.
