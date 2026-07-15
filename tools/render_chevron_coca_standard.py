#!/usr/bin/env python3
"""Render Chevron's four pages with the approved Coca-Cola visual contract.

All financial text, icons, charts, and labels are deterministic HTML/SVG.
The official company logo is loaded from a verified local asset.
"""

from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image

import render_cocacola_visual_refine as ui


ROOT = Path("/Users/jiangming/持仓分析/公司经营分析")
OUT = ROOT / "39_雪佛龙"
REVIEW = ROOT / "_review/chevron_coca_standard_20260714"
BEFORE = REVIEW / "before"
HTML = REVIEW / "html"
PACKET = REVIEW / "packet/chevron_packet.json"
LOGO_PATH = Path("/Users/jiangming/templates/assets/company_logos/chevron-official-crop.png")
STOCK_HISTORY_PATH = Path("/Users/jiangming/templates/data/market_history/cvx_stock_history_1962_2026.json")
LOGO = LOGO_PATH.as_uri()
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

ACCENT = "#0066B2"
DEEP = "#174C7E"
RED = "#D7193F"
GOLD = "#B88722"
GREEN = "#21865A"
RISK = "#B64742"

# Reuse the approved Coca-Cola layout system with Chevron brand colors.
ui.ACCENT = ACCENT
ui.DEEP = DEEP
ui.GOLD = GOLD
ui.GREEN = GREEN
ui.RISK = RISK


def icon(name: str, color: str = ACCENT, size: int = 36) -> str:
    custom = {
        "oil": "<path d='M24 5C18 14 11 21 11 30a13 13 0 0 0 26 0c0-9-7-16-13-25z'/><path d='M18 33c2 3 5 4 9 3'/>",
        "well": "<path d='M9 40h30M14 40l7-28h6l7 28M18 25h12M16 32h16'/><path d='M27 12l10 6-10 3M37 18v11'/>",
        "refinery": "<path d='M7 41V20l13 7V17l12 7V9h7v32z'/><path d='M12 34h4M22 34h4M32 34h4M35 9h4'/>",
        "reserve": "<path d='M8 35c8-4 15-4 23 0 4 2 7 2 10 0M8 28c8-4 15-4 23 0 4 2 7 2 10 0M12 19h24'/><path d='M16 19c0-7 4-12 8-12s8 5 8 12'/>",
        "merge": "<path d='M8 12h10c8 0 8 12 15 12h7M8 36h10c8 0 8-12 15-12'/><path d='M35 18l5 6-5 6'/>",
        "feedback": "<path d='M7 9h34v23H24l-9 8v-8H7z'/><path d='M15 18h18M15 25h12'/>",
        "people": "<circle cx='18' cy='15' r='6'/><circle cx='33' cy='17' r='5'/><path d='M6 41c1-9 7-14 14-14s13 5 14 14M29 29c6 1 10 5 12 12'/>",
        "ethics": "<path d='M24 6v36M11 14h26M14 14L8 28h12zM34 14l-6 14h12zM16 42h16'/>",
        "pin": "<path d='M24 43s13-12 13-24a13 13 0 1 0-26 0c0 12 13 24 13 24z'/><circle cx='24' cy='19' r='4'/>",
    }
    if name not in custom:
        return ui.icon(name, color, size)
    common = (
        f"width='{size}' height='{size}' viewBox='0 0 48 48' fill='none' "
        f"stroke='{color}' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'"
    )
    return f"<svg {common}>{custom[name]}</svg>"


