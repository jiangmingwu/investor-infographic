#!/usr/bin/env python3
"""Render the compact, data-led Coca-Cola company analysis refresh.

The financial text and diagrams are deterministic HTML/SVG. No image model is
used for figures, labels, charts, or logos.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("/Users/jiangming/持仓分析/公司经营分析")
REVIEW = ROOT / "_review/cocacola_profile_culture_20260712"
HTML = REVIEW / "html"
PACKET = REVIEW / "packet/cocacola_packet.json"
LOGO = Path("/Users/jiangming/templates/assets/company_logos/cocacola-official.png").as_uri()

ACCENT = "#D71920"
DEEP = "#7F1D2D"
GOLD = "#B88722"
GREEN = "#21865A"
RISK = "#B64742"


def icon(name: str, color: str = ACCENT, size: int = 36) -> str:
    """Small semantic line icons; never replace a company logo."""
    common = f"width='{size}' height='{size}' viewBox='0 0 48 48' fill='none' stroke='{color}' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'"
    shapes = {
        "can": "<rect x='15' y='6' width='18' height='36' rx='4'/><path d='M19 12h10M19 36h10M22 18h4M20 27h8'/>",
        "network": "<circle cx='12' cy='12' r='5'/><circle cx='36' cy='14' r='5'/><circle cx='24' cy='36' r='5'/><path d='M16 14l15 1M15 16l7 15M34 19l-7 12'/>",
        "bottle": "<path d='M20 5h8v9l5 8v18a3 3 0 0 1-3 3H18a3 3 0 0 1-3-3V22l5-8z'/><path d='M16 25h16M16 33h16'/>",
        "brands": "<circle cx='16' cy='17' r='9'/><circle cx='31' cy='17' r='9'/><circle cx='23.5' cy='31' r='9'/><path d='M15 17h2M30 17h2M22 31h3'/>",
        "up": "<path d='M8 35l11-12 8 7 13-17'/><path d='M31 13h9v9'/>",
        "profit": "<path d='M9 38h30M14 34V21M24 34V12M34 34V17'/><path d='M10 17l10-8 8 5 11-8'/>",
        "cash": "<rect x='6' y='12' width='36' height='24' rx='3'/><circle cx='24' cy='24' r='6'/><path d='M12 18h1M35 30h1'/>",
        "market": "<circle cx='24' cy='24' r='17'/><path d='M7 24h34M24 7c6 6 6 28 0 34M24 7c-6 6-6 28 0 34'/>",
        "scale": "<path d='M24 7v32M13 13h22M24 13l-9 13H7l6-13M24 13l9 13h8l-8-13M17 39h14'/>",
        "chart": "<path d='M8 39V9M8 39h33M13 32l9-8 7 4 10-13'/><circle cx='39' cy='15' r='2'/>",
        "capex": "<path d='M29 8a8 8 0 0 0-8 10L8 31l9 9 13-13a8 8 0 0 0 10-8l-7 3-5-5z'/><path d='M11 37l-3 3'/>",
        "coin": "<circle cx='24' cy='24' r='16'/><path d='M28 16c-1-2-4-3-7-2-5 2-4 7 1 8 6 1 7 6 2 9-3 2-7 1-9-2M24 11v26'/>",
        "shield": "<path d='M24 5l15 6v10c0 10-7 17-15 21-8-4-15-11-15-21V11z'/><path d='M16 24l5 5 11-12'/>",
        "risk": "<path d='M24 6l19 34H5z'/><path d='M24 18v10M24 34h.01'/>",
        "holders": "<circle cx='17' cy='15' r='6'/><circle cx='33' cy='17' r='5'/><path d='M6 40c1-9 7-14 14-14s13 5 14 14M29 28c6 1 10 5 12 12'/>",
        "code": "<rect x='11' y='6' width='26' height='36' rx='3'/><path d='M18 15h12M18 22h12M18 29l3 3 6-7'/>",
        "speak": "<path d='M8 10h32v22H22l-8 8v-8H8z'/><path d='M17 19h14M17 25h9'/>",
        "fair": "<path d='M24 6v36M11 14h26M14 14l-6 14h12l-6-14M34 14l-6 14h12l-6-14M16 42h16'/>",
        "heart": "<path d='M24 39S8 30 8 18c0-8 10-11 16-4 6-7 16-4 16 4 0 12-16 21-16 21z'/>",
        "pin": "<path d='M24 43s13-12 13-24a13 13 0 1 0-26 0c0 12 13 24 13 24z'/><circle cx='24' cy='19' r='4'/>",
    }
    return f"<svg {common}>{shapes[name]}</svg>"


def footer(lines: list[str]) -> str:
    body = "<br>".join(lines)
    return f"<footer>{body}<div class='signature'>by 江明</div></footer>"


def document(title: str, subtitle: str, body: str, foot: list[str], height: int) -> str:
    return f"""<!doctype html>
