# Company Research Packet

Use this schema before generating listed-company operating-analysis images. The packet is the audit contract between research, templates, and image review: research fills the packet first, rendering reads from it, and validation fails before delivery if the packet lacks evidence.

## Required Root Fields

- `company`: display company name.
- `output_root`: must be under `/Users/jiangming/持仓分析`.
- `logo`: official brand asset provenance.
- `currency`: main display currency and exchange-rate note.
- `company_profile`: the fixed eight company-file fields.
- `panorama_top_grid`: the six-card `经营全景` top snapshot.
- `core_drivers`: the `经营之道` core-business / moat evidence cards.
- `capital`: ROI/ROIC, 2026 CapEx, and shareholder-return evidence.
- `major_holders`: institutional / strategic / public notable holders for `经营全景` only.
- `management_culture`: people, organization, ethics, customer-treatment, or employee-practice evidence.
- `footer_lines`: compact audit footer lines, ending with a separate `by 江明` line.

## Logo

```json
{
  "official_source_url": "https://company.example/brand/logo.svg",
  "retrieved": "2026年7月",
  "sha256": "64 lowercase hex characters"
}
```

The source must be the company official site, brand page, investor-relations material, or annual report. Do not use ticker badges, Chinese abbreviation boxes, third-party logo libraries, or hand-redrawn approximations.

## Company Profile

`company_profile` must contain these eight keys with non-empty values:

1. `公司全称`
2. `成立时间`
3. `总部地址`
4. `交易所及代码`
5. `CEO / 主要负责人`
6. `员工人数`
7. `核心业务`
8. `当前市值`

Use `未披露` only when the value truly cannot be verified from public sources.

## Panorama Top Grid

Default six metric categories. The fiscal-year prefix should follow the latest complete fiscal year, such as `FY2024`, `FY2025`, or `FY2026`; do not hard-code `FY2025` when the source fiscal year differs:

- `FY20XX 营收`
- `FY20XX 经营利润`
- `FY20XX 经营现金流`
- `FY20XX 净利润`
- `当前市值`
- `PE / Forward PE`

Each card should provide `value`, `source`, and either `yoy` or `as_of` where relevant. Financial companies may use industry equivalents only when the packet also includes an explicit `industry_exception` reason.

## Core Drivers

`core_drivers` is the structured source for `经营之道`. Use 1-5 items; do not force four.

When refreshing an existing company set, treat its original company-specific HTML as the design baseline. Keep the existing card title, palette, icon, hierarchy, and explanation copy. The only normal edit here is to add one short `量化证据` line to that existing card. Do not replace the old layout with a generic core-driver grid just because a new metric is being added.

Each item must include:

```json
{
  "name": "原模板中的核心业务或核心能力标题",
  "metric": "量化证据：60% 市场份额 / 全球第一 / 该业务 $20B USD收入 / 123m用户",
  "evidence_kind": "市场份额 | 行业排名 | 业务收入或占比 | 销量或产量 | 渠道网络 | 品牌或产品组合 | 用户或装机 | 留存或认证 | 定价或利润率 | 专利或研发",
  "industry_meaning": "行业含义：这说明什么行业地位、切换成本、规模优势或变现能力。",
  "icon": "chip | memory | network | store | portfolio | shield | contract | logistics | people",
  "why_it_matters": "一句话说明为什么它能长期赚钱。",
  "source": "Annual report / investor day / credible market research, date"
}
```

Hard rule: every core card needs `量化证据 + 行业含义`. A business description without a directly related number, industry rank, share, installed base, business revenue mix, margin, retention, capacity, certified customers, or another hard indicator is not enough.

The metric must prove the specific card, not merely prove that the parent company is large. `当前市值`、CompaniesMarketCap 排名、员工人数、公司总营收、公司总利润、泛泛的“全球龙头” are invalid substitutes. Company-wide revenue/profit may be used only if the card explicitly proves the named business's revenue share, profit contribution, or position in that business. If no reliable quantitative evidence can be found, omit the card or describe it as an ordinary business; do not call it a moat.

## Capital

`capital` must include:

- `roi`: metric name, value, formula/source, and limitation if not comparable.
- `capex_2026`: public guidance / annual report / earnings call / investor day / credible estimate, or `未披露/不可比`.
- `shareholder_return`: dividend per share, dividend yield, buyback, payout, no-cash-dividend note, or another numeric shareholder-return figure.

Avoid vague phrases such as `现金分红稳定` unless paired with a number.

## Major Holders

`major_holders` belongs only in `经营全景`, after `亮点与风险`. Use 3-5 rows when available.

Each row:

```json
{
  "name": "BlackRock",
  "kind": "机构 | 战略股东 | 管理层 | 知名个人",
  "stake": "7.2%",
  "estimated_value": "$25.3B USD",
  "source": "Proxy / 13F / annual report, period"
}
```

Do not frame passive index positions as active bullish signals. Famous-person holdings require public filings.

## Management Culture

`management_culture` must use 1-3 real principles. It is about people, teams, ethics, customer-treatment practices, hiring, feedback, compensation, autonomy, decision rules, or employee behavior.

Each card:

```json
{
  "lens": "人才 | 员工 | 组织 | 客户 | 伦理",
  "principle": "公开可验证的做事原则",
  "practice": "做法：公司怎么落地这个原则。",
  "case_or_number": "案例：或 数字：用公开来源证明它不是空话。",
  "source": "Careers / handbook / founder letter / proxy / credible interview, date"
}
```

Reject production, manufacturing, supply chain, capacity, R&D route, CapEx, market share, segment revenue, valuation, and ordinary business strategy. Those belong in `经营之道` or `经营全景`, not management culture.

## Footer Lines

Footer lines are the quiet audit layer. Include compact source periods and avoid day-level ranges unless necessary:

- `经营数据：...，FY2025: 2025年1-12月`
- `行情数据：...，查看：2026年7月`
- `ROI口径：...`
- `2026 CapEx口径：...`
- `股东分红：...`
- `管理文化：...`
- `汇率口径：...`
- `免责声明：本图仅供学习参考，不构成投资建议`
- `by 江明`

`by 江明` must be a separate centered bottom line in the rendered image.
