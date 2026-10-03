# Company Research Packet

Use this schema before generating listed-company operating-analysis images. The packet is the audit contract between research, templates, and image review: research fills the packet first, rendering reads from it, and validation fails before delivery if the packet lacks evidence.

Apply [approved-original-layout.md](approved-original-layout.md): content/evidence improvements must not replace the company's approved visual design. The Amex files are historical layout references, not current source data.

## Required Root Fields

- `company`: display company name.
- `output_root`: must be under `/Users/jiangming/持仓分析`.
- `logo`: official brand asset provenance.
- `currency`: main display currency and exchange-rate note.
- `company_profile`: the fixed nine company-file fields.
- `panorama_top_grid`: the six-card `经营全景` top snapshot.
- `segment_mix` and `segments` (or the matching `panorama` nested fields): required for every newly created/refreshed panorama; legacy packets without them are not ready for delivery.
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

`company_profile` must contain these nine keys with non-empty values:

1. `公司全称`
2. `成立时间`
3. `创始人 / 创立主体`
4. `总部地址`
5. `交易所及代码`
6. `CEO / 主要负责人`
7. `员工人数`
8. `核心业务`
9. `当前市值`

Use `未披露` only when the value truly cannot be verified from public sources.
Use a company official history page, filing, or equivalent primary source for the founder field. For mergers, joint ventures, state-established companies, or spin-offs, identify the founding entity or formation mechanism rather than assigning an unsupported individual founder.

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
- `shareholder_return`: keep the current annual dividend/current or forward yield numeric display, then add `dividend_yield_average` with `value`, `label`, `period`, `formula`, and `source`. Use `近10年均值` when 10 years are available; otherwise use `可比期均值` and state the shorter public period. Retain raw observations and calculation rows, including split-consistent annual dividends/year-end prices if using the Amex method. Non-dividend years count as `0%`; absent history is not zero and must be explicitly unavailable.

Avoid vague phrases such as `现金分红稳定` unless paired with a number.

When dividend history cannot be reliably obtained, set average `value` to `资料不足`, retain the actual researched `period`, `formula` and `source`, and add a concrete `limitation`. Do not write a numeric zero for missing data. A shorter but reliable series uses `可比期均值`.

## Segment Mix

`segment_mix` contains `section_title`, `denominator` (`label`, `value`), `basis`, `mode` and `reconciliation`. Each `segments` row has `name`, `kind`, `share_pct`, `value` and `note`. Keep raw amounts for arithmetic review. Visible percentages must name their denominator and use the same period/currency.

- Reconcile actual reported amounts to the group total; retain corporate/unallocated/negative elimination rows instead of changing a reported segment value to force 100%.
- `top_products`, `top_brands`, `top_geographies` require an `other` row and `top_coverage_pct`; label the section accurately, not as reporting segments.
- `pre_elimination_segments` requires the explicit pre-elimination basis and an elimination row.
- English business/product names require Chinese parenthetical explanations.
- The existing validator checks structure/share totals, not source truth or all raw-amount mathematics. Independently recompute amounts/denominators and compare filings before rendering.

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

Retain each holder's actual holdings period, filing/publication date, security/entity scope and the valuation-price date. Prefer the latest verifiable report. If a recent Proxy cites an older holding, the position remains historical; mark this in the footer. Old shares multiplied by a current price are only an estimate, not proof of current shares or ownership percentage.

## Management Culture

Read [management-culture-evidence.md](management-culture-evidence.md) before selecting content. `management_culture` contains 1-3 evidence-backed distinctive practices, preferably 1-2. Prioritize meaningful employee treatment, then distinctive organization, ethics or customer commitments. Do not force a quota. If no practice qualifies, report the evidence gap and leave the page unfinished rather than inventing one.

Each card:

```json
{
  "lens": "人才 | 员工 | 组织 | 客户 | 伦理",
  "principle": "公开可验证的做事原则",
  "practice": "做法：公司怎么落地这个原则。",
  "case_or_number": "案例：或 数字：用公开来源证明它不是空话。",
  "source": "原始来源标题、适用/发布日期、URL、页码或段落",
  "distinctiveness": "这项做法特别在哪里，具体有什么可借鉴之处",
  "evidence_scope": "适用人群、地区/组织、时间、数字口径和关键限制",
  "evidence_status": "published_policy"
}
```

`evidence_status` is `published_policy` (published rule, not proof of execution) or `reported_practice` (attributed public execution case/statistic, not automatically independently audited). The three new fields are research metadata, not extra visible sections. Legacy packets must be enriched from sources before passing the refreshed validator; never auto-fill generic placeholders.

For superiority claims add a `comparison` record with company and benchmark values/definitions, comparable scope and both sources. This is a semantic review requirement; the structural validator does not verify comparisons or truth. Keep figures in USD where monetary and cite FX date.

Reject hiring volume, expansion plans, technical roadmaps, market share and financial results used as substitutes for culture. Do not reject employee benefits just because the text mentions manufacturing/production. Distinctive customer pricing discipline or anti-corruption practices may qualify when concrete rules and evidence support them. Review sources and claim scope before rendering; field completeness alone is not approval.

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
