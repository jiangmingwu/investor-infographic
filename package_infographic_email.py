#!/usr/bin/env python3
"""Package generated infographic images for Gmail delivery."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import zipfile
from pathlib import Path


DEFAULT_RECIPIENT = "xuexi1989@gmail.com"
DEFAULT_OUT_DIR = Path("/tmp/infographic_email_packages")
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def slugify(value: str) -> str:
    value = re.sub(r"\s+", "-", value.strip())
    value = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-._")
    return value or "infographics"


def collect_images(source_dir: Path) -> list[Path]:
    images = [
        path
        for path in source_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(images, key=lambda path: path.name)


def build_body(company: str, source_dir: Path, files: list[Path], today: str) -> str:
    file_lines = "\n".join(f"{idx}. {path.name}" for idx, path in enumerate(files, start=1))
    return (
        f"江明，\n\n"
        f"这是 {company} 的持仓/公司经营分析图片，附件为原图 ZIP 包。\n\n"
        f"附件内容：\n{file_lines}\n\n"
        f"本地路径：{source_dir}\n"
        f"发送日期：{today}\n\n"
        f"by 江明"
    )


def build_manifest(company: str, source_dir: Path, recipient: str, files: list[Path], today: str) -> str:
    file_lines = "\n".join(f"- {path.name}" for path in files)
    return (
        f"公司/主题：{company}\n"
        f"收件邮箱：{recipient}\n"
        f"本地路径：{source_dir}\n"
        f"打包日期：{today}\n\n"
        f"图片清单：\n{file_lines}\n"
    )


def package_images(
    source_dir: Path,
    company: str,
    recipient: str,
    out_dir: Path,
    today: str,
    subject: str | None = None,
) -> dict[str, object]:
    files = collect_images(source_dir)
    if not files:
        raise SystemExit(f"No image files found in {source_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)
    zip_name = f"{slugify(company)}_infographics_{today}.zip"
    zip_path = out_dir / zip_name
    manifest_name = f"{slugify(company)}_manifest_{today}.txt"
    manifest_text = build_manifest(company, source_dir, recipient, files, today)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, arcname=f"{source_dir.name}/{path.name}")
        archive.writestr(f"{source_dir.name}/{manifest_name}", manifest_text)

    subject = subject or f"持仓分析图片｜{company}｜{today}"
    body = build_body(company, source_dir, files, today)
    return {
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "zip_path": str(zip_path),
        "file_count": len(files),
        "files": [path.name for path in files],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package generated infographic images and print Gmail-ready metadata as JSON."
    )
    parser.add_argument("source_dir", help="Folder containing final infographic images.")
    parser.add_argument("--company", help="Company or topic name for email subject/body.")
    parser.add_argument("--to", default=DEFAULT_RECIPIENT, help="Recipient email address.")
    parser.add_argument("--subject", help="Override email subject.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="ZIP output directory.")
    parser.add_argument("--date", help="Date label, defaults to local YYYY-MM-DD.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    source_dir = Path(args.source_dir).expanduser().resolve()
    if not source_dir.is_dir():
        raise SystemExit(f"Source folder does not exist: {source_dir}")

    today = args.date or dt.date.today().isoformat()
    company = args.company or source_dir.name
    payload = package_images(
        source_dir=source_dir,
        company=company,
        recipient=args.to,
        out_dir=Path(args.out_dir).expanduser().resolve(),
        today=today,
        subject=args.subject,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
