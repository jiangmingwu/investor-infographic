#!/usr/bin/env python3
"""Add reviewed hand-drawn long-term price charts to post-Chevron profiles only."""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from render_post_chevron_standard_v2 import OUTPUT_ROOT, batch_companies
from render_post_cocacola_profile_culture import (
    load_stock_histories,
    profile_height,
    profile_page,
    render_html,
    visible_text,
)


REVIEW_ROOT = OUTPUT_ROOT / "_review/post_chevron_profile_stock_charts_20260715"
HTML_ROOT = REVIEW_ROOT / "html"
PACKET_ROOT = REVIEW_ROOT / "packets"
BEFORE_ROOT = REVIEW_ROOT / "before"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def non_profile_paths(company: dict) -> list[Path]:
    folder = OUTPUT_ROOT / company["folder"]
    return [
        folder / f"{company['prefix']}_sketch1.png",
        folder / f"{company['prefix']}_sketch2.png",
        folder / f"{company['prefix']}_管理文化.png",
    ]


def profile_path(company: dict) -> Path:
    return OUTPUT_ROOT / company["folder"] / f"{company['prefix']}_公司档案.png"


def backup_profile(company: dict) -> None:
    source = profile_path(company)
    target = BEFORE_ROOT / company["folder"] / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_file() and not target.exists():
        shutil.copy2(source, target)


def validate_profile(company: dict, source: str, target: Path) -> None:
    text = visible_text(source)
    for required in ("上市以来股价走势", "拆股调整", "不含股息再投资", "Yahoo Finance", "by 江明"):
        if required not in text:
            raise ValueError(f"{company['name']} profile missing {required}")
    if "..." in text or "…" in text:
        raise ValueError(f"{company['name']} profile contains ellipsis")
    if source.count("by 江明") != 1:
        raise ValueError(f"{company['name']} signature count invalid")
    with Image.open(target) as image:
        expected = (2700, profile_height(company) * 3)
        if image.size != expected:
            raise ValueError(f"{company['name']} profile size {image.size} != {expected}")


def contact_sheet(items: list[tuple[str, Path]], target: Path) -> None:
    width = 360
    label_height = 38
    thumbs = []
    for label, path in items:
        with Image.open(path) as source:
            image = source.convert("RGB")
            height = int(image.height * width / image.width)
            image.thumbnail((width, height), Image.Resampling.LANCZOS)
            thumbs.append((label, image.copy()))
    columns = 3
    rows = (len(thumbs) + columns - 1) // columns
    cell_height = max(image.height for _, image in thumbs) + label_height
    sheet = Image.new("RGB", (columns * width, rows * cell_height), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 21)
    except OSError:
        font = ImageFont.load_default()
    for index, (label, image) in enumerate(thumbs):
        x = (index % columns) * width
        y = (index // columns) * cell_height
        draw.text((x + 8, y + 5), label, fill="#222222", font=font)
        sheet.paste(image, (x, y + label_height))
    target.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(target, quality=92)


def main() -> int:
    for directory in (REVIEW_ROOT, HTML_ROOT, PACKET_ROOT, BEFORE_ROOT):
        directory.mkdir(parents=True, exist_ok=True)
    companies = batch_companies()
    histories = {slug: history for slug, history in load_stock_histories().items() if slug != "chevron"}
    if {company["slug"] for company in companies} != set(histories):
        raise ValueError("stock-history coverage does not match the post-Chevron company batch")

    untouched_before = {
        path: sha256(path)
        for company in companies
        for path in non_profile_paths(company)
        if path.is_file()
    }
    outputs = []
    for company in companies:
        print(f"render profile #{company['rank']} {company['name']}", flush=True)
        backup_profile(company)
        source = profile_page(company)
        html_path = HTML_ROOT / f"{company['rank']:02d}_{company['slug']}_profile.html"
        target = profile_path(company)
        render_html(source, html_path, target, profile_height(company))
        validate_profile(company, source, target)
        packet = {
            "company": company["name"],
            "rank": company["rank"],
            "generated": "2026-07-15",
            "stock_history": histories[company["slug"]],
            "output": str(target),
            "signature": "by 江明",
        }
        (PACKET_ROOT / f"{company['rank']:02d}_{company['slug']}.json").write_text(
            json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        outputs.append((f"#{company['rank']} {company['name']}", target))

    untouched_after = {path: sha256(path) for path in untouched_before}
    changed = [str(path) for path in untouched_before if untouched_before[path] != untouched_after[path]]
    if changed:
        raise ValueError("non-profile images changed unexpectedly: " + ", ".join(changed))

    contact = REVIEW_ROOT / "contact_公司档案_股价走势.jpg"
    contact_sheet(outputs, contact)
    manifest = [
        "# 雪佛龙之后公司档案股价走势图更新",
        "",
        f"- 生成时间：{datetime.now().isoformat(timespec='seconds')}",
        f"- 范围：{len(companies)}家公司，共{len(outputs)}张公司档案",
        "- 图表：手绘风长期股价折线，金额统一美元",
        "- 外币：瑞郎/港币按2026年7月15日固定汇率换算，限制写入页脚",
        "- 其他页面：经营之道、经营全景、管理文化哈希未变化",
        "- 邮件：未发送",
        "",
        *[f"- {label}：`{path}`" for label, path in outputs],
        "",
        f"- 视觉联系表：`{contact}`",
    ]
    (REVIEW_ROOT / "manifest.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    print(f"rendered {len(outputs)} profile charts")
    print(REVIEW_ROOT / "manifest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
