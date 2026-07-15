import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT))

import render_post_cocacola_profile_culture as profile_ui


EXPECTED_SLUGS = {
    "pg", "roche", "homedepot", "hsbc", "arm", "palantir",
    "agriculturalbank", "merck", "icbc", "goldmansachs", "novartis",
    "astrazeneca", "philipmorris", "kla", "gevernova", "rbc", "ibm", "dell",
}


class PostChevronProfileStockChartTests(unittest.TestCase):
    def test_every_post_chevron_company_has_auditable_stock_history(self):
        histories = profile_ui.load_stock_histories()
        self.assertEqual(set(histories) - {"chevron"}, EXPECTED_SLUGS)
        for slug in EXPECTED_SLUGS:
            history = histories[slug]
            self.assertEqual(history["display_currency"], "USD")
            self.assertGreaterEqual(len(history["series"]), 3, slug)
            self.assertTrue(history["listing_note"], slug)
            self.assertTrue(history["listing_source"], slug)
            self.assertEqual(history["source_name"], "Yahoo Finance")
            self.assertRegex(history["as_of"], r"2026-07-1[45]")
            self.assertLess(history["series"][0][0], history["series"][-1][0])
            for date, value in history["series"]:
                self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")
                self.assertGreater(value, 0)

    def test_non_us_listings_are_converted_to_usd_with_dated_fx(self):
        histories = profile_ui.load_stock_histories()
        for slug in ("roche", "agriculturalbank", "icbc"):
            history = histories[slug]
            self.assertNotEqual(history["source_currency"], "USD")
            self.assertGreater(history["fx_to_usd"], 0)
            self.assertEqual(history["fx_date"], "2026-07-15")
            self.assertIn("固定汇率", history["currency_note"])

    def test_profile_page_places_hand_drawn_chart_after_business_scope(self):
        companies = {company["slug"]: company for company in profile_ui.COMPANIES}
        for slug in EXPECTED_SLUGS:
            company = companies[slug]
            source = profile_ui.profile_page(company)
            business_at = source.index("业务范围")
            chart_at = source.index("上市以来股价走势")
            status_at = source.index("行业地位与核心亮点")
            self.assertLess(business_at, chart_at, slug)
            self.assertLess(chart_at, status_at, slug)
            self.assertIn("class='stock-chart'", source, slug)
            self.assertIn("拆股调整", source, slug)
            self.assertIn("不含股息再投资", source, slug)
            self.assertIn("Yahoo Finance", source, slug)
            self.assertEqual(source.count("by 江明"), 1, slug)
            self.assertGreater(profile_ui.profile_height(company), 1450)


if __name__ == "__main__":
    unittest.main()
