#!/usr/bin/env python3
"""Generate a GPT Image asset for the investor-infographic skill."""

from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate or edit a visual asset with GPT Image 2."
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Prompt text to send to the image model.")
    prompt_group.add_argument("--prompt-file", help="Path to a UTF-8 prompt file.")
    parser.add_argument("--output", required=True, help="Output image path.")
    parser.add_argument("--model", default="gpt-image-2", help="Image model name.")
    parser.add_argument("--size", default="1536x1024", help="Image size, e.g. 1536x1024.")
    parser.add_argument(
        "--quality",
        default="high",
        choices=["low", "medium", "high", "auto"],
        help="Rendering quality.",
    )
    parser.add_argument(
        "--background",
        default="auto",
        choices=["auto", "opaque"],
        help="gpt-image-2 supports auto or opaque backgrounds, not transparent.",
    )
    parser.add_argument(
        "--format",
        default="png",
        choices=["png", "jpeg", "webp"],
        help="Output image format.",
    )
    return parser.parse_args()


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt is not None:
        return args.prompt
    return Path(args.prompt_file).read_text(encoding="utf-8")


def main() -> None:
    args = parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit("Install the OpenAI Python package first: python3 -m pip install openai") from exc

    prompt = load_prompt(args)
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)

    client = OpenAI()
    result = client.images.generate(
        model=args.model,
        prompt=prompt,
        size=args.size,
        quality=args.quality,
        background=args.background,
        output_format=args.format,
    )
    image_base64 = result.data[0].b64_json
    output.write_bytes(base64.b64decode(image_base64))
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