def document(title: str, subtitle: str, body: str, foot: list[str], height: int) -> str:
    html = ui.document(title, subtitle, body, foot, height)
    extra = f"""
    .logo-box {{ height:132px; padding:7px; }}
    .logo-box img {{ width:168px; max-height:118px; object-fit:contain; }}
    .grid-core {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }}
    .grid-core .driver {{ min-height:225px; grid-template-columns:42px 1fr; padding:14px 12px; }}
    .grid-core .driver h3 {{ font-size:19px; }}
    .grid-core .driver .proof {{ color:{RED}; font-size:18px; }}
    .grid-core .driver .meaning {{ font-size:13px; }}
    .quote {{ margin-top:16px; border-left:6px solid {ACCENT}; background:rgba(0,102,178,.07); padding:14px 18px; color:#4B3A2D; font-family:'Songti SC','STSong',serif; font-size:20px; font-weight:850; line-height:1.42; }}
    .quote small {{ display:block; margin-top:6px; color:#817062; font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif; font-size:13px; }}
    .culture-stack {{ gap:11px; }}
    .culture-card {{ min-height:200px; }}
    .metric {{ border-color:{ACCENT}; }}
    .metric .value {{ color:{DEEP}; }}
    .stock-wrap {{ border:2px solid #DFCABB; border-radius:12px; background:rgba(255,255,255,.72); padding:12px 14px 9px; }}
    .stock-meta {{ display:flex; justify-content:space-between; align-items:flex-start; gap:18px; margin-bottom:5px; }}
    .stock-meta b {{ display:block; color:{DEEP}; font-size:16px; }}
    .stock-meta span {{ display:block; margin-top:3px; color:#8B7767; font-size:12px; font-weight:700; }}
    .stock-return {{ color:{ACCENT}; text-align:right; font-size:20px; font-weight:950; line-height:1.05; white-space:nowrap; }}
    .stock-return small {{ display:block; margin-top:4px; color:{GREEN}; font-size:12px; font-weight:850; }}
    .stock-chart {{ display:block; width:100%; height:210px; }}
    .stock-note {{ margin-top:2px; color:#8B7767; text-align:center; font-size:11px; font-weight:700; }}
    """
    return html.replace("</style>", extra + "</style>")


def footer_common() -> list[str]:
    return [
        "经营数据：Chevron 2025 Annual Report / 10-K，FY2025：2025年1-12月，金额为美元",
        "行情数据：StockAnalysis / S&P Global Market Intelligence，截至2026年7月14日盘中",
        "汇率口径：公司财报及行情本身以美元披露，无需换汇",
        "免责声明：本图仅供学习参考，不构成投资建议",
    ]


def metric(value: str, label: str, icon_name: str, delta: str = "", color: str = "muted") -> str:
    delta_html = f"<div class='delta {color}'>{delta}</div>" if delta else "<div class='delta muted'>&nbsp;</div>"
    return (
        f"<div class='metric'><div class='mi'>{icon(icon_name, ACCENT, 30)}</div>"
        f"<div class='value'>{value}</div><div class='label'>{label}</div>{delta_html}</div>"
    )


def load_stock_history() -> dict:
    history = json.loads(STOCK_HISTORY_PATH.read_text(encoding="utf-8"))
    points = history.get("annual_close", [])
    if history.get("symbol") != "CVX" or len(points) < 60:
        raise ValueError("Chevron stock history is incomplete")
    if points[0][0] != history.get("series_start") or points[-1][0] != history.get("series_end"):
        raise ValueError("Chevron stock history date range does not match its points")
    if any(not isinstance(year, int) or not isinstance(price, (int, float)) or price <= 0 for year, price in points):
        raise ValueError("Chevron stock history contains invalid values")
    return history


