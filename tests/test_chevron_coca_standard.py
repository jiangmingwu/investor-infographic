import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))

import render_chevron_coca_standard as chevron


class ChevronCocaStandardTest(unittest.TestCase):
    def test_company_profile_has_fixed_archive_fields_and_semantic_icons(self):
        packet = chevron.packet()
        expected = {
            "公司全称",
            "成立时间",
            "总部地址",
            "交易所及代码",
            "CEO / 主要负责人",
            "员工人数",
            "公司定位",
            "历史长度",
        }
        self.assertEqual(set(packet["company_profile"]), expected)
        self.assertEqual(len(packet["business_scope"]), 3)
        self.assertEqual(len(packet["industry_highlights"]), 3)
        for item in packet["business_scope"] + packet["industry_highlights"]:
            self.assertTrue(item["icon"])
        for item in packet["industry_highlights"]:
            self.assertRegex(item["metric"], r"\d")
            self.assertTrue(item["source"])

        html = chevron.company_profile()
        self.assertIn("公司档案", html)
        self.assertGreaterEqual(html.count("<svg "), 6)
        self.assertEqual(html.count("by 江明"), 1)

    def test_company_profile_adds_auditable_long_term_stock_chart(self):
        history = chevron.packet()["stock_history"]
        self.assertEqual(history["listed_year"], 1921)
        self.assertEqual(history["series_start"], 1962)
        self.assertGreaterEqual(history["series_end"], 2026)
        self.assertGreaterEqual(len(history["annual_close"]), 60)
        self.assertEqual(history["annual_close"][0][0], history["series_start"])
        self.assertEqual(history["annual_close"][-1][0], history["series_end"])
        for year, price in history["annual_close"]:
            self.assertIsInstance(year, int)
            self.assertGreater(price, 0)

        html = chevron.company_profile()
        self.assertIn("上市以来股价走势", html)
        self.assertIn("1921年上市", html)
        self.assertIn("公开价格序列1962-2026", html)
        self.assertIn("拆股调整", html)
        self.assertIn("不含股息再投资", html)
        self.assertIn("class='stock-chart'", html)
        self.assertIn("Yahoo Finance", html)

    def test_strategy_core_cards_are_data_backed_and_have_icons(self):
        packet = chevron.packet()
        self.assertGreaterEqual(len(packet["core_drivers"]), 3)
        self.assertLessEqual(len(packet["core_drivers"]), 5)
        for driver in packet["core_drivers"]:
            self.assertRegex(driver["metric"], r"\d")
            self.assertTrue(driver["icon"])
            self.assertIn("行业含义", driver["industry_meaning"])
            self.assertTrue(driver["source"])

        html = chevron.strategy()
        self.assertEqual(html.count("class='card driver'"), len(packet["core_drivers"]))
        self.assertGreaterEqual(html.count("<svg "), len(packet["core_drivers"]))
        self.assertNotIn("...", html)
        self.assertNotIn("…", html)

    def test_panorama_has_fixed_six_metrics_and_important_holders(self):
        packet = chevron.packet()
        self.assertEqual(len(packet["panorama_top_grid"]), 6)
        self.assertEqual(
            list(packet["panorama_top_grid"]),
            [
                "FY2025 营收",
                "FY2025 经营利润",
                "FY2025 经营现金流",
                "FY2025 净利润",
                "当前市值",
                "PE / Forward PE",
            ],
        )
        self.assertGreaterEqual(len(packet["major_holders"]), 4)
        for holder in packet["major_holders"]:
            self.assertRegex(holder["stake"], r"\d+(?:\.\d+)?%")
            self.assertRegex(holder["shares"], r"\d")
            self.assertRegex(holder["reported_value"], r"\$\d")
            self.assertTrue(holder["source"])

        html = chevron.panorama()
        self.assertEqual(html.count("class='metric'"), 6)
        self.assertIn("重要机构持仓", html)
        self.assertEqual(html.count("class='holder-row'"), len(packet["major_holders"]))
        self.assertNotIn("...", html)
        self.assertNotIn("…", html)

    def test_logo_and_footer_follow_fixed_visual_contract(self):
        for html in (chevron.strategy(), chevron.panorama()):
            self.assertIn("chevron-official-crop.png", html)
            self.assertRegex(html, r"\.logo-box img \{[^}]*width:1[4-9]\dpx")
            self.assertEqual(html.count("by 江明"), 1)
            self.assertRegex(html, r"<footer>.*<div class='signature'>by 江明</div></footer>")

    def test_capital_cards_are_numeric_and_not_duplicated_in_top_grid(self):
        packet = chevron.packet()
        self.assertRegex(packet["capital"]["roi"]["value"], r"\d")
        self.assertRegex(packet["capital"]["capex_2026"]["value"], r"\$\d")
        self.assertRegex(packet["capital"]["shareholder_return"]["value"], r"\$\d")
        top_text = " ".join(packet["panorama_top_grid"])
        self.assertNotRegex(top_text, re.compile(r"ROIC|CapEx|股东回报"))

    def test_management_culture_is_people_and_organization_only(self):
        packet = chevron.packet()
        self.assertGreaterEqual(len(packet["management_culture"]), 1)
        self.assertLessEqual(len(packet["management_culture"]), 4)
        for item in packet["management_culture"]:
            self.assertIn(item["lens"], {"人员", "组织", "伦理", "员工"})
            self.assertTrue(item["practice"].startswith("做法："))
            self.assertRegex(item["case_or_number"], r"案例：|数字：")
            self.assertTrue(item["source"])

        html = chevron.culture()
        self.assertEqual(
            html.count("class='card culture-card'"),
            len(packet["management_culture"]),
        )
        self.assertNotRegex(html, re.compile(r"资本开支|炼厂产能|油气储量|市场份额"))
        self.assertEqual(html.count("by 江明"), 1)


if __name__ == "__main__":
    unittest.main()
