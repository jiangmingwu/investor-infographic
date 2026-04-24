#!/usr/bin/env python3
"""
投资人持仓信息长图 - 通用模板引擎
风格：段永平投资全解析（暖橙色系）
默认输出 4K 分辨率（SCALE=3, 宽度2400px）

使用方式：
1. 复制 data_template.py 为新文件（如 data_cathie_wood.py）
2. 填入对应投资人的数据
3. 运行: python3 investor_infographic.py data_cathie_wood
   或:   python3 investor_infographic.py data_cathie_wood output_name.png
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys
import importlib

# ============ 缩放因子（3 = 4K级清晰度，宽度2400px）============
SCALE = 3

def s(v):
    """缩放像素值"""
    return int(v * SCALE)

# ============ 颜色配置（暖橙色系，匹配段永平原图）============
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

# ============ 字体配置 ============
def get_font(size, bold=False):
    scaled = s(size)
    if bold:
        try:
            return ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", scaled)
        except:
            pass
    try:
        return ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", scaled)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", scaled)
        except:
            return ImageFont.load_default()

# ============ 绘图引擎 ============
WIDTH = s(800)
PADDING = s(40)
CONTENT_W = WIDTH - PADDING * 2

class InfographicBuilder:
    def __init__(self, data):
        self.data = data
        self.y = 0
        # First pass: calculate height
        self.calculating = True
        self.img = Image.new("RGB", (WIDTH, 100), BG_COLOR)
        self.draw = ImageDraw.Draw(self.img)
        self._build()
        total_h = self.y + s(40)

        # Second pass: actually draw
        self.y = 0
        self.calculating = False
        self.img = Image.new("RGB", (WIDTH, total_h), BG_COLOR)
        self.draw = ImageDraw.Draw(self.img)
        self._build()

    def _build(self):
        d = self.data
        self._draw_header()
        if d.get("BASIC_INFO"):
            self._draw_section("人物简介", "👤", "kv", d["BASIC_INFO"])
        if d.get("PORTFOLIO_SUMMARY"):
            self._draw_section("持仓概览", "📊", "kv", d["PORTFOLIO_SUMMARY"])
        if d.get("TOP_HOLDINGS"):
            self._draw_top_holdings()
        if d.get("SECTOR_DISTRIBUTION"):
            self._draw_sector_distribution()
        if d.get("RECENT_CHANGES"):
            self._draw_recent_changes()
        if d.get("INVESTMENT_PHILOSOPHY"):
            self._draw_investment_philosophy()
        if d.get("KEY_METRICS"):
            self._draw_key_metrics()
        if d.get("FAMOUS_QUOTES"):
            self._draw_famous_quotes()
        for extra in d.get("EXTRA_SECTIONS", []):
            self._draw_section(extra["title"], extra.get("icon", "●"), "kv", extra["data"])
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

    def _draw_section(self, title, icon, style, data):
        self._draw_section_header(title, icon)
        if style == "kv":
            if isinstance(data, dict):
                for k, v in data.items():
                    self._draw_kv_pair(k, v)
            elif isinstance(data, list):
                for k, v in data:
                    self._draw_kv_pair(k, v)
        self.y += s(10)

    def _draw_top_holdings(self):
        holdings = self.data["TOP_HOLDINGS"]
        label = self.data.get("HOLDINGS_LABEL", "前15大持仓")
        self._draw_section_header(label, "🏆")

        font_h = get_font(14, bold=True)
        if not self.calculating:
            cols = [PADDING+s(15), PADDING+s(45), PADDING+s(210), PADDING+s(290),
                    PADDING+s(365), PADDING+s(460), PADDING+s(580)]
            headers = ["#", "公司名称", "代码", "占比", "市值", "持股数", "行业"]
            self.draw.rectangle([PADDING+s(8), self.y-s(2), WIDTH-PADDING-s(8), self.y+s(24)], fill=LIGHT_BG)
            for col, header in zip(cols, headers):
                self.draw.text((col, self.y+s(2)), header, fill=ACCENT_COLOR, font=font_h)
        self.y += s(30)

        font_row = get_font(14)
        font_row_b = get_font(14, bold=True)
        for i, row in enumerate(holdings):
            if not self.calculating:
                if i % 2 == 0:
                    self.draw.rectangle([PADDING+s(8), self.y-s(2), WIDTH-PADDING-s(8), self.y+s(22)], fill="#FFF8F0")
                cols = [PADDING+s(20), PADDING+s(45), PADDING+s(210), PADDING+s(290),
                        PADDING+s(365), PADDING+s(460), PADDING+s(580)]
                self.draw.text((cols[0], self.y), row[0], fill=GRAY_TEXT, font=font_row)
                self.draw.text((cols[1], self.y), row[1], fill=TEXT_COLOR, font=font_row_b)
                self.draw.text((cols[2], self.y), row[2], fill=ACCENT_COLOR, font=font_row)
                self.draw.text((cols[3], self.y), row[3], fill=TEXT_COLOR, font=font_row)
                self.draw.text((cols[4], self.y), row[4], fill=TEXT_COLOR, font=font_row)
                self.draw.text((cols[5], self.y), row[5], fill=GRAY_TEXT, font=font_row)
                self.draw.text((cols[6], self.y), row[6], fill=GRAY_TEXT, font=font_row)
            self.y += s(26)
        self.y += s(10)

    def _draw_sector_distribution(self):
        self._draw_section_header("行业分布", "📈")
        font = get_font(16)
        font_b = get_font(16, bold=True)
        # 先计算最长行业名称宽度，对齐进度条
        max_name_w = 0
        if not self.calculating:
            for sector, pct, *_ in self.data["SECTOR_DISTRIBUTION"]:
                nw = self.draw.textlength(sector, font=font_b)
                if nw > max_name_w:
                    max_name_w = nw
        bar_x_base = PADDING + s(20) + max_name_w + s(20)
        for sector, pct, *_ in self.data["SECTOR_DISTRIBUTION"]:
            if not self.calculating:
                x = PADDING + s(20)
                self.draw.text((x, self.y), sector, fill=TEXT_COLOR, font=font_b)
                bar_w = int(float(pct.strip('%')) * s(4))
                self.draw.rounded_rectangle(
                    [bar_x_base, self.y + s(3), bar_x_base + bar_w, self.y + s(20)],
                    radius=s(3), fill=SECTION_BG
                )
                self.draw.text((bar_x_base + bar_w + s(8), self.y + s(1)), pct, fill=ACCENT_COLOR, font=font)
            self.y += s(30)
        self.y += s(10)

    def _draw_recent_changes(self):
        label = self.data.get("CHANGES_LABEL", "近期持仓变动")
        self._draw_section_header(label, "🔄")
        font = get_font(15)
        font_b = get_font(15, bold=True)
        for action, target, detail, color in self.data["RECENT_CHANGES"]:
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

    def _draw_investment_philosophy(self):
        self._draw_section_header("投资哲学", "💡")
        font_title = get_font(16, bold=True)
        font_desc = get_font(14)
        for title, desc in self.data["INVESTMENT_PHILOSOPHY"]:
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
        self._draw_section_header("关键业绩指标", "📋")
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

    def _draw_famous_quotes(self):
        self._draw_section_header("经典语录", "✨")
        font = get_font(15)
        for quote in self.data["FAMOUS_QUOTES"]:
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
        lines = d.get("FOOTER_LINES", [
            f"数据来源：{d.get('DATA_SOURCE', '公开信息')}",
            "免责声明：本图仅供学习参考，不构成投资建议"
        ])
        if not any(str(line).strip() == "by 江明" for line in lines):
            lines = [*lines, "by 江明"]
        h = s(18 + len(lines) * 22)
        if not self.calculating:
            self.draw.rectangle([0, self.y, WIDTH, self.y + h], fill=HEADER_BG)
            font = get_font(13)
            for i, line in enumerate(lines):
                tw = self.draw.textlength(line, font=font)
                self.draw.text(((WIDTH - tw) / 2, self.y + s(12) + i * s(22)), line, fill="#F0D9C4", font=font)
        self.y += h

    def save(self, path):
        self.img.save(path, "PNG", quality=95)
        print(f"Saved to {path} ({self.img.size[0]}x{self.img.size[1]})")


def generate(data_module_name, output_path=None):
    """从数据模块生成图片"""
    mod = importlib.import_module(data_module_name)
    data = mod.DATA
    if output_path is None:
        output_path = os.path.expanduser(f"~/Downloads/{data_module_name.replace('data_', '')}.png")
    builder = InfographicBuilder(data)
    builder.save(output_path)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 investor_infographic.py <data_module_name> [output.png]")
        print("示例: python3 investor_infographic.py data_buffett")
        print("      python3 investor_infographic.py data_cathie_wood 木头姐持仓.png")
        sys.exit(1)

    module_name = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    path = generate(module_name, out)
    print(f"Done! -> {path}")