def stock_price_chart(history: dict) -> str:
    points = history["annual_close"]
    start_year, start_price = points[0]
    end_year, end_price = points[-1]
    width, height = 760, 210
    left, right, top, bottom = 48, 16, 12, 31
    plot_width = width - left - right
    plot_height = height - top - bottom
    y_max = max(50, math.ceil(max(price for _, price in points) / 50) * 50)

    def x_pos(year: int) -> float:
        return left + (year - start_year) / (end_year - start_year) * plot_width

    def y_pos(price: float) -> float:
        return top + (1 - price / y_max) * plot_height

    line = " ".join(
        ("M" if index == 0 else "L") + f"{x_pos(year):.1f},{y_pos(price):.1f}"
        for index, (year, price) in enumerate(points)
    )
    area = f"{line} L{x_pos(end_year):.1f},{top + plot_height:.1f} L{x_pos(start_year):.1f},{top + plot_height:.1f} Z"

    y_ticks = []
    for value in range(0, y_max + 1, 50):
        y = y_pos(value)
        y_ticks.append(
            f"<line x1='{left}' y1='{y:.1f}' x2='{width - right}' y2='{y:.1f}' stroke='#E8DDD3' stroke-width='1'/>"
            f"<text x='{left - 8}' y='{y + 4:.1f}' text-anchor='end' fill='#9B8776' font-size='10' font-weight='700'>${value}</text>"
        )
    x_ticks = []
    for year in (1962, 1980, 2000, 2020, end_year):
        x = x_pos(year)
        x_ticks.append(
            f"<line x1='{x:.1f}' y1='{top}' x2='{x:.1f}' y2='{top + plot_height}' stroke='#EFE5DC' stroke-width='1' stroke-dasharray='3 4'/>"
            f"<text x='{x:.1f}' y='{height - 8}' text-anchor='middle' fill='#806D5D' font-size='10' font-weight='800'>{year}</text>"
        )
    multiple = end_price / start_price
    annualized = (multiple ** (1 / (end_year - start_year)) - 1) * 100
    return f"""
    <div class='stock-wrap'>
      <div class='stock-meta'>
        <div><b>NYSE 1921年上市</b><span>公开价格序列{start_year}-{end_year} · 年末/最新收盘价</span></div>
        <div class='stock-return'>${start_price:.2f} → ${end_price:.2f}<small>约{multiple:.1f}倍 · 价格年化约{annualized:.1f}%</small></div>
      </div>
      <svg class='stock-chart' viewBox='0 0 {width} {height}' role='img' aria-label='Chevron long-term stock price chart'>
        <defs><linearGradient id='stockFill' x1='0' y1='0' x2='0' y2='1'><stop offset='0%' stop-color='{ACCENT}' stop-opacity='.22'/><stop offset='100%' stop-color='{ACCENT}' stop-opacity='.02'/></linearGradient></defs>
        {''.join(y_ticks)}{''.join(x_ticks)}
        <path d='{area}' fill='url(#stockFill)'/>
        <path d='{line}' fill='none' stroke='{ACCENT}' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'/>
        <circle cx='{x_pos(start_year):.1f}' cy='{y_pos(start_price):.1f}' r='4.5' fill='{GOLD}' stroke='white' stroke-width='2'/>
        <circle cx='{x_pos(end_year):.1f}' cy='{y_pos(end_price):.1f}' r='5' fill='{RED}' stroke='white' stroke-width='2'/>
      </svg>
      <div class='stock-note'>拆股调整收盘价，线性坐标，不含股息再投资；早于1962年的连续公开价格序列未纳入。</div>
    </div>"""


