#!/usr/bin/env python3
"""Regenerate the top-30 company operating and culture image set."""

from __future__ import annotations

import html
import importlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import textwrap

from company_infographic import generate as generate_company
from top30_enhancement_data import (
    ARCHETYPE_GROUPS,
    BLUE,
    COMMON_TRAITS,
    COMPANY_RUNS,
    CULTURE_PROFILES,
    OPERATING_OVERRIDES,
    apply_operating_overrides,
)


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
if DATA_DIR.is_dir() and str(DATA_DIR) not in sys.path:
    sys.path.insert(0, str(DATA_DIR))
SKETCH_DIR = ROOT / "sketch_refs"
OUT_ROOT = Path("/Users/jiangming/持仓分析/公司经营分析")
COMPARE_DIR = OUT_ROOT / "00_前30管理文化对比"
PLAYWRIGHT_PREFIX = Path("/tmp/codex-playwright-render")
SKETCH1_HEIGHT = 2180
SKETCH2_HEIGHT = 2080
MANAGEMENT_HEIGHT = 2050
COMPARE_HEIGHT = 1540
COMPARE_MATRIX_HEIGHT = 1640
LEGACY_MANAGEMENT_SLUGS = {"broadcom", "aramco", "meta"}
COMPANY_THEMES = {
    "nvidia": ("#76B900", "#4A7A00", "rgba(234,251,208,.62)"),
    "alphabet": ("#4285F4", "#0F9D58", "rgba(232,240,255,.68)"),
    "apple": ("#60656F", "#2E3035", "rgba(235,238,242,.72)"),
    "microsoft": ("#0078D4", "#2F7D32", "rgba(224,240,255,.68)"),
    "amazon": ("#FF9900", "#146EB4", "rgba(255,244,220,.72)"),
    "tsmc": ("#B21F2D", "#6B4E7A", "rgba(255,230,232,.64)"),
    "broadcom": ("#CC092F", "#9A0A25", "rgba(253,228,232,.68)"),
    "aramco": ("#00A3A1", "#006C67", "rgba(220,246,244,.68)"),
    "meta": ("#1877F2", "#0A5AC5", "rgba(224,238,255,.72)"),
    "tesla": ("#E31937", "#8B0A20", "rgba(253,228,232,.68)"),
    "walmart": ("#0071CE", "#FFC220", "rgba(225,241,255,.70)"),
    "berkshire": ("#4A6B3B", "#8B3A4E", "rgba(232,242,225,.68)"),
    "samsung": ("#1428A0", "#1F4E79", "rgba(228,233,255,.70)"),
    "jpmorgan": ("#6B4E2E", "#B28B5E", "rgba(244,235,222,.70)"),
    "lilly": ("#D52B1E", "#8B3A4E", "rgba(253,230,228,.68)"),
    "exxon": ("#D71920", "#0B3D91", "rgba(255,229,230,.68)"),
    "visa": ("#1A1F71", "#F7B600", "rgba(228,230,250,.70)"),
    "tencent": ("#2E8B57", "#1D5F3B", "rgba(226,244,233,.70)"),
    "skhynix": ("#E0002A", "#F37021", "rgba(255,230,235,.68)"),
    "asml": ("#005EB8", "#F28C28", "rgba(226,239,255,.70)"),
    "amd": ("#2E5D8A", "#B8532F", "rgba(232,240,255,.70)"),
    "oracle": ("#C74634", "#312D2A", "rgba(252,232,229,.70)"),
    "mastercard": ("#EB001B", "#F79E1B", "rgba(255,232,230,.68)"),
    "costco": ("#005DAA", "#E31837", "rgba(226,240,255,.70)"),
    "intel": ("#0068B5", "#00AEEF", "rgba(226,241,255,.70)"),
    "netflix": ("#E50914", "#221F1F", "rgba(255,228,230,.68)"),
    "caterpillar": ("#FFCD11", "#2D2D2D", "rgba(255,247,218,.72)"),
    "bankofamerica": ("#D4001A", "#004C97", "rgba(255,229,232,.68)"),
}


def theme_for(slug):
    return COMPANY_THEMES.get(slug, (BLUE, "#0A5AC5", "rgba(210,226,255,.65)"))


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def first_value(mapping, keywords, default="未披露"):
    for key, val in mapping.items():
        if any(k in key for k in keywords):
            return str(val)
    return default


