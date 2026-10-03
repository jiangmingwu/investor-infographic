#!/usr/bin/env python3
"""Regression tests for core-business evidence gates."""

from __future__ import annotations

import copy
import unittest

from validate_company_packet import ValidationError, validate_packet


def base_packet() -> dict:
    return {
        "company": "示例公司",
        "output_root": "/Users/jiangming/持仓分析/测试",
        "logo": {
            "official_source_url": "https://example.com/official-logo.svg",
            "retrieved": "2026年7月",
            "sha256": "0" * 64,
        },
        "currency": {"display": "USD", "exchange_rate_note": "USD 口径；查看：2026年7月"},
        "company_profile": {
            "公司全称": "Example Company Inc.",
            "成立时间": "2000年",
            "创始人 / 创立主体": "Example Founder",
            "总部地址": "New York, USA",
            "交易所及代码": "NYSE: EXM",
            "CEO / 主要负责人": "Example CEO",
            "员工人数": "10,000人",
            "核心业务": "示例核心业务",
            "当前市值": "$100B USD",
        },
        "panorama_top_grid": {
            "FY2025 营收": {"value": "$20B USD", "source": "年报"},
            "FY2025 经营利润": {"value": "$5B USD", "source": "年报"},
            "FY2025 经营现金流": {"value": "$6B USD", "source": "年报"},
            "FY2025 净利润": {"value": "$4B USD", "source": "年报"},
            "当前市值": {"value": "$100B USD", "source": "市场数据"},
            "PE / Forward PE": {"value": "20x / 18x", "source": "市场数据"},
        },
        "core_drivers": [
            {
                "name": "核心产品",
                "metric": "72% 市场份额",
                "evidence_kind": "市场份额",
                "industry_meaning": "行业含义：在该细分市场占主导地位，竞争者难以短期替代。",
                "icon": "chip",
                "why_it_matters": "核心产品贡献长期现金流。",
                "source": "公司年报，2026年7月",
            }
        ],
        "capital": {
            "roi": {"value": "12.5%", "source": "年报"},
            "capex_2026": {"value": "未披露/不可比", "source": "年报"},
            "shareholder_return": {
                "value": "$2.00/股，股息率2.0%",
                "source": "公司公告",
                "dividend_yield_average": {
                    "value": "2.8%",
                    "label": "近10年均值",
                    "period": "2016-2026",
                    "formula": "近10年TTM股息率历史样本算术平均",
                    "source": "FinanceCharts，2026年7月",
                },
            },
        },
        "major_holders": [],
        "management_culture": [
            {
                "lens": "员工",
                "principle": "公开的人才发展原则",
                "practice": "做法：公司公开培训与反馈机制。",
                "case_or_number": "案例：年度报告披露该机制。",
                "source": "公司官网，2026年7月",
                "distinctiveness": "测试占位：真实出图须另外通过选材与来源审查。",
                "evidence_scope": "测试占位：示例公司员工，2026年。",
                "evidence_status": "published_policy",
            }
        ],
        "footer_lines": [
            "经营数据：公司年报，FY2025：2025年1-12月",
            "行情数据：市场数据，查看：2026年7月",
            "汇率口径：USD，查看：2026年7月",
            "免责声明：本图仅供学习参考，不构成投资建议",
            "by 江明",
        ],
    }


class CoreEvidenceGateTest(unittest.TestCase):
    def test_rejects_profile_without_founder_or_founding_entity(self) -> None:
        packet = base_packet()
        del packet["company_profile"]["创始人 / 创立主体"]
        with self.assertRaisesRegex(ValidationError, "创始人 / 创立主体"):
            validate_packet(packet)

    def test_accepts_direct_business_evidence(self) -> None:
        validate_packet(base_packet())

    def test_rejects_shareholder_return_without_historical_dividend_yield(self) -> None:
        packet = base_packet()
        del packet["capital"]["shareholder_return"]["dividend_yield_average"]
        with self.assertRaisesRegex(ValidationError, "dividend_yield_average"):
            validate_packet(packet)

    def test_accepts_explicitly_unavailable_history_with_evidence(self) -> None:
        packet = base_packet()
        average = packet["capital"]["shareholder_return"]["dividend_yield_average"]
        average.update(value="资料不足", label="可比期均值",
                       limitation="上市不足一年，未取得完整年度股息与年末股价配对；已核查公司IR。")
        validate_packet(packet)

    def test_rejects_unavailable_history_without_explanation(self) -> None:
        packet = base_packet()
        packet["capital"]["shareholder_return"]["dividend_yield_average"]["value"] = "资料不足"
        with self.assertRaisesRegex(ValidationError, "limitation"):
            validate_packet(packet)

    def test_accepts_verified_distribution_network_evidence(self) -> None:
        packet = copy.deepcopy(base_packet())
        packet["core_drivers"][0].update(
            {
                "name": "全球装瓶体系",
                "metric": "200+ 装瓶伙伴 / 950+ 生产设施",
                "evidence_kind": "渠道网络",
            }
        )
        validate_packet(packet)

    def test_rejects_generic_title_and_company_size_fallback(self) -> None:
        packet = copy.deepcopy(base_packet())
        packet["core_drivers"][0]["name"] = "核心护城河"
        packet["core_drivers"][0]["metric"] = "CMC第38名 / 79,100人"
        with self.assertRaises(ValidationError):
            validate_packet(packet)


if __name__ == "__main__":
    unittest.main()
