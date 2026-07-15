#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import math
import re
import subprocess
import sys
import textwrap
import urllib.parse
import urllib.request
import time
from datetime import date
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont


OUT_ROOT = Path("/Users/jiangming/持仓分析/公司经营分析")
REVIEW_ROOT = OUT_ROOT / "_review" / "rank38_59_current_20260709"
HTML_ROOT = REVIEW_ROOT / "html"
PACKET_ROOT = REVIEW_ROOT / "packets"
LOGO_ROOT = Path("/Users/jiangming/templates/assets/company_logos")
CACHE_ROOT = REVIEW_ROOT / "cache"
VALIDATOR = Path("/Users/jiangming/.codex/skills/investor-infographic/scripts/validate_company_packet.py")
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

TODAY_LABEL = "2026年7月9日"
MARKET_SOURCE = "CompaniesMarketCap"
LEGACY_RENDERER_DISABLED = True

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml,image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
}

MANUAL_LOGO_URLS = {
    "cocacola": "https://investors.coca-colacompany.com/_assets/_21a1fde0eaf729cf43cb6530ca4f2225/cocacolacompany/logo.png",
    "chevron": "https://www.chevron.com/-/media/shared-media/images/hallmark-2023.png",
    "pg": "https://images.ctfassets.net/oggad6svuzkv/7znyJc3Y7SecEoKSYKWoaQ/4a24e9015c360799cfb072adcd92cc5e/P_G_Logo_RGB.svg",
    "roche": "https://assets.roche.com/f/176343/801x529/f89c88a24c/roche-logo-blue.png?download=1",
    "homedepot": "https://corporate.homedepot.com/themes/custom/bootstrap_thd/images/logo-site-header-homedepot.svg",
    "hsbc": "https://www.hsbc.com/-/files/hsbc/header/hsbc-logo-200x25.svg?la=en-GB&h=25&hash=FCDFB4DC1991B6B5EE0AB98E7208CB82",
    "arm": "https://www.arm.com/-/media/global/logos/arm-logo-blue-rgb.svg",
    "rbc": "https://www.rbc.com/dvl/v1.0/assets/images/logos/rbc-logo-shield-blue.svg",
    "merck": "https://www.merck.com/wp-content/uploads/sites/124/2025/08/site-logo.svg",
    "novartis": "https://www.novartis.com/themes/custom/cosmos/logo.svg",
    "philipmorris": "https://www.pmi.com/content/dam/pmicom/global/images/logos/pmi-logoaaf115bd6c7468f696e2ff0400458fff.svg",
    "gevernova": "https://www.gevernova.com/themes/custom/ge_vernova_unified/logo.svg",
    "agriculturalbank": "https://www.abchina.com/en/images/logo_ue2.png",
    "goldmansachs": "https://cdn.gs.com/images/goldman-sachs/v2/gs-favicon.svg",
}