def company_profile() -> str:
    p = packet()
    profile = "".join(
        f"<div class='p'><span class='k'>{key}</span><span class='v'>{value}</span></div>"
        for key, value in p["company_profile"].items()
    )
    business = "".join(
        f"<div class='card business-card{' wide' if i == 2 else ''}'><div>{icon(item['icon'], item['color'], 38)}</div>"
        f"<div><h3>{item['name']}</h3><div class='what'>{item['description']}</div></div></div>"
        for i, item in enumerate(p["business_scope"])
    )
    highlights = "".join(
        f"<div class='status-card'><div class='sicon'>{icon(item['icon'], item['color'], 30)}</div>"
        f"<div class='big'>{item['metric']}</div><div class='explain'>{item['meaning']}</div></div>"
        for item in p["industry_highlights"]
    )
    stock_chart = stock_price_chart(p["stock_history"])
    timeline = "".join(
        [
            "<div class='time'><div class='dot'></div><b>1879</b><span>Pacific Coast Oil成立</span></div>",
            "<div class='time'><div class='dot'></div><b>1984</b><span>收购Gulf并更名Chevron</span></div>",
            "<div class='time'><div class='dot'></div><b>2001</b><span>与Texaco完成合并</span></div>",
            "<div class='time'><div class='dot'></div><b>2025</b><span>完成Hess收购</span></div>",
        ]
    )
    body = f"""
    <div class='strap'>147年能源史 × 一体化油气体系 × 全球资产组合</div>
    <div class='logo-hero'><div class='logo-box'><img src='{LOGO}'></div><div class='thesis'>从上游资源到炼化销售的一体化能源公司，长期竞争力来自资源寿命、低成本资产和资本纪律。<small>本页只回答：它是谁、做什么、规模多大、处于什么行业位置。</small></div></div>
    <section class='section'><h2>基本信息</h2><div class='profile'>{profile}</div></section>
    <section class='section'><h2>业务范围</h2><div class='grid2'>{business}</div></section>
    <section class='section'><h2>上市以来股价走势</h2>{stock_chart}</section>
    <section class='section'><h2>行业地位与核心亮点</h2><div class='grid3'>{highlights}</div></section>
    <section class='section'><h2>关键历史节点</h2><div class='timeline'>{timeline}</div></section>"""
    foot = [
        "档案与历史：Chevron官网、2025 Annual Report / 10-K，核查：2026年7月",
        "人员规模：2025年末43,039人；总部：Houston, Texas；CEO：Mike Wirth",
        "行业数字：2025 Annual Report Supplement、4Q 2025 Earnings Release、Permian官方专题",
        "股价走势：Chevron官网确认NYSE上市；Yahoo Finance周线年末收盘价，1962年-2026年7月14日",
        "品牌资产：Chevron官网官方Hallmark图标，核查：2026年7月",
        "免责声明：本图仅供学习参考，不构成投资建议",
    ]
    return document("雪佛龙公司档案", "Chevron Corporation · NYSE: CVX · Company Profile", body, foot, 1910)


def strategy() -> str:
    p = packet()
    drivers = "".join(
        f"<div class='card driver'><div class='doodle'>{icon(item['icon'], item['color'], 40)}</div>"
        f"<div><h3>{item['name']}</h3><div class='proof'>{item['metric']}</div>"
        f"<div class='meaning'>{item['industry_meaning']}</div></div></div>"
        for item in p["core_drivers"]
    )
    body = f"""
    <div class='strap'>长期定位 × 核心业务 × 数据化护城河 × 战略动作</div>
    <div class='logo-hero'><div class='logo-box'><img src='{LOGO}'></div><div class='thesis'>以长寿命资源和低成本油气资产创造现金流，再把资金投向高回报增产、炼化网络与稳定股东回报。<small>核心只保留三项；每项都必须有数量、行业位置或资本回报证据。</small></div></div>
    <section class='section'><h2>核心业务与硬指标</h2><div class='grid-core'>{drivers}</div></section>
    <section class='section'><h2>近两年战略动作</h2>
      <div class='row'><div class='tag'>{icon('merge', ACCENT, 25)}完成Hess收购</div><div class='detail'>2025年完成交易，加入Guyana和Bakken等资产；整合目标指向更长资源寿命与更强自由现金流。</div><div class='right positive'>2025完成</div></div>
      <div class='row'><div class='tag'>{icon('capex', GOLD, 25)}收紧资本框架</div><div class='detail'>2026年合并资本开支公开指引为 <b>$18B-$19B</b>，位于长期区间低端。</div><div class='right warning'>$18B-$19B</div></div>
      <div class='row'><div class='tag'>{icon('well', GREEN, 25)}聚焦高回报增产</div><div class='detail'>约 <b>$6B</b> 投向美国页岩与致密油，支撑美国油当量日产量超过 <b>2M桶</b>。</div><div class='right positive'>&gt;2M桶/日</div></div>
    </section>
    <div class='quote'>“世界需要我们提供的能源，而雪佛龙从未像现在这样有能力交付。”<small>Mike Wirth，Chevron 2025 Annual Report（中文转述）</small></div>"""
    foot = footer_common() + [
        "核心证据：Chevron 2025 Annual Report Supplement；Permian官方专题，核查：2026年7月",
        "战略动作：Hess完成公告、2026 CapEx公开指引；数字均来自Chevron官网",
    ]
    return document("雪佛龙的经营之道", "Chevron · Resource + Permian + Downstream Playbook", body, foot, 1200)


