"""Protect the approved reference artifacts, not the truth of dated financial data."""
import base64
import hashlib
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "sketch_refs" / "amex_approved_20261002"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.text = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)

    def count(self, class_name):
        return sum(class_name in attrs.get("class", "").split() for _, attrs in self.tags)


class ApprovedReferenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((REFERENCE / "manifest.json").read_text())
        cls.pages = {}
        for entry in cls.manifest["pages"]:
            cls.pages[entry["name"]] = Page((REFERENCE / entry["file"]).read_text())

    def test_exact_approved_html(self):
        self.assertEqual(len(self.manifest["pages"]), 4)
        self.assertEqual(self.manifest["purpose"], "dated_layout_reference_not_live_data")
        for entry in self.manifest["pages"]:
            raw = (REFERENCE / entry["file"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"])

    def test_embedded_official_logo_and_no_external_assets(self):
        for page in self.pages.values():
            images = [attrs for tag, attrs in page.tags if tag == "img"]
            self.assertTrue(images)
            for img in images:
                self.assertTrue(img["src"].startswith("data:image/svg+xml;base64,"))
                raw = base64.b64decode(img["src"].split(",", 1)[1], validate=True)
                self.assertEqual(hashlib.sha256(raw).hexdigest(), self.manifest["logo"]["sha256"])
            self.assertFalse(any(tag in {"script", "link", "iframe"} for tag, _ in page.tags))
            self.assertNotIn("file:///", "".join(page.text))

    def test_four_page_roles(self):
        self.assertEqual(self.pages["profile"].count("p"), 9)
        self.assertEqual(self.pages["profile"].count("stock-wrap"), 1)
        self.assertEqual(self.pages["strategy"].count("driver-card"), 3)
        self.assertEqual(self.pages["panorama"].count("metric"), 6)
        self.assertEqual(self.pages["panorama"].count("holder-row"), 3)
        self.assertEqual(self.pages["culture"].count("culture-card"), 2)
        for name in ("profile", "strategy", "culture"):
            self.assertEqual(self.pages[name].count("holder-row"), 0)

    def test_sources_signature_and_no_ellipsis(self):
        for page in self.pages.values():
            self.assertEqual(page.count("signature"), 1)
            text = "".join(page.text)
            self.assertIn("by 江明", text)
            self.assertEqual(sum(tag == "footer" for tag, _ in page.tags), 1)
            self.assertIn("来源", text)
            self.assertNotIn("…", text)
            self.assertNotIn("\ufffd", text)
            self.assertNotIn("text-overflow:ellipsis", text)


if __name__ == "__main__":
    unittest.main()