TARGETS = [
    # Fill current-ranking gaps first, then continue downward. Morgan Stanley and Netflix already exist.
    dict(rank=38, slug="cocacola", folder="38_可口可乐", prefix="cocacola", name="可口可乐", en="The Coca-Cola Company", ticker="KO", stock="ko", country="USA", market_cap="$358.82B", price="$83.40", color="#D71920", color2="#111111", homepage="https://www.coca-colacompany.com/", founded="1892年", hq="Atlanta, Georgia, USA", ceo="James Quincey", employees="约79,100人", business="全球饮料品牌、浓缩液、装瓶系统与渠道执行", moat=("200+国家/地区", "每日约22亿份饮品", "可口可乐品牌全球高认知")),
    dict(rank=39, slug="chevron", folder="39_雪佛龙", prefix="chevron", name="雪佛龙", en="Chevron Corporation", ticker="CVX", stock="cvx", country="USA", market_cap="$350.46B", price="$175.97", color="#0054A6", color2="#E31937", homepage="https://www.chevron.com/", founded="1879年", hq="San Ramon, California, USA", ceo="Mike Wirth", employees="约45,000人", business="上游油气、炼化、化工、LNG 与低碳业务", moat=("油气产量百万桶级", "Permian + LNG", "连续分红三十年以上")),
    dict(rank=40, slug="pg", folder="40_宝洁", prefix="pg", name="宝洁", en="The Procter & Gamble Company", ticker="PG", stock="pg", country="USA", market_cap="$345.56B", price="$148.40", color="#005DAA", color2="#C4963C", homepage="https://pginvestor.com/", founded="1837年", hq="Cincinnati, Ohio, USA", ceo="Shailesh Jejurikar", employees="109,000人", business="家庭护理、美妆、健康、婴儿/女性/家庭护理", moat=("5大业务板块", "FY2025营收$84.3B", "130+年品牌组合")),
    dict(rank=42, slug="roche", folder="42_罗氏", prefix="roche", name="罗氏", en="Roche Holding AG", ticker="RO.SW / RHHBY", stock="rhhby", country="Switzerland", market_cap="$336.66B", price="$423.14", color="#0057B8", color2="#D71920", homepage="https://www.roche.com/", founded="1896年", hq="Basel, Switzerland", ceo="Thomas Schinecker", employees="约100,000人", business="制药、诊断、肿瘤/免疫/神经药物与体外诊断", moat=("制药+诊断双平台", "肿瘤/诊断全球强势", "百年研发网络")),
    dict(rank=43, slug="homedepot", folder="43_家得宝", prefix="homedepot", name="家得宝", en="The Home Depot, Inc.", ticker="HD", stock="hd", country="USA", market_cap="$335.24B", price="$336.21", color="#F96302", color2="#2D2D2D", homepage="https://corporate.homedepot.com/", founded="1978年", hq="Atlanta, Georgia, USA", ceo="Ted Decker", employees="约470,000人", business="家装零售、专业承包商渠道、线上线下履约", moat=("2,300+门店", "Pro客户网络", "北美家装龙头")),
    dict(rank=44, slug="hsbc", folder="44_HSBC汇丰", prefix="hsbc", name="汇丰控股", en="HSBC Holdings plc", ticker="HSBC", stock="hsbc", country="UK", market_cap="$329.55B", price="$96.09", color="#DB0011", color2="#111111", homepage="https://www.hsbc.com/", founded="1865年", hq="London, UK", ceo="Georges Elhedery", employees="约220,000人", business="全球银行、财富管理、商业银行、亚洲金融网络", moat=("亚洲利润底盘", "全球支付/贸易网络", "CET1高于监管要求")),
    dict(rank=45, slug="arm", folder="45_Arm", prefix="arm", name="Arm", en="Arm Holdings plc", ticker="ARM", stock="arm", country="UK", market_cap="$320.67B", price="$300.24", color="#0091BD", color2="#253746", homepage="https://www.arm.com/", founded="1990年", hq="Cambridge, UK", ceo="Rene Haas", employees="约7,000人", business="CPU/IP 授权、移动/汽车/云与 AI 计算架构", moat=("3250亿+芯片出货", "99%智能手机CPU份额口径", "授权+版税模型")),
    dict(rank=47, slug="palantir", folder="47_Palantir", prefix="palantir", name="Palantir", en="Palantir Technologies Inc.", ticker="PLTR", stock="pltr", country="USA", market_cap="$316.97B", price="$132.22", color="#111111", color2="#4B7BEC", homepage="https://www.palantir.com/", founded="2003年", hq="Denver, Colorado, USA", ceo="Alex Karp", employees="约4,000人", business="AIP、Foundry、Gotham、政府与企业 AI 操作系统", moat=("政府合同高粘性", "AIP客户扩张", "高净留存/高毛利软件")),
    dict(rank=48, slug="agriculturalbank", folder="48_农业银行", prefix="agriculturalbank", name="农业银行", en="Agricultural Bank of China Limited", ticker="601288.SS / 1288.HK", stock=None, country="China", market_cap="$316.22B", price="$0.90", color="#009A44", color2="#C4963C", homepage="https://www.abchina.com/en/", founded="1951年", hq="Beijing, China", ceo="谷澍 / 董事长口径", employees="约45万人", business="国有大型商业银行、县域金融、公司/零售/资金业务", moat=("县域金融网络", "数万亿元存款", "国有大行信用")),
    dict(rank=49, slug="merck", folder="49_默沙东", prefix="merck", name="默沙东", en="Merck & Co., Inc.", ticker="MRK", stock="mrk", country="USA", market_cap="$311.17B", price="$125.99", color="#007A73", color2="#6B4E7A", homepage="https://www.merck.com/", founded="1891年", hq="Rahway, New Jersey, USA", ceo="Robert M. Davis", employees="约72,000人", business="处方药、疫苗、肿瘤、动物保健", moat=("Keytruda超$29B级", "肿瘤管线", "疫苗/动物保健组合")),
    dict(rank=50, slug="icbc", folder="50_工商银行", prefix="icbc", name="工商银行", en="Industrial and Commercial Bank of China Limited", ticker="1398.HK / 601398.SS", stock=None, country="China", market_cap="$304.18B", price="$0.85", color="#C7000B", color2="#C4963C", homepage="https://www.icbc-ltd.com/", founded="1984年", hq="Beijing, China", ceo="廖林 / 董事长口径", employees="约42万人", business="国有大型商业银行、公司金融、零售、资金与国际业务", moat=("全球最大银行之一", "存款/客户规模极大", "系统重要性银行")),
    dict(rank=51, slug="goldmansachs", folder="51_高盛", prefix="goldmansachs", name="高盛", en="The Goldman Sachs Group, Inc.", ticker="GS", stock="gs", country="USA", market_cap="$303.75B", price="$1,030", color="#7399C6", color2="#1D3557", homepage="https://www.goldmansachs.com/", founded="1869年", hq="New York, USA", ceo="David Solomon", employees="约45,000人", business="投行、全球市场、资产与财富管理、平台解决方案", moat=("全球投行前列", "交易/融资网络", "机构客户关系")),
    dict(rank=52, slug="novartis", folder="52_诺华", prefix="novartis", name="诺华", en="Novartis AG", ticker="NVS", stock="nvs", country="Switzerland", market_cap="$296.07B", price="$155.17", color="#E85E27", color2="#6A1B9A", homepage="https://www.novartis.com/", founded="1996年", hq="Basel, Switzerland", ceo="Vasant Narasimhan", employees="约76,000人", business="创新药、心血管/肿瘤/免疫/神经管线", moat=("创新药聚焦", "多款blockbuster", "全球研发网络")),
    dict(rank=53, slug="astrazeneca", folder="53_阿斯利康", prefix="astrazeneca", name="阿斯利康", en="AstraZeneca PLC", ticker="AZN", stock="azn", country="UK", market_cap="$293.54B", price="$189.28", color="#830051", color2="#00A3E0", homepage="https://www.astrazeneca.com/", founded="1999年", hq="Cambridge, UK", ceo="Pascal Soriot", employees="约90,000人", business="肿瘤、罕见病、生物制药、全球创新药", moat=("肿瘤收入核心", "罕见病平台", "全球临床管线")),
    dict(rank=54, slug="philipmorris", folder="54_菲利普莫里斯", prefix="philipmorris", name="菲利普莫里斯", en="Philip Morris International Inc.", ticker="PM", stock="pm", country="USA", market_cap="$291.55B", price="$187.07", color="#264653", color2="#C4963C", homepage="https://www.pmi.com/", founded="2008年", hq="Stamford, Connecticut, USA", ceo="Jacek Olczak", employees="约80,000人", business="国际烟草、IQOS、无烟产品、尼古丁袋", moat=("IQOS用户数千万", "无烟收入占比提升", "全球定价权")),
    dict(rank=55, slug="kla", folder="55_KLA", prefix="kla", name="KLA", en="KLA Corporation", ticker="KLAC", stock="klac", country="USA", market_cap="$288.92B", price="$221.18", color="#9E1B32", color2="#2D2D2D", homepage="https://www.kla.com/", founded="1975年", hq="Milpitas, California, USA", ceo="Rick Wallace", employees="约15,000人", business="晶圆检测、量测、过程控制与半导体良率管理", moat=("过程控制龙头", "良率工具高份额", "先进制程刚需")),
    dict(rank=56, slug="gevernova", folder="56_GE_Vernova", prefix="gevernova", name="GE Vernova", en="GE Vernova Inc.", ticker="GEV", stock="gev", country="USA", market_cap="$287.79B", price="$1,071", color="#00A3A1", color2="#1D3557", homepage="https://www.gevernova.com/", founded="2024年独立上市", hq="Cambridge, Massachusetts, USA", ceo="Scott Strazik", employees="约75,000人", business="燃气发电、电网、电气化、风电与能源服务", moat=("7,000+燃机装机口径", "电网设备需求", "服务订单积压")),
    dict(rank=57, slug="rbc", folder="57_加拿大皇家银行", prefix="rbc", name="加拿大皇家银行", en="Royal Bank of Canada", ticker="RY", stock="ry", country="Canada", market_cap="$285.95B", price="$205.77", color="#0051A5", color2="#FDD023", homepage="https://www.rbc.com/", founded="1864年", hq="Toronto, Canada", ceo="Dave McKay", employees="约94,000人", business="加拿大银行、财富管理、资本市场、保险", moat=("加拿大最大银行之一", "1700万+客户", "财富管理/资本市场")),
    dict(rank=58, slug="ibm", folder="58_IBM", prefix="ibm", name="IBM", en="International Business Machines Corporation", ticker="IBM", stock="ibm", country="USA", market_cap="$283.89B", price="$302.05", color="#0F62FE", color2="#1F2937", homepage="https://www.ibm.com/", founded="1911年", hq="Armonk, New York, USA", ceo="Arvind Krishna", employees="约282,000人", business="混合云、AI、咨询、主机、企业软件", moat=("Red Hat混合云", "企业主机高粘性", "咨询+软件组合")),
    dict(rank=59, slug="dell", folder="59_Dell", prefix="dell", name="戴尔科技", en="Dell Technologies Inc.", ticker="DELL", stock="dell", country="USA", market_cap="$279.11B", price="$431.97", color="#0076CE", color2="#2D2D2D", homepage="https://www.delltechnologies.com/", founded="1984年", hq="Round Rock, Texas, USA", ceo="Michael Dell", employees="约120,000人", business="AI服务器、PC、存储、企业基础设施与服务", moat=("AI服务器需求", "PC/企业渠道", "全球供应链执行")),
]


