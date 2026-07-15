import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))


class PostChevronStandardV2Tests(unittest.TestCase):
    def setUp(self):
        import render_post_chevron_standard_v2 as batch

        self.batch = batch

    def test_batch_covers_every_company_after_chevron(self):
        expected = {
            "pg", "roche", "homedepot", "hsbc", "arm", "palantir",
            "agriculturalbank", "merck", "icbc", "goldmansachs",
            "novartis", "astrazeneca", "philipmorris", "kla",
            "gevernova", "rbc", "ibm", "dell",
        }
        self.assertEqual(set(self.batch.EVIDENCE), expected)

    def test_every_core_driver_has_numeric_evidence_and_industry_meaning(self):
        for slug, item in self.batch.EVIDENCE.items():
            drivers = item["drivers"]
            with self.subTest(slug=slug):
                self.assertGreaterEqual(len(drivers), 3)
                self.assertLessEqual(len(drivers), 5)
                for driver in drivers:
                    self.assertRegex(driver["metric"], r"\d")
                    self.assertTrue(driver["explanation"].startswith("行业含义："))
                    self.assertTrue(driver["source"].startswith("http"))

    def test_evidence_preserves_company_palette_and_official_logo(self):
        for company in self.batch.batch_companies():
            with self.subTest(slug=company["slug"]):
                self.assertRegex(company["color"], r"^#[0-9A-Fa-f]{6}$")
                self.assertTrue(company["logo_source"].startswith("http"))
                self.assertTrue(self.batch.Path(company["logo_path"]).is_file())

    def test_packet_uses_six_top_metrics_and_keeps_capital_below(self):
        company = next(c for c in self.batch.batch_companies() if c["slug"] == "pg")
        packet = self.batch.build_packet(
            company,
            self.batch.sample_financials(),
            self.batch.sample_holders(),
        )
        labels = [row["label"] for row in packet["panorama"]["metrics"]]
        self.assertEqual(len(labels), 6)
        self.assertEqual(labels[-2:], ["当前市值", "PE / Forward PE"])
        self.assertFalse(any(any(term in label for term in ("ROIC", "CapEx", "股东")) for label in labels))
        self.assertEqual([row["label"] for row in packet["panorama"]["capital"]], ["ROIC", "2026E CapEx", "股东回报"])

    def test_footer_has_all_audit_layers_and_no_inline_signature(self):
        company = next(c for c in self.batch.batch_companies() if c["slug"] == "pg")
        packet = self.batch.build_packet(company, self.batch.sample_financials(), self.batch.sample_holders())
        joined = "\n".join(packet["footer_lines"])
        for prefix in ("经营数据：", "行情数据：", "核心证据：", "ROI口径：", "2026 CapEx口径：", "股东分红：", "机构持仓：", "汇率口径：", "免责声明："):
            self.assertIn(prefix, joined)
        self.assertNotIn("by 江明", joined)
        self.assertNotRegex(joined, r"\.\.\.|…")

    def test_split_legacy_renderers_cannot_overwrite_unified_pages(self):
        import render_rank38_59_current as legacy_all
        import render_post_cocacola_profile_culture as legacy_half

        self.assertTrue(legacy_all.LEGACY_RENDERER_DISABLED)
        self.assertTrue(legacy_half.LEGACY_RENDERER_DISABLED)
        with self.assertRaisesRegex(RuntimeError, "render_post_chevron_standard_v2"):
            legacy_all.main()
        with self.assertRaisesRegex(RuntimeError, "render_post_chevron_standard_v2"):
            legacy_half.main()


if __name__ == "__main__":
    unittest.main()
