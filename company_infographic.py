#!/usr/bin/env python3
"""
公司经营情况长图 - 段永平橙色风格
基于 investor_infographic.py 改造：把"持仓/投资哲学"语义替换为"经营/护城河"。
默认 4K 输出（SCALE=3，宽度2400px）。

用法：
    python3 company_infographic.py data_pdd
    python3 company_infographic.py data_tencent 腾讯经营.png
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys
import importlib

SCALE = 3

def s(v):
    return int(v * SCALE)

BG_COLOR = "#FFFFFF"
HEADER_BG = "#E8883A"
SECTION_BG = "#EB9650"
SECTION_TEXT = "#FFFFFF"
ACCENT_COLOR = "#D4793A"
LIGHT_BG = "#FDF5EE"
BORDER_COLOR = "#F0D9C4"
TEXT_COLOR = "#3D3D3D"
GRAY_TEXT = "#888888"
TAG_BG = "#FEF7F0"
TAG_BORDER = "#F0D0A8"
GREEN_COLOR = "#5BA85B"
RED_COLOR = "#D9534F"


def get_font(size, bold=False):
    scaled = s(size)
    if bold:
        try:
            return ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", scaled)
        except Exception:
            pass
    try:
        return ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", scaled)
    except Exception:
        try:
            return ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", scaled)
        except Exception:
            return ImageFont.load_default()


WIDTH = s(800)
PADDING = s(40)
CONTENT_W = WIDTH - PADDING * 2


class CompanyInfographic:
    def __init__(self, data):
        self.data = data
        self.y = 0
        self.calculating = True
        self.img = Image.new("RGB", (WIDTH, 100), BG_COLOR)
        self.draw = ImageDraw.Draw(self.img)
        self._build()
        total_h = self.y + s(40)

        self.y = 0
        self.calculating = False
        self.img = Image.new("RGB", (WIDTH, total_h), BG_COLOR)
        self.draw = ImageDraw.Draw(self.img)
        self._build()

    def _build(self):
        d = self.data
        self._draw_header()
        if d.get("COMPANY_PROFILE"):
            self._draw_kv_section("公司档案", "🏢", d["COMPANY_PROFILE"])
        if d.get("FINANCIAL_SUMMARY"):
            self._draw_kv_section("核心财务摘要", "📊", d["FINANCIAL_SUMMARY"])
        if d.get("BUSINESS_SEGMENTS"):
            self._draw_business_segments()
        if d.get("REVENUE_MIX"):
            self._draw_revenue_mix()
        if d.get("STRATEGIC_MOVES"):
            self._draw_strategic_moves()
        if d.get("MOAT"):
            self._draw_moat()
        if d.get("KEY_METRICS"):
            self._draw_key_metrics()
        if d.get("RISKS_HIGHLIGHTS"):
            self._draw_risks_highlights()
        if d.get("QUOTES"):
            self._draw_quotes()
        self._draw_footer()

    def _draw_header(self):
        d = self.data
        h = s(160)
        if not self.calculating:
            self.draw.rectangle([0, 0, WIDTH, h], fill=HEADER_BG)
            font_title = get_font(42, bold=True)
            tw = self.draw.textlength(d["TITLE"], font=font_title)
            self.draw.text(((WIDTH - tw) / 2, s(25)), d["TITLE"], fill="white", font=font_title)
            font_sub = get_font(18)
            sw = self.draw.textlength(d["SUBTITLE"], font=font_sub)
            self.draw.text(((WIDTH - sw) / 2, s(82)), d["SUBTITLE"], fill="#F0D9C4", font=font_sub)
            font_date = get_font(14)
            dw = self.draw.textlength(d["UPDATE_DATE"], font=font_date)
            self.draw.text(((WIDTH - dw) / 2, s(115)), d["UPDATE_DATE"], fill="#F0D9C4", font=font_date)
            self.draw.rectangle([PADDING, s(142), WIDTH - PADDING, s(144)], fill="#F0D9C4")
        self.y = h + s(10)

    def _draw_section_header(self, title, icon="●"):
        h = s(44)
        if not self.calculating:
            self.draw.rounded_rectangle(
                [PADDING, self.y, WIDTH - PADDING, self.y + h],
                radius=s(6), fill=SECTION_BG
            )
            font = get_font(20, bold=True)
            text = f"  {icon}  {title}"
            self.draw.text((PADDING + s(12), self.y + s(10)), text, fill=SECTION_TEXT, font=font)
        self.y += h + s(12)

    def _draw_kv_pair(self, key, value):
        font_key = get_font(16, bold=True)
        font_val = get_font(16)
        x = PADDING + s(20)
        if not self.calculating:
            self.draw.text((x, self.y), f"{key}：", fill=ACCENT_COLOR, font=font_key)
            kw = self.draw.textlength(f"{key}：", font=font_key)
            self.draw.text((x + kw + s(4), self.y), value, fill=TEXT_COLOR, font=font_val)
        self.y += s(28)

    def _draw_kv_section(self, title, icon, data):
        self._draw_section_header(title, icon)
        if isinstance(data, dict):
            for k, v in data.items():
                self._draw_kv_pair(k, v)
        elif isinstance(data, list):
            for k, v in data:
                self._draw_kv_pair(k, v)
        self.y += s(10)

    def _draw_business_segments(self):
        segments = self.data["BUSINESS_SEGMENTS"]
        label = self.data.get("SEGMENTS_LABEL", "业务分部营收")
        self._draw_section_header(label, "🏆")

        font_h = get_font(14, bold=True)
        if not self.calculating:
            cols = [PADDING + s(15), PADDING + s(45), PADDING + s(230), PADDING + s(320),
                    PADDING + s(410), PADDING + s(500), PADDING + s(595)]
            headers = ["#", "业务分部", "占比", "营收", "同比", "趋势", "备注"]
            self.draw.rectangle([PADDING + s(8), self.y - s(2), WIDTH - PADDING - s(8), self.y + s(24)], fill=LIGHT_BG)
            for col, header in zip(cols, headers):
                self.draw.text((col, self.y + s(2)), header, fill=ACCENT_COLOR, font=font_h)
        self.y += s(30)

        font_row = get_font(14)
        font_row_b = get_font(14, bold=True)
        for i, row in enumerate(segments):
            if not self.calculating:
                if i % 2 == 0:
                    self.draw.rectangle([PADDING + s(8), self.y - s(2), WIDTH - PADDING - s(8), self.y + s(22)], fill="#FFF8F0")
                cols = [PADDING + s(20), PADDING + s(45), PADDING + s(230), PADDING + s(320),
                        PADDING + s(410), PADDING + s(500), PADDING + s(595)]
                self.draw.text((cols[0], self.y), row[0], fill=GRAY_TEXT, font=font_row)
                self.draw.text((cols[1], self.y), row[1], fill=TEXT_COLOR, font=font_row_b)
                self.draw.text((cols[2], self.y), row[2], fill=ACCENT_COLOR, font=font_row)
                self.draw.text((cols[3], self.y), row[3], fill=TEXT_COLOR, font=font_row_b)
                yoy = row[4]
                yoy_color = GREEN_COLOR if yoy.startswith("+") else (RED_COLOR if yoy.startswith("-") else TEXT_COLOR)
                self.draw.text((cols[4], self.y), yoy, fill=yoy_color, font=font_row_b)
                self.draw.text((cols[5], self.y), row[5], fill=GRAY_TEXT, font=font_row)
                self.draw.text((cols[6], self.y), row[6], fill=GRAY_TEXT, font=font_row)
            self.y += s(26)
        self.y += s(10)

    def _draw_revenue_mix(self):
        self._draw_section_header("收入结构占比", "📈")
        font = get_font(16)
        font_b = get_font(16, bold=True)
        max_name_w = 0
        if not self.calculating:
            for name, pct, *_ in self.data["REVENUE_MIX"]:
                nw = self.draw.textlength(name, font=font_b)
                if nw > max_name_w:
                    max_name_w = nw
        bar_x_base = PADDING + s(20) + max_name_w + s(20)
        for name, pct, *_ in self.data["REVENUE_MIX"]:
            if not self.calculating:
                x = PADDING + s(20)
                self.draw.text((x, self.y), name, fill=TEXT_COLOR, font=font_b)
                bar_w = int(float(pct.strip('%')) * s(4))
                self.draw.rounded_rectangle(
                    [bar_x_base, self.y + s(3), bar_x_base + bar_w, self.y + s(20)],
                    radius=s(3), fill=SECTION_BG
                )
                self.draw.text((bar_x_base + bar_w + s(8), self.y + s(1)), pct, fill=ACCENT_COLOR, font=font)
            self.y += s(30)
        self.y += s(10)

    def _draw_strategic_moves(self):
        label = self.data.get("MOVES_LABEL", "近期战略动作")
        self._draw_section_header(label, "🔄")
        font_b = get_font(15, bold=True)
        for action, target, detail, color in self.data["STRATEGIC_MOVES"]:
            if not self.calculating:
                x = PADDING + s(20)
                tag_w = self.draw.textlength(action, font=font_b) + s(16)
                self.draw.rounded_rectangle(
                    [x, self.y, x + tag_w, self.y + s(24)],
                    radius=s(4), fill=color
                )
                self.draw.text((x + s(8), self.y + s(2)), action, fill="white", font=font_b)
                tx = x + tag_w + s(10)
                self.draw.text((tx, self.y + s(2)), target, fill=TEXT_COLOR, font=font_b)
                self.draw.text((x + s(20), self.y + s(28)), detail, fill=GRAY_TEXT, font=get_font(13))
            self.y += s(54)
        self.y += s(5)

    def _draw_moat(self):
        self._draw_section_header("护城河 / 核心竞争力", "💡")
        font_title = get_font(16, bold=True)
        font_desc = get_font(14)
        for title, desc in self.data["MOAT"]:
            if not self.calculating:
                x = PADDING + s(20)
                self.draw.ellipse([x, self.y + s(5), x + s(10), self.y + s(15)], fill=ACCENT_COLOR)
                self.draw.text((x + s(18), self.y), title, fill=TEXT_COLOR, font=font_title)
                self._draw_wrapped_text(x + s(18), self.y + s(24), desc, font_desc, GRAY_TEXT, CONTENT_W - s(40))
            else:
                self.y += s(24)
                self._draw_wrapped_text(0, self.y, desc, font_desc, GRAY_TEXT, CONTENT_W - s(40))
            self.y += s(10)

    def _draw_wrapped_text(self, x, start_y, text, font, color, max_w):
        line = ""
        y = start_y
        for char in text:
            test = line + char
            tw = self.draw.textlength(test, font=font) if not self.calculating else len(test) * s(14)
            if tw > max_w:
                if not self.calculating:
                    self.draw.text((x, y), line, fill=color, font=font)
                y += s(22)
                line = char
            else:
                line = test
        if line:
            if not self.calculating:
                self.draw.text((x, y), line, fill=color, font=font)
            y += s(22)
        self.y = y

    def _draw_key_metrics(self):
        self._draw_section_header("关键经营指标", "📋")
        font_key = get_font(15, bold=True)
        font_val = get_font(15)
        for key, val in self.data["KEY_METRICS"]:
            if not self.calculating:
                x = PADDING + s(20)
                self.draw.rounded_rectangle(
                    [x, self.y - s(2), WIDTH - PADDING - s(20), self.y + s(26)],
                    radius=s(4), fill=LIGHT_BG
                )
                self.draw.text((x + s(12), self.y + s(2)), key, fill=TEXT_COLOR, font=font_key)
                vw = self.draw.textlength(val, font=font_val)
                self.draw.text((WIDTH - PADDING - s(32) - vw, self.y + s(2)), val, fill=ACCENT_COLOR, font=font_val)
            self.y += s(34)
        self.y += s(10)

    def _draw_risks_highlights(self):
        self._draw_section_header("亮点与风险", "⚖️")
        font_title = get_font(16, bold=True)
        font_desc = get_font(14)
        for kind, title, desc in self.data["RISKS_HIGHLIGHTS"]:
            tag_color = GREEN_COLOR if kind == "亮点" else RED_COLOR
            if not self.calculating:
                x = PADDING + s(20)
                tag_w = s(48)
                self.draw.rounded_rectangle(
                    [x, self.y, x + tag_w, self.y + s(22)],
                    radius=s(4), fill=tag_color
                )
                self.draw.text((x + s(8), self.y + s(2)), kind, fill="white", font=get_font(13, bold=True))
                self.draw.text((x + tag_w + s(10), self.y), title, fill=TEXT_COLOR, font=font_title)
                self._draw_wrapped_text(x + tag_w + s(10), self.y + s(24), desc, font_desc, GRAY_TEXT, CONTENT_W - tag_w - s(30))
            else:
                self.y += s(24)
                self._draw_wrapped_text(0, self.y, desc, font_desc, GRAY_TEXT, CONTENT_W - s(60))
            self.y += s(10)

    def _draw_quotes(self):
        label = self.data.get("QUOTES_LABEL", "管理层 & 分析师观点")
        self._draw_section_header(label, "✨")
        font = get_font(15)
        for quote in self.data["QUOTES"]:
            if not self.calculating:
                x = PADDING + s(20)
                qh = s(30)
                self.draw.rounded_rectangle(
                    [x, self.y, WIDTH - PADDING - s(20), self.y + qh],
                    radius=s(4), fill=TAG_BG, outline=TAG_BORDER
                )
                self.draw.text((x + s(12), self.y + s(5)), quote, fill=TEXT_COLOR, font=font)
            self.y += s(38)
        self.y += s(10)

    def _draw_footer(self):
        d = self.data
        h = s(60)
        if not self.calculating:
            self.draw.rectangle([0, self.y, WIDTH, self.y + h], fill=HEADER_BG)
            font = get_font(13)
            lines = d.get("FOOTER_LINES", [
                f"数据来源：{d.get('DATA_SOURCE', '公开财报')}",
                "免责声明：本图仅供学习参考，不构成投资建议"
            ])
            for i, line in enumerate(lines):
                tw = self.draw.textlength(line, font=font)
                self.draw.text(((WIDTH - tw) / 2, self.y + s(12) + i * s(22)), line, fill="#F0D9C4", font=font)
        self.y += h

    def save(self, path):
        self.img.save(path, "PNG", quality=95)
        print(f"Saved to {path} ({self.img.size[0]}x{self.img.size[1]})")


def generate(data_module_name, output_path=None):
    mod = importlib.import_module(data_module_name)
    data = mod.DATA
    if output_path is None:
        output_path = os.path.expanduser(f"~/Downloads/{data_module_name.replace('data_', '')}.png")
    builder = CompanyInfographic(data)
    builder.save(output_path)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 company_infographic.py <data_module> [output.png]")
        sys.exit(1)
    module_name = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    generate(module_name, out)