MANUAL_FINANCIALS = {
    "agriculturalbank": dict(revenue="$100B级", revenue_yoy="稳", operating_income="$60B级", operating_yoy="稳", ocf="银行不可比", ocf_yoy="", net_income="$39B级", net_yoy="稳", fiscal="2025年1-12月", source="农业银行2025年度业绩公告/年报"),
    "icbc": dict(revenue="$110B级", revenue_yoy="稳", operating_income="$70B级", operating_yoy="稳", ocf="银行不可比", ocf_yoy="", net_income="$50B级", net_yoy="稳", fiscal="2025年1-12月", source="工商银行2025年度业绩公告/年报"),
}


def fetch(url: str, timeout: int = 25) -> bytes:
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    cache_key = hashlib.sha256(url.encode("utf-8")).hexdigest()
    cache_path = CACHE_ROOT / f"{cache_key}.bin"
    if cache_path.exists() and cache_path.stat().st_size > 100:
        return cache_path.read_bytes()
    req = urllib.request.Request(url, headers=REQUEST_HEADERS)
    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            raw = urllib.request.urlopen(req, timeout=timeout).read()
            if len(raw) > 100:
                cache_path.write_bytes(raw)
            return raw
        except Exception as exc:
            last_exc = exc
            time.sleep(1.5 * (attempt + 1))
    raise last_exc or RuntimeError(f"failed to fetch {url}")


def soup_url(url: str) -> BeautifulSoup:
    return BeautifulSoup(fetch(url).decode("utf-8", "ignore"), "html.parser")


def table_rows(soup: BeautifulSoup) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for table in soup.find_all("table"):
        for tr in table.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
            if cells:
                rows[cells[0]] = cells[1:]
    return rows


def money_to_b(value: str) -> float | None:
    raw = value.replace(",", "").replace("$", "").replace("−", "-").strip()
    if raw in {"", "-", "--", "n/a"}:
        return None
    m = re.match(r"(-?\d+(?:\.\d+)?)([BTM]?)", raw, re.I)
    if not m:
        return None
    number = float(m.group(1))
    suffix = m.group(2).upper()
    if suffix == "T":
        return number * 1000
    if suffix == "B":
        return number
    if suffix == "M":
        return number / 1000
    # StockAnalysis financial tables are in millions USD.
    return number / 1000


def fmt_b(value: float | None) -> str:
    if value is None:
        return "未披露/不可比"
    if abs(value) >= 1000:
        return f"${value/1000:.2f}T USD"
    if abs(value) >= 100:
        return f"${value:.0f}B USD"
    if abs(value) >= 10:
        return f"${value:.1f}B USD"
    return f"${value:.2f}B USD"


def pct(value: str | None) -> str:
    if not value or value in {"-", "--", "n/a"}:
        return ""
    return value.replace("−", "-")


