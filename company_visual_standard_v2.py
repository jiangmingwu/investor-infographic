"""Deterministic hand-drawn company strategy and panorama pages.

The renderer owns presentation and hard gates. Company batch scripts only
provide researched packets. Final financial text and charts remain HTML/SVG.
"""

from __future__ import annotations

import base64
import html
import re
from pathlib import Path
from typing import Any


REQUIRED_METRICS = (
    "营收",
    "经营利润",
    "经营现金流",
    "净利润",
    "当前市值",
    "PE / Forward PE",
)
REQUIRED_FOOTERS = (
    "经营数据：",
    "行情数据：",
    "核心证据：",
    "ROI口径：",
    "2026 CapEx口径：",
    "股东分红：",
    "机构持仓：",
    "汇率口径：",
    "免责声明：",
)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def data_uri(path: str) -> str:
    source = Path(path)
    suffix = source.suffix.lower()
    mime = "image/svg+xml" if suffix == ".svg" else "image/jpeg" if suffix in {".jpg", ".jpeg"} else "image/png"
    return f"data:{mime};base64,{base64.b64encode(source.read_bytes()).decode('ascii')}"


def visible_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(visible_text(k) + " " + visible_text(v) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return " ".join(visible_text(x) for x in value)
    return re.sub(r"\s+", " ", str(value)).strip()


def _require_number(value: object, field: str) -> None:
    if not re.search(r"\d", str(value)):
        raise ValueError(f"{field}缺少数字证据")


def validate_packet(packet: dict[str, Any]) -> None:
    text = visible_text(packet)
    if "..." in text or "…" in text:
        raise ValueError("成图文字含省略号截断")

    logo = packet.get("logo", {})
    logo_path = Path(str(logo.get("path", "")))
    if not logo_path.is_file() or not str(logo.get("official_source_url", "")).startswith("http"):
        raise ValueError("缺少公司官方Logo文件或官方来源URL")

    drivers = packet.get("strategy", {}).get("drivers", [])
    if not 3 <= len(drivers) <= 5:
        raise ValueError("核心业务必须保留3-5项")
    for driver in drivers:
        for key in ("title", "icon", "metric", "explanation"):
            if not str(driver.get(key, "")).strip():
                raise ValueError(f"核心业务缺少字段：{key}")
        _require_number(driver["metric"], f"{driver['title']}的")
        if not str(driver["explanation"]).startswith("行业含义："):
            raise ValueError(f"{driver['title']}缺少行业含义解释")

    metrics = packet.get("panorama", {}).get("metrics", [])
    if len(metrics) != 6:
        raise ValueError("经营全景必须固定展示六项核心数据")
    labels = [str(item.get("label", "")) for item in metrics]
    industry_exception = str(packet.get("panorama", {}).get("industry_exception", "")).strip()
    if industry_exception:
        if len(industry_exception) < 12:
            raise ValueError("金融行业替代口径必须说明不可比原因")
        if "营收" not in labels[0] or "净利润" not in labels[3]:
            raise ValueError("金融行业六项数据仍须以营收开头、净利润为第四项")
        if "当前市值" not in labels[4] or "PE / Forward PE" not in labels[5]:
            raise ValueError("金融行业六项数据末两项仍须为当前市值和PE / Forward PE")
        if len(set(labels)) != 6:
            raise ValueError("金融行业六项数据不得重复")
    else:
        for required, label in zip(REQUIRED_METRICS, labels):
            if required not in label:
                raise ValueError(f"六项经营数据顺序或名称错误：应包含{required}")
    for item in metrics:
        _require_number(item.get("value", ""), f"{item.get('label', '经营指标')}的")

    capital = packet.get("panorama", {}).get("capital", [])
    if len(capital) != 3:
        raise ValueError("经营全景下部必须分别展示ROI、2026 CapEx和股东回报")
    for item in capital:
        if "未披露" not in str(item.get("value", "")):
            _require_number(item.get("value", ""), f"{item.get('label', '资本指标')}的")

    holders = packet.get("panorama", {}).get("holders", [])
    if not 3 <= len(holders) <= 5:
        raise ValueError("机构与重要股东必须保留3-5个可核验主体")
    for holder in holders:
        if not re.search(r"\d+(?:\.\d+)?%", str(holder.get("stake", ""))):
            raise ValueError(f"{holder.get('name', '机构')}缺少明确持股比例")
        if not re.search(r"\$\s*\d", str(holder.get("value", ""))):
            raise ValueError(f"{holder.get('name', '机构')}缺少美元持仓估值")
        if not re.search(r"20\d{2}", str(holder.get("period", ""))):
            raise ValueError(f"{holder.get('name', '机构')}缺少报告期")

    footer_lines = packet.get("footer_lines", [])
    for prefix in REQUIRED_FOOTERS:
        if not any(str(line).startswith(prefix) for line in footer_lines):
            raise ValueError(f"页脚缺少：{prefix}")


def icon(name: str, color: str, size: int = 38) -> str:
    shapes = {
        "factory": "<path d='M6 41V22l11 6V18l11 7V11h8v30z'/><path d='M11 34h5M22 34h5M33 34h4'/>",
        "network": "<circle cx='12' cy='12' r='5'/><circle cx='36' cy='14' r='5'/><circle cx='24' cy='36' r='5'/><path d='M16 14l15 1M15 16l7 15M34 19l-7 12'/>",
        "coin": "<circle cx='24' cy='24' r='17'/><path d='M29 16c-2-3-7-3-9 0-3 4 2 7 5 7 5 1 7 6 3 9-4 3-9 1-10-2M24 10v28'/>",
        "shield": "<path d='M24 5l15 6v10c0 10-7 17-15 21-8-4-15-11-15-21V11z'/><path d='M16 24l5 5 11-12'/>",
        "chip": "<rect x='11' y='11' width='26' height='26' rx='3'/><path d='M17 17h14v14H17zM5 16h6M5 24h6M5 32h6M37 16h6M37 24h6M37 32h6M16 5v6M24 5v6M32 5v6M16 37v6M24 37v6M32 37v6'/>",
        "cloud": "<path d='M13 37h25a8 8 0 0 0 0-16 14 14 0 0 0-27-3A10 10 0 0 0 13 37z'/>",
        "store": "<path d='M7 18h34l-4-10H11z'/><path d='M9 18v23h30V18M16 41V28h9v13'/>",
        "home": "<path d='M6 23L24 8l18 15M11 21v20h26V21M20 41V29h8v12'/>",
        "globe": "<circle cx='24' cy='24' r='18'/><path d='M6 24h36M24 6c7 7 7 29 0 36M24 6c-7 7-7 29 0 36'/>",
        "people": "<circle cx='18' cy='15' r='7'/><circle cx='34' cy='17' r='5'/><path d='M5 42c1-11 7-17 15-17s14 6 15 17M30 28c7 1 11 6 12 14'/>",
        "pill": "<path d='M11 11a10 10 0 0 1 14 0l12 12a10 10 0 0 1-14 14L11 25a10 10 0 0 1 0-14z'/><path d='M17 31l14-14'/>",
        "flask": "<path d='M18 5h12M21 5v13L10 38a3 3 0 0 0 3 5h22a3 3 0 0 0 3-5L27 18V5'/><path d='M15 33h18'/>",
        "server": "<rect x='8' y='7' width='32' height='14' rx='2'/><rect x='8' y='27' width='32' height='14' rx='2'/><path d='M14 14h.1M20 14h12M14 34h.1M20 34h12'/>",
        "chart": "<path d='M7 41V7M7 41h35M12 33l10-10 7 6 11-16'/>",
        "bolt": "<path d='M28 4L10 27h13l-3 17 18-25H25z'/>",
        "wind": "<path d='M5 17h25c8 0 8-10 1-10-4 0-6 2-6 5M5 25h34c7 0 7 10 0 10-4 0-6-2-6-5M5 33h18'/>",
        "medical": "<path d='M24 7v34M7 24h34'/><circle cx='24' cy='24' r='18'/>",
        "bank": "<path d='M5 18L24 7l19 11zM9 21h30M12 21v17M21 21v17M30 21v17M39 21v17M7 41h34'/>",
        "card": "<rect x='5' y='10' width='38' height='28' rx='4'/><path d='M5 19h38M12 30h10'/>",
        "truck": "<path d='M5 13h24v22H5zM29 21h8l6 8v6H29z'/><circle cx='13' cy='38' r='4'/><circle cx='36' cy='38' r='4'/>",
        "oil": "<path d='M24 5C18 14 11 21 11 30a13 13 0 0 0 26 0c0-9-7-16-13-25z'/><path d='M18 33c2 3 5 4 9 3'/>",
    }
    shape = shapes.get(name, shapes["chart"])
    return f"<svg width='{size}' height='{size}' viewBox='0 0 48 48' fill='none' stroke='{color}' stroke-width='2.8' stroke-linecap='round' stroke-linejoin='round'>{shape}</svg>"


def _footer(lines: list[str]) -> str:
    return "<footer>" + "<br>".join(esc(line) for line in lines) + "<div class='signature'>by 江明</div></footer>"


def _css(height: int, accent: str, deep: str, gold: str) -> str:
    template = """
*{{box-sizing:border-box}}html,body{{margin:0;width:900px;height:{height}px;overflow:hidden}}body{{color:#41372f;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',Arial,sans-serif;background-color:#f7f4ed;background-image:linear-gradient(rgba(174,142,105,.105) 1px,transparent 1px),linear-gradient(90deg,rgba(174,142,105,.105) 1px,transparent 1px);background-size:24px 24px}}.page{{width:900px;min-height:{height-1}px;padding:46px 52px 0}}.title{{margin:0;text-align:center;color:{accent};font-family:'Songti SC','STSong',serif;font-size:49px;font-weight:900;line-height:1.12;letter-spacing:0}}.subtitle{{margin:9px 0 0;text-align:center;color:#967c68;font-size:16px;font-weight:750}}.strap{{margin:17px auto 20px;border:2px solid {accent};color:#614f41;background:rgba(255,255,255,.62);border-radius:999px;padding:8px 18px;width:max-content;max-width:760px;text-align:center;font-size:17px;font-weight:850}}.logo-hero{{display:grid;grid-template-columns:190px 1fr;gap:24px;align-items:center;margin:5px 0 19px}}.logo-box{{height:132px;border:2px solid #d8c5b3;border-radius:12px;background:rgba(255,255,255,.82);display:flex;align-items:center;justify-content:center;padding:7px}}.logo-visible{{width:174px;height:116px;object-fit:contain}}.thesis{{border-left:7px solid {accent};padding:7px 0 7px 18px;color:#49392e;font-family:'Songti SC','STSong',serif;font-size:22px;font-weight:900;line-height:1.42}}.thesis small{{display:block;margin-top:5px;color:#8c7869;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif;font-size:13px;font-weight:700}}.section{{margin:20px 0 0}}.section h2{{margin:0 0 13px;color:{accent};text-align:center;font-family:'Songti SC','STSong',serif;font-size:28px;line-height:1.15;font-weight:900}}.section h2:before,.section h2:after{{content:'';display:inline-block;width:70px;border-top:2px solid #d6a89c;margin:0 14px;vertical-align:middle}}.driver-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}}.driver-card{{display:grid;grid-template-columns:46px 1fr;gap:10px;border:2px solid #dfcabb;border-radius:11px;background:rgba(255,255,255,.72);padding:14px;min-height:174px}}.driver-card:last-child:nth-child(odd){{grid-column:1/-1}}.driver-card h3{{margin:0;color:{deep};font-size:19px}}.proof{{margin-top:6px;color:{gold};font-size:21px;line-height:1.25;font-weight:950}}.meaning{{margin-top:8px;color:#4c3b2f;font-size:13px;line-height:1.42;font-weight:700}}.action{{display:grid;grid-template-columns:94px 1fr;gap:12px;border:2px solid #dfcabb;border-radius:10px;background:rgba(255,255,255,.7);padding:11px 14px;margin-bottom:9px}}.tag{{background:{accent};color:white;border-radius:7px;padding:6px 8px;text-align:center;font-size:13px;font-weight:900}}.action b{{color:{deep}}.action .detail{{font-size:14px;line-height:1.4}}.quote{{margin-top:13px;border-left:6px solid {accent};background:rgba(0,0,0,.035);padding:12px 16px;color:#4b3a2d;font-family:'Songti SC','STSong',serif;font-size:18px;font-weight:850;line-height:1.42}}.metrics{{display:grid;grid-template-columns:repeat(3,1fr);gap:11px}}.metric{{border:2px solid {accent};border-radius:11px;background:rgba(255,255,255,.76);padding:11px 8px;text-align:center;min-height:108px}}.metric .value{{color:{deep};font-size:22px;line-height:1.17;font-weight:950}}.metric .sub{{margin:5px 0;color:#8a6e5a;font-size:11px;font-weight:850;min-height:16px}}.metric .label{{font-size:13px;font-weight:900}}.segment-row{{display:grid;grid-template-columns:1.25fr .55fr .8fr 1fr;gap:8px;align-items:center;border-bottom:1px dashed #d8cbb9;padding:8px 10px;font-size:13px}}.segment-row b{{color:{deep};font-size:15px}}.segment-row .share{{color:{accent};font-size:17px;font-weight:950}}.capital-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:11px}}.capital-card{{border:2px solid #dfcabb;border-radius:11px;background:rgba(255,255,255,.72);padding:12px;min-height:126px}}.capital-card h3{{margin:0;color:{deep};font-size:16px}}.capital-card .value{{margin-top:6px;color:{gold};font-size:20px;font-weight:950;line-height:1.2}}.capital-card .note{{margin-top:6px;font-size:12px;line-height:1.35;font-weight:700}}.signal-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:11px}}.signal{{border:2px solid #dfcabb;border-radius:10px;background:rgba(255,255,255,.72);padding:11px 13px;min-height:90px}}.signal h3{{margin:0 0 5px;color:{accent};font-size:15px}}.signal p{{margin:0;font-size:12px;line-height:1.38;font-weight:700}}.holder-grid{{border:2px solid #d7c3b4;border-radius:11px;background:rgba(255,255,255,.62);padding:4px 14px}}.holder-row{{display:grid;grid-template-columns:1.55fr .62fr .78fr;gap:10px;align-items:center;min-height:42px;border-bottom:1px dashed #d8cbb9;font-size:12px}}.holder-row:last-child{{border-bottom:0}}.holder-row b{{color:{deep};font-size:14px}}.holder-row .stake{{color:{accent};font-size:16px;font-weight:950;text-align:right}}.holder-row .value{{color:{gold};font-size:14px;font-weight:900;text-align:right}}footer{{width:100%;margin-top:18px;padding:10px 12px 14px;border-top:1px solid #e5d5c8;color:#9e8c7c;text-align:center;font-size:9.5px;font-weight:600;line-height:1.48}}.signature{{margin-top:6px;color:#9e8c7c;font-size:9.5px;font-weight:600}}
"""
    return (template
            .replace("{height-1}", str(height - 1))
            .replace("{height}", str(height))
            .replace("{accent}", accent)
            .replace("{deep}", deep)
            .replace("{gold}", gold)
            .replace("{{", "{")
            .replace("}}", "}"))


def _document(packet: dict[str, Any], title: str, subtitle: str, strap: str, body: str, height: int) -> str:
    colors = packet["colors"]
    logo = data_uri(packet["logo"]["path"])
    logo_background = esc(packet["logo"].get("background", "rgba(255,255,255,.82)"))
    head = f"<div class='strap'>{esc(strap)}</div><div class='logo-hero'><div class='logo-box' style='background:{logo_background}'><img class='logo-visible' src='{logo}'></div>"
    return f"<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><style>{_css(height, colors['accent'], colors['deep'], colors['gold'])}</style></head><body><main class='page'><h1 class='title'>{esc(title)}</h1><div class='subtitle'>{esc(subtitle)}</div>{head}{body}{_footer(packet['footer_lines'])}</main></body></html>"


def strategy_page(packet: dict[str, Any], height: int = 1260) -> str:
    validate_packet(packet)
    accent = packet["colors"]["accent"]
    strategy = packet["strategy"]
    drivers = "".join(
        f"<div class='driver-card'><div>{icon(item['icon'], accent, 40)}</div><div><h3>{esc(item['title'])}</h3><div class='proof'>{esc(item['metric'])}</div><div class='meaning'>{esc(item['explanation'])}</div></div></div>"
        for item in strategy["drivers"]
    )
    actions = "".join(
        f"<div class='action'><div class='tag'>{esc(item['tag'])}</div><div class='detail'><b>{esc(item['title'])}</b>：{esc(item['detail'])}</div></div>"
        for item in strategy.get("moves", [])[:4]
    )
    quote = f"<div class='quote'>{esc(strategy['quote'])}</div>" if strategy.get("quote") else ""
    body = f"<div class='thesis'>{esc(strategy['thesis'])}<small>只保留真正核心的3-5项；每项都必须有量化证据和行业含义。</small></div></div><section class='section'><h2>核心业务与硬指标</h2><div class='driver-grid'>{drivers}</div></section><section class='section'><h2>近年战略动作</h2>{actions}</section>{quote}"
    return _document(packet, f"{packet['company']}的经营之道", f"{packet['ticker']} · Business Playbook · 核心业务与硬指标", "长期战略定位 × 核心业务 × 数据化护城河 × 战略动作", body, height)


def panorama_page(packet: dict[str, Any], height: int = 1670) -> str:
    validate_packet(packet)
    panorama = packet["panorama"]
    metrics = "".join(
        f"<div class='metric'><div class='value'>{esc(item['value'])}</div><div class='sub'>{esc(item.get('sub', '')) or '&nbsp;'}</div><div class='label'>{esc(item['label'])}</div></div>"
        for item in panorama["metrics"]
    )
    segments = "".join(
        f"<div class='segment-row'><b>{esc(item['name'])}</b><span class='share'>{esc(item['share'])}</span><span>{esc(item['value'])}</span><span>{esc(item['note'])}</span></div>"
        for item in panorama.get("segments", [])[:6]
    )
    capital = "".join(
        f"<div class='capital-card'><h3>{esc(item['label'])}</h3><div class='value'>{esc(item['value'])}</div><div class='note'>{esc(item['note'])}</div></div>"
        for item in panorama["capital"]
    )
    signals = "".join(
        f"<div class='signal'><h3>{esc(item['kind'])}｜{esc(item['title'])}</h3><p>{esc(item['detail'])}</p></div>"
        for item in panorama.get("signals", [])[:4]
    )
    holders = "".join(
        f"<div class='holder-row'><b>{esc(item['kind'])}｜{esc(item['name'])}</b><span class='stake'>{esc(item['stake'])}</span><span class='value'>{esc(item['value'])}</span></div>"
        for item in panorama["holders"]
    )
    thesis = panorama.get("thesis") or packet["strategy"]["thesis"]
    body = f"<div class='thesis'>{esc(thesis)}<small>全年经营按最新完整财年；市值与估值按生成当日或最近交易日。</small></div></div><section class='section'><h2>核心财务与当前估值</h2><div class='metrics'>{metrics}</div></section><section class='section'><h2>业务分部表现</h2>{segments}</section><section class='section'><h2>ROI / CapEx / 股东回报</h2><div class='capital-grid'>{capital}</div></section><section class='section'><h2>亮点与风险</h2><div class='signal-grid'>{signals}</div></section><section class='section'><h2>机构与重要股东</h2><div class='holder-grid'>{holders}</div></section>"
    return _document(packet, f"{packet['company']}经营全景", f"{packet['ticker']} · Financial Dashboard · 全年经营 + 当前估值", "六项核心数据 × 分部结构 × 资本配置 × 机构持仓", body, height)