def compact(text, limit=78):
    text = str(text).replace("\n", " ").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def strategy_text(text, limit=42):
    text = compact(text, limit * 2)
    replacements = [
        (r"\$[\d,\.]+(?:\s?(?:T|B|M|万亿|亿美元|亿|美元|\+|区间))*", "相关规模"),
        (r"FY\d{2,4}", "最新年度"),
        (r"\bPE\b|P/E", "市场定价"),
        (r"市值|股价|估值", "市场位置"),
        (r"全年营收|营收|收入", "业务规模"),
        (r"净利润|净利|利润", "利润质量"),
        (r"自由现金流|现金流", "现金创造"),
        (r"CapEx|资本开支", "长期投入"),
        (r"毛利率|营业利润率", "盈利结构"),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip(" ，；,;")
    return compact(text, limit)


def first_tuple_value(rows, index, default=""):
    if rows and len(rows[0]) > index:
        return rows[0][index]
    return default


def source_footer(slug, data, extra=None):
    lines = data.get("FOOTER_LINES") or [data.get("DATA_SOURCE", "公司公开资料"), "免责声明：本图仅供学习参考，不构成投资建议"]
    source = "；".join(
        str(line)
        for line in lines
        if line and "by 江明" not in str(line) and not str(line).startswith("免责声明")
    )
    if extra:
        source = f"{extra}；{source}"
    return f"{source}<br>货币口径：图中金额均为 USD/美元；仅供学习参考，不构成投资建议<br>by 江明"


def strategy_footer(slug, data):
    lines = data.get("FOOTER_LINES") or [data.get("DATA_SOURCE", "公司公开资料")]
    keep = []
    for line in lines:
        text = str(line)
        if not text or "by 江明" in text or text.startswith("免责声明"):
            continue
        if any(k in text for k in ("ROI口径", "ROI 口径", "CapEx口径", "CapEx 口径", "行情数据", "最新市值", "股价")):
            continue
        keep.append(text)
    source = "；".join(keep[:3]) or "公司年报、业绩资料、管理层公开表述"
    return f"经营之道：{source}；财务看板、ROI/ROIC、2026 CapEx 与估值详见《经营全景》<br>货币口径：图中金额均为 USD/美元；仅供学习参考，不构成投资建议<br>by 江明"


def strip_codex_blocks(html_text):
    html_text = re.sub(
        r"\n?<!-- codex-(?:role-note|roi-capex|legacy-style|legacy-footer)-start -->.*?<!-- codex-(?:role-note|roi-capex|legacy-style|legacy-footer)-end -->\n?",
        "\n",
        html_text,
        flags=re.S,
    )
    html_text = re.sub(
        r"\n\s*(?:<div\s+class=[\"']row[\"'][^>]*>.*?</div>\s*){1,8}<div\s+class=[\"']by[\"'][^>]*>\s*by 江明\s*</div>\s*</div>",
        "\n",
        html_text,
        flags=re.S,
    )
    return html_text


def div_end(html_text, start):
    first_close = html_text.find(">", start)
    if first_close < 0:
        return None
    depth = 1
    for tag in re.finditer(r"</?div\b[^>]*>", html_text[first_close + 1 :], flags=re.I):
        if tag.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return first_close + 1 + tag.end()
        else:
            depth += 1
    return None


LEGACY_FOOTER_CSS = """<!-- codex-legacy-footer-start -->
body { position: relative; }
.footer {
  position: absolute !important;
  left: 40px !important;
  right: 40px !important;
  bottom: 24px !important;
  margin-top: 0 !important;
  padding-bottom: 0 !important;
  text-align: center !important;
}
<!-- codex-legacy-footer-end -->"""


def inject_style(html_text, style_text):
    if "</style>" not in html_text:
        return html_text
    return html_text.replace("</style>", f"\n{style_text}\n</style>", 1)


def ensure_min_body_height(html_text, min_height):
    def repl(match):
        current = int(match.group(1))
        return f"height:{max(current, min_height)}px"

    patterns = [
        r"height\s*:\s*(\d+)px",
        r"height=(\d+)px",
    ]
    for pattern in patterns:
        updated, count = re.subn(pattern, repl, html_text, count=1)
        if count:
            return updated
    return html_text


def replace_footer(html_text, footer_html):
    pattern = r'<div\s+class=["\']footer["\'][^>]*>'
    match = re.search(pattern, html_text)
    if not match:
        return html_text

    end = div_end(html_text, match.start())
    if end is None:
        return html_text
    return html_text[: match.start()] + f'<div class="footer">{footer_html}</div>' + html_text[end:]


def replace_first_class_block(html_text, class_name, replacement):
    pattern = rf'<div\b(?=[^>]*class=["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\'])[^>]*>'
    match = re.search(pattern, html_text)
    if not match:
        return html_text
    end = div_end(html_text, match.start())
    if end is None:
        return html_text
    return html_text[: match.start()] + replacement + html_text[end:]


def insert_before_footer(html_text, block):
    pattern = r'(<div\s+class=["\']footer["\'][^>]*>)'
    updated, count = re.subn(pattern, block + r"\n\1", html_text, count=1)
    return updated if count else html_text.replace("</body>", block + "\n</body>", 1)


def insert_before_first_section(html_text, block):
    pattern = r'(<div\s+class=["\']section-title["\'][^>]*>)'
    updated, count = re.subn(pattern, block + r"\n\1", html_text, count=1)
    return updated if count else insert_before_footer(html_text, block)


def make_strategy_panel(slug, data):
    ov = OPERATING_OVERRIDES[slug]
    accent, _, _ = theme_for(slug)
    nodes = ov.get("flywheel", [])[:4]
    thesis = strategy_text(ov.get("thesis", ""), 62)
    return f"""<!-- codex-strategy-panel-start -->
<div class="bigbox codex-strategy-panel">
  <div style="flex:1">
    <div class="t1">经营主线：不是财务表，而是复利逻辑</div>
    <div class="s1">{esc(thesis)}<br>关键链条：{esc(" → ".join(nodes[:4]))}</div>
  </div>
  <div style="text-align:center">
    <div class="num" style="color:{accent}">逻辑</div>
    <div class="lab">数据只作证据</div>
  </div>
</div>
<!-- codex-strategy-panel-end -->"""


def make_strategy_evidence(slug, data):
    ov = OPERATING_OVERRIDES[slug]
    moat = data.get("MOAT", [])
    moves = data.get("STRATEGIC_MOVES", [])
    risk = data.get("RISKS_HIGHLIGHTS", [])
    cells = [
        ("护城河", strategy_text(first_tuple_value(moat, 0, "结构优势"), 22), strategy_text(first_tuple_value(moat, 1, "长期竞争壁垒"), 34)),
        ("飞轮", strategy_text(" → ".join(ov.get("flywheel", [])[:3]), 22), "解释增长如何自我强化"),
        ("战略动作", strategy_text(first_tuple_value(moves, 1, "下一步动作"), 22), strategy_text(first_tuple_value(moves, 2, "管理层正在推进的关键动作"), 34)),
        ("关键变量", strategy_text(first_tuple_value(risk, 1, "需要验证的变量"), 22), strategy_text(first_tuple_value(risk, 2, "这决定逻辑能否兑现"), 34)),
    ]
    cell_html = "".join(
        f"<div class=\"yld-cell\"><div class=\"yld-num\">{esc(title)}</div><div class=\"yld-lab\">{esc(main)}</div><div class=\"yld-sub\">{esc(sub)}</div></div>"
        for title, main, sub in cells
    )
    return f"""<!-- codex-strategy-evidence-start -->
<div class="yieldbox codex-strategy-evidence">
  <div class="yld-title">经营证据：只保留能解释护城河的数据</div>
  <div class="yld-row">{cell_html}</div>
</div>
<!-- codex-strategy-evidence-end -->"""


def replace_strategy_stats(html_text, slug):
    ov = OPERATING_OVERRIDES[slug]
    nodes = ov.get("flywheel", [])[:4]
    stats = f"""<div class="stats">
      <span>核心逻辑：{esc(strategy_text(ov.get("thesis", ""), 34))}</span><br>
      <span>飞轮变量：{esc(" → ".join(nodes[:4]))}</span>
    </div>"""
    return replace_first_class_block(html_text, "stats", stats)


def scrub_strategy_financial_labels(html_text):
    replacements = [
        ("关键经营数字", "经营证据"),
        ("核心经营数据", "经营证据"),
        ("FY2025", "最新年度"),
        ("FY2026", "最新年度"),
        ("全年营收", "业务规模"),
        ("营收", "业务规模"),
        ("净利润", "利润质量"),
        ("净利", "利润质量"),
        ("自由现金流", "现金创造"),
        ("最新市值", "市场位置"),
        ("股价 / 市值", "市场位置"),
        ("市值", "市场位置"),
        ("PE", "市场定价"),
        ("CapEx", "长期投入"),
        ("资本开支", "长期投入"),
    ]
    for old, new in replacements:
        html_text = html_text.replace(old, new)
    return re.sub(r"\$[\d,\.]+(?:\s?(?:T|B|M|万亿|亿美元|亿|美元|\+|区间))*", "规模数据见全景", html_text)


def differentiate_strategy_sketch(html_text, slug, data):
    html_text = replace_strategy_stats(html_text, slug)
    html_text = replace_first_class_block(html_text, "bigbox", make_strategy_panel(slug, data))
    html_text = replace_first_class_block(html_text, "yieldbox", make_strategy_evidence(slug, data))
    return scrub_strategy_financial_labels(html_text)


def augment_legacy_sketch1(html_text, slug, data):
    accent, _, soft = theme_for(slug)
    style = f"""<!-- codex-legacy-style-start -->
:root {{ --codex-accent: {accent}; --codex-soft: {soft}; }}
.codex-role-note {{
  margin: 18px 40px 0;
  border: 2px dashed var(--codex-accent);
  border-radius: 12px;
  background: rgba(255,255,255,.52);
  padding: 12px 18px;
  color: #5A4A3A;
  font-size: 17px;
  line-height: 1.55;
  text-align: center;
}}
.codex-role-note b {{ color: var(--codex-accent); }}
.codex-strategy-panel .num {{ font-size: 42px !important; }}
.codex-strategy-evidence .yld-num {{ font-size: 24px !important; line-height: 1.15 !important; color: var(--codex-accent) !important; }}
.codex-strategy-evidence .yld-lab {{ font-size: 16px !important; font-weight: 800 !important; color: #4B3B2F !important; }}
.codex-strategy-evidence .yld-sub {{ font-size: 13px !important; line-height: 1.35 !important; color: #7B6650 !important; }}
<!-- codex-legacy-style-end -->"""
    block = """<!-- codex-role-note-start -->
<div class="codex-role-note"><b>经营之道：</b>只讲护城河、飞轮和战略变量；营收、利润、估值、ROI/ROIC 和 2026 CapEx 放在“经营全景”。</div>
<!-- codex-role-note-end -->"""
    html_text = strip_codex_blocks(html_text)
    html_text = ensure_min_body_height(html_text, 2300)
    html_text = differentiate_strategy_sketch(html_text, slug, data)
    html_text = inject_style(html_text, style + "\n" + LEGACY_FOOTER_CSS)
    html_text = replace_footer(html_text, strategy_footer(slug, data))
    return insert_before_footer(html_text, block)


def augment_legacy_sketch2(html_text, slug, data):
    ov = OPERATING_OVERRIDES[slug]
    accent, _, soft = theme_for(slug)
    style = f"""<!-- codex-legacy-style-start -->
:root {{ --codex-accent: {accent}; --codex-soft: {soft}; }}
.codex-roi-capex {{
  margin: 18px 40px 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}}
.codex-fin-card {{
  border: 2px solid var(--codex-accent);
  border-radius: 12px;
  background: var(--codex-soft);
  padding: 13px 16px;
  min-height: 108px;
}}
.codex-fin-card .k {{ color: var(--codex-accent); font-weight: 800; font-size: 18px; }}
.codex-fin-card .v {{ font-family: 'Songti SC','STSong','SimSun',serif; color: #3A2A1E; font-size: 30px; font-weight: 700; margin-top: 4px; }}
.codex-fin-card .n {{ color: #6F5E4D; font-size: 15px; line-height: 1.35; margin-top: 5px; }}
<!-- codex-legacy-style-end -->"""
    block = f"""<!-- codex-roi-capex-start -->
<div class="codex-roi-capex">
  <div class="codex-fin-card"><div class="k">ROI / ROIC</div><div class="v">{esc(ov['roi'])}</div><div class="n">{esc(compact(ov['roi_note'], 58))}</div></div>
  <div class="codex-fin-card"><div class="k">2026 CapEx</div><div class="v">{esc(ov['capex'])}</div><div class="n">{esc(compact(ov['capex_note'], 58))}</div></div>
</div>
<!-- codex-roi-capex-end -->"""
    html_text = strip_codex_blocks(html_text)
    html_text = ensure_min_body_height(html_text, 2320)
    html_text = inject_style(html_text, style + "\n" + LEGACY_FOOTER_CSS)
    html_text = replace_footer(html_text, source_footer(slug, data, "经营全景：公司年报/业绩资料/行情资料"))
    return insert_before_first_section(html_text, block)


def html_canvas_size(path, fallback_height):
    text = Path(path).read_text(encoding="utf-8")
    width_match = re.search(r"width\s*:\s*(\d+)px", text)
    height_match = re.search(r"height\s*:\s*(\d+)px", text)
    return {
        "width": int(width_match.group(1)) if width_match else 900,
        "height": int(height_match.group(1)) if height_match else fallback_height,
    }


def css(height, accent="#1877F2", soft="rgba(210,226,255,.65)"):
    return f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  width: 900px; height: {height}px; overflow: hidden; position: relative;
  background: #F7F4ED; color: #3A2A1E;
  font-family: 'PingFang SC', 'Hiragino Sans GB', 'Noto Sans SC', sans-serif;
}}
body::before {{
  content: ''; position: absolute; inset: 0; pointer-events: none; opacity: .36;
  background:
    repeating-linear-gradient(0deg, transparent, transparent 39px, #E8E4DC 39px, #E8E4DC 40px),
    repeating-linear-gradient(90deg, transparent, transparent 39px, #E8E4DC 39px, #E8E4DC 40px);
}}
.page {{ position: relative; z-index: 1; padding: 42px 40px 0; }}
.title {{ text-align:center; color:{accent}; font-family:'Songti SC','STSong',serif; font-size:72px; font-weight:800; letter-spacing:4px; line-height:1.08; }}
.subtitle {{ margin-top:10px; text-align:center; color:#9B8A7A; font-size:22px; font-style:italic; }}
.pill {{ margin:22px auto 30px; width:max-content; max-width:780px; border:3px solid {accent}; border-radius:999px; padding:12px 28px; color:#5E5A6D; font-size:26px; font-weight:800; background:rgba(255,255,255,.45); }}
.hero {{ display:flex; gap:28px; align-items:center; margin:18px 0 28px; }}
.mark {{ width:190px; height:190px; border:4px solid {accent}; border-radius:28px; display:flex; align-items:center; justify-content:center; color:{accent}; font-family:'Songti SC','STSong',serif; font-size:78px; font-weight:900; background:rgba(255,255,255,.45); transform:rotate(-1.5deg); }}
.thesis {{ flex:1; border-left:8px solid {accent}; padding-left:24px; }}
.thesis .k {{ color:{accent}; font-size:26px; font-weight:900; margin-bottom:8px; }}
.thesis .v {{ font-family:'Songti SC','STSong',serif; font-size:39px; line-height:1.35; font-weight:800; color:#3A2A1E; }}
.section-title {{ margin:32px 0 20px; text-align:center; color:{accent}; font-family:'Songti SC','STSong',serif; font-size:48px; font-weight:900; }}
.grid-4 {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }}
.stat {{ border:3px solid; border-radius:14px; padding:15px 8px; min-height:120px; text-align:center; background:rgba(255,255,255,.48); }}
.stat .num {{ font-family:'Songti SC','STSong',serif; font-size:37px; font-weight:900; line-height:1.05; }}
.stat .lab {{ margin-top:8px; font-size:18px; line-height:1.3; color:#6E6256; }}
.cards {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
.card {{ background:rgba(255,255,255,.6); border:3px solid #D5BFAE; border-radius:18px; padding:20px; min-height:190px; }}
.card h3 {{ color:{accent}; font-family:'Songti SC','STSong',serif; font-size:32px; line-height:1.15; margin-bottom:8px; }}
.tag {{ display:inline-block; background:{accent}; color:white; border-radius:8px; padding:5px 12px; font-size:17px; font-weight:800; margin-bottom:10px; }}
.body {{ color:#4B3B2F; font-size:21px; line-height:1.55; }}
.flow {{ display:flex; align-items:stretch; gap:12px; margin:10px 0 22px; }}
.flow .node {{ flex:1; border:3px solid {accent}; border-radius:14px; padding:14px 8px; text-align:center; background:rgba(255,255,255,.55); }}
.flow .node b {{ display:block; color:{accent}; font-size:22px; margin-bottom:6px; }}
.arrow {{ align-self:center; color:#8A7A68; font-size:28px; font-weight:900; }}
.segments {{ border:3px solid #D5BFAE; border-radius:16px; padding:16px 18px; background:rgba(255,255,255,.5); }}
.seg-row {{ display:grid; grid-template-columns:34px 235px 100px 100px 1fr; gap:12px; align-items:center; min-height:46px; border-bottom:1px dashed #D8CBB9; font-size:19px; }}
.seg-row:last-child {{ border-bottom:0; }}
.rank {{ width:30px; height:30px; border-radius:50%; background:{accent}; color:white; display:flex; align-items:center; justify-content:center; font-weight:900; }}
.bar-bg {{ height:22px; background:#EDE6DA; border-radius:5px; overflow:hidden; }}
.bar {{ height:100%; background:{accent}; border-radius:5px; }}
.note-box {{ margin-top:24px; border:4px solid {accent}; background:{soft}; border-radius:18px; padding:24px 28px; }}
.note-box h3 {{ color:{accent}; font-family:'Songti SC','STSong',serif; font-size:34px; margin-bottom:8px; }}
.note-box p {{ font-size:23px; line-height:1.55; }}
.list {{ font-size:23px; line-height:1.55; color:#4B3B2F; }}
.list li {{ margin:8px 0 8px 28px; }}
.footer {{ position:absolute; left:24px; right:24px; bottom:26px; text-align:center; color:#B0A090; font-size:16px; line-height:1.58; }}
"""


def make_sketch1(slug, run, data):
    ov = OPERATING_OVERRIDES[slug]
    moat = data.get("MOAT", [])[:4]
    moves = data.get("STRATEGIC_MOVES", [])[:3]
    nodes = ov["flywheel"][:5]
    cards = []
    for title, desc in moat[:4]:
        cards.append(f"<div class='card'><h3>{esc(title)}</h3><div class='body'>{esc(compact(desc, 72))}</div></div>")
    move_lines = "".join(f"<li><b>{esc(a)}：</b>{esc(compact(t, 32))}，{esc(compact(d, 58))}</li>" for a, t, d, *_ in moves)
    flow = ""
    for i, node in enumerate(nodes):
        if i:
            flow += "<div class='arrow'>→</div>"
        flow += f"<div class='node'><b>{esc(node)}</b><span>经营飞轮</span></div>"
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>{css(SKETCH1_HEIGHT, BLUE)}</style></head><body>
<div class='page'>
  <div class='title'>{esc(run['name'])} 的 经 营 之 道</div>
  <div class='subtitle'>{esc(run['ticker'])} · Business Logic · 低重复版</div>
  <div class='pill'>只回答：这家公司为什么能长期赚钱</div>
  <div class='hero'><div class='mark'>{esc(run['name'][:2])}</div><div class='thesis'><div class='k'>一句话逻辑</div><div class='v'>{esc(ov['thesis'])}</div></div></div>
  <div class='section-title'>核心飞轮</div>
  <div class='flow'>{flow}</div>
  <div class='section-title'>护城河不是口号</div>
  <div class='cards'>{''.join(cards)}</div>
  <div class='section-title'>正在发生的变化</div>
  <div class='note-box'><h3>2025-2026 关键动作</h3><ul class='list'>{move_lines}</ul></div>
  <div class='note-box'><h3>这张图的边界</h3><p>这里不重复财务表。ROI、2026 CapEx、分部收入和估值放在“经营全景”里，这张只讲商业逻辑和护城河。</p></div>
</div>
<div class='footer'>{source_footer(slug, data, '经营之道：公司年报/业绩资料/管理层公开表述')}</div>
</body></html>"""


def make_sketch2(slug, run, data):
    ov = OPERATING_OVERRIDES[slug]
    fs = data.get("FINANCIAL_SUMMARY", {})
    revenue = first_value(fs, ["营收", "收入"])
    profit = first_value(fs, ["净利润", "Non-GAAP 净利", "经营利润", "利润"])
    stats = [
        ("营收", revenue),
        ("利润", profit),
        ("ROI", ov["roi"]),
        ("2026 CapEx", ov["capex"]),
    ]
    stat_html = "".join(f"<div class='stat' style='border-color:{BLUE}'><div class='num' style='color:{BLUE}'>{esc(compact(v, 18))}</div><div class='lab'>{esc(k)}</div></div>" for k, v in stats)
    seg_rows = ""
    for idx, row in enumerate(data.get("BUSINESS_SEGMENTS", [])[:5], 1):
        _, name, pct, rev, yoy, *_ = row
        try:
            width = min(100, max(4, float(str(pct).replace('%', '').replace('约', ''))))
        except Exception:
            width = 18
        seg_rows += f"<div class='seg-row'><div class='rank'>{idx}</div><b>{esc(name)}</b><span>{esc(pct)}</span><b>{esc(rev)}</b><div class='bar-bg'><div class='bar' style='width:{width}%'></div></div></div>"
    risks = "".join(f"<li><b>{esc(kind)} · {esc(title)}：</b>{esc(compact(desc, 64))}</li>" for kind, title, desc in data.get("RISKS_HIGHLIGHTS", [])[:5])
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>{css(SKETCH2_HEIGHT, '#8B3A4E')}</style></head><body>
<div class='page'>
  <div class='title'>{esc(run['name'])} 经营全景</div>
  <div class='subtitle'>{esc(run['ticker'])} · Financial Dashboard · ROI + 2026 CapEx</div>
  <div class='pill'>只回答：现在怎么赚钱，钱投到哪里</div>
  <div class='grid-4'>{stat_html}</div>
  <div class='section-title'>业务分部与收入结构</div>
  <div class='segments'>{seg_rows}</div>
  <div class='cards' style='margin-top:24px'>
    <div class='card'><span class='tag'>ROI / ROIC</span><h3>{esc(ov['roi'])}</h3><div class='body'>{esc(ov['roi_note'])}</div></div>
    <div class='card'><span class='tag'>2026 CapEx</span><h3>{esc(ov['capex'])}</h3><div class='body'>{esc(ov['capex_note'])}</div></div>
  </div>
  <div class='section-title'>亮点与风险</div>
  <div class='note-box'><ul class='list'>{risks}</ul></div>
  <div class='note-box'><h3>一句话判断</h3><p>{esc(run['name'])} 的经营全景，核心是把利润质量、资本开支和长期回报放在同一张表里看，而不是只看营收增长。</p></div>
</div>
<div class='footer'>{source_footer(slug, data, '经营全景：公司年报/业绩资料/行情资料')}</div>
</body></html>"""


def make_management(slug, run):
    c = CULTURE_PROFILES[slug]
    accent, _, soft = theme_for(slug)
    stats = "".join(f"<div class='stat' style='border-color:{accent}'><div class='num' style='color:{accent}'>{esc(a)}</div><div class='lab'>{esc(b)}</div></div>" for a, b in c["stats"])
    cards = "".join(f"<div class='card'><span class='tag'>{esc(tag)}</span><h3>{esc(title)}</h3><div class='body'>{esc(body)}</div></div>" for title, tag, body in c["mechanisms"])
    emp = "".join(f"<li>{esc(x)}</li>" for x in c["employee_view"])
    inv = "".join(f"<li>{esc(x)}</li>" for x in c["investor_view"])
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>{css(MANAGEMENT_HEIGHT, accent, soft)}</style></head><body>
<div class='page'>
  <div class='title'>{esc(run['name'])} 的 管 理 文 化</div>
  <div class='subtitle'>{esc(c['archetype'])} · Management Culture</div>
  <div class='pill'>{esc(c['tagline'])}</div>
  <div class='hero'><div class='mark'>{esc(run['name'][:2])}</div><div class='thesis'><div class='k'>不是福利清单，而是组织如何赚钱</div><div class='v'>{esc(c['thesis'])}</div></div></div>
  <div class='grid-4'>{stats}</div>
  <div class='section-title'>四个管理机制</div>
  <div class='cards'>{cards}</div>
  <div class='section-title'>员工与投资人两种视角</div>
  <div class='cards'>
    <div class='card'><h3>员工视角</h3><ul class='list'>{emp}</ul></div>
    <div class='card'><h3>投资人视角</h3><ul class='list'>{inv}</ul></div>
  </div>
  <div class='note-box'><h3>一句话总结</h3><p>{esc(c['summary'])}</p></div>
</div>
<div class='footer'>管理文化：{esc(c['sources'])}<br>货币口径：图中金额均为 USD/美元；仅供学习参考，不构成投资建议<br>by 江明</div>
</body></html>"""


def make_compare_pages():
    pages = []
    normal_height = COMPARE_HEIGHT
    matrix_height = COMPARE_MATRIX_HEIGHT
    common_cards = "".join(f"<div class='card'><h3>{esc(t)}</h3><div class='body'>{esc(d)}</div></div>" for t, d in COMMON_TRAITS)
    pages.append(("top30_management_01_共性总览", normal_height, f"""<!doctype html><html><head><meta charset='utf-8'><style>{css(normal_height, BLUE)}</style></head><body>
<div class='page'><div class='title'>前30公司管理文化共性</div><div class='subtitle'>Top 30 Management Culture · 时代共同特征</div><div class='pill'>优秀公司共同点：人才、资本、机制、信任</div><div class='cards'>{common_cards}</div><div class='note-box'><h3>结论</h3><p>这个时代最强公司，不只是技术强，而是能把高人才密度、长期资本开支、硬绩效机制和平台信任组合成一个可复利的组织系统。</p></div></div><div class='footer'>来源：前30公司年报、Proxy/治理文件、官方 Careers/文化页面，核查 2026-05-09<br>货币口径：图中金额均为 USD/美元；仅供学习参考，不构成投资建议<br>by 江明</div></body></html>"""))

    group_cards = ""
    for name, slugs, desc in ARCHETYPE_GROUPS:
        companies = "、".join(CULTURE_PROFILES[s]["archetype"].split("型")[0] + "/" + s for s in slugs[:7])
        real_names = "、".join(next(r["name"] for r in COMPANY_RUNS if r["slug"] == s) for s in slugs[:8])
        group_cards += f"<div class='card'><h3>{esc(name)}</h3><div class='body'><b>代表：</b>{esc(real_names)}<br>{esc(desc)}</div></div>"
    pages.append(("top30_management_02_组织模型", normal_height, f"""<!doctype html><html><head><meta charset='utf-8'><style>{css(normal_height, '#8B3A4E')}</style></head><body><div class='page'><div class='title'>五种优秀组织模型</div><div class='subtitle'>Founder / Engineering / Customer / Network / Capital</div><div class='pill'>不是所有优秀公司都用同一种文化</div><div class='cards'>{group_cards}</div><div class='note-box'><h3>怎么看</h3><p>文化没有唯一答案。重资产公司要工程纪律，轻资产平台要网络信任，创始人公司要战略集中，金融公司要风险纪律，零售公司要一线执行。</p></div></div><div class='footer'>来源：前30公司年报、Proxy/治理文件、官方 Careers/文化页面，核查 2026-05-09<br>仅供学习参考，不构成投资建议<br>by 江明</div></body></html>"""))

    def matrix_page(name, runs):
        rows = ""
        for run in runs:
            c = CULTURE_PROFILES[run["slug"]]
            ov = OPERATING_OVERRIDES[run["slug"]]
            rows += f"<div class='seg-row' style='grid-template-columns:46px 110px 190px 210px 1fr'><div class='rank'>{run['rank']}</div><b>{esc(run['name'])}</b><span>{esc(c['archetype'])}</span><span>{esc(compact(c['tagline'], 20))}</span><span>{esc(compact(ov['capex'], 22))}</span></div>"
        return f"""<!doctype html><html><head><meta charset='utf-8'><style>{css(matrix_height, '#6B4E7A')}</style></head><body><div class='page'><div class='title'>{esc(name)}</div><div class='subtitle'>公司 · 组织模型 · 文化关键词 · 2026 CapEx</div><div class='pill'>把公司放在同一张管理文化表里看</div><div class='segments'>{rows}</div><div class='note-box'><h3>读法</h3><p>同样是大公司，真正的差异不在口号，而在人才筛选、资本开支、绩效机制和风险边界。CapEx 高不一定好，关键是组织有没有把钱投到自己的瓶颈上。</p></div></div><div class='footer'>来源：前30公司年报、Proxy/治理文件、官方 Careers/文化页面，核查 2026-05-09<br>货币口径：图中金额均为 USD/美元；仅供学习参考，不构成投资建议<br>by 江明</div></body></html>"""

    pages.append(("top30_management_03_前15矩阵", matrix_height, matrix_page("前15公司管理文化矩阵", COMPANY_RUNS[:15])))
    pages.append(("top30_management_04_后15矩阵", matrix_height, matrix_page("后15公司管理文化矩阵", COMPANY_RUNS[15:])))

    formula_cards = "".join(
        f"<div class='card'><h3>{esc(t)}</h3><div class='body'>{esc(d)}</div></div>"
        for t, d in [
            ("第一层：选人", "高人才密度、关键岗位高标准、愿意付出高薪酬或高股权。"),
            ("第二层：机制", "目标清楚、反馈足够硬、好项目能拿到资源，低回报项目会被停止。"),
            ("第三层：资本", "现金流投向真正瓶颈：AI 算力、制程、产能、网络安全、内容或药物管线。"),
            ("第四层：信任", "客户、员工、监管和供应链都信任公司能长期兑现承诺。"),
            ("第五层：时间", "优秀公司不是不犯错，而是能用长期主义和复盘机制修正错误。"),
            ("反面信号", "口号很多、绩效很软、资本开支讲不清、创始人押注无反馈、人才流失却不调整。"),
        ]
    )
    pages.append(("top30_management_05_优秀公司公式", normal_height, f"""<!doctype html><html><head><meta charset='utf-8'><style>{css(normal_height, '#0A5AC5')}</style></head><body><div class='page'><div class='title'>优秀公司管理文化公式</div><div class='subtitle'>What Great Companies Have In Common</div><div class='pill'>高人才密度 × 硬机制 × 长期资本 × 信任</div><div class='cards'>{formula_cards}</div><div class='note-box'><h3>最终判断</h3><p>真正优秀的公司，会让人才、机制和资本互相增强。只有文化，没有现金流，是口号；只有现金流，没有文化，是周期；二者能相互喂养，才是长期复利。</p></div></div><div class='footer'>来源：前30公司年报、Proxy/治理文件、官方 Careers/文化页面，核查 2026-05-09<br>仅供学习参考，不构成投资建议<br>by 江明</div></body></html>"""))
    return pages


def write_html(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def ensure_playwright():
    if not (PLAYWRIGHT_PREFIX / "node_modules" / "playwright").exists():
        subprocess.run(
            ["npm", "install", "--prefix", str(PLAYWRIGHT_PREFIX), "--no-audit", "--no-fund", "--ignore-scripts", "playwright"],
            check=True,
        )


def render_jobs(jobs):
    ensure_playwright()
    script = """
const fs = require('fs');
const { chromium } = require('playwright');
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--disable-dev-shm-usage'] });
  for (const job of jobs) {
    const page = await browser.newPage({ viewport: { width: job.width, height: job.height }, deviceScaleFactor: job.scale || 3 });
    await page.route('**/*', route => {
      const url = route.request().url();
      if (url.includes('fonts.googleapis.com') || url.includes('fonts.gstatic.com')) return route.abort();
      return route.continue();
    });
    await page.goto('file://' + job.html, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(150);
    await page.screenshot({ path: job.out, fullPage: false, animations: 'disabled', timeout: 60000 });
    await page.close();
    console.log(`${job.out} ${job.width * (job.scale || 3)}x${job.height * (job.scale || 3)}`);
  }
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
"""
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        js_path = td / "render.js"
        jobs_path = td / "jobs.json"
        js_path.write_text(script, encoding="utf-8")
        jobs_path.write_text(json.dumps(jobs, ensure_ascii=False), encoding="utf-8")
        env = os.environ.copy()
        env["NODE_PATH"] = str(PLAYWRIGHT_PREFIX / "node_modules")
        subprocess.run(["node", str(js_path), str(jobs_path)], check=True, env=env)


def main():
    SKETCH_DIR.mkdir(parents=True, exist_ok=True)
    COMPARE_DIR.mkdir(parents=True, exist_ok=True)
    jobs = []

    for run in COMPANY_RUNS:
        slug = run["slug"]
        out_dir = OUT_ROOT / run["folder"]
        out_dir.mkdir(parents=True, exist_ok=True)
        mod = importlib.import_module(f"data_{slug}")
        data = apply_operating_overrides(dict(mod.DATA), slug)

        generate_company(f"data_{slug}", str(out_dir / f"{run['prefix']}_经营分析.png"))

        sketch1 = SKETCH_DIR / f"{slug}_sketch1.html"
        sketch2 = SKETCH_DIR / f"{slug}_sketch2.html"
        culture = SKETCH_DIR / f"{slug}_management_culture.html"
        sketch1_html = sketch1.read_text(encoding="utf-8") if sketch1.exists() else make_sketch1(slug, run, data)
        sketch2_html = sketch2.read_text(encoding="utf-8") if sketch2.exists() else make_sketch2(slug, run, data)
        if culture.exists():
            culture_html = replace_footer(
                strip_codex_blocks(culture.read_text(encoding="utf-8")),
                f"管理文化：{esc(CULTURE_PROFILES[slug]['sources'])}<br>货币口径：图中金额均为 USD/美元；仅供学习参考，不构成投资建议<br>by 江明",
            )
        else:
            culture_html = make_management(slug, run)

        write_html(sketch1, augment_legacy_sketch1(sketch1_html, slug, data))
        write_html(sketch2, augment_legacy_sketch2(sketch2_html, slug, data))
        write_html(culture, culture_html)

        sketch1_size = html_canvas_size(sketch1, SKETCH1_HEIGHT)
        sketch2_size = html_canvas_size(sketch2, SKETCH2_HEIGHT)
        culture_size = html_canvas_size(culture, MANAGEMENT_HEIGHT)

        jobs.extend([
            {"html": str(sketch1), "out": str(out_dir / f"{run['prefix']}_sketch1.png"), **sketch1_size, "scale": 3},
            {"html": str(sketch2), "out": str(out_dir / f"{run['prefix']}_sketch2.png"), **sketch2_size, "scale": 3},
            {"html": str(culture), "out": str(out_dir / f"{run['prefix']}_管理文化.png"), **culture_size, "scale": 3},
        ])

    for name, height, content in make_compare_pages():
        html_path = SKETCH_DIR / f"{name}.html"
        out_path = COMPARE_DIR / f"{name}.png"
        write_html(html_path, content)
        jobs.append({"html": str(html_path), "out": str(out_path), "width": 900, "height": height, "scale": 3})

    render_jobs(jobs)
    print(f"Rendered {len(jobs)} hand-drawn images and regenerated {len(COMPANY_RUNS)} operating images.")


if __name__ == "__main__":
    main()