def panorama() -> str:
    p = packet()
    values = p["panorama_top_grid"]
    top = "".join(
        [
            metric(values["FY2025 营收"]["value"], "FY2025 营收", "up", "同比 -4.64%", "negative"),
            metric(values["FY2025 经营利润"]["value"], "FY2025 经营利润", "profit", "同比 -12.61%", "negative"),
            metric(values["FY2025 经营现金流"]["value"], "FY2025 经营现金流", "cash", "同比 +7.77%", "positive"),
            metric(values["FY2025 净利润"]["value"], "FY2025 净利润", "coin", "同比 -30.36%", "negative"),
            metric(values["当前市值"]["value"], "当前市值", "market", "2026年7月14日盘中", "warning"),
            metric(values["PE / Forward PE"]["value"], "PE / Forward PE", "scale", "当前估值", "muted"),
        ]
    )
    holders = "".join(
        f"<div class='holder-row'><div class='holder-name'>{icon('holders', item['color'], 24)}{item['name']}</div>"
        f"<div class='holder-stake'>{item['stake']}</div><div class='holder-shares'>{item['shares']}</div>"
        f"<div class='holder-value'>{item['reported_value']}</div></div>"
        for item in p["major_holders"]
    )
    body = f"""
    <div class='strap'>六项核心数据 × 资本配置 × 亮点风险 × 机构持仓</div>
    <div class='logo-hero'><div class='logo-box'><img src='{LOGO}'></div><div class='thesis'>2025年经营现金流逆势增长，但利润随油价与周期回落；当前估值要同时看Forward PE和资本回报。<small>全年经营按FY2025；市值与估值按生成当日。</small></div></div>
    <section class='section'><h2>核心财务与当前估值</h2><div class='grid3'>{top}</div></section>
    <section class='section'><h2>资本配置与股东回报</h2><div class='capital'>
      <div class='card'><div class='cap-head'>{icon('chart', ACCENT, 28)}资本效率</div><div class='cap-num'>ROIC 4.37%</div><div class='cap-sub'>WACC 6.37%，当前回报低于资本成本约2个百分点。</div></div>
      <div class='card'><div class='cap-head'>{icon('capex', GOLD, 28)}2026 CapEx</div><div class='cap-num'>$18B-$19B</div><div class='cap-sub'>公司公开合并资本开支指引；另有联营资本开支$1.3B-$1.7B。</div></div>
      <div class='card'><div class='cap-head'>{icon('coin', GREEN, 28)}股东分红</div><div class='cap-num'>$7.12/股 · 3.93%</div><div class='cap-sub'>连续39年提高股息；FY2025现金分红$12.75B。</div></div>
    </div></section>
    <section class='section'><h2>亮点与风险</h2><div class='signal-grid'>
      <div class='signal good'><h3>{icon('up', GREEN, 26)}亮点</h3><ul><li><b>经营现金流$33.94B</b>，同比<b>+7.77%</b>，收入下降时仍保持现金创造。</li><li><b>Permian 1M桶/日</b>，2020-2024 ROI比同区同行平均高<b>10%</b>。</li></ul></div>
      <div class='signal bad'><h3>{icon('risk', RISK, 26)}风险</h3><ul><li><b>归母净利润-30.36%</b>，盈利仍高度暴露于油气价格与炼化利润率。</li><li><b>ROIC 4.37% &lt; WACC 6.37%</b>，Hess整合和新增资本效率需要跟踪。</li></ul></div>
    </div></section>
    <section class='section'><h2>重要机构持仓</h2><div class='ownership-note'>Q1 2026 13F期末持仓；比例按约19.92亿股估算，金额为2026年3月31日申报价值，不代表主动看多。</div>{holders}</section>"""
    foot = footer_common() + [
        "ROI口径：StockAnalysis / S&P Global，ROIC 4.37%、WACC 6.37%，截至2026年7月14日",
        "2026 CapEx：Chevron 2025年12月3日公开指引；股息：年化$7.12/股、股息率3.93%",
        "机构持仓：Q1 2026 13F汇总及Chevron 2026 Proxy；持仓期末为2026年3月31日",
    ]
    return document("雪佛龙 FY2025 经营全景", "Chevron Corporation · NYSE: CVX · 全年经营与当前估值", body, foot, 1710)


