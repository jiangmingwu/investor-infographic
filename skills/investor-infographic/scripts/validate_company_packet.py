#!/usr/bin/env python3
"""Validate Jiangming company infographic research packets before rendering."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_PROFILE_KEYS = [
    "公司全称",
    "成立时间",
    "创始人 / 创立主体",
    "总部地址",
    "交易所及代码",
    "CEO / 主要负责人",
    "员工人数",
    "核心业务",
    "当前市值",
]

DEFAULT_TOP_GRID_PATTERNS = [
    r"^FY\d{4}\s*营收$",
    r"^FY\d{4}\s*经营利润$",
    r"^FY\d{4}\s*经营现金流$",
    r"^FY\d{4}\s*净利润$",
    r"^当前市值$",
    r"^PE / Forward PE$",
]

ALLOWED_HOLDER_KINDS = {"机构", "战略股东", "管理层", "知名个人"}
ALLOWED_CULTURE_LENSES = {"人才", "员工", "组织", "客户", "伦理"}

ALLOWED_CULTURE_EVIDENCE_STATUS = {"published_policy", "reported_practice"}

HARD_METRIC_RE = re.compile(
    r"(\d|%|\$|USD|美元|#\d|第[一二三四五六七八九十0-9]+|全球第|全球第一|全球第二|"
    r"市占率|份额|收入|用户|客户|门店|资产|AUM|ROE|ROIC|ROTCE|CET1|装机|专利)",
    re.I,
)

ALLOWED_EVIDENCE_KINDS = {
    "市场份额",
    "行业排名",
    "业务收入或占比",
    "销量或产量",
    "渠道网络",
    "品牌或产品组合",
    "用户或装机",
    "留存或认证",
    "定价或利润率",
    "专利或研发",
}

GENERIC_CORE_TITLES = {
    "规模收入底盘",
    "利润与现金流",
    "核心护城河",
    "客户与渠道",
    "综合优势",
}

INVALID_CORE_METRIC_RE = re.compile(
    r"(?:CMC\s*第|CompaniesMarketCap|当前市值|员工(?:人数)?|总员工|全公司营收|公司总营收|公司总利润)",
    re.I,
)


class ValidationError(Exception):
    pass


def fail(path: str, message: str) -> None:
    raise ValidationError(f"{path}: {message}")


def require_mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(path, "must be an object")
    return value


def require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        fail(path, "must be a list")
    return value


def require_text(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(path, "must be non-empty text")
    return value.strip()


def validate_logo(packet: dict[str, Any]) -> None:
    logo = require_mapping(packet.get("logo"), "logo")
    url = require_text(logo.get("official_source_url"), "logo.official_source_url")
    if not url.startswith(("https://", "http://")):
        fail("logo.official_source_url", "must be an official URL")
    require_text(logo.get("retrieved"), "logo.retrieved")
    sha = require_text(logo.get("sha256"), "logo.sha256")
    if not re.fullmatch(r"[0-9a-f]{64}", sha):
        fail("logo.sha256", "must be 64 lowercase hex characters")


def validate_currency(packet: dict[str, Any]) -> None:
    currency = require_mapping(packet.get("currency"), "currency")
    display = require_text(currency.get("display"), "currency.display")
    if display.upper() != "USD":
        fail("currency.display", "must be USD")
    require_text(currency.get("exchange_rate_note"), "currency.exchange_rate_note")


def validate_profile(packet: dict[str, Any]) -> None:
    profile = require_mapping(packet.get("company_profile"), "company_profile")
    for key in REQUIRED_PROFILE_KEYS:
        require_text(profile.get(key), f"company_profile.{key}")


def validate_top_grid(packet: dict[str, Any]) -> None:
    top_grid = require_mapping(packet.get("panorama_top_grid"), "panorama_top_grid")
    if "industry_exception" not in packet:
        labels = list(top_grid.keys())
        missing_patterns = []
        for pattern in DEFAULT_TOP_GRID_PATTERNS:
            if not any(re.search(pattern, label) for label in labels):
                missing_patterns.append(pattern)
        if missing_patterns:
            fail("panorama_top_grid", "missing default six-card metric categories")
    if len(top_grid) != 6:
        fail("panorama_top_grid", "must contain exactly six visible top cards")
    for key, card in top_grid.items():
        card_map = require_mapping(card, f"panorama_top_grid.{key}")
        require_text(card_map.get("value"), f"panorama_top_grid.{key}.value")
        require_text(card_map.get("source"), f"panorama_top_grid.{key}.source")


def validate_core_drivers(packet: dict[str, Any]) -> None:
    drivers = require_list(packet.get("core_drivers"), "core_drivers")
    if not 1 <= len(drivers) <= 5:
        fail("core_drivers", "must contain 1-5 truly core items")
    for index, item in enumerate(drivers):
        path = f"core_drivers[{index}]"
        driver = require_mapping(item, path)
        name = require_text(driver.get("name"), f"{path}.name")
        if name in GENERIC_CORE_TITLES:
            fail(f"{path}.name", "must retain a company-specific business or capability title")
        metric = require_text(driver.get("metric"), f"{path}.metric")
        if not HARD_METRIC_RE.search(metric):
            fail(f"{path}.metric", "must contain a hard metric")
        if INVALID_CORE_METRIC_RE.search(metric):
            fail(f"{path}.metric", "must not use company size, CMC rank, or employee count as moat evidence")
        evidence_kind = require_text(driver.get("evidence_kind"), f"{path}.evidence_kind")
        if evidence_kind not in ALLOWED_EVIDENCE_KINDS:
            fail(f"{path}.evidence_kind", "must be a direct business-evidence type")
        meaning = require_text(driver.get("industry_meaning"), f"{path}.industry_meaning")
        if not meaning.startswith("行业含义："):
            fail(f"{path}.industry_meaning", "must start with 行业含义：")
        require_text(driver.get("icon"), f"{path}.icon")
        require_text(driver.get("why_it_matters"), f"{path}.why_it_matters")
        require_text(driver.get("source"), f"{path}.source")


def validate_capital(packet: dict[str, Any]) -> None:
    capital = require_mapping(packet.get("capital"), "capital")
    for key in ("roi", "capex_2026", "shareholder_return"):
        item = require_mapping(capital.get(key), f"capital.{key}")
        value = require_text(item.get("value"), f"capital.{key}.value")
        require_text(item.get("source"), f"capital.{key}.source")
        if key in {"roi", "shareholder_return"} and not re.search(r"\d|未披露|不可比", value):
            fail(f"capital.{key}.value", "must contain a number or explicit limitation")
        if key == "shareholder_return" and any(term in value for term in ("稳定分红", "现金分红稳定", "回购+股息")):
            fail(f"capital.{key}.value", "must not be a vague shareholder-return phrase")
        if key == "shareholder_return":
            average = require_mapping(
                item.get("dividend_yield_average"),
                "capital.shareholder_return.dividend_yield_average",
            )
            average_value = require_text(
                average.get("value"),
                "capital.shareholder_return.dividend_yield_average.value",
            )
            if average_value == "资料不足":
                require_text(
                    average.get("limitation"),
                    "capital.shareholder_return.dividend_yield_average.limitation",
                )
            elif not re.search(r"\d+(?:\.\d+)?%", average_value):
                fail(
                    "capital.shareholder_return.dividend_yield_average.value",
                    "must contain a numeric percentage",
                )
            label = require_text(
                average.get("label"),
                "capital.shareholder_return.dividend_yield_average.label",
            )
            if label not in {"近10年均值", "可比期均值"}:
                fail(
                    "capital.shareholder_return.dividend_yield_average.label",
                    "must identify a 10-year or shorter comparable period",
                )
            for field in ("period", "formula", "source"):
                require_text(
                    average.get(field),
                    f"capital.shareholder_return.dividend_yield_average.{field}",
                )


def validate_major_holders(packet: dict[str, Any]) -> None:
    holders = require_list(packet.get("major_holders"), "major_holders")
    if holders and not 3 <= len(holders) <= 5:
        fail("major_holders", "must contain 3-5 rows when used")
    for index, item in enumerate(holders):
        path = f"major_holders[{index}]"
        holder = require_mapping(item, path)
        require_text(holder.get("name"), f"{path}.name")
        kind = require_text(holder.get("kind"), f"{path}.kind")
        if kind not in ALLOWED_HOLDER_KINDS:
            fail(f"{path}.kind", "must be 机构, 战略股东, 管理层, or 知名个人")
        stake = require_text(holder.get("stake"), f"{path}.stake")
        if not re.search(r"\d+(?:\.\d+)?%", stake):
            fail(f"{path}.stake", "must contain an ownership percentage")
        value = require_text(holder.get("estimated_value"), f"{path}.estimated_value")
        if "$" not in value and "USD" not in value and "美元" not in value:
            fail(f"{path}.estimated_value", "must be a USD estimated value")
        require_text(holder.get("source"), f"{path}.source")


def validate_segment_mix(packet: dict[str, Any]) -> None:
    """Fail closed for every new/refreshed panorama business-mix block."""
    mix_value = packet.get("segment_mix")
    if mix_value is None:
        panorama = packet.get("panorama")
        if isinstance(panorama, dict):
            mix_value = panorama.get("segment_mix")
            rows_value = panorama.get("segments")
        else:
            return
    else:
        rows_value = packet.get("segments")
    if mix_value is None:
        return  # Legacy packets remain readable; refreshed packets must add this block.
    mix = require_mapping(mix_value, "segment_mix")
    rows = require_list(rows_value, "segments")
    title = require_text(mix.get("section_title"), "segment_mix.section_title")
    denominator = require_mapping(mix.get("denominator"), "segment_mix.denominator")
    require_text(denominator.get("label"), "segment_mix.denominator.label")
    require_text(denominator.get("value"), "segment_mix.denominator.value")
    basis = require_text(mix.get("basis"), "segment_mix.basis")
    if "占比" not in basis and "分母" not in basis:
        fail("segment_mix.basis", "must explain the denominator")
    mode = require_text(mix.get("mode"), "segment_mix.mode")
    reconciliation = require_mapping(mix.get("reconciliation"), "segment_mix.reconciliation")
    coverage = reconciliation.get("coverage_pct")
    if not isinstance(coverage, (int, float)) or not 99 <= float(coverage) <= 101:
        fail("segment_mix.reconciliation.coverage_pct", "must reconcile to 100%")
    share_total = 0.0
    kinds = set()
    for index, value in enumerate(rows):
        path = f"segments[{index}]"
        row = require_mapping(value, path)
        name = require_text(row.get("name"), f"{path}.name")
        kind = require_text(row.get("kind"), f"{path}.kind")
        kinds.add(kind)
        share = row.get("share_pct")
        if not isinstance(share, (int, float)):
            fail(f"{path}.share_pct", "must be numeric and tied to the visible denominator")
        share_total += float(share)
        if re.search(r"[A-Za-z]{2,}", name) and kind not in {"other", "unallocated", "elimination", "adjustment"}:
            if not re.search(r"[（(][^()（）]*[\u4e00-\u9fff][^()（）]*[）)]", name):
                fail(f"{path}.name", "English drug/business name requires a Chinese parenthetical explanation")
        for key in ("value", "note"):
            text = require_text(row.get(key), f"{path}.{key}")
            if re.fullmatch(r"[+-]?\d+(?:\.\d+)?%", text):
                fail(f"{path}.{key}", "isolated percentage without denominator or meaning")
    if not 99 <= share_total <= 101:
        fail("segments", f"shares must reconcile to 100%, got {share_total:.2f}%")
    if mode in {"top_products", "top_brands", "top_geographies"}:
        if "业务分部" in title:
            fail("segment_mix.section_title", "Top items must not be labeled as business segments")
        if "other" not in kinds or reconciliation.get("top_coverage_pct") is None:
            fail("segment_mix.reconciliation", "Top items require an other row and top coverage")
    if mode == "pre_elimination_segments" and ("elimination" not in kinds or "抵销前" not in title + basis):
        fail("segment_mix", "pre-elimination segments require explicit basis and elimination row")


def validate_management_culture(packet: dict[str, Any]) -> None:
    cards = require_list(packet.get("management_culture"), "management_culture")
    if not 1 <= len(cards) <= 3:
        fail("management_culture", "must contain 1-3 real principles")
    for index, item in enumerate(cards):
        path = f"management_culture[{index}]"
        card = require_mapping(item, path)
        lens = require_text(card.get("lens"), f"{path}.lens")
        if lens not in ALLOWED_CULTURE_LENSES:
            fail(f"{path}.lens", "must be 人才, 员工, 组织, 客户, or 伦理")
        for key in (
            "principle", "practice", "case_or_number", "source",
            "distinctiveness", "evidence_scope",
        ):
            require_text(card.get(key), f"{path}.{key}")
        status = require_text(card.get("evidence_status"), f"{path}.evidence_status")
        if status not in ALLOWED_CULTURE_EVIDENCE_STATUS:
            fail(f"{path}.evidence_status", "must be published_policy or reported_practice")
        if "做法：" not in card["practice"]:
            fail(f"{path}.practice", "must include 做法：")
        if "案例：" not in card["case_or_number"] and "数字：" not in card["case_or_number"]:
            fail(f"{path}.case_or_number", "must include 案例： or 数字：")
        # Employee practices can mention factories or production. Relevance,
        # distinctiveness and source support require the documented semantic review.


def validate_footer(packet: dict[str, Any]) -> None:
    lines = [require_text(line, f"footer_lines[{index}]") for index, line in enumerate(require_list(packet.get("footer_lines"), "footer_lines"))]
    if "by 江明" not in lines:
        fail("footer_lines", "must include a separate by 江明 line")
    joined = " ".join(lines)
    for required in ("经营数据", "行情数据", "汇率口径", "免责声明"):
        if required not in joined:
            fail("footer_lines", f"missing {required}")


def validate_packet(packet: dict[str, Any]) -> None:
    for key in (
        "company",
        "output_root",
        "logo",
        "currency",
        "company_profile",
        "panorama_top_grid",
        "core_drivers",
        "capital",
        "major_holders",
        "management_culture",
        "footer_lines",
    ):
        if key not in packet:
            fail(key, "missing required field")

    require_text(packet.get("company"), "company")
    output_root = require_text(packet.get("output_root"), "output_root")
    if not output_root.startswith("/Users/jiangming/持仓分析"):
        fail("output_root", "must be under /Users/jiangming/持仓分析")

    validate_logo(packet)
    validate_currency(packet)
    validate_profile(packet)
    validate_top_grid(packet)
    validate_core_drivers(packet)
    validate_capital(packet)
    validate_segment_mix(packet)
    validate_major_holders(packet)
    validate_management_culture(packet)
    validate_footer(packet)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_company_packet.py <packet.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
        validate_packet(require_mapping(packet, "packet"))
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