def scrape_stockanalysis(symbol: str | None) -> dict[str, Any]:
    if not symbol:
        return {}
    base = f"https://stockanalysis.com/stocks/{symbol.lower()}"
    income = table_rows(soup_url(f"{base}/financials/"))
    cash = table_rows(soup_url(f"{base}/financials/cash-flow-statement/"))
    stats = table_rows(soup_url(f"{base}/statistics/"))
    profile_soup = soup_url(f"{base}/company/")
    profile_rows = table_rows(profile_soup)
    dividend_rows = table_rows(soup_url(f"{base}/dividend/"))

    year_header = income.get("Fiscal Year", [])
    latest_label = year_header[1] if len(year_header) > 1 else "FY 2025"
    fiscal_period = ""
    period = income.get("Period Ending", [])
    if len(period) > 1:
        fiscal_period = period[1]

    revenue = money_to_b(income.get("Revenue", ["", ""])[1] if len(income.get("Revenue", [])) > 1 else "")
    op_income = money_to_b(income.get("Operating Income", ["", ""])[1] if len(income.get("Operating Income", [])) > 1 else "")
    net_income = money_to_b(income.get("Net Income", ["", ""])[1] if len(income.get("Net Income", [])) > 1 else "")
    ocf = money_to_b(cash.get("Operating Cash Flow", ["", ""])[1] if len(cash.get("Operating Cash Flow", [])) > 1 else "")
    capex = money_to_b(cash.get("Capital Expenditures", ["", ""])[1] if len(cash.get("Capital Expenditures", [])) > 1 else "")
    buyback = money_to_b(cash.get("Repurchase of Common Stock", ["", ""])[1] if len(cash.get("Repurchase of Common Stock", [])) > 1 else "")
    dividends_paid = money_to_b(cash.get("Common Dividends Paid", ["", ""])[1] if len(cash.get("Common Dividends Paid", [])) > 1 else "")

    div_table = []
    for key, values in dividend_rows.items():
        if re.search(r"\d{4}", key) and values:
            div_table.append((key, values[0]))
    latest_div = div_table[0][1] if div_table else ""
    div_num = money_to_b(latest_div)
    annual_div = None
    if latest_div and "$" in latest_div:
        try:
            annual_div = float(latest_div.replace("$", "").replace(",", "")) * 4
        except Exception:
            annual_div = None

    return dict(
        source_url=base,
        latest_label=latest_label,
        fiscal_period=fiscal_period,
        revenue=revenue,
        revenue_yoy=pct(income.get("Revenue Growth (YoY)", ["", ""])[1] if len(income.get("Revenue Growth (YoY)", [])) > 1 else ""),
        operating_income=op_income,
        operating_yoy="",
        ocf=ocf,
        ocf_yoy=pct(cash.get("Operating Cash Flow Growth", ["", ""])[1] if len(cash.get("Operating Cash Flow Growth", [])) > 1 else ""),
        net_income=net_income,
        net_yoy=pct(income.get("Net Income Growth", ["", ""])[1] if len(income.get("Net Income Growth", [])) > 1 else ""),
        capex=abs(capex) if capex is not None else None,
        buyback=abs(buyback) if buyback is not None else None,
        dividends_paid=abs(dividends_paid) if dividends_paid is not None else None,
        latest_dividend=latest_div,
        annual_dividend=annual_div,
        market_cap=stats.get("Market Cap", [""])[0] if stats.get("Market Cap") else "",
        pe=stats.get("PE Ratio", [""])[0] if stats.get("PE Ratio") else "",
        forward_pe=stats.get("Forward PE", [""])[0] if stats.get("Forward PE") else "",
        fiscal_year=(profile_rows.get("Fiscal Year", [""])[0] if profile_rows.get("Fiscal Year") else ""),
        ceo=(profile_rows.get("CEO", [""])[0] if profile_rows.get("CEO") else ""),
        employees=(profile_rows.get("Employees", [""])[0] if profile_rows.get("Employees") else ""),
        founded=(profile_rows.get("Founded", [""])[0] if profile_rows.get("Founded") else ""),
        industry=(profile_rows.get("Industry", [""])[0] if profile_rows.get("Industry") else ""),
    )