def culture() -> str:
    p = packet()
    cards = "".join(
        f"<div class='card culture-card'><div>{icon(item['icon'], item['color'], 47)}</div><div>"
        f"<h3>{item['principle']}</h3><div class='rule'>{item['practice']}</div>"
        f"<div class='case'>{item['case_or_number']}</div><div class='lesson'>{item['lesson']}</div>"
        f"<span class='lens'>{item['lens']}</span></div></div>"
        for item in p["management_culture"]
    )
    body = f"""
    <div class='strap'>一线安全授权 × 正确方式取得结果 × 反馈与领导力</div>
    <div class='logo-hero'><div class='logo-box'><img src='{LOGO}'></div><div class='thesis'>雪佛龙文化的辨识度，在于它把安全授权、伦理问责和人才反馈做成可执行机制。<small>只呈现人员管理、组织行为与员工体验的真实做法。</small></div></div>
    <section class='section'><h2>三个可验证的管理机制</h2><div class='culture-stack'>{cards}</div></section>"""
    foot = [
        "管理文化：The Chevron Way、Operational Excellence、2026 Proxy，核查：2026年7月",
        "员工机制：Chevron Diversity & Inclusion官网；4,500人、57国、22种语言为公司公开口径",
        "福利说明：Chevron Careers按当地市场提供绩效奖金、健康、退休与灵活工作等项目",
        "汇率口径：本页无非美元金额；免责声明：本图仅供学习参考，不构成投资建议",
    ]
    return document("雪佛龙管理文化", "Chevron · Management Culture · 可运行的人员与组织机制", body, foot, 1240)


