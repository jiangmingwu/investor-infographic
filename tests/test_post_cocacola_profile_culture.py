#!/usr/bin/env python3
"""Hard-rule tests for the post-Coca-Cola profile/culture refresh."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))

import render_post_cocacola_profile_culture as batch


EXPECTED = {
    "chevron", "pg", "roche", "homedepot", "hsbc", "arm", "palantir",
    "agriculturalbank", "merck", "icbc", "goldmansachs", "novartis",
    "astrazeneca", "philipmorris", "kla", "gevernova", "rbc", "ibm", "dell",
}


def test_company_data_contract() -> None:
    assert {c["slug"] for c in batch.COMPANIES} == EXPECTED
    assert len(batch.COMPANIES) == 19
    for company in batch.COMPANIES:
        assert Path(company["logo_path"]).is_file(), company["slug"]
        assert company["logo_source"].startswith("https://"), company["slug"]
        assert len(company["businesses"]) in {2, 3, 4}, company["slug"]
        assert len(company["status"]) == 3, company["slug"]
        assert len(company["timeline"]) == 4, company["slug"]
        assert 1 <= len(company["culture"]) <= 3, company["slug"]
        for key in ("en", "founded", "hq", "ticker", "ceo", "employees", "core_business", "current_market_cap"):
            assert company[key].strip(), (company["slug"], key)


def test_culture_is_concrete_and_people_focused() -> None:
    forbidden = re.compile(r"市场份额|产能|资本开支|CapEx|估值|市值|供应链优势|制造工艺|产品路线图")
    for company in batch.COMPANIES:
        for item in company["culture"]:
            assert item["practice"].startswith("做法："), company["slug"]
            assert item["case"].startswith(("案例：", "数字：")), company["slug"]
            assert item["lesson"].startswith("可借鉴："), company["slug"]
            assert item["source"].startswith("https://"), company["slug"]
            assert item["lens"] in {"组织", "人才", "反馈", "员工", "领导", "伦理", "客户"}
            text = "".join(str(item[k]) for k in ("title", "practice", "case", "lesson"))
            assert not forbidden.search(text), (company["slug"], text)


def test_html_contract() -> None:
    for company in batch.COMPANIES:
        profile = batch.profile_page(company)
        culture = batch.culture_page(company)
        for html in (profile, culture):
            visible = re.sub(r"<[^>]+>", "", html)
            assert "..." not in visible and "…" not in visible
            assert visible.count("by 江明") == 1
            assert "overflow:hidden" in html
            assert "公司官方" in visible
        assert "公司档案" in profile
        for label in ("公司全称", "成立时间", "总部地址", "交易所及代码", "CEO / 主要负责人", "员工人数", "核心业务", "当前市值"):
            assert label in profile, (company["slug"], label)
        assert "经营利润" not in profile
        assert "管理文化" in culture


def test_output_names_and_four_page_rule() -> None:
    for company in batch.COMPANIES:
        out = batch.OUTPUT_ROOT / company["folder"]
        expected_profile = out / f"{company['prefix']}_公司档案.png"
        expected_culture = out / f"{company['prefix']}_管理文化.png"
        old_profile = out / f"{company['prefix']}_经营分析.png"
        if batch.RENDER_COMPLETE:
            assert expected_profile.is_file()
            assert expected_culture.is_file()
            assert not old_profile.exists()
            assert len(list(out.glob("*.png"))) == 4, out


if __name__ == "__main__":
    test_company_data_contract()
    test_culture_is_concrete_and_people_focused()
    test_html_contract()
    test_output_names_and_four_page_rule()
    print("post-Coca-Cola profile/culture hard rules: PASS")