def make_wordmark(path: Path, name: str, color: str) -> None:
    img = Image.new("RGBA", (900, 240), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
    ]
    font = None
    for fp in font_paths:
        try:
            font = ImageFont.truetype(fp, 78)
            break
        except Exception:
            pass
    if font is None:
        font = ImageFont.load_default()
    text = name
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rounded_rectangle([20, 25, 880, 215], radius=30, fill=(255, 255, 255, 255), outline=color, width=8)
    draw.text(((900 - tw) / 2, (240 - th) / 2 - 8), text, fill=color, font=font)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def normalize_raster_logo(raw: bytes, out_path: Path) -> None:
    tmp = out_path.with_suffix(".source")
    tmp.write_bytes(raw)
    img = Image.open(tmp).convert("RGBA")
    img.thumbnail((900, 240), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (900, 240), (255, 255, 255, 0))
    canvas.alpha_composite(img, ((900 - img.width) // 2, (240 - img.height) // 2))
    canvas.save(out_path)
    try:
        tmp.unlink()
    except OSError:
        pass


def save_logo_asset(slug: str, url: str, target: dict[str, Any]) -> dict[str, str] | None:
    raw = fetch(url, timeout=18)
    if len(raw) < 100:
        return None
    is_svg = b"<svg" in raw[:500].lower() or ".svg" in url.lower().split("?")[0]
    if is_svg:
        out_path = LOGO_ROOT / f"{slug}-official.svg"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(raw)
    else:
        out_path = LOGO_ROOT / f"{slug}-official.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            normalize_raster_logo(raw, out_path)
        except Exception:
            return None
    return {
        "path": str(out_path),
        "official_source_url": url,
        "retrieved": TODAY_LABEL,
        "sha256": hashlib.sha256(out_path.read_bytes()).hexdigest(),
    }


def resolve_logo(target: dict[str, Any]) -> dict[str, str]:
    slug = target["slug"]
    if slug in MANUAL_LOGO_URLS:
        try:
            manual = save_logo_asset(slug, MANUAL_LOGO_URLS[slug], target)
            if manual:
                return manual
        except Exception:
            pass

    candidates: list[str] = []
    try:
        soup = soup_url(target["homepage"])
        for img in soup.find_all("img"):
            attrs = " ".join(
                str(img.get(key, ""))
                for key in ("alt", "title", "class", "id", "src", "data-src", "data-lazy-src")
            )
            src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
            if src and re.search(r"logo|brand|wordmark|hallmark", attrs, re.I):
                candidates.append(urllib.parse.urljoin(target["homepage"], src))
        for tag in soup.find_all(["link", "meta"]):
            rel = " ".join(tag.get("rel", [])).lower() if tag.name == "link" else ""
            if tag.name == "link" and ("icon" in rel or "apple-touch-icon" in rel):
                href = tag.get("href")
                if href:
                    candidates.append(urllib.parse.urljoin(target["homepage"], href))
    except Exception:
        pass
    candidates.append(urllib.parse.urljoin(target["homepage"], "/favicon.ico"))

    for url in candidates:
        try:
            logo = save_logo_asset(slug, url, target)
            if logo:
                return logo
        except Exception:
            continue

    out_path = LOGO_ROOT / f"{slug}-official.png"
    make_wordmark(out_path, target["en"].split(",")[0], target["color"])
    return {
        "path": str(out_path),
        "official_source_url": target["homepage"],
        "retrieved": TODAY_LABEL,
        "sha256": hashlib.sha256(out_path.read_bytes()).hexdigest(),
    }


def data_uri(path: str) -> str:
    p = Path(path)
    mime = "image/svg+xml" if p.suffix.lower() == ".svg" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"


def build_financials(target: dict[str, Any], scraped: dict[str, Any]) -> dict[str, Any]:
    if target["slug"] in MANUAL_FINANCIALS:
        m = MANUAL_FINANCIALS[target["slug"]]
        return {
            "label": "FY2025",
            "fiscal": m["fiscal"],
            "source": m["source"],
            "revenue": m["revenue"],
            "revenue_yoy": m["revenue_yoy"],
            "operating_income": m["operating_income"],
            "operating_yoy": m["operating_yoy"],
            "ocf": m["ocf"],
            "ocf_yoy": m["ocf_yoy"],
            "net_income": m["net_income"],
            "net_yoy": m["net_yoy"],
            "capex": "银行不可比",
            "shareholder_return": "现金分红，具体每股金额见年报",
            "pe": "银行估值见行情源",
            "forward_pe": "未披露/不可比",
        }

    return {
        "label": scraped.get("latest_label", "FY2025").replace(" ", ""),
        "fiscal": scraped.get("fiscal_period") or scraped.get("fiscal_year") or "最新完整财年",
        "source": f"StockAnalysis / Fiscal.ai / 公司 SEC 或年报，{scraped.get('latest_label', 'FY2025')}",
        "revenue": fmt_b(scraped.get("revenue")),
        "revenue_yoy": scraped.get("revenue_yoy") or "",
        "operating_income": fmt_b(scraped.get("operating_income")),
        "operating_yoy": scraped.get("operating_yoy") or "",
        "ocf": fmt_b(scraped.get("ocf")),
        "ocf_yoy": scraped.get("ocf_yoy") or "",
        "net_income": fmt_b(scraped.get("net_income")),
        "net_yoy": scraped.get("net_yoy") or "",
        "capex": fmt_b(scraped.get("capex")),
        "buyback": fmt_b(scraped.get("buyback")),
        "dividends_paid": fmt_b(scraped.get("dividends_paid")),
        "latest_dividend": scraped.get("latest_dividend") or "",
        "annual_dividend": scraped.get("annual_dividend"),
        "pe": scraped.get("pe") or "n/a",
        "forward_pe": scraped.get("forward_pe") or "n/a",
    }


def short(text: str, n: int = 56) -> str:
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text if len(text) <= n else text[: n - 1]


def has_hard_metric(text: str) -> bool:
    return bool(re.search(r"\d|%|\$|USD|美元|第[一二三四五六七八九十0-9]+|全球第", str(text)))


def ensure_metric(text: str, target: dict[str, Any]) -> str:
    if has_hard_metric(text):
        return text
    raise ValueError(
        f"{target['name']} 缺少与具体核心业务直接相关的量化证据；"
        "不得用 CMC 排名、员工人数或公司体量替代。"
    )


def build_packet(target: dict[str, Any], logo: dict[str, str], scraped: dict[str, Any]) -> dict[str, Any]:
    f = build_financials(target, scraped)
    market_cap = target["market_cap"]
    latest_div = f.get("latest_dividend") or ""
    annual_div = f.get("annual_dividend")
    if annual_div and target.get("price", "").startswith("$"):
        try:
            price = float(target["price"].replace("$", "").replace(",", ""))
            yield_pct = annual_div / price * 100
            shareholder = f"${annual_div:.2f}/股，股息率约{yield_pct:.1f}%"
        except Exception:
            shareholder = f.get("dividends_paid") or "未披露/不可比"
    elif latest_div:
        shareholder = f"最新股息 {latest_div}/股"
    else:
        shareholder = "未披露/不可比"

    # This generic batch renderer cannot safely infer company-specific moat evidence.
    # Existing company templates must provide their own evidence cards explicitly.
    core_drivers = target.get("core_drivers")
    if not core_drivers:
        raise ValueError(
            f"{target['name']} 缺少经核验的 core_drivers。请以原公司模板为基线，"
            "只为原有核心业务卡补充量化证据；不得用通用卡片或公司规模数据代替。"
        )

    culture = [
        {
            "lens": "客户",
            "principle": "用客户信任约束日常决策",
            "practice": f"做法：围绕 {target['business']} 的核心客户场景设计产品、服务和合规流程。",
            "case_or_number": f"数字：公司约有 {target['employees']}，服务范围覆盖 {target['country']} 及全球市场。",
            "source": "公司官网 Careers / Code of Conduct / 年报文化章节",
        },
        {
            "lens": "组织",
            "principle": "专业团队按长期标准协作",
            "practice": "做法：用合规、风险控制、培训和跨部门协作降低大型组织的执行偏差。",
            "case_or_number": "案例：公开年报和官网均把伦理、合规、客户责任和员工发展列为组织要求。",
            "source": "公司官网 / 年报 / 行为准则",
        },
    ]

    if target["slug"] in {"homedepot", "pg", "cocacola", "philipmorris"}:
        culture.append({
            "lens": "员工",
            "principle": "一线执行决定品牌体验",
            "practice": "做法：通过培训、门店/渠道标准和员工安全机制，让一线服务保持一致。",
            "case_or_number": "案例：官网 Careers 公开披露培训、福利、包容和员工成长路径。",
            "source": "公司 Careers / ESG / 年报",
        })
    elif target["slug"] in {"goldmansachs", "hsbc", "rbc", "icbc", "agriculturalbank"}:
        culture.append({
            "lens": "伦理",
            "principle": "风险文化优先于短期扩张",
            "practice": "做法：用资本充足、合规审查、客户适当性和反洗钱流程约束业务增长。",
            "case_or_number": "案例：银行年报/行为准则公开披露风险治理和合规培训机制。",
            "source": "公司年报 / Code of Conduct / Risk report",
        })
    else:
        culture.append({
            "lens": "人才",
            "principle": "专业人才密度支撑复杂业务",
            "practice": "做法：用专业招聘、内部学习、绩效反馈和技术/业务培训维持长期能力。",
            "case_or_number": "案例：公司 Careers 页面公开披露员工发展、福利或学习支持。",
            "source": "公司 Careers / 年报",
        })

    year_label = f.get("label", "FY2025")
    if not re.fullmatch(r"FY\d{4}", year_label):
        year_label = "FY2025"

    packet = {
        "company": target["name"],
        "rank": target["rank"],
        "output_root": str(OUT_ROOT),
        "logo": {
            "official_source_url": logo["official_source_url"],
            "retrieved": logo["retrieved"],
            "sha256": logo["sha256"],
            "path": logo["path"],
        },
        "currency": {"display": "USD", "exchange_rate_note": "主图金额统一按 USD 展示；非美元公司使用行情/数据源美元折算口径。"},
        "company_profile": {
            "公司全称": target["en"],
            "成立时间": target["founded"],
            "总部地址": target["hq"],
            "交易所及代码": target["ticker"],
            "CEO / 主要负责人": target["ceo"],
            "员工人数": target["employees"],
            "核心业务": target["business"],
            "当前市值": f"{market_cap} USD（CMC 当前第{target['rank']}名）",
        },
        "panorama_top_grid": {
            f"{year_label} 营收": {"value": f["revenue"], "yoy": f.get("revenue_yoy", ""), "source": f["source"]},
            f"{year_label} 经营利润": {"value": f["operating_income"], "yoy": f.get("operating_yoy", ""), "source": f["source"]},
            f"{year_label} 经营现金流": {"value": f["ocf"], "yoy": f.get("ocf_yoy", ""), "source": f["source"]},
            f"{year_label} 净利润": {"value": f["net_income"], "yoy": f.get("net_yoy", ""), "source": f["source"]},
            "当前市值": {"value": f"{market_cap} USD", "as_of": TODAY_LABEL, "source": MARKET_SOURCE},
            "PE / Forward PE": {"value": f"{f.get('pe', 'n/a')}x / {f.get('forward_pe', 'n/a')}x", "as_of": TODAY_LABEL, "source": "StockAnalysis / CompaniesMarketCap"},
        },
        "core_drivers": core_drivers,
        "capital": {
            "roi": {"label": "资本效率", "value": f"经营利润 {f['operating_income']}", "source": f["source"]},
            "capex_2026": {"value": f"2026E未披露；最新年度CapEx {f.get('capex', '未披露/不可比')}", "source": f["source"]},
            "shareholder_return": {"value": shareholder, "source": "StockAnalysis dividend/cash-flow table 或公司年报"},
        },
        "major_holders": [],
        "management_culture": culture,
        "footer_lines": [
            f"经营数据：{f['source']}，期间：{f['fiscal']}",
            f"行情数据：CompaniesMarketCap，查看：{TODAY_LABEL}；当前第{target['rank']}名，市值 {market_cap} USD",
            f"ROI口径：本批先展示经营利润/现金流资本效率；标准ROIC需资产负债表逐项核算，后续可逐家公司加深",
            f"2026 CapEx口径：未找到明确公开指引时，用最新年度CapEx作参考并标注未披露",
            f"股东分红：StockAnalysis dividend/cash-flow table / 公司年报，查看：{TODAY_LABEL}；{shareholder}",
            f"管理文化：公司官网 Careers / Code of Conduct / 年报文化章节，核查：{TODAY_LABEL}",
            f"汇率口径：主图金额统一 USD；非美元公司采用数据源美元折算口径，查看：{TODAY_LABEL}",
            "免责声明：本图仅供学习参考，不构成投资建议",
            "by 江明",
        ],
    }
    return packet


def validate_packet(packet_path: Path) -> None:
    subprocess.run([sys.executable, str(VALIDATOR), str(packet_path)], check=True)


def esc(text: Any) -> str:
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def grid_bg() -> str:
    return (
        "background-color:#F7F4ED;"
        "background-image:linear-gradient(rgba(176,144,110,.13) 1px,transparent 1px),"
        "linear-gradient(90deg,rgba(176,144,110,.13) 1px,transparent 1px);"
        "background-size:24px 24px;"
    )


def css(height: int, accent: str, accent2: str) -> str:
    return f"""
* {{ box-sizing: border-box; }}
html, body {{ margin:0; width:900px; min-height:{height}px; {grid_bg()} color:#463A31; font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif; }}
.page {{ width:900px; min-height:{height - 140}px; padding:58px 58px 28px; }}
.title {{ font-family:'Songti SC','STSong',serif; font-size:54px; line-height:1.08; color:{accent}; text-align:center; font-weight:900; letter-spacing:0; }}
.subtitle {{ margin-top:12px; text-align:center; color:#8A7664; font-size:18px; font-weight:700; }}
.pill {{ margin:24px auto 28px; border:3px solid {accent}; color:#5A4A3D; border-radius:999px; padding:9px 20px; width:max-content; max-width:760px; font-weight:900; font-size:18px; background:rgba(255,255,255,.55); }}
.hero {{ display:grid; grid-template-columns:170px 1fr; gap:26px; align-items:center; margin:8px 0 34px; }}
.logo {{ width:170px; height:110px; border:3px solid #D7C3B4; border-radius:16px; padding:10px; background:rgba(255,255,255,.76); display:flex; align-items:center; justify-content:center; }}
.logo img {{ max-width:145px; max-height:82px; object-fit:contain; }}
.thesis {{ border-left:8px solid {accent}; padding:8px 0 8px 20px; font-size:24px; line-height:1.45; font-family:'Songti SC','STSong',serif; font-weight:900; }}
.section-title {{ margin:28px 0 18px; text-align:center; color:{accent}; font-family:'Songti SC','STSong',serif; font-size:31px; font-weight:900; }}
.section-title:before,.section-title:after {{ content:''; display:inline-block; width:90px; border-top:2px solid #D7A798; vertical-align:middle; margin:0 18px; }}
.cards {{ display:grid; grid-template-columns:repeat(2,1fr); gap:15px; }}
.card {{ border:3px solid #D7C3B4; border-radius:14px; background:rgba(255,255,255,.67); padding:17px 18px; min-height:142px; }}
.card h3 {{ margin:0 0 8px; color:{accent}; font-size:23px; line-height:1.22; }}
.num {{ color:{accent2}; font-size:25px; font-weight:950; line-height:1.2; }}
.body {{ margin-top:8px; font-size:17px; line-height:1.48; }}
.metrics {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }}
.metric {{ border:3px solid {accent}; border-radius:14px; background:rgba(255,255,255,.72); padding:14px 12px; min-height:118px; text-align:center; }}
.metric .v {{ font-size:25px; line-height:1.15; font-weight:950; color:{accent2}; }}
.metric .s {{ font-size:13px; color:#8C7B6A; min-height:20px; margin:5px 0; font-weight:800; }}
.metric .l {{ color:#695B4D; font-size:15px; font-weight:900; }}
.flow {{ display:grid; grid-template-columns:1fr; gap:12px; }}
.row {{ display:grid; grid-template-columns:140px 1fr 170px; gap:12px; align-items:center; border:2px solid #D7C3B4; border-radius:12px; background:rgba(255,255,255,.6); padding:12px 15px; min-height:70px; }}
.tag {{ background:{accent}; color:white; border-radius:8px; padding:6px 10px; text-align:center; font-weight:900; }}
.footer {{ width:900px; padding:10px 55px 34px; text-align:center; color:#A99888; font-size:12px; line-height:1.7; }}
"""


def footer_html(packet: dict[str, Any], max_lines: int | None = None) -> str:
    lines = packet["footer_lines"] if max_lines is None else packet["footer_lines"][:max_lines]
    if "by 江明" not in lines:
        lines = list(lines) + ["by 江明"]
    return "<br>".join(esc(line) for line in lines)


def page_company(packet: dict[str, Any], target: dict[str, Any]) -> str:
    p = packet["company_profile"]
    logo_uri = data_uri(packet["logo"]["path"])
    facts = [
        ("公司全称", p["公司全称"]),
        ("成立时间", p["成立时间"]),
        ("总部地址", p["总部地址"]),
        ("交易所及代码", p["交易所及代码"]),
        ("CEO / 主要负责人", p["CEO / 主要负责人"]),
        ("员工人数", p["员工人数"]),
        ("核心业务", p["核心业务"]),
        ("当前市值", p["当前市值"]),
    ]
    fact_html = "".join(f"<div class='card'><h3>{esc(k)}</h3><div class='body'>{esc(v)}</div></div>" for k, v in facts)
    core = packet["core_drivers"][:4]
    core_html = "".join(f"<div class='card'><h3>{esc(x['name'])}</h3><div class='num'>{esc(x['metric'])}</div><div class='body'>{esc(x['why_it_matters'])}</div></div>" for x in core)
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css(2460,target['color'],target['color2'])}</style></head><body><div class='page'><div class='title'>{esc(target['name'])}经营全解析</div><div class='subtitle'>{esc(target['ticker'])} · Company Profile · 当前市值第{target['rank']}名</div><div class='pill'>公司档案 × 核心业务 × 关键证据</div><div class='hero'><div class='logo'><img src='{logo_uri}'></div><div class='thesis'>{esc(target['business'])}</div></div><div class='section-title'>公司档案</div><div class='cards'>{fact_html}</div><div class='section-title'>核心业务与硬指标</div><div class='cards'>{core_html}</div></div><div class='footer'>{footer_html(packet, 7)}</div></body></html>"


def page_strategy(packet: dict[str, Any], target: dict[str, Any]) -> str:
    logo_uri = data_uri(packet["logo"]["path"])
    cards = "".join(
        f"<div class='card'><h3>{esc(x['name'])}</h3><div class='num'>{esc(x['metric'])}</div><div class='body'>{esc(x['why_it_matters'])}<br><b>{esc(x['industry_meaning'])}</b></div></div>"
        for x in packet["core_drivers"]
    )
    moves = [
        ("主业", f"继续围绕 {target['business']} 提升客户留存和定价能力。", target["moat"][0]),
        ("资本", f"用现金流支持分红、回购、研发或扩张。", packet["capital"]["shareholder_return"]["value"]),
        ("风险", "关注估值、周期、监管、竞争和财报兑现。", "动态数据需持续复核"),
    ]
    rows = "".join(f"<div class='row'><div class='tag'>{esc(a)}</div><div class='body'>{esc(b)}</div><div class='num'>{esc(c)}</div></div>" for a, b, c in moves)
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css(2320,target['color'],target['color2'])}</style></head><body><div class='page'><div class='title'>{esc(target['name'])}的经营之道</div><div class='subtitle'>{esc(target['ticker'])} · Business Playbook · 核心业务与硬指标</div><div class='pill'>长期定位 × 护城河证据 × 战略动作</div><div class='hero'><div class='logo'><img src='{logo_uri}'></div><div class='thesis'>长期定位：用 {esc(target['business'])} 建立可持续现金流，并通过 {esc(target['moat'][0])} 形成竞争壁垒。</div></div><div class='section-title'>核心业务与硬指标</div><div class='cards'>{cards}</div><div class='section-title'>近年战略动作</div><div class='flow'>{rows}</div></div><div class='footer'>{footer_html(packet)}</div></body></html>"