def packet() -> dict:
    return {
        "company": "雪佛龙",
        "rank": 39,
        "logo": {
            "official_source_url": "https://www.chevron.com/-/media/shared-media/images/hallmark-2023.png",
            "path": str(LOGO_PATH),
            "retrieved": "2026年7月",
        },
        "currency": {"display": "USD", "exchange_rate_note": "财报与行情均为美元，无需换汇。"},
        "stock_history": load_stock_history(),
        "company_profile": {
            "公司全称": "Chevron Corporation",
            "成立时间": "1879年",
            "总部地址": "Houston, Texas, USA",
            "交易所及代码": "NYSE: CVX",
            "CEO / 主要负责人": "Mike Wirth",
            "员工人数": "43,039人（2025年末）",
            "公司定位": "全球一体化能源公司",
            "历史长度": "截至2026年约147年",
        },
        "business_scope": [
            {"name": "上游油气", "description": "勘探、开发和生产原油与天然气，核心地区包括Permian、美国湾、Guyana和澳大利亚。", "icon": "oil", "color": ACCENT},
            {"name": "下游与化工", "description": "炼油、燃料销售、润滑油，以及Chevron Phillips Chemical等联营化工业务。", "icon": "refinery", "color": RED},
            {"name": "LNG与新能源", "description": "运营澳大利亚LNG，并布局可再生燃料、碳捕集、氢与新型电力项目。", "icon": "reserve", "color": GREEN},
        ],
        "industry_highlights": [
            {"metric": "10.6B桶油当量储量", "meaning": "2025年末已探明储量，提供长周期资源基础", "icon": "reserve", "color": ACCENT, "source": "Chevron 4Q 2025 Earnings Release"},
            {"metric": "Permian 1M桶/日", "meaning": "2025年平均产量创纪录；ROI高于同区同行", "icon": "well", "color": GOLD, "source": "Chevron Permian官方专题，2026年"},
            {"metric": "炼能1.819M桶/日", "meaning": "2025年末全球炼油能力；另有13,798个零售网点", "icon": "refinery", "color": RED, "source": "Chevron 2025 Annual Report Supplement"},
        ],
        "core_drivers": [
            {"name": "全球上游资源库", "metric": "10.6B桶油当量储量", "icon": "reserve", "color": ACCENT, "industry_meaning": "行业含义：已探明储量决定未来可持续生产年限，是一体化油气公司的资源底盘。", "source": "Chevron 4Q 2025 Earnings Release"},
            {"name": "Permian低成本资产", "metric": "1M桶/日 · ROI高10%", "icon": "well", "color": GOLD, "industry_meaning": "行业含义：75%土地受益于矿权；2020-2024 ROI比同区同行平均高10%，证明成本和回报优势。", "source": "Chevron Permian官方专题，2025-2026"},
            {"name": "炼化与零售网络", "metric": "1.819M桶/日 · 13,798点", "icon": "refinery", "color": RED, "industry_meaning": "行业含义：炼油能力与全球零售终端承接上游资源，并分散单一上游价格周期。", "source": "Chevron 2025 Annual Report Supplement"},
        ],
        "panorama_top_grid": {
            "FY2025 营收": {"value": "$184.43B", "yoy": "-4.64%", "source": "Chevron 2025 10-K"},
            "FY2025 经营利润": {"value": "$16.36B", "yoy": "-12.61%", "source": "Chevron 2025 10-K"},
            "FY2025 经营现金流": {"value": "$33.94B", "yoy": "+7.77%", "source": "Chevron 2025 10-K"},
            "FY2025 净利润": {"value": "$12.30B", "yoy": "-30.36%", "source": "Chevron 2025 10-K，归母口径"},
            "当前市值": {"value": "$358.31B", "as_of": "2026年7月14日盘中", "source": "StockAnalysis / S&P Global"},
            "PE / Forward PE": {"value": "31.69x / 11.46x", "as_of": "2026年7月14日盘中", "source": "StockAnalysis / S&P Global"},
        },
        "capital": {
            "roi": {"value": "ROIC 4.37% / WACC 6.37%", "source": "StockAnalysis / S&P Global，2026-07-14"},
            "capex_2026": {"value": "$18B-$19B", "source": "Chevron 2026 CapEx公开指引，2025-12-03"},
            "shareholder_return": {"value": "$7.12/股 / 3.93%", "source": "StockAnalysis，2026-07-14"},
        },
        "major_holders": [
            {"name": "State Street", "stake": "7.69%", "shares": "1.531亿股 · Q1 2026", "reported_value": "$31.68B", "source": "Q1 2026 13F，2026-03-31", "color": ACCENT},
            {"name": "BlackRock", "stake": "7.26%", "shares": "1.447亿股 · Q1 2026", "reported_value": "$29.94B", "source": "Q1 2026 13F，2026-03-31", "color": DEEP},
            {"name": "Vanguard Capital Mgmt", "stake": "6.15%", "shares": "1.225亿股 · Q1 2026", "reported_value": "$25.34B", "source": "Q1 2026 13F，2026-03-31", "color": GREEN},
            {"name": "Berkshire Hathaway", "stake": "4.24%", "shares": "0.844亿股 · 季减35.2%", "reported_value": "$17.46B", "source": "Berkshire Q1 2026 13F，2026-03-31", "color": GOLD},
        ],
        "management_culture": [
            {"lens": "员工", "principle": "任何人都有权停止不安全的工作", "practice": "做法：Operational Excellence把人员与环境安全置于产量和进度之前；员工与承包商既有权也有责任停止不安全作业。", "case_or_number": "案例：Stop-Work Authority写入OEMS；风险消除后才恢复作业，不要求先等待管理层逐级批准。", "lesson": "可借鉴：把安全授权交给离风险最近的人，并保护其停止工作的权利。", "icon": "shield", "color": ACCENT, "source": "Chevron Operational Excellence / Workforce Health and Safety"},
            {"lens": "伦理", "principle": "结果必须以正确的方式取得", "practice": "做法：The Chevron Way以信任、诚信、高绩效和问责作为行为标准，不允许短期业绩抵消行为问题。", "case_or_number": "案例：董事、高管和员工每两年认证遵守Business Conduct and Ethics Code；出现疑虑须主动提问和报告。", "lesson": "可借鉴：把价值观变成周期性认证、报告义务和明确问责。", "icon": "ethics", "color": RED, "source": "Chevron 2026 Proxy；The Chevron Way"},
            {"lens": "人员", "principle": "用持续反馈和教练培养各层级领导者", "practice": "做法：全年多次员工调查观察文化与福祉，并用一对一教练和同伴小组培养主管、经理和个人贡献者。", "case_or_number": "数字：自2020年起已为4,500+人提供教练，覆盖57个国家、22种语言。", "lesson": "可借鉴：领导力发展不只面向高管；用反馈频率和覆盖人数衡量是否真正落地。", "icon": "feedback", "color": GREEN, "source": "Chevron Diversity & Inclusion官网，核查2026年7月"},
        ],
    }


