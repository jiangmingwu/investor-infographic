from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "investor-infographic" / "SKILL.md"
TEMPLATE_SYSTEM = ROOT / "skills" / "investor-infographic" / "references" / "template-system.md"
AGENT_CONFIG = ROOT / "skills" / "investor-infographic" / "agents" / "openai.yaml"


class CurrentSkillStandardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = SKILL.read_text(encoding="utf-8")

    def test_company_default_is_four_hand_drawn_pages(self) -> None:
        for page in ("公司档案", "经营之道", "经营全景", "管理文化"):
            self.assertIn(page, self.text)
        self.assertIn("四张手绘", self.text)
        self.assertNotIn("one orange operating-analysis image plus three company-style hand-drawn images", self.text)

    def test_company_profile_contains_long_term_stock_chart(self) -> None:
        self.assertIn("上市以来股价走势", self.text)
        self.assertIn("split-adjusted closing prices", self.text)
        self.assertIn("cash-dividend reinvestment is excluded", self.text)

    def test_legacy_orange_renderer_is_opt_in(self) -> None:
        self.assertIn("Legacy orange company renderer", self.text)
        self.assertIn("only when the user explicitly requests", self.text)

    def test_template_reference_uses_current_four_page_contract(self) -> None:
        reference = TEMPLATE_SYSTEM.read_text(encoding="utf-8")
        for page in ("公司档案", "经营之道", "经营全景", "管理文化"):
            self.assertIn(page, reference)
        self.assertIn("上市以来股价走势", reference)
        self.assertNotIn("At installation time there were 34 data files", reference)
        self.assertNotIn("At installation time there were 58 HTML files", reference)

    def test_agent_prompt_names_the_current_company_pages(self) -> None:
        config = AGENT_CONFIG.read_text(encoding="utf-8")
        self.assertIn("公司档案、经营之道、经营全景、管理文化", config)


if __name__ == "__main__":
    unittest.main()