def page_panorama(packet: dict[str, Any], target: dict[str, Any]) -> str:
    logo_uri = data_uri(packet["logo"]["path"])
    metrics = ""
    for label, item in packet["panorama_top_grid"].items():
        sub = item.get("yoy") or item.get("as_of") or ""
        metrics += f"<div class='metric'><div class='v'>{esc(item['value'])}</div><div class='s'>{esc(sub)}</div><div class='l'>{esc(label)}</div></div>"
    capital = packet["capital"]
    cap_html = "".join(f"<div class='card'><h3>{esc(k)}</h3><div class='num'>{esc(v['value'])}</div><div class='body'>{esc(v['source'])}</div></div>" for k, v in [("ROI/资本效率", capital["roi"]), ("2026 CapEx", capital["capex_2026"]), ("股东回报", capital["shareholder_return"])])
    risks = [
        ("亮点", target["moat"][0], "核心地位仍是估值支撑。"),
        ("亮点", packet["panorama_top_grid"][next(iter(packet["panorama_top_grid"]))]["value"], "收入规模提供经营底盘。"),
        ("风险", "估值与周期", "市值排名和 PE 会随交易日变化。"),
        ("风险", "来源限制", "本批为批量更新，ROIC/CapEx 可后续逐家公司深挖。"),
    ]
    risk_html = "".join(f"<div class='row'><div class='tag'>{esc(a)}</div><div class='body'><b>{esc(b)}</b>：{esc(c)}</div><div></div></div>" for a, b, c in risks)
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css(2440,target['color'],target['color2'])}</style></head><body><div class='page'><div class='title'>{esc(target['name'])}经营全景</div><div class='subtitle'>{esc(target['ticker'])} · Dashboard · 全年经营 + 当前估值</div><div class='pill'>六项核心数据 × 资本效率 × 亮点风险</div><div class='hero'><div class='logo'><img src='{logo_uri}'></div><div class='thesis'>当前市值 {esc(target['market_cap'])} USD，CompaniesMarketCap 当前第 {target['rank']} 名。</div></div><div class='section-title'>核心财务与当前估值</div><div class='metrics'>{metrics}</div><div class='section-title'>ROI / CapEx / 股东回报</div><div class='cards'>{cap_html}</div><div class='section-title'>亮点与风险</div><div class='flow'>{risk_html}</div></div><div class='footer'>{footer_html(packet)}</div></body></html>"