def validate_html(name: str, html: str) -> None:
    if "..." in html or "…" in html:
        raise ValueError(f"visible ellipsis found in {name}")
    if html.count("by 江明") != 1:
        raise ValueError(f"signature count invalid in {name}")
    if "chevron-official-crop.png" not in html:
        raise ValueError(f"official cropped logo missing in {name}")


def validate_logo_asset() -> None:
    image = Image.open(LOGO_PATH).convert("RGBA")
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        raise ValueError("official Chevron logo is blank")
    visible_w = bbox[2] - bbox[0]
    visible_h = bbox[3] - bbox[1]
    if visible_w / image.width < 0.75 or visible_h / image.height < 0.75:
        raise ValueError("Chevron logo contains excessive transparent padding")


def render_html(html: str, html_path: Path, png_path: Path, height: int) -> None:
    validate_html(html_path.name, html)
    html_path.write_text(html, encoding="utf-8")
    subprocess.run(
        [
            str(CHROME),
            "--headless",
            "--hide-scrollbars",
            "--disable-gpu",
            f"--screenshot={png_path}",
            f"--window-size=900,{height}",
            "--force-device-scale-factor=3",
            html_path.as_uri(),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    rendered = Image.open(png_path)
    if rendered.size != (2700, height * 3):
        raise ValueError(f"unexpected output size for {png_path}: {rendered.size}")


def backup_existing() -> None:
    BEFORE.mkdir(parents=True, exist_ok=True)
    for name in (
        "chevron_公司档案.png",
        "chevron_sketch1.png",
        "chevron_sketch2.png",
        "chevron_管理文化.png",
    ):
        source = OUT / name
        target = BEFORE / name
        if source.exists() and not target.exists():
            shutil.copy2(source, target)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    HTML.mkdir(parents=True, exist_ok=True)
    PACKET.parent.mkdir(parents=True, exist_ok=True)
    validate_logo_asset()
    backup_existing()
    PACKET.write_text(json.dumps(packet(), ensure_ascii=False, indent=2), encoding="utf-8")
    pages = [
        ("chevron_company.html", "chevron_公司档案.png", company_profile(), 1910),
        ("chevron_strategy.html", "chevron_sketch1.png", strategy(), 1200),
        ("chevron_panorama.html", "chevron_sketch2.png", panorama(), 1710),
        ("chevron_culture.html", "chevron_管理文化.png", culture(), 1240),
    ]
    for html_name, png_name, content, height in pages:
        render_html(content, HTML / html_name, OUT / png_name, height)
    print(f"rendered {len(pages)} Chevron pages to {OUT}")
    print(f"review packet: {PACKET}")


if __name__ == "__main__":
    main()
