#!/usr/bin/env python3
"""Structural regressions only; synthetic fixtures do not prove real culture."""

from __future__ import annotations

import copy
import unittest

from validate_company_packet import ValidationError, validate_management_culture


def fixture() -> dict:
    return {
        "management_culture": [{
            "lens": "员工",
            "principle": "一线员工的安全停工权",
            "practice": "做法：制造一线员工发现危险可停止生产并请求复核。",
            "case_or_number": "案例：测试手册说明审批和申诉流程。",
            "source": "合成测试手册，不用于实际出图。",
            "distinctiveness": "明确谁有权停止工作，以及复核责任，非扩产战略。",
            "evidence_scope": "测试公司一线员工；2026年；公开制度，执行情况未验证。",
            "evidence_status": "published_policy",
        }],
    }


class ManagementCultureGateTest(unittest.TestCase):
    def test_one_specific_policy_is_enough_without_numeric_padding(self) -> None:
        validate_management_culture(fixture())

    def test_reported_practice_status_is_supported(self) -> None:
        packet = fixture()
        packet["management_culture"][0]["evidence_status"] = "reported_practice"
        validate_management_culture(packet)

    def test_rejects_missing_or_empty_research_metadata(self) -> None:
        for key in ("distinctiveness", "evidence_scope", "evidence_status"):
            for value in (None, "", "  ", 0, {}, []):
                with self.subTest(key=key, value=value):
                    packet = fixture()
                    packet["management_culture"][0][key] = value
                    with self.assertRaisesRegex(ValidationError, key):
                        validate_management_culture(packet)

    def test_rejects_ambiguous_evidence_status(self) -> None:
        packet = fixture()
        packet["management_culture"][0]["evidence_status"] = "verified"
        with self.assertRaisesRegex(ValidationError, "evidence_status"):
            validate_management_culture(packet)

    def test_legacy_packet_needs_real_enrichment(self) -> None:
        packet = fixture()
        for key in ("distinctiveness", "evidence_scope", "evidence_status"):
            del packet["management_culture"][0][key]
        with self.assertRaisesRegex(ValidationError, "distinctiveness"):
            validate_management_culture(packet)

    def test_no_evidence_is_not_a_finished_page(self) -> None:
        with self.assertRaisesRegex(ValidationError, "1-3"):
            validate_management_culture({"management_culture": []})

    def test_rejects_padding_beyond_three(self) -> None:
        packet = fixture()
        packet["management_culture"] *= 4
        with self.assertRaisesRegex(ValidationError, "1-3"):
            validate_management_culture(packet)

    def test_original_card_requirements_still_hold(self) -> None:
        for key in ("lens", "principle", "practice", "case_or_number", "source"):
            packet = fixture()
            del packet["management_culture"][0][key]
            with self.subTest(key=key), self.assertRaisesRegex(ValidationError, key):
                validate_management_culture(packet)
        for key in ("practice", "case_or_number"):
            packet = fixture()
            packet["management_culture"][0][key] = "无要求的短标签"
            with self.subTest(key=key), self.assertRaisesRegex(ValidationError, key):
                validate_management_culture(packet)

    def test_customer_pricing_rule_not_rejected_as_financial_keyword(self) -> None:
        packet = fixture()
        card = packet["management_culture"][0]
        card.update({
            "lens": "客户",
            "principle": "不以市场份额扩张牺牲顾客承诺",
            "practice": "做法：测试制度要求涨价前履行顾客承诺审查。",
            "case_or_number": "案例：测试会议记录披露否决涨价决定。",
            "distinctiveness": "顾客承诺对涨价审批具有约束。",
            "evidence_scope": "合成测试公司；2026年一例，不证明普遍执行。",
            "evidence_status": "reported_practice",
        })
        validate_management_culture(packet)

    def test_validator_does_not_mutate_research_packet(self) -> None:
        packet = fixture()
        original = copy.deepcopy(packet)
        validate_management_culture(packet)
        self.assertEqual(packet, original)


if __name__ == "__main__":
    unittest.main()
