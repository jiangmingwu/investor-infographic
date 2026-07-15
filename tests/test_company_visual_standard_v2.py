import sys
import unittest
from pathlib import Path


TEMPLATE_ROOT = Path(__file__).resolve().parents[1]
if str(TEMPLATE_ROOT) not in sys.path:
    sys.path.insert(0, str(TEMPLATE_ROOT))


class CompanyVisualStandardV2Tests(unittest.TestCase):
    def setUp(self):
        import company_visual_standard_v2 as standard

        self.standard = standard
        self.packet = {
            "company": "测试公司",
            "ticker": "NYSE: TEST",
            "colors": {"accent": "#0054A6", "deep": "#123E66", "gold": "#E31937"},
            "logo": {
                "path": "/Users/jiangming/templates/assets/company_logos/chevron-official-crop.png",
                "official_source_url": "https://www.chevron.com/",
                "sha256": "abc",
                "background": "#F26A21",
            },
            "strategy": {
                "thesis": "用可验证的规模、客户价值和资本纪律创造长期现金流。",
                "drivers": [
                    {"title": "核心业务A", "icon": "factory", "metric": "全球第1，份额55%", "explanation": "行业含义：规模超过第二名，客户切换成本高。"},
                    {"title": "核心业务B", "icon": "network", "metric": "1.2亿用户", "explanation": "行业含义：网络规模形成复购与数据优势。"},
                    {"title": "核心业务C", "icon": "coin", "metric": "毛利率68%", "explanation": "行业含义：高毛利为持续研发提供资金。"},
                ],
                "moves": [
                    {"tag": "并购", "title": "补齐产品", "detail": "2025年完成关键资产整合。"},
                ],
                "quote": "真正的优势必须能在数字里被看见。",
            },
            "panorama": {
                "metrics": [
                    {"label": "FY2025 营收", "value": "$100B", "sub": "同比 +10%"},
                    {"label": "FY2025 经营利润", "value": "$20B", "sub": "同比 +8%"},
                    {"label": "FY2025 经营现金流", "value": "$25B", "sub": "同比 +7%"},
                    {"label": "FY2025 净利润", "value": "$15B", "sub": "同比 +6%"},
                    {"label": "当前市值", "value": "$300B", "sub": "截至2026年7月"},
                    {"label": "PE / Forward PE", "value": "20.0x / 18.0x", "sub": "当前估值"},
                ],
                "segments": [
                    {"name": "业务A", "share": "60%", "value": "$60B", "note": "收入占比"},
                    {"name": "业务B", "share": "40%", "value": "$40B", "note": "收入占比"},
                ],
                "capital": [
                    {"label": "ROIC", "value": "18.2%", "note": "高于WACC 7.1%"},
                    {"label": "2026E CapEx", "value": "$12-14B", "note": "公司公开指引"},
                    {"label": "股东回报", "value": "$2.00/股 · 2.1%", "note": "年度股息与股息率"},
                ],
                "signals": [
                    {"kind": "亮点", "title": "份额领先", "detail": "核心市场份额55%。"},
                    {"kind": "风险", "title": "估值", "detail": "当前PE高于十年中位数。"},
                ],
                "holders": [
                    {"name": "Vanguard", "kind": "机构", "stake": "9.1%", "value": "$27.3B", "period": "2026Q1", "note": "13F"},
                    {"name": "BlackRock", "kind": "机构", "stake": "7.2%", "value": "$21.6B", "period": "2026Q1", "note": "13F"},
                    {"name": "State Street", "kind": "机构", "stake": "4.3%", "value": "$12.9B", "period": "2026Q1", "note": "13F"},
                ],
            },
            "footer_lines": [
                "经营数据：公司2025年报，FY2025：2025年1-12月",
                "行情数据：StockAnalysis，查看：2026年7月",
                "核心证据：公司年报与投资者资料，核查：2026年7月",
                "ROI口径：NOPAT / 平均投入资本，FY2025",
                "2026 CapEx口径：公司公开指引，核查：2026年7月",
                "股东分红：公司IR，查看：2026年7月",
                "机构持仓：Nasdaq 13F，报告期：2026Q1",
                "汇率口径：主图金额统一美元；汇率查看：2026年7月",
                "免责声明：本图仅供学习参考，不构成投资建议",
            ],
        }

    def test_valid_packet_passes_all_hard_gates(self):
        self.standard.validate_packet(self.packet)

    def test_strategy_rejects_non_numeric_core_evidence(self):
        self.packet["strategy"]["drivers"][0]["metric"] = "行业领先"
        with self.assertRaisesRegex(ValueError, "数字证据"):
            self.standard.validate_packet(self.packet)

    def test_panorama_requires_fixed_six_metrics(self):
        self.packet["panorama"]["metrics"].pop()
        with self.assertRaisesRegex(ValueError, "六项"):
            self.standard.validate_packet(self.packet)

    def test_financial_company_allows_explicit_industry_metric_replacements(self):
        self.packet["panorama"]["industry_exception"] = "银行经营利润与经营现金流不可比，改用净利差和客户存款。"
        self.packet["panorama"]["metrics"][1] = {
            "label": "FY2025 净利差",
            "value": "1.88%",
            "sub": "银行盈利能力",
        }
        self.packet["panorama"]["metrics"][2] = {
            "label": "FY2025 客户存款",
            "value": "$1.80T",
            "sub": "同比 +6%",
        }
        self.standard.validate_packet(self.packet)

    def test_panorama_requires_numeric_holder_rows(self):
        self.packet["panorama"]["holders"][0]["stake"] = "大股东"
        with self.assertRaisesRegex(ValueError, "持股比例"):
            self.standard.validate_packet(self.packet)

    def test_html_has_semantic_icons_large_logo_holders_and_signature(self):
        strategy = self.standard.strategy_page(self.packet)
        panorama = self.standard.panorama_page(self.packet)
        self.assertEqual(strategy.count("class='driver-card'"), 3)
        self.assertGreaterEqual(strategy.count("<svg"), 3)
        self.assertIn("logo-visible", strategy)
        self.assertEqual(panorama.count("class='holder-row'"), 3)
        self.assertIn("机构与重要股东", panorama)
        self.assertIn("<div class='signature'>by 江明</div>", strategy)
        self.assertIn("<div class='signature'>by 江明</div>", panorama)

    def test_logo_brand_background_is_preserved(self):
        strategy = self.standard.strategy_page(self.packet)
        self.assertIn("background:#F26A21", strategy)

    def test_visible_text_rejects_ellipsis(self):
        self.packet["strategy"]["quote"] = "这里不允许..."
        with self.assertRaisesRegex(ValueError, "省略号"):
            self.standard.validate_packet(self.packet)


if __name__ == "__main__":
    unittest.main()