<html lang='zh-CN'><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{title}</title>
<style>
* {{ box-sizing:border-box; }}
html,body {{ margin:0; width:900px; height:{height}px; overflow:hidden; }}
body {{ color:#42372F; font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif; background-color:#F7F4ED; background-image:linear-gradient(rgba(174,142,105,.105) 1px,transparent 1px),linear-gradient(90deg,rgba(174,142,105,.105) 1px,transparent 1px); background-size:24px 24px; }}
.page {{ width:900px; min-height:{height - 1}px; padding:50px 52px 0; position:relative; }}
.title {{ margin:0; text-align:center; color:{ACCENT}; font-family:'Songti SC','STSong',serif; font-size:51px; font-weight:900; line-height:1.12; letter-spacing:0; }}
.subtitle {{ margin:10px 0 0; text-align:center; color:#9C7D67; font-size:17px; font-weight:750; letter-spacing:.25px; }}
.strap {{ margin:18px auto 22px; border:2px solid {ACCENT}; color:#6A5140; background:rgba(255,255,255,.62); border-radius:999px; padding:8px 18px; width:max-content; max-width:760px; text-align:center; font-size:17px; font-weight:850; }}
.section {{ margin:24px 0 0; }}
.section h2 {{ margin:0 0 14px; color:{ACCENT}; text-align:center; font-family:'Songti SC','STSong',serif; font-size:29px; line-height:1.15; font-weight:900; }}
.section h2:before,.section h2:after {{ content:''; display:inline-block; width:78px; border-top:2px solid #D6A89C; margin:0 15px; vertical-align:middle; }}
.logo-hero {{ display:grid; grid-template-columns:170px 1fr; gap:24px; align-items:center; margin:6px 0 24px; }}
.logo-box {{ height:112px; border:2px solid #D8C5B3; border-radius:14px; background:rgba(255,255,255,.76); display:flex; align-items:center; justify-content:center; padding:10px; }}
.logo-box img {{ width:148px; max-height:84px; object-fit:contain; }}
.thesis {{ border-left:7px solid {ACCENT}; padding:8px 0 8px 18px; color:#4B3A2D; font-family:'Songti SC','STSong',serif; font-size:23px; font-weight:900; line-height:1.42; }}
.thesis small {{ display:block; margin-top:5px; color:#8E7969; font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif; font-size:14px; font-weight:700; }}
.grid2 {{ display:grid; grid-template-columns:repeat(2,1fr); gap:13px; }}
.grid3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }}
.card {{ border:2px solid #DFCABB; border-radius:12px; background:rgba(255,255,255,.68); padding:14px 15px; }}
.card h3 {{ margin:0; color:{DEEP}; font-size:20px; line-height:1.25; }}
.card p {{ margin:6px 0 0; font-size:15px; font-weight:650; line-height:1.43; }}
.metric {{ border:2px solid {ACCENT}; border-radius:12px; background:rgba(255,255,255,.76); padding:12px 10px 11px; min-height:124px; text-align:center; }}
.metric .mi {{ display:flex; justify-content:center; height:30px; margin-bottom:4px; }}
.metric .value {{ color:#1C1A19; font-size:25px; font-weight:950; line-height:1.08; white-space:nowrap; }}
.metric .label {{ margin-top:5px; color:#6D5A4B; font-size:14px; font-weight:850; }}
.metric .delta {{ margin-top:4px; font-size:13px; font-weight:900; }}
.positive {{ color:{GREEN}; }} .warning {{ color:{GOLD}; }} .negative {{ color:{RISK}; }} .muted {{ color:#988675; }}
.driver {{ display:grid; grid-template-columns:44px 1fr; gap:10px; min-height:155px; }}
.driver .doodle {{ padding-top:1px; }}
.driver h3 {{ font-size:21px; }}
.driver .proof {{ margin-top:6px; color:{ACCENT}; font-size:19px; font-weight:950; line-height:1.2; }}
.driver .meaning {{ margin-top:6px; color:#59483A; font-size:14px; line-height:1.42; font-weight:650; }}
.profile {{ display:grid; grid-template-columns:repeat(2,1fr); gap:10px 14px; }}
.profile .p {{ border-bottom:1px solid #E0CFC0; padding:0 0 8px; min-height:42px; }}
.profile .k {{ display:block; color:#A07061; font-size:13px; font-weight:850; }}
.profile .v {{ display:block; margin-top:2px; color:#42372F; font-size:16px; font-weight:800; line-height:1.26; }}
.business-card {{ display:grid; grid-template-columns:42px 1fr; gap:10px; min-height:130px; }}
.business-card h3 {{ font-size:19px; }}
.business-card .what {{ margin-top:5px; color:#4C3B2F; font-size:14px; line-height:1.4; font-weight:680; }}
.status-card {{ border:2px solid #DFCABB; border-radius:12px; background:rgba(255,255,255,.72); padding:13px 11px; text-align:center; min-height:118px; }}
.status-card .sicon {{ height:31px; }}
.status-card .big {{ margin-top:4px; color:{ACCENT}; font-size:21px; line-height:1.15; font-weight:950; }}
.status-card .explain {{ margin-top:6px; color:#6F5B4B; font-size:13px; line-height:1.35; font-weight:700; }}
.timeline {{ display:grid; grid-template-columns:repeat(4,1fr); gap:7px; position:relative; }}
.timeline:before {{ content:''; position:absolute; left:8%; right:8%; top:19px; border-top:2px solid #D5AA95; z-index:0; }}
.time {{ position:relative; z-index:1; text-align:center; }}
.time .dot {{ width:12px; height:12px; margin:13px auto 7px; border-radius:50%; background:{ACCENT}; box-shadow:0 0 0 5px #F7F4ED; }}
.time b {{ display:block; color:{DEEP}; font-size:16px; }}
.time span {{ display:block; margin-top:3px; color:#756352; font-size:12px; line-height:1.3; font-weight:700; }}
.wide {{ grid-column:1/-1; }}
.row {{ display:grid; grid-template-columns:150px 1fr 112px; gap:12px; align-items:center; border:1.5px solid #E2CFBF; background:rgba(255,255,255,.64); border-radius:10px; padding:10px 12px; margin-bottom:8px; min-height:56px; }}
.row .tag {{ display:flex; align-items:center; gap:6px; color:{DEEP}; font-size:15px; font-weight:900; }}
.row .detail {{ font-size:14px; line-height:1.35; font-weight:680; }}
.row .right {{ text-align:right; color:{ACCENT}; font-size:14px; font-weight:900; }}
.bar-row {{ display:grid; grid-template-columns:155px 1fr 116px; gap:10px; align-items:center; margin:8px 0; }}
.bar-label {{ display:flex; align-items:center; gap:7px; color:#4B3A2D; font-size:14px; font-weight:850; }}
.track {{ height:16px; overflow:hidden; border-radius:9px; background:#EDE6DE; }}
.bar {{ height:100%; border-radius:9px; }}
.bar-value {{ text-align:right; color:#564334; font-size:14px; font-weight:900; }}
.capital {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }}
.capital .card {{ min-height:128px; }}
.capital .cap-head {{ display:flex; align-items:center; gap:9px; color:{DEEP}; font-size:16px; font-weight:900; }}
.capital .cap-num {{ margin-top:9px; color:#1C1A19; font-size:23px; font-weight:950; line-height:1.1; }}
.capital .cap-sub {{ margin-top:5px; color:#7E6C5C; font-size:13px; line-height:1.35; font-weight:700; }}
.signal-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.signal {{ border:2px solid #DCC6B5; background:rgba(255,255,255,.64); border-radius:12px; padding:12px 14px; }}
.signal.good {{ border-color:#A8D3BD; }} .signal.bad {{ border-color:#E3B8B5; }}
.signal h3 {{ display:flex; align-items:center; gap:8px; margin:0 0 7px; font-size:18px; color:{DEEP}; }}
.signal.good h3 {{ color:{GREEN}; }} .signal.bad h3 {{ color:{RISK}; }}
.signal ul {{ margin:0; padding-left:18px; }}
.signal li {{ margin:5px 0; font-size:14px; line-height:1.36; font-weight:680; }}
.ownership-note {{ margin:0 0 8px; color:#8C796A; text-align:center; font-size:12px; font-weight:700; }}
.holder-row {{ display:grid; grid-template-columns:215px 104px 1fr 118px; align-items:center; gap:10px; border:1.5px solid #E0CBBB; border-radius:10px; background:rgba(255,255,255,.68); padding:10px 12px; margin-bottom:7px; min-height:52px; }}
.holder-name {{ display:flex; gap:8px; align-items:center; font-size:15px; font-weight:900; color:{DEEP}; }}
.holder-stake {{ color:{ACCENT}; font-size:16px; font-weight:950; }}
.holder-shares {{ color:#5A493B; font-size:13px; font-weight:750; }}
.holder-value {{ color:#1F1D1B; font-size:14px; font-weight:900; text-align:right; }}
.flywheel {{ display:grid; grid-template-columns:repeat(5,1fr); gap:7px; align-items:stretch; }}
.fly {{ position:relative; border:2px solid #E0CABB; border-radius:10px; background:rgba(255,255,255,.66); padding:10px 8px; text-align:center; min-height:102px; }}
.fly:not(:last-child):after {{ content:'›'; position:absolute; right:-11px; top:35px; color:{GOLD}; font-size:28px; font-weight:950; z-index:1; }}
.fly .ficon {{ height:31px; }} .fly b {{ display:block; margin-top:3px; color:{DEEP}; font-size:14px; line-height:1.2; }} .fly span {{ display:block; margin-top:4px; color:#806F5F; font-size:12px; line-height:1.25; font-weight:700; }}
.culture-stack {{ display:grid; grid-template-columns:1fr; gap:12px; }}
.culture-card {{ display:grid; grid-template-columns:58px 1fr; gap:14px; min-height:190px; }}
.culture-card h3 {{ margin:0; color:{DEEP}; font-size:22px; }}
.culture-card .rule {{ margin-top:6px; color:#4C3B2E; font-size:14px; line-height:1.42; font-weight:680; }}
.culture-card .case {{ margin-top:6px; color:{ACCENT}; font-size:13px; line-height:1.4; font-weight:800; }}
.culture-card .lesson {{ margin-top:7px; padding:6px 9px; border-left:4px solid {GREEN}; background:rgba(33,134,90,.07); color:#3F5548; font-size:13px; line-height:1.35; font-weight:800; }}
.culture-card .lens {{ display:inline-block; margin-top:7px; padding:3px 7px; border-radius:6px; color:white; background:{ACCENT}; font-size:11px; font-weight:900; }}
footer {{ width:100%; margin-top:22px; padding:13px 12px 20px; border-top:1px solid #E5D5C8; color:#A49180; text-align:center; font-size:11px; font-weight:600; line-height:1.55; }}
.signature {{ margin-top:7px; color:#A49180; font-size:12px; font-weight:600; }}
</style></head>
<body><main class='page'><h1 class='title'>{title}</h1><div class='subtitle'>{subtitle}</div>{body}{footer(foot)}</main></body></html>"""


FOOT_COMMON = [
    "经营数据：The Coca-Cola Company FY2025 Form 10-K，FY2025：2025年1-12月",
    "行情数据：StockAnalysis，收盘：2026年7月9日；市值、估值与机构持仓估值按该日价格计算",
    "股东与资本：2026 Proxy、伯克希尔 Q1 2026 13F；其他机构为公开 13F 申报实体，可能含被动指数/受托资金",
    "汇率口径：全部金额均为美元；公司财报本身以美元披露，无需换汇",
    "免责声明：本图仅供学习参考，不构成投资建议",
]


def metric(value: str, label: str, i: str, delta: str = "", color: str = "muted") -> str:
    delta_html = f"<div class='delta {color}'>{delta}</div>" if delta else "<div class='delta muted'>&nbsp;</div>"
    return f"<div class='metric'><div class='mi'>{icon(i, ACCENT, 30)}</div><div class='value'>{value}</div><div class='label'>{label}</div>{delta_html}</div>"


def overview() -> str:
    profile = "".join([
        "<div class='p'><span class='k'>公司全称</span><span class='v'>The Coca-Cola Company</span></div>",
        "<div class='p'><span class='k'>历史</span><span class='v'>品牌始于1886年 · 公司成立于1892年</span></div>",
        "<div class='p'><span class='k'>总部地址</span><span class='v'>Atlanta, Georgia, USA</span></div>",
        "<div class='p'><span class='k'>交易所及代码</span><span class='v'>NYSE: KO</span></div>",
        "<div class='p'><span class='k'>现任CEO</span><span class='v'>Henrique Braun · 2026年3月就任</span></div>",
        "<div class='p'><span class='k'>执行董事长</span><span class='v'>James Quincey</span></div>",
        "<div class='p'><span class='k'>员工人数</span><span class='v'>约65,900人 · 美国约8,900人</span></div>",
        "<div class='p'><span class='k'>公司定位</span><span class='v'>全球全品类饮料公司</span></div>",
    ])
    business = "".join([
        f"<div class='card business-card'><div>{icon('bottle', ACCENT, 38)}</div><div><h3>品牌与浓缩液</h3><div class='what'>管理品牌、配方与营销，向装瓶伙伴销售浓缩液、糖浆及相关原料。</div></div></div>",
        f"<div class='card business-card'><div>{icon('network', GOLD, 38)}</div><div><h3>成品饮料与装瓶</h3><div class='what'>在部分市场直接装瓶和销售，并通过独立装瓶商、经销商与零售商触达消费者。</div></div></div>",
        f"<div class='card business-card wide'><div>{icon('brands', GREEN, 38)}</div><div><h3>全品类饮料组合</h3><div class='what'>覆盖气泡饮料、水、运动饮料、咖啡、茶、果汁、乳制品、植物饮料、能量饮料与预调酒。</div></div></div>",
    ])
    status = "".join([
        f"<div class='status-card'><div class='sicon'>{icon('market', ACCENT, 30)}</div><div class='big'>200+ 国家 · 每天22亿份</div><div class='explain'>全球覆盖与日常消费规模</div></div>",
        f"<div class='status-card'><div class='sicon'>{icon('can', GOLD, 30)}</div><div class='big'>338亿箱 · 商标可乐47%</div><div class='explain'>FY2025标准箱销量与核心品牌占比</div></div>",
        f"<div class='status-card'><div class='sicon'>{icon('network', GREEN, 30)}</div><div class='big'>200+伙伴 · 950+设施</div><div class='explain'>本地装瓶与生产网络</div></div>",
    ])
    timeline = "".join([
        "<div class='time'><div class='dot'></div><b>1886</b><span>亚特兰大诞生首杯可口可乐</span></div>",
        "<div class='time'><div class='dot'></div><b>1892</b><span>The Coca-Cola Company成立</span></div>",
        "<div class='time'><div class='dot'></div><b>1919</b><span>股票开始在NYSE交易</span></div>",
        "<div class='time'><div class='dot'></div><b>2026</b><span>Henrique Braun接任CEO</span></div>",
    ])
    body = f"""
    <div class='strap'>140年品牌历史 × 全球全品类饮料公司 × 本地化装瓶网络</div>
    <div class='logo-hero'><div class='logo-box'><img src='{LOGO}'></div><div class='thesis'>从1886年亚特兰大的一杯汽水，发展成覆盖全球200多个国家和地区的饮料系统。<small>这张图只回答：它是谁、做什么、规模多大、处于什么行业位置。</small></div></div>
    <section class='section'><h2>基本信息</h2><div class='profile'>{profile}</div></section>
    <section class='section'><h2>业务范围</h2><div class='grid2'>{business}</div></section>
    <section class='section'><h2>行业地位与核心亮点</h2><div class='grid3'>{status}</div></section>
    <section class='section'><h2>关键历史节点</h2><div class='timeline'>{timeline}</div></section>"""
    foot = [
        "档案与历史：Coca-Cola官网历史页、Shareowners FAQ，核查：2026年7月",
        "业务与规模：The Coca-Cola Company FY2025 Form 10-K，2025年1-12月",
        "领导层：Henrique Braun于2026年3月31日就任CEO；James Quincey转任执行董事长",
        "品牌资产：The Coca-Cola Company投资者关系官网官方Logo",
        "免责声明：本图仅供学习参考，不构成投资建议",
    ]
    return document("可口可乐公司档案", "The Coca-Cola Company · NYSE: KO · Company Profile", body, foot, 1480)


def strategy() -> str:
    drivers = "".join([
        f"<div class='card driver'><div class='doodle'>{icon('can', ACCENT, 40)}</div><div><h3>商标可乐</h3><div class='proof'>47% 全球标准箱销量</div><div class='meaning'>一个核心商标占全球 338 亿标准箱销量近半；这是渠道谈判和价格体系的主锚点。</div></div></div>",
        f"<div class='card driver'><div class='doodle'>{icon('network', GOLD, 40)}</div><div><h3>装瓶与分销网络</h3><div class='proof'>200+ 伙伴 / 950+ 工厂</div><div class='meaning'>装瓶伙伴负责本地制造与配送，系统覆盖 200+ 国家和地区，后来者很难从零复制。</div></div></div>",
        f"<div class='card driver'><div class='doodle'>{icon('bottle', GREEN, 40)}</div><div><h3>浓缩液特许模式</h3><div class='proof'>装瓶投资收入：52% → 12%</div><div class='meaning'>从 2015 到 2025，重资产装瓶比重下降，母公司把资源集中在品牌、配方与浓缩液。</div></div></div>",
        f"<div class='card driver'><div class='doodle'>{icon('brands', DEEP, 40)}</div><div><h3>多品类品牌组合</h3><div class='proof'>约 200 品牌 / 30 个 $1B 品牌</div><div class='meaning'>不只依赖汽水；多品类组合提高货架效率，也降低单品类口味变化的冲击。</div></div></div>",
    ])
    fly = "".join([
        f"<div class='fly'><div class='ficon'>{icon('brands', ACCENT, 29)}</div><b>品牌心智</b><span>47% 核心商标销量</span></div>",
        f"<div class='fly'><div class='ficon'>{icon('network', GOLD, 29)}</div><b>渠道周转</b><span>200+ 装瓶伙伴</span></div>",
        f"<div class='fly'><div class='ficon'>{icon('up', GREEN, 29)}</div><b>定价组合</b><span>FY25 +4%</span></div>",
        f"<div class='fly'><div class='ficon'>{icon('cash', DEEP, 29)}</div><b>现金回收</b><span>经营现金流 $7.4B</span></div>",
        f"<div class='fly'><div class='ficon'>{icon('coin', ACCENT, 29)}</div><b>股东回报</b><span>年化 $2.12/股</span></div>",
    ])
    body = f"""
    <div class='strap'>长期定位 × 核心业务 × 数据化护城河</div>
    <div class='logo-hero'><div class='logo-box'><img src='{LOGO}'></div><div class='thesis'>用品牌和浓缩液连接全球装瓶伙伴，让饮料在当地货架持续周转。<small>长期目标不是自己经营每一家工厂，而是以较轻的资产占据品牌、配方和系统控制点。</small></div></div>
    <section class='section'><h2>核心业务与硬指标</h2><div class='grid2'>{drivers}</div></section>
    <section class='section'><h2>增长飞轮</h2><div class='flywheel'>{fly}</div></section>
    <section class='section'><h2>近两年可观察动作</h2>
      <div class='row'><div class='tag'>{icon('up', ACCENT, 25)}量价管理</div><div class='detail'>FY2025 <b>价格/组合 +4%</b>；在全球箱销量持平下，以品牌和组合改善驱动收入。</div><div class='right positive'>+4%</div></div>
      <div class='row'><div class='tag'>{icon('capex', GOLD, 25)}系统投入</div><div class='detail'>公司公开 FY2026 资本开支指引约 <b>$2.2B</b>，继续支持运营系统和增长项目。</div><div class='right warning'>$2.2B</div></div>
    </section>"""
    foot = FOOT_COMMON + ["核心业务证据：FY2025 Form 10-K；Coca-Cola System / Brands 官网，核查：2026年7月"]
    return document("可口可乐的经营之道", "Coca-Cola · Brand + Concentrate + Bottling Playbook", body, foot, 1600)


def panorama() -> str:
    top = "".join([
        metric('$47.9B','FY2025 营收','up','同比 +1.9%','positive'),
        metric('$13.8B','FY2025 经营利润','profit','同比 +37.7%','positive'),
        metric('$7.4B','FY2025 经营现金流','cash','同比 +8.9%','positive'),
        metric('$13.1B','FY2025 净利润','coin','同比 +23.3%','positive'),
        metric('$355.5B','当前市值','market','最新收盘','warning'),
        metric('26.43x / 25.44x','PE / Forward PE','scale','当前估值','muted'),
    ])
    bars = "".join([
        f"<div class='bar-row'><div class='bar-label'>{icon('market', ACCENT, 22)}北美</div><div class='track'><div class='bar' style='width:100%;background:{ACCENT}'></div></div><div class='bar-value'>$19.6B · 40.8%</div></div>",
        f"<div class='bar-row'><div class='bar-label'>{icon('market', GOLD, 22)}EMEA</div><div class='track'><div class='bar' style='width:55%;background:{GOLD}'></div></div><div class='bar-value'>$10.8B · 22.6%</div></div>",
        f"<div class='bar-row'><div class='bar-label'>{icon('market', GREEN, 22)}拉丁美洲</div><div class='track'><div class='bar' style='width:32%;background:{GREEN}'></div></div><div class='bar-value'>$6.3B · 13.2%</div></div>",
        f"<div class='bar-row'><div class='bar-label'>{icon('market', DEEP, 22)}装瓶投资</div><div class='track'><div class='bar' style='width:29%;background:{DEEP}'></div></div><div class='bar-value'>$5.7B · 12.0%</div></div>",
        f"<div class='bar-row'><div class='bar-label'>{icon('market', '#6A7B88', 22)}亚太</div><div class='track'><div class='bar' style='width:27%;background:#6A7B88'></div></div><div class='bar-value'>$5.3B · 11.1%</div></div>",
    ])
    holders = "".join([
        f"<div class='holder-row'><div class='holder-name'>{icon('holders', ACCENT, 24)}伯克希尔·哈撒韦</div><div class='holder-stake'>9.29%</div><div class='holder-shares'>4.00 亿股 · 巴菲特长期持仓</div><div class='holder-value'>约 $33.1B</div></div>",
        f"<div class='holder-row'><div class='holder-name'>{icon('holders', GOLD, 24)}Vanguard Capital Mgmt</div><div class='holder-stake'>5.52%</div><div class='holder-shares'>2.37 亿股 · 13F 申报实体</div><div class='holder-value'>约 $19.6B</div></div>",
        f"<div class='holder-row'><div class='holder-name'>{icon('holders', GREEN, 24)}BlackRock Inst. Trust</div><div class='holder-stake'>4.87%</div><div class='holder-shares'>2.10 亿股 · 13F 申报实体</div><div class='holder-value'>约 $17.3B</div></div>",
        f"<div class='holder-row'><div class='holder-name'>{icon('holders', DEEP, 24)}State Street IM</div><div class='holder-stake'>3.89%</div><div class='holder-shares'>1.67 亿股 · 13F 申报实体</div><div class='holder-value'>约 $13.8B</div></div>",
    ])
    body = f"""
    <div class='strap'>财务表现 × 业务结构 × 资本配置 × 机构持仓</div>
    <section class='section'><h2>核心财务</h2><div class='grid3'>{top}</div></section>
    <section class='section'><h2>业务分部表现</h2>{bars}</section>
    <section class='section'><h2>资本配置与股东回报</h2><div class='capital'>
      <div class='card'><div class='cap-head'>{icon('chart', ACCENT, 28)}资本效率</div><div class='cap-num'>ROIC +6pct</div><div class='cap-sub'>公司公开目标口径：2025 较 2015 改善；未披露绝对 ROIC。</div></div>
      <div class='card'><div class='cap-head'>{icon('capex', GOLD, 28)}2026 CapEx</div><div class='cap-num'>$2.2B</div><div class='cap-sub'>公司公开指引；FY2025 实际资本开支 $2.1B。</div></div>
      <div class='card'><div class='cap-head'>{icon('coin', GREEN, 28)}股东分红</div><div class='cap-num'>$2.12/股</div><div class='cap-sub'>年化股息；按行情日约 2.6%，FY25 现金分红 $8.8B。</div></div>
    </div></section>
    <section class='section'><h2>亮点与风险</h2><div class='signal-grid'>
      <div class='signal good'><h3>{icon('up', GREEN, 26)}亮点</h3><ul><li><b>价格/组合 +4%</b>：量持平下仍能推动全年收入增长。</li><li><b>经营现金流 $7.4B</b>：同比 <b>+8.9%</b>，支撑分红和系统投入。</li></ul></div>
      <div class='signal bad'><h3>{icon('risk', RISK, 26)}风险</h3><ul><li><b>北美箱销量 -1%</b>：成熟市场的量增压力仍在。</li><li><b>全球箱销量持平</b>：增长更依赖价格/组合，量价平衡需持续跟踪。</li></ul></div>
    </div></section>
    <section class='section'><h2>重要机构持仓</h2><div class='ownership-note'>持仓为公开 Proxy / Q1 2026 13F 申报；金额按 2026年7月9日收盘价估算，不等同于主动看多。</div>{holders}</section>"""
    foot = FOOT_COMMON + ["ROI口径：公司公开为 ROIC 较 2015 改善 6 个百分点，未披露绝对值；非自行估算", "2026 CapEx：FY2025 Form 10-K，指引约 $2.2B；股东分红：FY2025 $8.779B，年化 $2.12/股"]
    return document("可口可乐 FY2025 经营全景", "The Coca-Cola Company · NYSE: KO · 已交付的全年经营成果", body, foot, 1860)


def culture() -> str:
    cards = "".join([
        f"<div class='card culture-card'><div>{icon('network', ACCENT, 47)}</div><div><h3>全球能力统一建设，本地市场拥有执行权</h3><div class='rule'><b>做法：</b>地区团队靠近消费者执行；全球品类团队负责品牌与创新；Platform Services统一承接数据、消费者洞察和共享服务。</div><div class='case'><b>案例：</b>2020年把17个业务单元压缩为9个运营单元，并设置5个全球品类团队，减少重复部门、加快跨市场复制。</div><div class='lesson'>可借鉴：靠近客户的人决策，重复建设的能力统一平台化。</div><span class='lens'>组织</span></div></div>",
        f"<div class='card culture-card'><div>{icon('chart', GOLD, 47)}</div><div><h3>把文化变成可招聘、可反馈的行为</h3><div class='rule'><b>做法：</b>用Curious、Empowered、Inclusive、Agile四种可观察行为管理；Agile明确要求先做1.0，再通过真实反馈迭代2.0、3.0。</div><div class='case'><b>案例：</b>Aon测评用于部分候选人和员工；Performance Enablement与匿名文化调查评估领导、团队和工作体验，并与历史结果比较。公司每季度安排高管员工问答。</div><div class='lesson'>可借鉴：价值观要进入招聘、领导标准、日常反馈和员工调查。</div><span class='lens'>人才｜组织</span></div></div>",
        f"<div class='card culture-card'><div>{icon('holders', GREEN, 47)}</div><div><h3>用真实项目培养人，而不是只靠上课</h3><div class='rule'><b>做法：</b>Thrive Opportunity Marketplace按员工的技能、兴趣和时间，把短期项目与内部人才匹配；员工不用等待正式岗位空缺。</div><div class='case'><b>案例：</b>Blaze项目持续24个月，安排4次、每次6个月轮岗；现任CEO Henrique Braun在公司跨地区、跨职能历练近30年后升任CEO。</div><div class='lesson'>可借鉴：把项目变成培养岗位，建立公司内部的人才市场。</div><span class='lens'>人才</span></div></div>",
    ])
    body = f"""
    <div class='strap'>网络化组织 × 行为管理闭环 × 内部人才市场</div>
    <div class='logo-hero'><div class='logo-box'><img src='{LOGO}'></div><div class='thesis'>真正值得学习的，不是四句文化口号，而是把全球分权、统一能力、人才流动和员工反馈做成一套可以运行的管理系统。<small>以下三项分别回答：怎样组织、怎样管理行为、怎样培养人才。</small></div></div>
    <section class='section'><h2>三个有辨识度的管理机制</h2><div class='culture-stack'>{cards}</div></section>"""
    foot = [
        "组织机制：Coca-Cola Networked Organization官方公告，2020年；FY2025 Form 10-K",
        "行为管理：Coca-Cola Purpose & Growth Culture、Leadership and Growth Insights、FY2025 Form 10-K",
        "人才发展：Thrive Opportunity Marketplace、Career Development、Blaze项目及Henrique Braun官方履历",
        "汇率口径：本页无非美元金额；所有日期与资料来源均在脚注列示",
        "免责声明：本图仅供学习参考，不构成投资建议",
    ]
    return document("可口可乐如何管理65,900名员工", "Coca-Cola · Management Culture · 可运行的组织与人才系统", body, foot, 1370)


def packet() -> dict:
    return {
        "company": "可口可乐",
        "rank": 36,
        "output_root": str(ROOT),
        "logo": {
            "official_source_url": "https://investors.coca-colacompany.com/_assets/_21a1fde0eaf729cf43cb6530ca4f2225/cocacolacompany/logo.png",
            "retrieved": "2026年7月",
            "sha256": "17618360a606872158861906d1f2c59372460c34ef5cba115f034f93738ec1d0",
            "path": "/Users/jiangming/templates/assets/company_logos/cocacola-official.png",
        },
        "currency": {"display": "USD", "exchange_rate_note": "主图以 $ 表示美元；财报与行情均为美元，无需换汇。"},
        "company_profile": {
            "公司全称": "The Coca-Cola Company", "成立时间": "品牌始于1886年；公司成立于1892年", "总部地址": "Atlanta, Georgia, USA", "交易所及代码": "NYSE: KO", "CEO / 主要负责人": "Henrique Braun（CEO）；James Quincey（执行董事长）", "员工人数": "65,900人", "核心业务": "品牌与浓缩液、成品饮料与装瓶、全品类饮料组合", "当前市值": "$355.5B",
        },
        "panorama_top_grid": {
            "FY2025 营收": {"value": "$47.9B", "yoy": "+1.9%", "source": "Coca-Cola FY2025 Form 10-K"},
            "FY2025 经营利润": {"value": "$13.8B", "yoy": "+37.7%", "source": "Coca-Cola FY2025 Form 10-K"},
            "FY2025 经营现金流": {"value": "$7.4B", "yoy": "+8.9%", "source": "Coca-Cola FY2025 Form 10-K"},
            "FY2025 净利润": {"value": "$13.1B", "yoy": "+23.3%", "source": "Coca-Cola FY2025 Form 10-K"},
            "当前市值": {"value": "$355.5B", "as_of": "2026年7月9日", "source": "StockAnalysis"},
            "PE / Forward PE": {"value": "26.43x / 25.44x", "as_of": "2026年7月9日", "source": "StockAnalysis"},
        },
        "core_drivers": [
            {"name": "商标可乐", "metric": "47% 全球标准箱销量", "evidence_kind": "销量或产量", "industry_meaning": "行业含义：单一核心商标占全球销量近一半，品牌心智与定价权有直接量化基础。", "icon": "can", "why_it_matters": "FY2025 商标可乐占全球338亿标准箱销量的47%。", "source": "Coca-Cola FY2025 Form 10-K，2026年2月"},
            {"name": "全球装瓶与分销体系", "metric": "200+ 伙伴 / 950+ 工厂", "evidence_kind": "渠道网络", "industry_meaning": "行业含义：本地装瓶和配送网络把品牌落到当地货架，渠道密度难以复制。", "icon": "network", "why_it_matters": "系统覆盖200+国家和地区。", "source": "Coca-Cola System 官网，核查2026年7月"},
            {"name": "浓缩液特许模式", "metric": "装瓶收入占 12%", "evidence_kind": "业务收入或占比", "industry_meaning": "行业含义：重资产装瓶比重下降，母公司更专注品牌、浓缩液与资本回报。", "icon": "bottle", "why_it_matters": "装瓶投资收入由2015年的52%降至2025年的12%。", "source": "Coca-Cola System 官网，口径截至2025年12月"},
            {"name": "多品类品牌组合", "metric": "约200品牌 / 30个$1B品牌", "evidence_kind": "品牌或产品组合", "industry_meaning": "行业含义：跨品类组合提高渠道谈判与货架效率，减少对单一汽水类别的依赖。", "icon": "brands", "why_it_matters": "官网披露约200个品牌，其中30个为十亿美元级品牌。", "source": "Coca-Cola Brands 官网，核查2026年7月"},
        ],
        "capital": {
            "roi": {"value": "ROIC较2015年 +6pct", "source": "Coca-Cola Financial Ambition，2025口径；未披露绝对ROIC"},
            "capex_2026": {"value": "$2.2B（公司指引）", "source": "Coca-Cola FY2025 Form 10-K，2026年2月"},
            "shareholder_return": {"value": "$2.12/股，股息率约2.6%，FY2025分红$8.8B", "source": "FY2025 Form 10-K / StockAnalysis，2026年7月"},
        },
        "major_holders": [
            {"name": "伯克希尔·哈撒韦", "kind": "机构", "stake": "9.29%", "estimated_value": "约$33.1B", "source": "Coca-Cola 2026 Proxy；Berkshire Q1 2026 13F，4.00亿股"},
            {"name": "Vanguard Capital Management", "kind": "机构", "stake": "5.52%", "estimated_value": "约$19.6B", "source": "Q1 2026 13F申报实体，2.37亿股；按2026年7月9日收盘价估算"},
            {"name": "BlackRock Institutional Trust", "kind": "机构", "stake": "4.87%", "estimated_value": "约$17.3B", "source": "Q1 2026 13F申报实体，2.10亿股；按2026年7月9日收盘价估算"},
            {"name": "State Street Investment Management", "kind": "机构", "stake": "3.89%", "estimated_value": "约$13.8B", "source": "Q1 2026 13F申报实体，1.67亿股；按2026年7月9日收盘价估算"},
        ],
        "management_culture": [
            {"lens": "组织", "principle": "全球能力统一建设，本地市场拥有执行权", "practice": "做法：地区团队负责贴近消费者执行，全球品类团队负责品牌与创新，Platform Services统一承接共享能力。", "case_or_number": "案例：2020年把17个业务单元压缩为9个运营单元，并设置5个全球品类团队，减少重复部门、加快跨区域复制。", "source": "Coca-Cola Networked Organization官方公告，2020年；FY2025 Form 10-K"},
            {"lens": "人才", "principle": "把文化变成可招聘、可反馈的行为", "practice": "做法：以Curious、Empowered、Inclusive、Agile四种可观察行为贯穿招聘评估、领导标准和员工反馈。", "case_or_number": "案例：Aon测评用于部分候选人与员工；匿名文化调查与历史结果比较，公司每季度安排高管员工问答。", "source": "Coca-Cola Leadership and Growth Insights；FY2025 Form 10-K"},
            {"lens": "人才", "principle": "用真实项目培养人", "practice": "做法：Thrive Opportunity Marketplace按技能、兴趣和时间匹配内部短期项目。", "case_or_number": "数字：Blaze为24个月项目，包含4次、每次6个月轮岗；Henrique Braun在公司历练近30年后升任CEO。", "source": "Coca-Cola Career Development；Blaze项目；Henrique Braun官方履历，核查2026年7月"},
        ],
        "footer_lines": FOOT_COMMON + ["ROI口径：公司公开ROIC较2015年改善6个百分点，未披露绝对值", "管理文化：Networked Organization、Growth Culture、Thrive / Blaze，核查：2026年7月", "by 江明"],
    }


def main() -> None:
    HTML.mkdir(parents=True, exist_ok=True)
    PACKET.parent.mkdir(parents=True, exist_ok=True)
    pages = {
        "cocacola_company.html": overview(),
        "cocacola_strategy.html": strategy(),
        "cocacola_panorama.html": panorama(),
        "cocacola_culture.html": culture(),
    }
    for name, content in pages.items():
        (HTML / name).write_text(content, encoding="utf-8")
    PACKET.write_text(json.dumps(packet(), ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", ", ".join(pages))
    print(PACKET)


if __name__ == "__main__":
    main()