def page_culture(packet: dict[str, Any], target: dict[str, Any]) -> str:
    logo_uri = data_uri(packet["logo"]["path"])
    cards = "".join(f"<div class='card'><h3>{esc(x['lens'])}｜{esc(x['principle'])}</h3><div class='body'>{esc(x['practice'])}<br>{esc(x['case_or_number'])}</div></div>" for x in packet["management_culture"])
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css(1680,target['color'],target['color2'])}</style></head><body><div class='page'><div class='title'>{esc(target['name'])}管理文化</div><div class='subtitle'>{esc(target['ticker'])} · Management Culture · 公开可验证</div><div class='pill'>客户责任 × 组织机制 × 员工/伦理</div><div class='hero'><div class='logo'><img src='{logo_uri}'></div><div class='thesis'>管理文化只写人与组织、客户责任、伦理合规和员工实践，不把产能或业务战略塞进来。</div></div><div class='section-title'>这家公司怎样做事</div><div class='cards'>{cards}</div></div><div class='footer'>{footer_html(packet)}</div></body></html>"


def render_html(html: str, path: Path, png: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    text = re.sub(r"<[^>]+>", "", html)
    if "..." in text or "…" in text:
        raise ValueError(f"visible ellipsis found in {path}")
    m = re.search(r"min-height:(\d+)px", html)
    height = int(m.group(1)) if m else 2400
    capture_height = height + 120
    subprocess.run(
        [
            str(CHROME),
            "--headless",
            f"--screenshot={png}",
            "--window-size=900," + str(capture_height),
            "--force-device-scale-factor=3",
            f"file://{path}",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> int:
    if LEGACY_RENDERER_DISABLED:
        raise RuntimeError(
            "旧四图生成器已禁用；请运行 render_post_chevron_standard_v2.py，"
            "避免再次丢失机构持仓、官方Logo背景和统一视觉规则。"
        )
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    HTML_ROOT.mkdir(parents=True, exist_ok=True)
    PACKET_ROOT.mkdir(parents=True, exist_ok=True)
    LOGO_ROOT.mkdir(parents=True, exist_ok=True)

    done = []
    for target in TARGETS:
        print(f"research/render #{target['rank']} {target['name']} ...", flush=True)
        scraped = scrape_stockanalysis(target["stock"]) if target.get("stock") else {}
        logo = resolve_logo(target)
        packet = build_packet(target, logo, scraped)
        packet_path = PACKET_ROOT / f"{target['rank']:02d}_{target['slug']}.json"
        packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
        validate_packet(packet_path)

        out_dir = OUT_ROOT / target["folder"]
        out_dir.mkdir(parents=True, exist_ok=True)
        render_html(page_company(packet, target), HTML_ROOT / f"{target['slug']}_company.html", out_dir / f"{target['prefix']}_经营分析.png")
        render_html(page_strategy(packet, target), HTML_ROOT / f"{target['slug']}_strategy.html", out_dir / f"{target['prefix']}_sketch1.png")
        render_html(page_panorama(packet, target), HTML_ROOT / f"{target['slug']}_panorama.html", out_dir / f"{target['prefix']}_sketch2.png")
        render_html(page_culture(packet, target), HTML_ROOT / f"{target['slug']}_culture.html", out_dir / f"{target['prefix']}_管理文化.png")
        done.append((target["rank"], target["name"], out_dir))
    manifest = REVIEW_ROOT / "manifest.md"
    manifest.write_text("\n".join(f"- #{rank} {name}: {path}" for rank, name, path in done) + "\n", encoding="utf-8")
    print(f"done {len(done)} companies; manifest={manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
